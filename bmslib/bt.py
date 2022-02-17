from bleak import BleakClient

from util import get_logger
from .bms import BmsSample

logger = get_logger()


class BtBms():
    def __init__(self, address, name, keep_alive=False):
        self.client = BleakClient(address, disconnected_callback=self._on_disconnect)
        self.name = name
        self.keep_alive = keep_alive

    def _on_disconnect(self, client):
        if self.keep_alive:
            logger.warning('BMS %s disconnected!', self.__str__())

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def fetch(self) -> BmsSample:
        raise NotImplementedError()

    async def fetch_voltages(self):
        raise NotImplementedError()

    async def fetch_temperatures(self):
        raise NotImplementedError()

    def __str__(self):
        return f'{self.__class__.__name__}({self.client.address})'

    async def __aenter__(self):
        # print("enter")
        if self.keep_alive and self.client.is_connected:
            return
        await self.connect()

    async def __aexit__(self, *args):
        # print("exit")
        if self.keep_alive:
            return
        await self.disconnect()

    def __await__(self):
        return self.__aexit__().__await__()

    def set_keep_alive(self, keep):
        if keep:
            logger.info("BMS %s keep alive enabled", self.__str__())
        self.keep_alive = keep
