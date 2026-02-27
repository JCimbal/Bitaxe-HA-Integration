"""Config flow for the BitAxe integration."""
from __future__ import annotations

import asyncio
import ipaddress

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN


class BitAxeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BitAxe."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            ip_address = user_input["ip_address"]
            device_name = user_input["device_name"]

            # Validate IP address format
            try:
                ipaddress.ip_address(ip_address)
            except ValueError:
                errors["base"] = "invalid_ip"
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_data_schema(),
                    errors=errors,
                )

            # Test connection to the device
            session = async_get_clientsession(self.hass)
            try:
                async with asyncio.timeout(10):
                    resp = await session.get(f"http://{ip_address}/api/system/info")
                    resp.raise_for_status()
            except (aiohttp.ClientError, TimeoutError):
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_data_schema(),
                    errors=errors,
                )

            # Ensure unique device per IP
            await self.async_set_unique_id(ip_address)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=device_name,
                data={"ip_address": ip_address, "device_name": device_name},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_data_schema(),
            errors=errors,
        )

    @staticmethod
    def _get_data_schema():
        """Return the schema for user input."""
        return vol.Schema({
            vol.Required("ip_address"): str,
            vol.Required("device_name"): str,
        })

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return BitAxeOptionsFlowHandler(config_entry)


class BitAxeOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle BitAxe options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(step_id="init")
