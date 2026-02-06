# Muslim Assistant for Home Assistant

**Your comprehensive Islamic companion -- now with Adhan and Quran audio playback.**

Version 2.0.0 | Home Assistant Integration | HACS Compatible

Muslim Assistant is an open-source [Home Assistant](https://www.home-assistant.io/) integration that brings a full suite of Islamic tools into your smart home. Prayer times, Quran, Adhan, Hijri calendar, duas, Tasbih, Zakat calculator, mosque finder, and much more -- all accessible as sensors, services, and automations.

> **Repository:** [https://github.com/awjaq/Muslim-Assistant](https://github.com/awjaq/Muslim-Assistant)

---

## What's New in v2.0

- **Adhan Audio Playback** -- Play the Adhan call to prayer on any `media_player` entity (Amazon Echo/Alexa, Google Home/Nest, Sonos, HomePod, Chromecast, and more) via the new `play_adhan` service.
- **Quran Audio Playback** -- Stream Quran recitation with 11 world-renowned reciters through the new `play_quran` service.
- **Prayer Time Adjustments** -- Fine-tune each of the six prayer times with offsets from -30 to +30 minutes to match your local mosque schedule.
- **Options Flow** -- Reconfigure your reciter, Adhan sound, prayer offsets, and target media player at any time from Settings without removing the integration.
- **Media Player Entity** -- A dedicated `media_player.muslim_assistant_audio_player` entity for playback state and control.
- **Quran Verse Audio** -- The Quran Verse of the Day sensor now includes an `audio_url` attribute for direct audio access.
- **16 Services** -- Two new services (`play_adhan` and `play_quran`) join the existing 14 for a total of 16.

---

## Features Overview

### Prayer Times and Adhan
- Accurate prayer times for **Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha**
- **16+ calculation methods** including ISNA, MWL, Umm Al-Qura (Makkah), Egyptian, Karachi, Turkey, Dubai, and more
- Support for **Hanafi** and **Standard** (Shafi/Maliki/Hanbali) Asr calculation
- **Next Prayer** sensor with countdown timer
- **Prayer time adjustments** of +/- 30 minutes per prayer (v2.0)
- **Adhan audio playback** on smart speakers via media_player (v2.0)

### Quran
- **Verse of the Day** sensor with Arabic text, English translation, and `audio_url` attribute (v2.0)
- **Quran audio playback** with 11 selectable reciters (v2.0)
- **Get Surah** service -- fetch any of the 114 surahs with full Arabic and translation
- **Get Ayah** service -- fetch any specific verse by surah:ayah reference
- Powered by the [Al Quran Cloud API](https://alquran.cloud/)

#### Available Reciters (v2.0)

| # | Reciter |
|---|---------|
| 1 | Mishary Rashid Alafasy |
| 2 | Abdur-Rahman As-Sudais |
| 3 | Abdul Basit (Murattal) |
| 4 | Abdul Basit (Mujawwad) |
| 5 | Mohamed Siddiq Al-Minshawi |
| 6 | Mahmoud Khalil Al-Husary |
| 7 | Abu Bakr Al-Shatri |
| 8 | Saad Al-Ghamdi |
| 9 | Maher Al-Muaiqly |
| 10 | Hani Ar-Rifai |
| 11 | Ahmed Al-Ajamy |

### Qibla Direction
- Precise compass bearing to the **Kaaba in Makkah**
- Degrees and cardinal direction (N, NE, E, SE, S, SW, W, NW)
- Detailed instructions attribute for easy orientation
- Based on your configured latitude/longitude

### Hijri (Islamic) Calendar
- Current **Hijri date** with day, month, and year
- Month names in **English and Arabic**
- Weekday names in **English and Arabic**
- Gregorian date cross-reference

### Daily Duas and Dhikr
- **20+ authentic duas** covering daily life situations:
  - Morning and Evening remembrance
  - Before/After eating
  - Entering/Leaving the mosque
  - Before/After Wudu (ablution)
  - Entering/Leaving home
  - Travel, Distress, Istikhara
  - Dhikr: SubhanAllah, Alhamdulillah, Allahu Akbar
  - Seeking Forgiveness (Astaghfirullah)
  - Salawat upon the Prophet (peace be upon him)
- **Context-aware**: shows relevant dua based on time of day
- Arabic text, transliteration, and English translation

### 99 Names of Allah (Asma ul Husna)
- **Daily rotating** Name of Allah sensor
- All 99 names with Arabic text and English meaning
- Service to fetch any specific name or all names

### Inspirational Islamic Quotes
- **30 curated quotes** from the Quran and authentic Hadiths
- Daily rotating quote with **Arabic text and source**
- Sources include Sahih Bukhari, Sahih Muslim, Jami at-Tirmidhi, and more

### Tasbih (Digital Counter)
- Digital Tasbih counter for Dhikr
- **Services**: increment, reset, set target, set dhikr text
- Track completed sets and remaining count
- Customizable target (default 33)

### Ramadan / Fasting Tracker
- Automatic detection when it is **Ramadan** (9th Hijri month)
- Current Ramadan day number and days remaining
- **Suhoor** (pre-dawn meal) end time (= Fajr)
- **Iftar** (fast-breaking) time (= Maghrib)

### Zakat Calculator
- Calculate your annual **Zakat obligation** (2.5%)
- Supports: cash savings, gold, silver, business assets, stocks, rental income
- Deduct debts for net Zakatable amount
- Multi-currency support

### Hajj and Umrah Guides
- Complete **step-by-step Hajj guide** with all 10 pillars/steps
- Complete **Umrah guide** with all 5 steps
- Each step includes Arabic name, description, and practical tips

### Islamic Greeting Cards
- **12 occasion templates**: Eid ul-Fitr, Eid ul-Adha, Ramadan, Jummah, New Year, Mawlid, Isra and Mi'raj, Laylat al-Qadr, Wedding, New Baby, General, Condolence
- Personalize with recipient name and custom message
- Arabic text included

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

### Makkah Live
- **Live stream** link from Masjid al-Haram, Makkah
- Always-available sensor for quick access

### Prayer Requests
- Submit prayer requests via Home Assistant service
- Category support: health, guidance, forgiveness, family, success, travel, deceased
- Fires Home Assistant events for automation with notifications

---

## Installation

### HACS (Recommended)

1. Open **HACS** in your Home Assistant instance.
2. Click the **three dots** menu in the top right.
3. Select **Custom repositories**.
4. Add `https://github.com/awjaq/Muslim-Assistant` with category **Integration**.
5. Search for **Muslim Assistant** and click **Install**.
6. Restart Home Assistant.

### Manual Installation

1. Download or clone the repository:
   ```
   git clone https://github.com/awjaq/Muslim-Assistant.git
   ```
2. Copy the `custom_components/muslim_assistant` folder into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant.

---

## Configuration

### No API Keys Needed

Muslim Assistant uses **free, open APIs** that require **no API keys or accounts**:

- **[Aladhan API](https://aladhan.com/prayer-times-api)** -- Prayer times, Qibla, Hijri calendar (free, no key)
- **[Al Quran Cloud API](https://alquran.cloud/api)** -- Quran text, translations, audio (free, no key)
- **[OpenStreetMap Overpass API](https://overpass-api.de/)** -- Mosque and halal restaurant finder (free, no key)

You don't need to configure or enter any API keys. Everything works out of the box.

### Initial Setup

1. Go to **Settings > Devices & Services**.
2. Click **+ Add Integration**.
3. Search for **Muslim Assistant**.
4. Configure:
   - **Name** -- Display name (default: "Muslim Assistant")
   - **Calculation Method** -- Choose from 16+ methods (see table below)
   - **School** -- Standard (Shafi/Maliki/Hanbali) or Hanafi

> **Location is automatic!** Muslim Assistant uses your Home Assistant's configured location (Settings > System > General). If you're using the HA mobile app, your phone's GPS is used. No need to enter latitude/longitude manually.

### Options Flow (v2.0)

After initial setup, you can reconfigure audio, prayer, and automation settings at any time without removing the integration:

1. Go to **Settings > Devices & Services**.
2. Find **Muslim Assistant** and click **Configure**.
3. Choose a settings category:

**Audio & Speaker Settings:**
- Quran reciter (11 world-renowned reciters)
- Adhan sound
- Target speakers — **multi-select device picker** showing all your media players (Alexa, Google Home, Sonos, phones, etc.). Audio plays on all selected devices simultaneously.

**Prayer Time Adjustments:**
- Per-prayer offsets from -30 to +30 minutes

**Automations:**
- Toggle built-in automations on/off (see [Built-in Automations](#built-in-automations) below)

---

## Calculation Methods

| Method | Description / Region |
|--------|----------------------|
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

---

## Sensors (18 Total)

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Fajr Prayer Time | `sensor.muslim_assistant_fajr_prayer_time` | Fajr prayer time (adjustable offset) |
| Sunrise | `sensor.muslim_assistant_sunrise_prayer_time` | Sunrise time (adjustable offset) |
| Dhuhr Prayer Time | `sensor.muslim_assistant_dhuhr_prayer_time` | Dhuhr prayer time (adjustable offset) |
| Asr Prayer Time | `sensor.muslim_assistant_asr_prayer_time` | Asr prayer time (adjustable offset) |
| Maghrib Prayer Time | `sensor.muslim_assistant_maghrib_prayer_time` | Maghrib prayer time (adjustable offset) |
| Isha Prayer Time | `sensor.muslim_assistant_isha_prayer_time` | Isha prayer time (adjustable offset) |
| Next Prayer | `sensor.muslim_assistant_next_prayer` | Next upcoming prayer with countdown |
| Qibla Direction | `sensor.muslim_assistant_qibla_direction` | Compass bearing to Makkah (degrees, cardinal direction, instructions attribute) |
| Hijri Date | `sensor.muslim_assistant_hijri_date` | Current Islamic calendar date |
| Daily Dua | `sensor.muslim_assistant_daily_dua` | Context-aware daily supplication |
| Quran Verse | `sensor.muslim_assistant_quran_verse` | Quran verse of the day (includes `audio_url` attribute in v2.0) |
| Ramadan Tracker | `sensor.muslim_assistant_ramadan_tracker` | Ramadan fasting tracker |
| Tasbih Counter | `sensor.muslim_assistant_tasbih_counter` | Digital Tasbih counter |
| Name of Allah | `sensor.muslim_assistant_name_of_allah` | Daily rotating Name of Allah |
| Islamic Quote | `sensor.muslim_assistant_islamic_quote` | Daily inspirational quote |
| Nearby Mosques | `sensor.muslim_assistant_nearby_mosques` | Count of nearby mosques |
| Halal Restaurants | `sensor.muslim_assistant_halal_restaurants` | Count of nearby halal restaurants |
| Makkah Live | `sensor.muslim_assistant_makkah_live` | Makkah live stream link |

### Media Player Entity (v2.0)

| Entity | Entity ID | Description |
|--------|-----------|-------------|
| Audio Player | `media_player.muslim_assistant_audio_player` | Playback entity for Adhan and Quran audio. Reports state (playing, idle, paused) and current media metadata. |

---

## Services (16 Total)

### `muslim_assistant.play_adhan` (v2.0)

Play the Adhan call to prayer on the configured media player. Works with Amazon Echo/Alexa, Google Home/Nest, Sonos, Chromecast, HomePod, and any Home Assistant `media_player` entity.

```yaml
service: muslim_assistant.play_adhan
data:
  entity_id: media_player.living_room_speaker
```

### `muslim_assistant.play_quran` (v2.0)

Play Quran audio for a specific surah using the configured reciter on the target media player. Optionally override the reciter for a single call.

```yaml
service: muslim_assistant.play_quran
data:
  surah_number: 36
  entity_id: media_player.bedroom_speaker
  reciter: "Mishary Rashid Alafasy"
```

### `muslim_assistant.get_surah`

Fetch a complete surah with Arabic text and English translation.

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

Set the dhikr text for the Tasbih counter.

```yaml
service: muslim_assistant.tasbih_set_dhikr
data:
  dhikr: "SubhanAllah"
```

### `muslim_assistant.get_dua`

Get a dua from the collection, optionally filtered by category.

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

---

## Example Automations

### Play Adhan on Speaker at Every Prayer Time (v2.0)

Automatically play the Adhan on your smart speaker whenever the next prayer changes.

```yaml
automation:
  - alias: "Play Adhan at Prayer Time"
    description: "Plays the Adhan on the living room speaker at each prayer time"
    trigger:
      - platform: state
        entity_id: sensor.muslim_assistant_next_prayer
    condition:
      - condition: template
        value_template: >
          {{ trigger.from_state.state != trigger.to_state.state }}
    action:
      - service: muslim_assistant.play_adhan
        data:
          entity_id: media_player.living_room_speaker
```

### Play Quran Recitation After Fajr (v2.0)

Stream Surah Al-Mulk every morning after Fajr prayer.

```yaml
automation:
  - alias: "Quran After Fajr"
    description: "Plays Surah Al-Mulk on the bedroom speaker 15 minutes after Fajr"
    trigger:
      - platform: template
        value_template: >
          {{ states('sensor.muslim_assistant_fajr_prayer_time') != 'unknown' }}
      - platform: time
        at: sensor.muslim_assistant_fajr_prayer_time
    action:
      - delay: "00:15:00"
      - service: muslim_assistant.play_quran
        data:
          surah_number: 67
          entity_id: media_player.bedroom_speaker
          reciter: "Mishary Rashid Alafasy"
```

### Play Surah Al-Kahf on Friday (v2.0)

Stream Surah Al-Kahf every Friday morning.

```yaml
automation:
  - alias: "Surah Al-Kahf on Jummah"
    description: "Plays Surah Al-Kahf on Fridays"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: time
        weekday:
          - fri
    action:
      - service: muslim_assistant.play_quran
        data:
          surah_number: 18
          entity_id: media_player.living_room_speaker
```

### Adhan Notification (Mobile)

```yaml
automation:
  - alias: "Adhan Mobile Notification"
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

---

## Dashboard

Muslim Assistant **automatically creates a dashboard** in your sidebar when the integration is set up. Look for **"Muslim Assistant"** in the left sidebar after installation.

The dashboard includes 4 organized sections:
- **Prayer Times** -- Hero next prayer card + full daily schedule
- **Qibla & Calendar** -- Compass direction, full Hijri date (Arabic + English), Ramadan tracker
- **Daily Inspiration** -- Quran verse, Name of Allah, Dua, Islamic quote
- **Audio & Tools** -- Adhan/Quran playback buttons, Tasbih counter, nearby places, Makkah Live, guides

### Manual Setup (if auto-creation doesn't work)

1. Go to **Settings > Dashboards**.
2. Click **+ Add Dashboard**.
3. Name: **Muslim Assistant**, Icon: `mdi:mosque`.
4. Open it > **Edit Dashboard** > **3-dot menu** > **Raw configuration editor**.
5. Paste the contents of `dashboard/muslim_assistant_dashboard.yaml` from this repository.
6. Click **Save**.

---

## Integration Icon (Brand Logo)

The icon on the **Settings > Integrations** page in Home Assistant comes from the [home-assistant/brands](https://github.com/home-assistant/brands) repository, not from local files. To get the Muslim Assistant icon showing:

### Submit to HA Brands Repository

1. Fork [home-assistant/brands](https://github.com/home-assistant/brands).
2. Create a folder: `custom_integrations/muslim_assistant/`
3. Copy the PNG files from the `brand/` folder in this repository:
   - `icon.png` (256x256)
   - `icon@2x.png` (512x512)
4. Submit a Pull Request.
5. Once merged, the icon will appear automatically in Home Assistant.

The `brand/` folder in this repository contains the ready-to-submit PNG files.

> **Note:** Entity icons (prayer times, Quran, Qibla, etc.) already display correctly using Material Design Icons in the HA UI. The brand logo only affects the integration card on the Settings > Integrations page.

---

## Built-in Automations

Muslim Assistant includes **built-in automations** that you can enable with a single toggle — no YAML needed. Go to **Configure > Automations** to turn them on or off.

| Automation | What It Does |
|-----------|-------------|
| **Play Adhan at prayer times** | Automatically plays the Adhan on your configured speakers when each prayer time arrives. Skips Sunrise. |
| **Prayer time notifications** | Sends a mobile notification to your phone when each prayer time arrives. |
| **Quran after Fajr** | Plays Surah Al-Mulk on your speakers 15 minutes after Fajr prayer. |
| **Surah Al-Kahf on Fridays** | Plays Surah Al-Kahf on your speakers every Friday. |
| **Suhoor reminder (Ramadan)** | Sends a notification reminding you to eat Suhoor when Fajr is approaching during Ramadan. |

> **Note:** For notification-based automations, you need to select a **Notification Service** (e.g., `notify.mobile_app_your_phone`) in the Automations settings. For audio automations, make sure you have **Target Speakers** configured in Audio settings.

---

## FAQ

### How do I add the dashboard?

Muslim Assistant **automatically creates a dashboard** in your sidebar when the integration is set up. Look for **"Muslim Assistant"** in the left sidebar.

If it doesn't appear automatically:

1. Go to **Settings > Dashboards**.
2. Click **+ Add Dashboard**.
3. Name: **Muslim Assistant**, Icon: `mdi:mosque`.
4. Open it, click the **pencil icon** (Edit) at the top right.
5. Click the **3-dot menu** > **Raw configuration editor**.
6. Paste the contents of `dashboard/muslim_assistant_dashboard.yaml` from this repository.
7. Click **Save**.

---

### How do I play the Adhan?

There are **3 ways** to play the Adhan:

**Option 1: From the Dashboard**

The Muslim Assistant dashboard has an **"Play Adhan"** button. Just tap it.

**Option 2: Enable Auto-Adhan (Recommended)**

1. Go to **Settings > Devices & Services > Muslim Assistant > Configure**.
2. Select **Automations**.
3. Turn on **"Play Adhan at every prayer time"**.
4. The Adhan will now play automatically on your configured speakers at every prayer time.

**Option 3: Developer Tools (Manual)**

1. Go to **Developer Tools > Services** (or **Actions** in newer HA versions).
2. Select `muslim_assistant.play_adhan`.
3. Click **Perform Action**.

> **Important:** You must configure at least one **Target Speaker** first! Go to **Configure > Audio & Speaker Settings** and select your speakers from the device picker.

---

### How do I get Alexa devices to show up as speakers?

There are **two options** to get your Echo/Alexa devices into Home Assistant:

**Option 1: Official [Alexa Devices](https://www.home-assistant.io/integrations/alexa_devices/) Integration (Built-in, HA 2025.6+)**

1. Go to **Settings > Devices & Services > + Add Integration**.
2. Search for **"Alexa Devices"** and log in with your Amazon account.
3. Requires **multi-factor authentication** via an authenticator app (e.g., Microsoft Authenticator). Enable it in your Amazon account under **Login & Security > 2-step verification > Backup methods > Add new app**.

> **Limitation:** The official integration does **not yet** support full `media_player` entities (planned for a future release). You can use `alexa_devices.send_text_command` to play audio as a workaround, but your Echo devices won't appear in the Muslim Assistant **Target Speakers** picker until media_player support is added.

**Option 2: [Alexa Media Player](https://github.com/alandtse/alexa_media_player) Custom Integration via HACS (Recommended for audio playback)**

1. Open **HACS** in your Home Assistant sidebar.
2. Go to **Integrations** > search for **"Alexa Media Player"**.
3. Install it and **restart Home Assistant**.
4. Go to **Settings > Devices & Services > + Add Integration**.
5. Search for **"Alexa Media Player"** and log in with your Amazon account.
6. After setup, all your Echo/Alexa devices will appear as `media_player.echo_*` entities.

This creates full `media_player` entities, so your Echo devices will show up in the Muslim Assistant **Target Speakers** picker and work with auto-play Adhan, Quran playback, and all audio features.

> **Note:** You can run both integrations simultaneously. The official integration is more stable but has fewer features. The HACS integration provides full media_player control but uses an unofficial API.

---

### How do I get Google Home / Nest speakers to show up?

Google Cast devices (Google Home, Nest Hub, Chromecast, etc.) should appear automatically via the built-in **Google Cast** integration. If they don't:

1. Go to **Settings > Devices & Services**.
2. Check if **Google Cast** is listed. If not, click **+ Add Integration** and search for **Google Cast**.
3. Your Google/Nest speakers will appear as `media_player.*` entities.

---

### How do I play audio on my phone?

Install the **Home Assistant Companion App** on your phone (iOS or Android). It automatically registers your phone as a `media_player` entity. Then select it in **Configure > Audio & Speaker Settings > Target Speakers**.

---

### Can I play audio on multiple speakers at the same time?

Yes! The Target Speakers picker supports **multi-select**. Pick as many devices as you want — Alexa, Google Home, Sonos, phones, etc. Audio will play on **all selected devices simultaneously**.

1. Go to **Configure > Audio & Speaker Settings**.
2. Click the **Target Speakers** field.
3. Select multiple devices from the list.

---

### How do I set up automations without writing YAML?

Muslim Assistant includes **built-in automations** that you can toggle on/off:

1. Go to **Settings > Devices & Services > Muslim Assistant > Configure**.
2. Select **Automations**.
3. Toggle on the automations you want:
   - Auto-play Adhan at prayer times
   - Prayer time mobile notifications
   - Quran after Fajr
   - Surah Al-Kahf on Fridays
   - Suhoor reminders during Ramadan
4. If using notification automations, select your **Notification Service** (e.g., `notify.mobile_app_your_phone`).

No YAML, no manual automation setup — everything is handled internally by the integration.

---

### How do I change the Quran reciter or Adhan sound?

1. Go to **Settings > Devices & Services > Muslim Assistant > Configure**.
2. Select **Audio & Speaker Settings**.
3. Pick your preferred **Quran Reciter** from 11 available reciters.
4. Pick your preferred **Adhan Sound**.
5. Click **Submit**.

---

### How do I adjust prayer times to match my local mosque?

1. Go to **Settings > Devices & Services > Muslim Assistant > Configure**.
2. Select **Prayer Time Adjustments**.
3. Set an offset from **-30 to +30 minutes** for each prayer (Fajr, Dhuhr, Asr, Maghrib, Isha).
4. Click **Submit**.

---

### Where does the integration get its data? Do I need API keys?

No API keys needed. Muslim Assistant uses **free, open APIs**:

- **[Aladhan API](https://aladhan.com)** — Prayer times, Qibla, Hijri calendar
- **[Al Quran Cloud API](https://alquran.cloud)** — Quran text, translations, audio
- **[OpenStreetMap Overpass API](https://overpass-api.de)** — Mosque and halal restaurant finder

Everything works out of the box with no configuration.

---

### How does location work? Do I need to enter my coordinates?

No. Muslim Assistant **automatically detects your location** from your Home Assistant settings (**Settings > System > General**). If you use the HA Companion App, your phone's GPS is used. You don't need to enter latitude/longitude manually.

---

## API Credits

This integration uses the following free APIs:

- [Aladhan Prayer Times API](https://aladhan.com/prayer-times-api) -- Prayer times, Qibla direction, and Hijri calendar
- [Al Quran Cloud API](https://alquran.cloud/) -- Quran text, translations, and audio recitations
- [OpenStreetMap Overpass API](https://overpass-api.de/) -- Mosque and halal restaurant finder

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request at [https://github.com/awjaq/Muslim-Assistant](https://github.com/awjaq/Muslim-Assistant).

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes.
4. Push to your branch and open a Pull Request.

For bugs or feature requests, please [open an issue](https://github.com/awjaq/Muslim-Assistant/issues).

---

## License

This project is open source and available under the [MIT License](LICENSE).
