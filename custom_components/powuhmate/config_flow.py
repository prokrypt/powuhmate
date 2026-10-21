import voluptuous as vol
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak, async_discovered_service_info
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ADDRESS

from .const import DOMAIN

NAME = "PowerMate Bluetooth"


class PowuhmateConfigFlow(ConfigFlow, domain=DOMAIN):
    _address: str

    async def async_step_bluetooth(self, info: BluetoothServiceInfoBleak):
        await self.async_set_unique_id(info.address)
        self._abort_if_unique_id_configured()
        self._address = info.address
        self.context["title_placeholders"] = {"name": f"{NAME} {info.address}"}
        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=f"{NAME} {self._address}", data={CONF_ADDRESS: self._address})
        self._set_confirm_only()
        return self.async_show_form(step_id="confirm", description_placeholders={"address": self._address})

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_ADDRESS])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f"{NAME} {user_input[CONF_ADDRESS]}", data=user_input)
        current = self._async_current_ids()
        found = [i.address for i in async_discovered_service_info(self.hass) if i.name == NAME and i.address not in current]
        if not found:
            return self.async_abort(reason="no_devices_found")
        return self.async_show_form(step_id="user", data_schema=vol.Schema({vol.Required(CONF_ADDRESS): vol.In(found)}))
