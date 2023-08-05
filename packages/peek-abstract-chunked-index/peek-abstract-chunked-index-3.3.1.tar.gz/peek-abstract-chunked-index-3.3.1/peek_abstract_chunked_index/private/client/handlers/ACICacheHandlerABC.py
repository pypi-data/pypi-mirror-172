import logging
from abc import ABCMeta
from collections import defaultdict
from typing import Dict
from typing import List

from twisted.internet.defer import Deferred
from twisted.internet.defer import DeferredList
from twisted.internet.defer import inlineCallbacks
from vortex.DeferUtil import vortexLogFailure
from vortex.PayloadEndpoint import PayloadEndpoint
from vortex.PayloadEnvelope import PayloadEnvelope
from vortex.VortexABC import SendVortexMsgResponseCallable
from vortex.VortexFactory import VortexFactory

from peek_abstract_chunked_index.private.client.controller.ACICacheControllerABC import (
    ACICacheControllerABC,
)

# ModelSet HANDLER
from peek_abstract_chunked_index.private.tuples.ACIUpdateDateTupleABC import (
    ACIUpdateDateTupleABC,
)
from peek_plugin_base.PeekVortexUtil import peekServerName


class ACICacheHandlerABC(metaclass=ABCMeta):
    _UpdateDateTuple: ACIUpdateDateTupleABC = None
    _updateFromDeviceFilt: Dict = None
    _updateFromLogicFilt: Dict = None
    _logger: logging.Logger = None

    def __init__(self, cacheController: ACICacheControllerABC, clientId: str):
        """App ChunkedIndex Handler

        This class handles the custom needs of the desktop/mobile apps observing chunkedIndexs.

        """
        self._cacheController = cacheController
        self._clientId = clientId

        self._epObserve = PayloadEndpoint(
            self._updateFromDeviceFilt, self._processObserve
        )

        self._uuidsObserving = set()

        # If the vortex goes online, check the cache.
        # Before this line of code, the vortex is already online.
        (
            VortexFactory.subscribeToVortexStatusChange(peekServerName)
            .filter(lambda online: online is True)
            .subscribe(on_next=self._startObserving)
        )

    def _startObserving(self, *args):
        # Tell the logic service that this vortexUuid is interested in its data
        VortexFactory.sendVortexMsg(
            vortexMsgs=PayloadEnvelope(
                filt=self._updateFromLogicFilt
            ).toVortexMsg(),
            destVortexName=peekServerName,
        )

    @inlineCallbacks
    def start(self):
        yield self._startObserving()

    def shutdown(self):
        self._epObserve.shutdown()
        self._epObserve = None

    def _filterOutOfflineVortexes(self):
        # TODO, Change this to observe offline vortexes
        # This depends on the VortexFactory offline observable implementation.
        # Which is incomplete at this point :-|

        vortexUuids = (
            set(VortexFactory.getRemoteVortexUuids()) & self._uuidsObserving
        )
        self._uuidsObserving = vortexUuids

    # ---------------
    # Process update from the server

    def notifyOfUpdate(self, chunkKeys: List[str]):
        """Notify of ChunkedIndex Updates

        This method is called by the client.ChunkedIndexCacheController when it receives updates
        from the server.

        """
        self._filterOutOfflineVortexes()

        def cratePayloadEnvelope():
            payloadEnvelope = PayloadEnvelope()
            payloadEnvelope.data = []
            return payloadEnvelope

        payloadsByVortexUuid = defaultdict(cratePayloadEnvelope)

        for chunkKey in chunkKeys:
            encodedChunkedIndexChunk = self._cacheController.encodedChunk(
                chunkKey
            )

            # Queue up the required client notifications
            for vortexUuid in self._uuidsObserving:
                self._logger.debug(
                    "Sending unsolicited chunkedIndex %s to vortex %s",
                    chunkKey,
                    vortexUuid,
                )
                payloadsByVortexUuid[vortexUuid].data.append(
                    encodedChunkedIndexChunk
                )

        # Send the updates to the clients
        dl = []
        for vortexUuid, payloadEnvelope in list(payloadsByVortexUuid.items()):
            payload.filt = self._updateFromDeviceFilt

            # Serialise in thread, and then send.
            d = payloadEnvelope.toVortexMsgDefer(base64Encode=False)
            d.addCallback(
                VortexFactory.sendVortexMsg, destVortexUuid=vortexUuid
            )
            dl.append(d)

        # Log the errors, otherwise we don't care about them
        dl = DeferredList(dl, fireOnOneErrback=True)
        dl.addErrback(vortexLogFailure, self._logger, consumeError=True)

    # ---------------
    # Process observes from the devices
    @inlineCallbacks
    def _processObserve(
        self,
        payloadEnvelope: PayloadEnvelope,
        vortexUuid: str,
        sendResponse: SendVortexMsgResponseCallable,
        **kwargs
    ):

        payload = yield payloadEnvelope.decodePayloadDefer()

        updateDatesTuples: ACIUpdateDateTupleABC = payload.tuples[0]

        self._uuidsObserving.add(vortexUuid)

        yield self._replyToObserve(
            payload.filt,
            updateDatesTuples.ckiUpdateDateByChunkKey,
            sendResponse,
            vortexUuid,
        )

    # ---------------
    # Reply to device observe

    @inlineCallbacks
    def _replyToObserve(
        self,
        filt,
        lastUpdateByChunkedIndexKey: Dict[str, str],
        sendResponse: SendVortexMsgResponseCallable,
        vortexUuid: str,
    ) -> None:
        """Reply to Observe

        The client has told us that it's observing a new set of chunkedIndexs, and the lastUpdate
        it has for each of those chunkedIndexs. We will send them the chunkedIndexs that are out of date
        or missing.

        :param filt: The payload filter to respond to.
        :param lastUpdateByChunkedIndexKey: The dict of chunkedIndexKey:lastUpdate
        :param sendResponse: The callable provided by the Vortex (handy)
        :returns: None

        """
        yield None

        chunkedIndexTuplesToSend = []

        # Check and send any updates
        for chunkedIndexKey, lastUpdate in lastUpdateByChunkedIndexKey.items():
            if vortexUuid not in VortexFactory.getRemoteVortexUuids():
                self._logger.debug(
                    "Vortex %s is offline, stopping update", vortexUuid
                )
                return

            # NOTE: lastUpdate can be null.
            encodedChunkedIndexTuple = self._cacheController.encodedChunk(
                chunkedIndexKey
            )
            if not encodedChunkedIndexTuple:
                self._logger.debug(
                    "ChunkedIndex %s is not in the cache" % chunkedIndexKey
                )
                continue

            # We are king, If it's it's not our version, it's the wrong version ;-)
            self._logger.debug(
                "%s, %s,  %s",
                encodedChunkedIndexTuple.ckiLastUpdate == lastUpdate,
                encodedChunkedIndexTuple.ckiLastUpdate,
                lastUpdate,
            )

            if encodedChunkedIndexTuple.ckiLastUpdate == lastUpdate:
                self._logger.debug(
                    "ChunkedIndex %s matches the cache" % chunkedIndexKey
                )
                continue

            chunkedIndexTuplesToSend.append(encodedChunkedIndexTuple)
            self._logger.debug(
                "Sending chunkedIndex %s from the cache" % chunkedIndexKey
            )

        # Send the payload to the frontend
        payloadEnvelope = PayloadEnvelope(
            filt=filt, data=chunkedIndexTuplesToSend
        )
        d: Deferred = payloadEnvelope.toVortexMsgDefer(base64Encode=False)
        d.addCallback(sendResponse)
        d.addErrback(vortexLogFailure, self._logger, consumeError=True)
