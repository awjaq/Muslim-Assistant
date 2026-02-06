"""Dashboard configuration for Muslim Assistant auto-creation."""

# This is the Lovelace dashboard config that gets auto-created
# when the integration is set up. It can also be imported manually
# via Settings > Dashboards.

DASHBOARD_CONFIG = {
    "views": [
        {
            "title": "Muslim Assistant",
            "path": "muslim-assistant",
            "icon": "mdi:star-crescent",
            "type": "sections",
            "max_columns": 4,
            "sections": [
                # ── Column 1: Prayer Times ─────────────────────
                {
                    "title": "Prayer Times",
                    "type": "grid",
                    "cards": [
                        {
                            "type": "markdown",
                            "content": (
                                "# {{ states('sensor.muslim_assistant_next_prayer') }}\n"
                                "## {{ state_attr('sensor.muslim_assistant_next_prayer', 'time') }}\n"
                                "{{ state_attr('sensor.muslim_assistant_next_prayer', 'time_remaining') }} remaining\n"
                            ),
                        },
                        {
                            "type": "entities",
                            "show_header_toggle": False,
                            "entities": [
                                {
                                    "entity": "sensor.muslim_assistant_fajr_prayer_time",
                                    "name": "Fajr",
                                    "icon": "mdi:weather-sunset-up",
                                },
                                {
                                    "entity": "sensor.muslim_assistant_sunrise_prayer_time",
                                    "name": "Sunrise",
                                    "icon": "mdi:weather-sunny",
                                },
                                {
                                    "entity": "sensor.muslim_assistant_dhuhr_prayer_time",
                                    "name": "Dhuhr",
                                    "icon": "mdi:white-balance-sunny",
                                },
                                {
                                    "entity": "sensor.muslim_assistant_asr_prayer_time",
                                    "name": "Asr",
                                    "icon": "mdi:weather-sunny-alert",
                                },
                                {
                                    "entity": "sensor.muslim_assistant_maghrib_prayer_time",
                                    "name": "Maghrib",
                                    "icon": "mdi:weather-sunset-down",
                                },
                                {
                                    "entity": "sensor.muslim_assistant_isha_prayer_time",
                                    "name": "Isha",
                                    "icon": "mdi:weather-night",
                                },
                            ],
                        },
                    ],
                },
                # ── Column 2: Qibla & Calendar ─────────────────
                {
                    "title": "Qibla & Calendar",
                    "type": "grid",
                    "cards": [
                        {
                            "type": "markdown",
                            "content": (
                                "### Qibla Direction\n"
                                "# {{ states('sensor.muslim_assistant_qibla_direction') }}\u00b0 "
                                "{{ state_attr('sensor.muslim_assistant_qibla_direction', 'cardinal_direction') }}\n"
                                "{{ state_attr('sensor.muslim_assistant_qibla_direction', 'instructions') }}\n"
                            ),
                        },
                        {
                            "type": "markdown",
                            "content": (
                                "### Hijri Calendar\n"
                                "# {{ state_attr('sensor.muslim_assistant_hijri_date', 'hijri_day') }} "
                                "{{ state_attr('sensor.muslim_assistant_hijri_date', 'hijri_month') }} "
                                "{{ state_attr('sensor.muslim_assistant_hijri_date', 'hijri_year') }}\n"
                                "**{{ state_attr('sensor.muslim_assistant_hijri_date', 'hijri_month_arabic') }}** "
                                "\u2014 {{ state_attr('sensor.muslim_assistant_hijri_date', 'hijri_weekday') }} "
                                "({{ state_attr('sensor.muslim_assistant_hijri_date', 'hijri_weekday_arabic') }})\n\n"
                                "{{ state_attr('sensor.muslim_assistant_hijri_date', 'gregorian_date') }}\n"
                            ),
                        },
                        {
                            "type": "entity",
                            "entity": "sensor.muslim_assistant_ramadan_tracker",
                            "name": "Ramadan Tracker",
                            "icon": "mdi:moon-waning-crescent",
                        },
                    ],
                },
                # ── Column 3: Daily Inspiration ────────────────
                {
                    "title": "Daily Inspiration",
                    "type": "grid",
                    "cards": [
                        {
                            "type": "markdown",
                            "content": (
                                "### Quran Verse\n"
                                "**{{ states('sensor.muslim_assistant_quran_verse') }}**\n\n"
                                "{{ state_attr('sensor.muslim_assistant_quran_verse', 'text_arabic') }}\n\n"
                                "*{{ state_attr('sensor.muslim_assistant_quran_verse', 'text_translation') }}*\n"
                            ),
                        },
                        {
                            "type": "markdown",
                            "content": (
                                "### Name of Allah "
                                "#{{ state_attr('sensor.muslim_assistant_name_of_allah', 'number') }}\n"
                                "# {{ state_attr('sensor.muslim_assistant_name_of_allah', 'arabic') }}\n"
                                "**{{ states('sensor.muslim_assistant_name_of_allah') }}** \u2014 "
                                "{{ state_attr('sensor.muslim_assistant_name_of_allah', 'meaning') }}\n"
                            ),
                        },
                        {
                            "type": "markdown",
                            "content": (
                                "### Daily Dua\n"
                                "**{{ states('sensor.muslim_assistant_daily_dua') }}**\n\n"
                                "{{ state_attr('sensor.muslim_assistant_daily_dua', 'arabic') }}\n\n"
                                "*{{ state_attr('sensor.muslim_assistant_daily_dua', 'transliteration') }}*\n\n"
                                "{{ state_attr('sensor.muslim_assistant_daily_dua', 'translation') }}\n"
                            ),
                        },
                        {
                            "type": "markdown",
                            "content": (
                                "### Islamic Quote\n"
                                "{{ state_attr('sensor.muslim_assistant_islamic_quote', 'arabic') }}\n\n"
                                "*{{ state_attr('sensor.muslim_assistant_islamic_quote', 'quote_full') }}*\n\n"
                                "\u2014 {{ state_attr('sensor.muslim_assistant_islamic_quote', 'source') }}\n"
                            ),
                        },
                    ],
                },
                # ── Column 4: Audio & Tools ────────────────────
                {
                    "title": "Audio & Tools",
                    "type": "grid",
                    "cards": [
                        {
                            "type": "button",
                            "name": "Play Adhan",
                            "icon": "mdi:mosque",
                            "icon_height": "40px",
                            "tap_action": {
                                "action": "perform-action",
                                "perform_action": "muslim_assistant.play_adhan",
                                "data": {},
                            },
                            "hold_action": {"action": "none"},
                        },
                        {
                            "type": "button",
                            "name": "Al-Fatiha",
                            "icon": "mdi:book-open-page-variant",
                            "icon_height": "40px",
                            "tap_action": {
                                "action": "perform-action",
                                "perform_action": "muslim_assistant.play_quran",
                                "data": {"surah_number": 1},
                            },
                            "hold_action": {"action": "none"},
                        },
                        {
                            "type": "button",
                            "name": "Yasin",
                            "icon": "mdi:book-open-page-variant",
                            "icon_height": "40px",
                            "tap_action": {
                                "action": "perform-action",
                                "perform_action": "muslim_assistant.play_quran",
                                "data": {"surah_number": 36},
                            },
                            "hold_action": {"action": "none"},
                        },
                        {
                            "type": "button",
                            "name": "Ar-Rahman",
                            "icon": "mdi:book-open-page-variant",
                            "icon_height": "40px",
                            "tap_action": {
                                "action": "perform-action",
                                "perform_action": "muslim_assistant.play_quran",
                                "data": {"surah_number": 55},
                            },
                            "hold_action": {"action": "none"},
                        },
                        {
                            "type": "button",
                            "name": "Al-Mulk",
                            "icon": "mdi:book-open-page-variant",
                            "icon_height": "40px",
                            "tap_action": {
                                "action": "perform-action",
                                "perform_action": "muslim_assistant.play_quran",
                                "data": {"surah_number": 67},
                            },
                            "hold_action": {"action": "none"},
                        },
                        {
                            "type": "button",
                            "name": "Al-Baqarah",
                            "icon": "mdi:book-open-page-variant",
                            "icon_height": "40px",
                            "tap_action": {
                                "action": "perform-action",
                                "perform_action": "muslim_assistant.play_quran",
                                "data": {"surah_number": 2},
                            },
                            "hold_action": {"action": "none"},
                        },
                        # ── Tasbih ──
                        {
                            "type": "entity",
                            "entity": "sensor.muslim_assistant_tasbih_counter",
                            "name": "Tasbih Counter",
                            "icon": "mdi:counter",
                        },
                        {
                            "type": "horizontal-stack",
                            "cards": [
                                {
                                    "type": "button",
                                    "name": "+1",
                                    "icon": "mdi:plus",
                                    "tap_action": {
                                        "action": "perform-action",
                                        "perform_action": "muslim_assistant.tasbih_increment",
                                        "data": {},
                                    },
                                    "hold_action": {"action": "none"},
                                    "double_tap_action": {"action": "none"},
                                },
                                {
                                    "type": "button",
                                    "name": "Reset",
                                    "icon": "mdi:restart",
                                    "tap_action": {
                                        "action": "perform-action",
                                        "perform_action": "muslim_assistant.tasbih_reset",
                                        "data": {},
                                    },
                                    "hold_action": {"action": "none"},
                                },
                            ],
                        },
                        # ── Nearby ──
                        {
                            "type": "entity",
                            "entity": "sensor.muslim_assistant_nearby_mosques",
                            "name": "Nearby Mosques",
                            "icon": "mdi:mosque",
                        },
                        {
                            "type": "entity",
                            "entity": "sensor.muslim_assistant_halal_restaurants",
                            "name": "Halal Restaurants",
                            "icon": "mdi:food-halal",
                        },
                        # ── Makkah Live ──
                        {
                            "type": "button",
                            "name": "Makkah Live",
                            "icon": "mdi:video",
                            "icon_height": "40px",
                            "tap_action": {
                                "action": "url",
                                "url_path": "https://www.youtube.com/@saudiqurantv/live",
                            },
                            "hold_action": {"action": "none"},
                        },
                        # ── Guides ──
                        {
                            "type": "horizontal-stack",
                            "cards": [
                                {
                                    "type": "button",
                                    "name": "Hajj Guide",
                                    "icon": "mdi:book-open-variant",
                                    "tap_action": {
                                        "action": "perform-action",
                                        "perform_action": "muslim_assistant.get_hajj_guide",
                                        "data": {},
                                    },
                                    "hold_action": {"action": "none"},
                                },
                                {
                                    "type": "button",
                                    "name": "Umrah Guide",
                                    "icon": "mdi:walk",
                                    "tap_action": {
                                        "action": "perform-action",
                                        "perform_action": "muslim_assistant.get_umrah_guide",
                                        "data": {},
                                    },
                                    "hold_action": {"action": "none"},
                                },
                            ],
                        },
                        {
                            "type": "button",
                            "name": "99 Names of Allah",
                            "icon": "mdi:star-crescent",
                            "tap_action": {
                                "action": "perform-action",
                                "perform_action": "muslim_assistant.get_allah_names",
                                "data": {},
                            },
                            "hold_action": {"action": "none"},
                        },
                    ],
                },
            ],
        }
    ],
}
