"""The BitAxe integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Set up BitAxe from a config entry."""
    ip_address = entry.data["ip_address"]

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"BitAxe ({ip_address})",
        update_method=lambda: fetch_bitaxe_data(hass, ip_address),
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Unload a BitAxe config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)
    return unload_ok


async def fetch_bitaxe_data(hass: HomeAssistant, ip_address: str) -> dict:
    """Fetch data from the BitAxe API."""
    url = f"http://{ip_address}/api/system/info"
    session = async_get_clientsession(hass)
    try:
        async with asyncio.timeout(10):
            response = await session.get(url)
            response.raise_for_status()
            data = await response.json()
            _LOGGER.debug("Fetched data: %s", data)
            return data
    except (aiohttp.ClientError, TimeoutError) as err:
        _LOGGER.error("Error fetching data from BitAxe API: %s", err)
        raise UpdateFailed(f"Error communicating with BitAxe: {err}") from err


async def post_bitaxe_command(hass: HomeAssistant, ip_address: str, endpoint: str) -> None:
    """Send a POST command to the BitAxe device."""
    url = f"http://{ip_address}{endpoint}"
    session = async_get_clientsession(hass)
    try:
        async with asyncio.timeout(10):
            response = await session.post(url)
            response.raise_for_status()
    except (aiohttp.ClientError, TimeoutError) as err:
        _LOGGER.error("Error sending POST to BitAxe (%s): %s", endpoint, err)
        raise HomeAssistantError(f"Error communicating with BitAxe: {err}") from err


async def patch_bitaxe_system(
    hass: HomeAssistant, ip_address: str, payload: dict
) -> None:
    """Send a PATCH request to update settings on the BitAxe device."""
    url = f"http://{ip_address}/api/system"
    session = async_get_clientsession(hass)
    try:
        async with asyncio.timeout(10):
            response = await session.patch(url, json=payload)
            response.raise_for_status()
    except (aiohttp.ClientError, TimeoutError) as err:
        _LOGGER.error("Error sending PATCH to BitAxe: %s", err)
        raise HomeAssistantError(f"Error communicating with BitAxe: {err}") from err
