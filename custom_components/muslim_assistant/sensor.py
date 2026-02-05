"""Sensor platform for Muslim Assistant integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import DEGREE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MAKKAH_LIVE_STREAM_URL, PRAYERS
from .coordinator import MuslimAssistantCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Muslim Assistant sensors."""
    coordinator: MuslimAssistantCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    # Individual prayer time sensors
    for prayer in PRAYERS:
        entities.append(PrayerTimeSensor(coordinator, entry, prayer))

    # Next prayer sensor
    entities.append(NextPrayerSensor(coordinator, entry))

    # Qibla direction sensor
    entities.append(QiblaSensor(coordinator, entry))

    # Hijri date sensor
    entities.append(HijriDateSensor(coordinator, entry))

    # Daily Dua sensor
    entities.append(DailyDuaSensor(coordinator, entry))

    # Quran Verse of the Day sensor
    entities.append(QuranVerseSensor(coordinator, entry))

    # Ramadan tracker sensor
    entities.append(RamadanSensor(coordinator, entry))

    # Tasbih counter sensor
    entities.append(TasbihCounterSensor(coordinator, entry))

    # 99 Names of Allah sensor
    entities.append(AllahNamesSensor(coordinator, entry))

    # Islamic Quote sensor
    entities.append(IslamicQuoteSensor(coordinator, entry))

    # Nearby Mosques sensor
    entities.append(MosqueFinderSensor(coordinator, entry))

    # Halal Food Finder sensor
    entities.append(HalalFinderSensor(coordinator, entry))

    # Makkah Live sensor
    entities.append(MakkahLiveSensor(coordinator, entry))

    async_add_entities(entities)


class MuslimAssistantEntity(CoordinatorEntity):
    """Base entity for Muslim Assistant."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Muslim Assistant",
            "manufacturer": "Muslim Assistant Community",
            "model": "Islamic Companion",
            "sw_version": "1.0.0",
        }


class PrayerTimeSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for individual prayer times."""

    _attr_icon = "mdi:mosque"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
        prayer: str,
    ) -> None:
        """Initialize the prayer time sensor."""
        super().__init__(coordinator, entry)
        self._prayer = prayer
        self._attr_unique_id = f"{entry.entry_id}_{prayer.lower()}"
        self._attr_translation_key = f"prayer_{prayer.lower()}"
        self._attr_name = f"{prayer} Prayer Time"

    @property
    def native_value(self) -> str | None:
        """Return the prayer time."""
        if self.coordinator.data:
            timings = self.coordinator.data.get("prayer_times", {})
            time_str = timings.get(self._prayer, "")
            # Strip timezone info
            return time_str.split(" ")[0] if time_str else None
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        attrs = {
            "prayer": self._prayer,
            "calculation_method": self.coordinator.calc_method,
            "school": self.coordinator.school,
        }
        if self.coordinator.data:
            meta = self.coordinator.data.get("meta", {})
            attrs["method_name"] = meta.get("method", {}).get("name", "")
        return attrs


class NextPrayerSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for the next upcoming prayer."""

    _attr_icon = "mdi:clock-alert"
    _attr_name = "Next Prayer"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the next prayer sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_next_prayer"

    @property
    def native_value(self) -> str | None:
        """Return the name of the next prayer."""
        if self.coordinator.data:
            next_prayer = self.coordinator.data.get("next_prayer", {})
            return next_prayer.get("name")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data:
            next_prayer = self.coordinator.data.get("next_prayer", {})
            return {
                "time": next_prayer.get("time", ""),
                "time_remaining": next_prayer.get("time_remaining", ""),
                "timestamp": next_prayer.get("timestamp", ""),
                "all_prayer_times": {
                    prayer: self.coordinator.data.get("prayer_times", {})
                    .get(prayer, "")
                    .split(" ")[0]
                    for prayer in PRAYERS
                },
            }
        return {}


class QiblaSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for Qibla direction."""

    _attr_icon = "mdi:compass"
    _attr_name = "Qibla Direction"
    _attr_native_unit_of_measurement = DEGREE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Qibla sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_qibla"

    @property
    def native_value(self) -> float | None:
        """Return the Qibla direction in degrees."""
        if self.coordinator.data:
            qibla = self.coordinator.data.get("qibla", {})
            direction = qibla.get("direction")
            if direction is not None:
                return round(float(direction), 2)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data:
            qibla = self.coordinator.data.get("qibla", {})
            direction = qibla.get("direction", 0)
            # Convert degrees to cardinal direction
            cardinal = self._degrees_to_cardinal(float(direction))
            return {
                "cardinal_direction": cardinal,
                "latitude": self.coordinator.latitude,
                "longitude": self.coordinator.longitude,
                "kaaba_latitude": 21.4225,
                "kaaba_longitude": 39.8262,
            }
        return {}

    @staticmethod
    def _degrees_to_cardinal(degrees: float) -> str:
        """Convert degrees to cardinal direction."""
        dirs = [
            "N", "NNE", "NE", "ENE",
            "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW",
            "W", "WNW", "NW", "NNW",
        ]
        idx = round(degrees / 22.5) % 16
        return dirs[idx]


class HijriDateSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for Hijri (Islamic) calendar date."""

    _attr_icon = "mdi:calendar-star"
    _attr_name = "Hijri Date"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Hijri date sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_hijri_date"

    @property
    def native_value(self) -> str | None:
        """Return the Hijri date."""
        if self.coordinator.data:
            hijri = self.coordinator.data.get("hijri_date", {})
            return hijri.get("full_date")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data:
            hijri = self.coordinator.data.get("hijri_date", {})
            gregorian = self.coordinator.data.get("date", {}).get("gregorian", {})
            return {
                "hijri_day": hijri.get("day", ""),
                "hijri_month": hijri.get("month", ""),
                "hijri_month_arabic": hijri.get("month_ar", ""),
                "hijri_month_number": hijri.get("month_number", 0),
                "hijri_year": hijri.get("year", ""),
                "hijri_weekday": hijri.get("weekday", ""),
                "hijri_weekday_arabic": hijri.get("weekday_ar", ""),
                "gregorian_date": gregorian.get("date", ""),
            }
        return {}


class DailyDuaSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for daily Dua/supplication."""

    _attr_icon = "mdi:hands-pray"
    _attr_name = "Daily Dua"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the daily dua sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_daily_dua"

    @property
    def native_value(self) -> str | None:
        """Return the name of the current dua."""
        if self.coordinator.data:
            dua_data = self.coordinator.data.get("daily_dua", {})
            current = dua_data.get("current", {})
            return current.get("name")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the dua details."""
        if self.coordinator.data:
            dua_data = self.coordinator.data.get("daily_dua", {})
            current = dua_data.get("current", {})
            daily = dua_data.get("daily", {})
            return {
                "arabic": current.get("arabic", ""),
                "transliteration": current.get("transliteration", ""),
                "translation": current.get("translation", ""),
                "daily_dua_name": daily.get("name", ""),
                "daily_dua_arabic": daily.get("arabic", ""),
                "daily_dua_transliteration": daily.get("transliteration", ""),
                "daily_dua_translation": daily.get("translation", ""),
            }
        return {}


class QuranVerseSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for Quran Verse of the Day."""

    _attr_icon = "mdi:book-open-page-variant"
    _attr_name = "Quran Verse"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Quran verse sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_quran_verse"

    @property
    def native_value(self) -> str | None:
        """Return the surah name and ayah number."""
        if self.coordinator.data:
            verse = self.coordinator.data.get("quran_verse", {})
            if verse:
                return f"{verse.get('surah_name', '')} ({verse.get('surah_number', '')}:{verse.get('ayah_number', '')})"
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the verse details."""
        if self.coordinator.data:
            verse = self.coordinator.data.get("quran_verse", {})
            return {
                "surah_name": verse.get("surah_name", ""),
                "surah_name_arabic": verse.get("surah_name_arabic", ""),
                "surah_number": verse.get("surah_number", ""),
                "ayah_number": verse.get("ayah_number", ""),
                "text_arabic": verse.get("text_arabic", ""),
                "text_translation": verse.get("text_translation", ""),
                "edition": verse.get("edition", ""),
            }
        return {}


class RamadanSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for Ramadan / fasting tracker."""

    _attr_icon = "mdi:food-off"
    _attr_name = "Ramadan Tracker"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Ramadan sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_ramadan"

    @property
    def native_value(self) -> str | None:
        """Return Ramadan status."""
        if self.coordinator.data:
            ramadan = self.coordinator.data.get("ramadan", {})
            if ramadan.get("is_ramadan"):
                return f"Day {ramadan.get('ramadan_day', 0)} of Ramadan"
            return "Not Ramadan"
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return Ramadan details."""
        if self.coordinator.data:
            ramadan = self.coordinator.data.get("ramadan", {})
            timings = self.coordinator.data.get("prayer_times", {})
            attrs = {
                "is_ramadan": ramadan.get("is_ramadan", False),
                "ramadan_day": ramadan.get("ramadan_day", 0),
                "days_remaining": ramadan.get("days_remaining", 0),
                "current_hijri_month": ramadan.get("month_name", ""),
            }
            if ramadan.get("is_ramadan"):
                # Suhoor ends at Fajr, Iftar at Maghrib
                fajr = timings.get("Fajr", "").split(" ")[0]
                maghrib = timings.get("Maghrib", "").split(" ")[0]
                attrs["suhoor_ends"] = fajr
                attrs["iftar_time"] = maghrib
            return attrs
        return {}


class TasbihCounterSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for Tasbih (digital counter)."""

    _attr_icon = "mdi:counter"
    _attr_name = "Tasbih Counter"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Tasbih counter sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_tasbih"
        self._count = 0
        self._target = 33
        self._dhikr = "SubhanAllah"

    @property
    def native_value(self) -> int:
        """Return the current count."""
        return self._count

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return tasbih details."""
        return {
            "count": self._count,
            "target": self._target,
            "dhikr": self._dhikr,
            "completed_sets": self._count // self._target if self._target else 0,
            "remaining": max(0, self._target - (self._count % self._target)) if self._target else 0,
        }

    def increment(self, amount: int = 1) -> None:
        """Increment the counter."""
        self._count += amount
        self.async_write_ha_state()

    def reset(self) -> None:
        """Reset the counter."""
        self._count = 0
        self.async_write_ha_state()

    def set_target(self, target: int) -> None:
        """Set the target count."""
        self._target = target
        self.async_write_ha_state()

    def set_dhikr(self, dhikr: str) -> None:
        """Set the dhikr text."""
        self._dhikr = dhikr
        self.async_write_ha_state()


class AllahNamesSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for the 99 Names of Allah (Asma ul Husna)."""

    _attr_icon = "mdi:star-crescent"
    _attr_name = "Name of Allah"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the 99 Names sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_allah_name"

    @property
    def native_value(self) -> str | None:
        """Return the name of Allah for today."""
        if self.coordinator.data:
            name_data = self.coordinator.data.get("allah_name", {})
            return name_data.get("name")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the name details."""
        if self.coordinator.data:
            name_data = self.coordinator.data.get("allah_name", {})
            return {
                "number": name_data.get("number", 0),
                "arabic": name_data.get("arabic", ""),
                "meaning": name_data.get("meaning", ""),
                "total_names": 99,
            }
        return {}


class IslamicQuoteSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for daily Islamic inspirational quotes."""

    _attr_icon = "mdi:format-quote-close"
    _attr_name = "Islamic Quote"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Islamic quote sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_islamic_quote"

    @property
    def native_value(self) -> str | None:
        """Return the quote text."""
        if self.coordinator.data:
            quote_data = self.coordinator.data.get("islamic_quote", {})
            quote = quote_data.get("quote", "")
            # HA sensor state has 255 char limit, truncate if needed
            return quote[:255] if quote else None
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the quote details."""
        if self.coordinator.data:
            quote_data = self.coordinator.data.get("islamic_quote", {})
            return {
                "quote_full": quote_data.get("quote", ""),
                "source": quote_data.get("source", ""),
                "arabic": quote_data.get("arabic", ""),
            }
        return {}


class MosqueFinderSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for nearby mosques."""

    _attr_icon = "mdi:mosque"
    _attr_name = "Nearby Mosques"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the mosque finder sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_nearby_mosques"

    @property
    def native_value(self) -> int | None:
        """Return the number of nearby mosques found."""
        if self.coordinator.data:
            mosques = self.coordinator.data.get("nearby_mosques", [])
            return len(mosques)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the list of nearby mosques."""
        if self.coordinator.data:
            mosques = self.coordinator.data.get("nearby_mosques", [])
            attrs: dict[str, Any] = {"mosques": mosques}
            if mosques:
                nearest = mosques[0]
                attrs["nearest_name"] = nearest.get("name", "")
                attrs["nearest_distance_km"] = nearest.get("distance_km", 0)
                attrs["nearest_latitude"] = nearest.get("latitude", 0)
                attrs["nearest_longitude"] = nearest.get("longitude", 0)
            return attrs
        return {}


class HalalFinderSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for nearby halal restaurants."""

    _attr_icon = "mdi:food-halal"
    _attr_name = "Halal Restaurants"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the halal finder sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_halal_restaurants"

    @property
    def native_value(self) -> int | None:
        """Return the number of nearby halal restaurants."""
        if self.coordinator.data:
            halal = self.coordinator.data.get("nearby_halal", [])
            return len(halal)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the list of nearby halal restaurants."""
        if self.coordinator.data:
            halal = self.coordinator.data.get("nearby_halal", [])
            attrs: dict[str, Any] = {"restaurants": halal}
            if halal:
                nearest = halal[0]
                attrs["nearest_name"] = nearest.get("name", "")
                attrs["nearest_distance_km"] = nearest.get("distance_km", 0)
                attrs["nearest_cuisine"] = nearest.get("cuisine", "")
                attrs["nearest_latitude"] = nearest.get("latitude", 0)
                attrs["nearest_longitude"] = nearest.get("longitude", 0)
            return attrs
        return {}


class MakkahLiveSensor(MuslimAssistantEntity, SensorEntity):
    """Sensor for Makkah Live stream link."""

    _attr_icon = "mdi:video"
    _attr_name = "Makkah Live"

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Makkah Live sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_makkah_live"

    @property
    def native_value(self) -> str:
        """Return the Makkah Live status."""
        return "Available"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the stream details."""
        return {
            "stream_url": MAKKAH_LIVE_STREAM_URL,
            "description": "Live stream from Masjid al-Haram, Makkah",
            "location": "Makkah, Saudi Arabia",
        }
