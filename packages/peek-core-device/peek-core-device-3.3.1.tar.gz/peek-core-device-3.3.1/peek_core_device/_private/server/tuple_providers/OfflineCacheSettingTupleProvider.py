import logging
from typing import Union

import sqlalchemy

from peek_core_device._private.storage.DeviceInfoTable import DeviceInfoTable
from peek_core_device._private.storage.GpsLocationTable import GpsLocationTable
from twisted.internet.defer import Deferred
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

from peek_core_device._private.storage.Setting import (
    OFFLINE_CACHE_REFRESH_SECONDS,
)
from peek_core_device._private.storage.Setting import globalSetting
from peek_core_device._private.tuples.OfflineCacheSettingTuple import (
    OfflineCacheSettingTuple,
)

logger = logging.getLogger(__name__)


class OfflineCacheSettingTupleProvider(TuplesProviderABC):
    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator

    @deferToThreadWrapWithLogger(logger)
    def makeVortexMsg(
        self, filt: dict, tupleSelector: TupleSelector
    ) -> Union[Deferred, bytes]:

        deviceToken = tupleSelector.selector.get("deviceToken")

        ormSession = self._ormSessionCreator()
        try:
            try:
                deviceTuple = (
                    ormSession.query(DeviceInfoTable)
                    .filter(DeviceInfoTable.deviceToken == deviceToken)
                    .one()
                )

            except sqlalchemy.orm.exc.NoResultFound:
                deviceTuple = DeviceInfoTable(isOfflineCacheEnabled=False)

            syncSeconds = globalSetting(
                ormSession, OFFLINE_CACHE_REFRESH_SECONDS
            )

            tuples = [
                OfflineCacheSettingTuple(
                    offlineEnabled=deviceTuple.isOfflineCacheEnabled,
                    offlineCacheSyncSeconds=syncSeconds,
                )
            ]

            # Create the vortex message
            return (
                Payload(filt, tuples=tuples).makePayloadEnvelope().toVortexMsg()
            )

        finally:
            ormSession.close()
