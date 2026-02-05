"""Data coordinator for Muslim Assistant integration."""

from __future__ import annotations

import logging
import math
from datetime import datetime, timedelta
from typing import Any

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    ALADHAN_API_BASE,
    AUDIO_BITRATE,
    CALC_METHOD_MAP,
    CONF_ADHAN_SOUND,
    CONF_ASR_OFFSET,
    CONF_DHUHR_OFFSET,
    CONF_FAJR_OFFSET,
    CONF_ISHA_OFFSET,
    CONF_MAGHRIB_OFFSET,
    CONF_QURAN_RECITER,
    DAILY_DUAS,
    DEFAULT_ADHAN,
    DEFAULT_RECITER,
    ISLAMIC_QUOTES,
    NAMES_OF_ALLAH,
    OVERPASS_API,
    PRAYERS,
    PRAYER_ASR,
    PRAYER_DHUHR,
    PRAYER_FAJR,
    PRAYER_ISHA,
    PRAYER_MAGHRIB,
    QURAN_API_BASE,
    QURAN_CDN_BASE,
    QURAN_RECITERS,
    SCHOOLS,
    SURAH_COUNT,
    UPDATE_INTERVAL_PRAYER,
)

_LOGGER = logging.getLogger(__name__)

# Mapping prayer names to offset config keys
PRAYER_OFFSET_MAP = {
    PRAYER_FAJR: CONF_FAJR_OFFSET,
    PRAYER_DHUHR: CONF_DHUHR_OFFSET,
    PRAYER_ASR: CONF_ASR_OFFSET,
    PRAYER_MAGHRIB: CONF_MAGHRIB_OFFSET,
    PRAYER_ISHA: CONF_ISHA_OFFSET,
}


