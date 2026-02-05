# Muslim Assistant - Home Assistant Integration

A comprehensive Islamic companion integration for [Home Assistant](https://www.home-assistant.io/), providing accurate prayer times, Qibla direction, Hijri calendar, Quran verses, daily Duas, Tasbih counter, Ramadan tracking, and more.

Inspired by [Muslim Pro](https://www.muslimpro.com/) features, built as an open-source Home Assistant Community Store (HACS) integration.

## Features

### Prayer Times
- Accurate prayer times for **Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha**
- **16+ calculation methods** including ISNA, MWL, Umm Al-Qura (Makkah), Egyptian, Karachi, Turkey, Dubai, and more
- Support for **Hanafi** and **Standard** (Shafi/Maliki/Hanbali) Asr calculation
- **Next Prayer** sensor with countdown timer
- Location-based automatic calculation

### Qibla Direction
- Precise compass bearing to the **Kaaba in Makkah**
- Degrees and cardinal direction (N, NE, E, etc.)
- Based on your configured latitude/longitude

### Hijri (Islamic) Calendar
- Current **Hijri date** with day, month, and year
- Month names in **English and Arabic**
- Weekday names in **English and Arabic**
- Gregorian date cross-reference

### Quran
- **Verse of the Day** - random ayah with Arabic text and English translation
- **Get Surah** service - fetch any of the 114 surahs with full Arabic and translation
- **Get Ayah** service - fetch any specific verse by surah:ayah reference
- Powered by the [Al Quran Cloud API](https://alquran.cloud/)

### Daily Duas & Dhikr
- **20+ authentic Duas** covering daily life situations:
  - Morning & Evening remembrance
  - Before/After eating
  - Entering/Leaving the mosque
  - Before/After Wudu (ablution)
  - Entering/Leaving home
  - Travel, Distress, Istikhara
  - Dhikr: SubhanAllah, Alhamdulillah, Allahu Akbar
  - Seeking Forgiveness (Astaghfirullah)
  - Salawat upon the Prophet
- **Context-aware**: shows relevant Dua based on time of day
- Daily rotating Dua
- Arabic text, transliteration, and English translation

### Tasbih (Digital Counter)
- Digital Tasbih counter for Dhikr
- **Services**: increment, reset, set target, set dhikr text
- Track completed sets and remaining count
- Customizable target (default 33)

### Ramadan / Fasting Tracker
- Automatic detection when it's **Ramadan** (9th Hijri month)
- Current Ramadan day number
- Days remaining in Ramadan
- **Suhoor** (pre-dawn meal) end time (= Fajr)
- **Iftar** (fast-breaking) time (= Maghrib)

## Installation

### HACS (Recommended)

1. Open **HACS** in your Home Assistant instance
2. Click the **three dots** menu in the top right
3. Select **Custom repositories**
4. Add `https://github.com/awjaq/Muslim-Assistant` with category **Integration**
5. Click **Install**
6. Restart Home Assistant

### Manual Installation

1. Download or clone this repository
2. Copy the `custom_components/muslim_assistant` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings > Devices & Services**
2. Click **+ Add Integration**
3. Search for **Muslim Assistant**
4. Configure:
   - **Name**: Display name for the integration
   - **Latitude/Longitude**: Your location (auto-filled from HA config)
   - **Calculation Method**: Choose from 16+ methods
   - **School**: Standard (Shafi/Maliki/Hanbali) or Hanafi

### Calculation Methods

| Method | Region |
|--------|--------|
| ISNA | Islamic Society of North America |
| MWL | Muslim World League |
| Makkah | Umm Al-Qura University, Makkah |
| Egypt | Egyptian General Authority of Survey |
| Karachi | University of Islamic Sciences, Karachi |
| Tehran | Institute of Geophysics, University of Tehran |
| Gulf | Gulf Region |
| Kuwait | Kuwait |
| Qatar | Qatar |
| Singapore | Majlis Ugama Islam Singapura |
| France | Union Organization Islamic de France |
| Turkey | Diyanet Isleri Baskanligi, Turkey |
| Russia | Spiritual Administration of Muslims of Russia |
| Moonsighting | Moonsighting Committee Worldwide |
| Dubai | Dubai |
| Shia Ithna-Ansari | Shia Ithna-Ansari |

## Sensors

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Fajr Prayer Time | `sensor.muslim_assistant_fajr_prayer_time` | Fajr prayer time |
| Sunrise | `sensor.muslim_assistant_sunrise_prayer_time` | Sunrise time |
| Dhuhr Prayer Time | `sensor.muslim_assistant_dhuhr_prayer_time` | Dhuhr prayer time |
| Asr Prayer Time | `sensor.muslim_assistant_asr_prayer_time` | Asr prayer time |
| Maghrib Prayer Time | `sensor.muslim_assistant_maghrib_prayer_time` | Maghrib prayer time |
| Isha Prayer Time | `sensor.muslim_assistant_isha_prayer_time` | Isha prayer time |
| Next Prayer | `sensor.muslim_assistant_next_prayer` | Next upcoming prayer name with countdown |
| Qibla Direction | `sensor.muslim_assistant_qibla_direction` | Compass bearing to Makkah in degrees |
| Hijri Date | `sensor.muslim_assistant_hijri_date` | Current Islamic calendar date |
| Daily Dua | `sensor.muslim_assistant_daily_dua` | Context-aware daily supplication |
| Quran Verse | `sensor.muslim_assistant_quran_verse` | Random Quran verse of the day |
| Ramadan Tracker | `sensor.muslim_assistant_ramadan_tracker` | Ramadan fasting tracker |
| Tasbih Counter | `sensor.muslim_assistant_tasbih_counter` | Digital Tasbih counter |

## Services

### `muslim_assistant.get_surah`
Fetch a complete Surah with Arabic text and English translation.

```yaml
service: muslim_assistant.get_surah
data:
  surah_number: 1
```

### `muslim_assistant.get_ayah`
Fetch a specific verse from the Quran.

```yaml
service: muslim_assistant.get_ayah
data:
  surah_number: 2
  ayah_number: 255
```

### `muslim_assistant.tasbih_increment`
Increment the Tasbih counter.

```yaml
service: muslim_assistant.tasbih_increment
data:
  amount: 1
```

### `muslim_assistant.tasbih_reset`
Reset the Tasbih counter to zero.

```yaml
service: muslim_assistant.tasbih_reset
```

### `muslim_assistant.tasbih_set_target`
Set the target count for the Tasbih counter.

```yaml
service: muslim_assistant.tasbih_set_target
data:
  target: 33
```

### `muslim_assistant.tasbih_set_dhikr`
Set the Dhikr text for the Tasbih counter.

```yaml
service: muslim_assistant.tasbih_set_dhikr
data:
  dhikr: "SubhanAllah"
```

### `muslim_assistant.get_dua`
Get a Dua from the collection, optionally filtered by category.

```yaml
service: muslim_assistant.get_dua
data:
  category: "morning"
```

## Example Automations

### Adhan Notification at Prayer Times

```yaml
automation:
  - alias: "Adhan Notification"
    trigger:
      - platform: state
        entity_id: sensor.muslim_assistant_next_prayer
    action:
      - service: notify.mobile_app
        data:
          title: "Prayer Time"
          message: >
            It's time for {{ states('sensor.muslim_assistant_next_prayer') }} prayer
            at {{ state_attr('sensor.muslim_assistant_next_prayer', 'time') }}
```

### Suhoor Reminder During Ramadan

```yaml
automation:
  - alias: "Suhoor Reminder"
    trigger:
      - platform: time
        at: "03:30:00"
    condition:
      - condition: state
        entity_id: sensor.muslim_assistant_ramadan_tracker
        attribute: is_ramadan
        state: true
    action:
      - service: notify.mobile_app
        data:
          title: "Suhoor Reminder"
          message: >
            Time to prepare for Suhoor! Fasting begins at
            {{ state_attr('sensor.muslim_assistant_ramadan_tracker', 'suhoor_ends') }}
```

### Daily Quran Verse Notification

```yaml
automation:
  - alias: "Daily Quran Verse"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "Quran Verse of the Day"
          message: >
            {{ state_attr('sensor.muslim_assistant_quran_verse', 'text_translation') }}
            - {{ states('sensor.muslim_assistant_quran_verse') }}
```

## API Credits

This integration uses the following free APIs:

- [Aladhan Prayer Times API](https://aladhan.com/prayer-times-api) - Prayer times, Qibla direction, and Hijri calendar
- [Al Quran Cloud API](https://alquran.cloud/) - Quran text, translations, and audio

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
