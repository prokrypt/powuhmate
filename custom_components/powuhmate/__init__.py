import asyncio
import logging
import time

from bleak.exc import BleakError
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection
from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant

from .const import ACTIONS, EVENT, UUID_LED, UUID_READ, is_duplicate

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    entry.async_create_background_task(hass, _run(hass, entry.data[CONF_ADDRESS]), "powuhmate")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True  # background task is cancelled by HA on unload


async def _run(hass: HomeAssistant, address: str) -> None:
    last = [None, 0.0]

    def on_notify(_char, data: bytearray) -> None:
        code, now = data[0], time.monotonic()
        dup = is_duplicate(code, last[0], now - last[1])
        last[:] = [code, now]
        if not dup:
            hass.bus.async_fire(EVENT, {"address": address, "action": ACTIONS.get(code, f"0x{code:02x}")})

    # shortcut: blind reconnect loop like the expect script; upgrade to an advertisement callback if it drains battery
    while True:
        device = bluetooth.async_ble_device_from_address(hass, address, connectable=True)
        if device:
            gone = asyncio.Event()
            client = None
            try:
                client = await establish_connection(
                    BleakClientWithServiceCache, device, address, disconnected_callback=lambda _: gone.set()
                )
                await client.start_notify(UUID_READ, on_notify)
                await client.write_gatt_char(UUID_LED, b"\xa0", response=True)  # blink on connect
                _LOGGER.info("PowerMate %s connected", address)
                await gone.wait()
            except (BleakError, asyncio.TimeoutError) as err:
                _LOGGER.debug("PowerMate %s: %s", address, err)
            finally:
                if client and client.is_connected:
                    await client.disconnect()
        await asyncio.sleep(5)
