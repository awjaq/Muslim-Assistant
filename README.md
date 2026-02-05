# Muslim Assistant - Home Assistant Integration

A comprehensive Islamic companion integration for [Home Assistant](https://www.home-assistant.io/), providing all the features of [Muslim Pro](https://www.muslimpro.com/) as an open-source Home Assistant Community Store (HACS) integration.

## Features

### Prayer Times & Adhan
- Accurate prayer times for **Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha**
- **16+ calculation methods** including ISNA, MWL, Umm Al-Qura (Makkah), Egyptian, Karachi, Turkey, Dubai, and more
- Support for **Hanafi** and **Standard** (Shafi/Maliki/Hanbali) Asr calculation
- **Next Prayer** sensor with countdown timer
- Location-based automatic calculation
- Use with HA automations for **Adhan notifications**

### Qibla Direction
- Precise compass bearing to the **Kaaba in Makkah**
- Degrees and cardinal direction (N, NE, E, etc.)
- Based on your configured latitude/longitude

### Holy Quran
- **Verse of the Day** - random ayah with Arabic text and English translation
- **Get Surah** service - fetch any of the 114 surahs with full Arabic and translation
- **Get Ayah** service - fetch any specific verse by surah:ayah reference
- Powered by the [Al Quran Cloud API](https://alquran.cloud/)

### Hijri (Islamic) Calendar
- Current **Hijri date** with day, month, and year
- Month names in **English and Arabic**
- Weekday names in **English and Arabic**
- Gregorian date cross-reference

### 99 Names of Allah (Asma ul Husna)
- **Daily rotating** Name of Allah sensor
- All 99 names with Arabic text and English meaning
- Service to fetch any specific name or all names

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

### Inspirational Islamic Quotes
- **30 curated quotes** from Quran and authentic Hadiths
- Daily rotating quote with **Arabic text and source**
- Quotes from Sahih Bukhari, Sahih Muslim, Jami at-Tirmidhi, and more

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

### Mosque Finder
- Find **nearby mosques** within 5km radius
- Shows name, distance, address, and GPS coordinates
- Sorted by proximity
- Powered by OpenStreetMap Overpass API

### Halal Food Finder
- Find **nearby halal restaurants** within 5km radius
- Shows name, distance, cuisine type, phone, website
- Sorted by proximity
- Powered by OpenStreetMap Overpass API

### Zakat Calculator
- Calculate your annual **Zakat obligation** (2.5%)
- Supports: cash savings, gold, silver, business assets, stocks, rental income
- Deduct debts for net Zakatable amount
- Multi-currency support

### Hajj & Umrah Guides
- Complete **step-by-step Hajj guide** with all 10 pillars/steps
- Complete **Umrah guide** with all 5 steps
- Each step includes Arabic name, description, and practical tips

### Islamic Greeting Cards
- **12 occasion templates**: Eid ul-Fitr, Eid ul-Adha, Ramadan, Jummah, New Year, Mawlid, Isra & Mi'raj, Laylat al-Qadr, Wedding, New Baby, General, Condolence
- Personalize with recipient name and custom message
- Arabic text included

### Makkah Live
- **Live stream** link from Masjid al-Haram, Makkah
- Always available sensor for quick access

### Prayer Requests
- Submit prayer requests via HA service
- Category support: health, guidance, forgiveness, family, success, travel, deceased
- Fires HA events for automation with notifications

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

## Sensors (18 Total)

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Fajr Prayer Time | `sensor.muslim_assistant_fajr_prayer_time` | Fajr prayer time |
| Sunrise | `sensor.muslim_assistant_sunrise_prayer_time` | Sunrise time |
| Dhuhr Prayer Time | `sensor.muslim_assistant_dhuhr_prayer_time` | Dhuhr prayer time |
| Asr Prayer Time | `sensor.muslim_assistant_asr_prayer_time` | Asr prayer time |
| Maghrib Prayer Time | `sensor.muslim_assistant_maghrib_prayer_time` | Maghrib prayer time |
| Isha Prayer Time | `sensor.muslim_assistant_isha_prayer_time` | Isha prayer time |
| Next Prayer | `sensor.muslim_assistant_next_prayer` | Next upcoming prayer with countdown |
| Qibla Direction | `sensor.muslim_assistant_qibla_direction` | Compass bearing to Makkah (degrees) |
| Hijri Date | `sensor.muslim_assistant_hijri_date` | Current Islamic calendar date |
| Daily Dua | `sensor.muslim_assistant_daily_dua` | Context-aware daily supplication |
| Quran Verse | `sensor.muslim_assistant_quran_verse` | Random Quran verse of the day |
| Ramadan Tracker | `sensor.muslim_assistant_ramadan_tracker` | Ramadan fasting tracker |
| Tasbih Counter | `sensor.muslim_assistant_tasbih_counter` | Digital Tasbih counter |
| Name of Allah | `sensor.muslim_assistant_name_of_allah` | Daily rotating Name of Allah |
| Islamic Quote | `sensor.muslim_assistant_islamic_quote` | Daily inspirational quote |
| Nearby Mosques | `sensor.muslim_assistant_nearby_mosques` | Count of nearby mosques |
| Halal Restaurants | `sensor.muslim_assistant_halal_restaurants` | Count of nearby halal restaurants |
| Makkah Live | `sensor.muslim_assistant_makkah_live` | Makkah live stream link |

## Services (14 Total)

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

### `muslim_assistant.calculate_zakat`
Calculate your annual Zakat obligation.
```yaml
service: muslim_assistant.calculate_zakat
data:
  savings: 10000
  gold_value: 5000
  silver_value: 1000
  business_assets: 0
  stocks_investments: 3000
  debts: 2000
  currency: "USD"
```

### `muslim_assistant.get_hajj_guide`
Get a comprehensive step-by-step Hajj guide.
```yaml
service: muslim_assistant.get_hajj_guide
```

### `muslim_assistant.get_umrah_guide`
Get a step-by-step Umrah guide.
```yaml
service: muslim_assistant.get_umrah_guide
```

### `muslim_assistant.send_greeting`
Generate an Islamic greeting card for an occasion.
```yaml
service: muslim_assistant.send_greeting
data:
  occasion: "Eid ul-Fitr"
  recipient_name: "Ahmad"
  custom_message: "Wishing you and your family joy!"
```

### `muslim_assistant.prayer_request`
Submit a prayer request.
```yaml
service: muslim_assistant.prayer_request
data:
  prayer_text: "Please make dua for my family's health."
  requester_name: "Ahmad"
  category: "health"
```

### `muslim_assistant.get_allah_names`
Get one or all of the 99 Names of Allah.
```yaml
service: muslim_assistant.get_allah_names
data:
  number: 1
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

### Daily Name of Allah Notification

```yaml
automation:
  - alias: "Daily Name of Allah"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "Name of Allah #{{ state_attr('sensor.muslim_assistant_name_of_allah', 'number') }}"
          message: >
            {{ states('sensor.muslim_assistant_name_of_allah') }}
            ({{ state_attr('sensor.muslim_assistant_name_of_allah', 'arabic') }})
            - {{ state_attr('sensor.muslim_assistant_name_of_allah', 'meaning') }}
```

### Daily Islamic Quote

```yaml
automation:
  - alias: "Daily Islamic Quote"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "Islamic Wisdom"
          message: >
            "{{ state_attr('sensor.muslim_assistant_islamic_quote', 'quote_full') }}"
            - {{ state_attr('sensor.muslim_assistant_islamic_quote', 'source') }}
```

### Jummah (Friday) Reminder

```yaml
automation:
  - alias: "Jummah Reminder"
    trigger:
      - platform: time
        at: "11:00:00"
    condition:
      - condition: time
        weekday:
          - fri
    action:
      - service: muslim_assistant.send_greeting
        data:
          occasion: "Jummah (Friday)"
      - service: notify.mobile_app
        data:
          title: "Jummah Mubarak"
          message: >
            Don't forget Jummah prayer today!
            Dhuhr is at {{ states('sensor.muslim_assistant_dhuhr_prayer_time') }}
```

## API Credits

This integration uses the following free APIs:

- [Aladhan Prayer Times API](https://aladhan.com/prayer-times-api) - Prayer times, Qibla direction, and Hijri calendar
- [Al Quran Cloud API](https://alquran.cloud/) - Quran text, translations, and audio
- [OpenStreetMap Overpass API](https://overpass-api.de/) - Mosque and Halal restaurant finder

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