class MuslimAssistantCoordinator(DataUpdateCoordinator):
    """Coordinate data updates for Muslim Assistant."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        latitude: float,
        longitude: float,
        calc_method: str,
        school: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Muslim Assistant",
            update_interval=timedelta(seconds=UPDATE_INTERVAL_PRAYER),
            config_entry=entry,
        )
        self.latitude = latitude
        self.longitude = longitude
        self.calc_method = calc_method
        self.calc_method_id = CALC_METHOD_MAP.get(calc_method, 2)
        self.school_id = SCHOOLS.get(school, 0)
        self.school = school
        self._entry = entry

    @property
    def options(self) -> dict[str, Any]:
        """Return the current options."""
        return self._entry.options

    def _get_prayer_offset(self, prayer: str) -> int:
        """Get the user-configured offset in minutes for a prayer."""
        offset_key = PRAYER_OFFSET_MAP.get(prayer)
        if offset_key:
            return self.options.get(offset_key, 0)
        return 0

    def _apply_offset(self, time_str: str, prayer: str) -> str:
        """Apply user-configured minute offset to a prayer time string."""
        offset = self._get_prayer_offset(prayer)
        if offset == 0:
            return time_str
        try:
            clean = time_str.split(" ")[0]
            hour, minute = map(int, clean.split(":"))
            dt = datetime.now().replace(hour=hour, minute=minute, second=0)
            dt += timedelta(minutes=offset)
            return dt.strftime("%H:%M")
        except (ValueError, IndexError):
            return time_str

    def get_quran_reciter_edition(self) -> str:
        """Get the configured Quran reciter API edition ID."""
        reciter_name = self.options.get(CONF_QURAN_RECITER, DEFAULT_RECITER)
        return QURAN_RECITERS.get(reciter_name, "ar.alafasy")

    def get_quran_audio_url(self, surah: int, ayah: int | None = None) -> str:
        """Build a Quran audio URL for a surah or specific ayah."""
        edition = self.get_quran_reciter_edition()
        if ayah is not None:
            return f"{QURAN_CDN_BASE}/audio/{AUDIO_BITRATE}/{edition}/{ayah}.mp3"
        return f"{QURAN_CDN_BASE}/audio-surah/{AUDIO_BITRATE}/{edition}/{surah}.mp3"

    def get_adhan_audio_url(self) -> str:
        """Get the Adhan audio URL based on user's preference."""
        adhan_name = self.options.get(CONF_ADHAN_SOUND, DEFAULT_ADHAN)
        adhan_map = {
            "Makkah (Mishary Alafasy)": "https://cdn.aladhan.com/audio/adhaan/1.mp3",
            "Madinah": "https://cdn.aladhan.com/audio/adhaan/2.mp3",
            "Al-Aqsa": "https://cdn.aladhan.com/audio/adhaan/3.mp3",
            "Egypt (Abdul Basit)": "https://cdn.aladhan.com/audio/adhaan/4.mp3",
        }
        return adhan_map.get(adhan_name, adhan_map["Makkah (Mishary Alafasy)"])

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from APIs."""
        try:
            async with aiohttp.ClientSession() as session:
                data: dict[str, Any] = {}

                # Fetch prayer times
                prayer_data = await self._fetch_prayer_times(session)
                raw_timings = prayer_data.get("timings", {})
                data["date"] = prayer_data.get("date", {})
                data["meta"] = prayer_data.get("meta", {})

                # Apply user offsets to prayer times
                adjusted_timings = {}
                for prayer in PRAYERS:
                    raw = raw_timings.get(prayer, "")
                    clean = raw.split(" ")[0] if raw else ""
                    adjusted_timings[prayer] = self._apply_offset(clean, prayer)
                data["prayer_times"] = adjusted_timings
                data["prayer_times_raw"] = {
                    p: raw_timings.get(p, "").split(" ")[0]
                    for p in PRAYERS
                }

                # Calculate next prayer
                data["next_prayer"] = self._calculate_next_prayer(
                    adjusted_timings
                )

                # Fetch Qibla direction
                qibla_data = await self._fetch_qibla(session)
                data["qibla"] = qibla_data

                # Get Hijri date from prayer times response
                hijri = data["date"].get("hijri", {})
                data["hijri_date"] = {
                    "day": hijri.get("day", ""),
                    "month": hijri.get("month", {}).get("en", ""),
                    "month_ar": hijri.get("month", {}).get("ar", ""),
                    "month_number": hijri.get("month", {}).get("number", 0),
                    "year": hijri.get("year", ""),
                    "designation": hijri.get("designation", {}).get(
                        "abbreviated", "AH"
                    ),
                    "weekday": hijri.get("weekday", {}).get("en", ""),
                    "weekday_ar": hijri.get("weekday", {}).get("ar", ""),
                    "full_date": (
                        f"{hijri.get('day', '')} "
                        f"{hijri.get('month', {}).get('en', '')} "
                        f"{hijri.get('year', '')}"
                    ),
                }

                # Check Ramadan status
                data["ramadan"] = self._check_ramadan(data["hijri_date"])

                # Get daily dua (context-aware)
                data["daily_dua"] = self._get_daily_dua()

                # Fetch random Quran verse
                quran_data = await self._fetch_random_ayah(session)
                data["quran_verse"] = quran_data

                # 99 Names of Allah (daily rotation)
                data["allah_name"] = self._get_daily_allah_name()

                # Islamic inspirational quote
                data["islamic_quote"] = self._get_daily_quote()

                # Nearby mosques
                mosques = await self._fetch_nearby_mosques(session)
                data["nearby_mosques"] = mosques

                # Nearby halal restaurants
                halal = await self._fetch_nearby_halal(session)
                data["nearby_halal"] = halal

                return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(
                f"Error communicating with API: {err}"
            ) from err
        except Exception as err:
            raise UpdateFailed(f"Error updating data: {err}") from err

    async def _fetch_prayer_times(
        self, session: aiohttp.ClientSession
    ) -> dict[str, Any]:
        """Fetch prayer times from Aladhan API."""
        now = datetime.now()
        url = (
            f"{ALADHAN_API_BASE}/timings/{int(now.timestamp())}"
            f"?latitude={self.latitude}"
            f"&longitude={self.longitude}"
            f"&method={self.calc_method_id}"
            f"&school={self.school_id}"
        )
        async with session.get(url) as resp:
            resp.raise_for_status()
            result = await resp.json()
            return result.get("data", {})

    async def _fetch_qibla(
        self, session: aiohttp.ClientSession
    ) -> dict[str, Any]:
        """Fetch Qibla direction from Aladhan API."""
        url = f"{ALADHAN_API_BASE}/qibla/{self.latitude}/{self.longitude}"
        async with session.get(url) as resp:
            resp.raise_for_status()
            result = await resp.json()
            qibla_data = result.get("data", {})
            return {
                "direction": qibla_data.get("direction", 0),
                "latitude": qibla_data.get("latitude", self.latitude),
                "longitude": qibla_data.get("longitude", self.longitude),
            }

    async def _fetch_random_ayah(
        self, session: aiohttp.ClientSession
    ) -> dict[str, Any]:
        """Fetch a random Quran ayah."""
        import random

        surah = random.randint(1, SURAH_COUNT)
        url = f"{QURAN_API_BASE}/surah/{surah}"
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                result = await resp.json()
                surah_data = result.get("data", {})
                ayahs = surah_data.get("ayahs", [])
                if ayahs:
                    ayah = random.choice(ayahs)
                    ayah_num = ayah.get("numberInSurah", 1)
                    global_num = ayah.get("number", 1)
                    trans_url = (
                        f"{QURAN_API_BASE}/ayah/{surah}:{ayah_num}/en.asad"
                    )
                    async with session.get(trans_url) as trans_resp:
                        trans_resp.raise_for_status()
                        trans_result = await trans_resp.json()
                        trans_data = trans_result.get("data", {})
                        edition = self.get_quran_reciter_edition()
                        audio_url = (
                            f"{QURAN_CDN_BASE}/audio/"
                            f"{AUDIO_BITRATE}/{edition}/{global_num}.mp3"
                        )
                        return {
                            "surah_name": surah_data.get("englishName", ""),
                            "surah_name_arabic": surah_data.get("name", ""),
                            "surah_number": surah,
                            "ayah_number": ayah_num,
                            "ayah_global_number": global_num,
                            "text_arabic": ayah.get("text", ""),
                            "text_translation": trans_data.get("text", ""),
                            "edition": trans_data.get("edition", {}).get(
                                "englishName", ""
                            ),
                            "audio_url": audio_url,
                        }
                return {}
        except Exception:
            _LOGGER.debug(
                "Failed to fetch Quran verse, will retry next update"
            )
            return {}

    def _calculate_next_prayer(
        self, timings: dict[str, str]
    ) -> dict[str, Any]:
        """Calculate the next upcoming prayer."""
        now = datetime.now()

        for prayer in PRAYERS:
            time_str = timings.get(prayer, "")
            if not time_str:
                continue
            clean = time_str.split(" ")[0]
            try:
                prayer_time = datetime.strptime(clean, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
                if prayer_time > now:
                    time_remaining = prayer_time - now
                    hours, remainder = divmod(
                        int(time_remaining.total_seconds()), 3600
                    )
                    minutes, _ = divmod(remainder, 60)
                    return {
                        "name": prayer,
                        "time": clean,
                        "time_remaining": f"{hours}h {minutes}m",
                        "timestamp": prayer_time.isoformat(),
                    }
            except ValueError:
                continue

        # If all prayers have passed, next prayer is Fajr tomorrow
        fajr_str = timings.get("Fajr", "05:00").split(" ")[0]
        try:
            fajr_time = datetime.strptime(fajr_str, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            ) + timedelta(days=1)
            time_remaining = fajr_time - now
            hours, remainder = divmod(
                int(time_remaining.total_seconds()), 3600
            )
            minutes, _ = divmod(remainder, 60)
            return {
                "name": "Fajr",
                "time": fajr_str,
                "time_remaining": f"{hours}h {minutes}m",
                "timestamp": fajr_time.isoformat(),
            }
        except ValueError:
            return {"name": "Fajr", "time": "05:00", "time_remaining": "N/A"}

    def _check_ramadan(self, hijri_date: dict[str, Any]) -> dict[str, Any]:
        """Check if it's currently Ramadan and return fasting info."""
        month_number = hijri_date.get("month_number", 0)
        day = hijri_date.get("day", "")
        is_ramadan = month_number == 9

        return {
            "is_ramadan": is_ramadan,
            "ramadan_day": int(day) if is_ramadan and day else 0,
            "days_remaining": (30 - int(day)) if is_ramadan and day else 0,
            "month_name": hijri_date.get("month", ""),
        }

    def _get_daily_dua(self) -> dict[str, Any]:
        """Get the daily dua based on the current time (context-aware)."""
        now = datetime.now()
        hour = now.hour

        if 4 <= hour < 7:
            dua = DAILY_DUAS[0]  # Morning Remembrance
        elif 7 <= hour < 12:
            dua = DAILY_DUAS[3]  # Upon Waking Up
        elif 12 <= hour < 15:
            dua = DAILY_DUAS[4]  # Before Eating
        elif 15 <= hour < 18:
            dua = DAILY_DUAS[12]  # Istikhara
        elif 18 <= hour < 21:
            dua = DAILY_DUAS[1]  # Evening Remembrance
        else:
            dua = DAILY_DUAS[2]  # Before Sleeping

        day_of_year = now.timetuple().tm_yday
        rotating_dua = DAILY_DUAS[day_of_year % len(DAILY_DUAS)]

        return {
            "current": dua,
            "daily": rotating_dua,
        }

    def _get_daily_allah_name(self) -> dict[str, Any]:
        """Get the 99 Names of Allah entry for today."""
        now = datetime.now()
        day_of_year = now.timetuple().tm_yday
        index = day_of_year % len(NAMES_OF_ALLAH)
        name = NAMES_OF_ALLAH[index]
        return {
            "number": name["number"],
            "name": name["name"],
            "arabic": name["arabic"],
            "meaning": name["meaning"],
        }

    def _get_daily_quote(self) -> dict[str, Any]:
        """Get a daily Islamic inspirational quote."""
        now = datetime.now()
        day_of_year = now.timetuple().tm_yday
        index = day_of_year % len(ISLAMIC_QUOTES)
        quote = ISLAMIC_QUOTES[index]
        return {
            "quote": quote["quote"],
            "source": quote["source"],
            "arabic": quote["arabic"],
        }

    async def _fetch_nearby_mosques(
        self, session: aiohttp.ClientSession
    ) -> list[dict[str, Any]]:
        """Fetch nearby mosques using Overpass API."""
        try:
            query = f"""
            [out:json][timeout:10];
            (
              node["amenity"="place_of_worship"]["religion"="muslim"](around:5000,{self.latitude},{self.longitude});
              way["amenity"="place_of_worship"]["religion"="muslim"](around:5000,{self.latitude},{self.longitude});
            );
            out center 10;
            """
            async with session.post(
                OVERPASS_API,
                data={"data": query},
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    mosques = []
                    for element in result.get("elements", [])[:10]:
                        tags = element.get("tags", {})
                        lat = element.get("lat") or element.get(
                            "center", {}
                        ).get("lat", 0)
                        lon = element.get("lon") or element.get(
                            "center", {}
                        ).get("lon", 0)
                        if lat and lon:
                            distance = self._haversine_distance(
                                self.latitude, self.longitude, lat, lon
                            )
                            mosques.append(
                                {
                                    "name": tags.get(
                                        "name", "Unknown Mosque"
                                    ),
                                    "latitude": lat,
                                    "longitude": lon,
                                    "distance_km": round(distance, 2),
                                    "address": tags.get("addr:street", ""),
                                    "city": tags.get("addr:city", ""),
                                }
                            )
                    mosques.sort(key=lambda x: x["distance_km"])
                    return mosques
                return []
        except Exception:
            _LOGGER.debug("Failed to fetch nearby mosques")
            return []

    async def _fetch_nearby_halal(
        self, session: aiohttp.ClientSession
    ) -> list[dict[str, Any]]:
        """Fetch nearby halal restaurants using Overpass API."""
        try:
            query = f"""
            [out:json][timeout:10];
            (
              node["cuisine"~"halal|muslim"](around:5000,{self.latitude},{self.longitude});
              node["diet:halal"="yes"](around:5000,{self.latitude},{self.longitude});
              node["halal"="yes"](around:5000,{self.latitude},{self.longitude});
              way["cuisine"~"halal|muslim"](around:5000,{self.latitude},{self.longitude});
              way["diet:halal"="yes"](around:5000,{self.latitude},{self.longitude});
            );
            out center 10;
            """
            async with session.post(
                OVERPASS_API,
                data={"data": query},
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    restaurants = []
                    for element in result.get("elements", [])[:10]:
                        tags = element.get("tags", {})
                        lat = element.get("lat") or element.get(
                            "center", {}
                        ).get("lat", 0)
                        lon = element.get("lon") or element.get(
                            "center", {}
                        ).get("lon", 0)
                        if lat and lon:
                            distance = self._haversine_distance(
                                self.latitude, self.longitude, lat, lon
                            )
                            restaurants.append(
                                {
                                    "name": tags.get(
                                        "name", "Unknown Restaurant"
                                    ),
                                    "latitude": lat,
                                    "longitude": lon,
                                    "distance_km": round(distance, 2),
                                    "cuisine": tags.get("cuisine", "halal"),
                                    "address": tags.get("addr:street", ""),
                                    "city": tags.get("addr:city", ""),
                                    "phone": tags.get("phone", ""),
                                    "website": tags.get("website", ""),
                                }
                            )
                    restaurants.sort(key=lambda x: x["distance_km"])
                    return restaurants
                return []
        except Exception:
            _LOGGER.debug("Failed to fetch nearby halal restaurants")
            return []

    @staticmethod
    def _haversine_distance(
        lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Calculate the great-circle distance between two points on Earth."""
        r = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c

    async def async_get_surah(self, surah_number: int) -> dict[str, Any]:
        """Fetch a specific surah from the Quran API."""
        async with aiohttp.ClientSession() as session:
            url = (
                f"{QURAN_API_BASE}/surah/{surah_number}"
                f"/editions/quran-uthmani,en.asad"
            )
            async with session.get(url) as resp:
                resp.raise_for_status()
                result = await resp.json()
                data_list = result.get("data", [])
                if len(data_list) >= 2:
                    arabic = data_list[0]
                    english = data_list[1]
                    edition = self.get_quran_reciter_edition()
                    return {
                        "surah_number": surah_number,
                        "name": arabic.get("englishName", ""),
                        "name_arabic": arabic.get("name", ""),
                        "revelation_type": arabic.get("revelationType", ""),
                        "number_of_ayahs": arabic.get("numberOfAyahs", 0),
                        "audio_url": (
                            f"{QURAN_CDN_BASE}/audio-surah/"
                            f"{AUDIO_BITRATE}/{edition}/{surah_number}.mp3"
                        ),
                        "ayahs": [
                            {
                                "number": a.get("numberInSurah", 0),
                                "arabic": a.get("text", ""),
                                "translation": (
                                    english.get("ayahs", [])[i].get(
                                        "text", ""
                                    )
                                    if i < len(english.get("ayahs", []))
                                    else ""
                                ),
                            }
                            for i, a in enumerate(arabic.get("ayahs", []))
                        ],
                    }
                return {}

    async def async_get_ayah(
        self, surah: int, ayah: int
    ) -> dict[str, Any]:
        """Fetch a specific ayah."""
        async with aiohttp.ClientSession() as session:
            url = (
                f"{QURAN_API_BASE}/ayah/{surah}:{ayah}"
                f"/editions/quran-uthmani,en.asad"
            )
            async with session.get(url) as resp:
                resp.raise_for_status()
                result = await resp.json()
                data_list = result.get("data", [])
                if len(data_list) >= 2:
                    arabic_data = data_list[0]
                    english_data = data_list[1]
                    global_num = arabic_data.get("number", 1)
                    edition = self.get_quran_reciter_edition()
                    return {
                        "surah": arabic_data.get("surah", {}).get(
                            "englishName", ""
                        ),
                        "surah_arabic": arabic_data.get("surah", {}).get(
                            "name", ""
                        ),
                        "surah_number": surah,
                        "ayah_number": ayah,
                        "arabic": arabic_data.get("text", ""),
                        "translation": english_data.get("text", ""),
                        "audio_url": (
                            f"{QURAN_CDN_BASE}/audio/"
                            f"{AUDIO_BITRATE}/{edition}/{global_num}.mp3"
                        ),
                    }
                return {}
