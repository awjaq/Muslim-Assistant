# Alexa / Echo Guide

How to use Amazon Echo devices with Muslim Assistant: connecting them to Home Assistant, why they behave differently from other speakers, playing the real Adhan at prayer time, and playing it on several Echos at once.

**Contents**

1. [Connect your Echo devices to Home Assistant](#1-connect-your-echo-devices-to-home-assistant)
2. [Why Alexa said it "can't play" the Adhan](#2-why-alexa-said-it-cant-play-the-adhan)
3. [Choose what your Echos do](#3-choose-what-your-echos-do)
4. [Play the real Adhan at prayer time](#4-play-the-real-adhan-at-prayer-time)
5. [Play the Adhan on several Echos at once](#5-play-the-adhan-on-several-echos-at-once)
6. [Test it](#6-test-it)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Connect your Echo devices to Home Assistant

Echo devices only show up in the Muslim Assistant **Target Speakers** list when they are `media_player` entities in Home Assistant. There are two integrations for Alexa. Only one of them does that today.

| | Alexa Media Player (HACS) | Alexa Devices (built in) |
|---|---|---|
| Shows Echos in **Target Speakers** | Yes | Not yet |
| Announcements | Yes | Yes |
| Run Alexa routines | Yes | No |
| Works with Muslim Assistant | **Yes, use this one** | No |

### Install Alexa Media Player

1. Open **HACS** in the Home Assistant sidebar.
2. Search for **Alexa Media Player** and install it.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → + Add Integration**, search for **Alexa Media Player** and sign in with your Amazon account.
5. Your Echos appear as `media_player.*` entities, for example `media_player.kitchen_echo_show`.

You can keep the built-in [Alexa Devices](https://www.home-assistant.io/integrations/alexa_devices/) integration as well. The two can run side by side.

---

## 2. Why Alexa said it "can't play" the Adhan

Google Home, Sonos and phones can play an MP3 link sent from Home Assistant. Echo devices can't. When an Echo receives a link, Alexa treats it as a voice search, finds nothing, and says it can't play it.

Muslim Assistant now never sends the audio link to an Echo. You choose what your Echos do instead (next section). Any other speakers in **Target Speakers** still play the full Adhan audio.

**Quran playback always skips Echo devices**, for the same reason.

---

## 3. Choose what your Echos do

Go to **Settings → Devices & Services → Muslim Assistant → Configure → Audio & Speaker Settings** and set **Alexa / Echo behavior**:

| Option | What happens at prayer time |
|---|---|
| **Announce the prayer name** (default) | Every Echo in **Target Speakers** says "It is time for Dhuhr prayer". |
| **Run an Alexa routine** | Muslim Assistant starts an Alexa routine you made. The routine can play the real Adhan. See [section 4](#4-play-the-real-adhan-at-prayer-time). |
| **Stay silent** | Echos are skipped. |

For the Adhan to play automatically, turn on **Configure → Automations → Play Adhan at every prayer time**. It starts at the exact prayer minute.

---

## 4. Play the real Adhan at prayer time

Alexa can't play the Adhan file directly, but an Alexa routine can play an Adhan from a music service or skill. Muslim Assistant starts that routine at prayer time.

### Make the routine in the Alexa app

1. Go to **More → Routines → +**.
2. **When this happens → Voice**: type a phrase, for example `adhan time`.
3. **Add action**, then choose one:
   - **Music & Podcasts**: search for an Adhan, for example `Adhan Makkah` on Amazon Music. Best choice if you want several Echos, see [section 5](#5-play-the-adhan-on-several-echos-at-once).
   - **Customized**: type what you'd say to Alexa, for example `play Adhan Makkah on Amazon Music`, or open an Adhan skill.
4. **From**: choose the Echo, or speaker group, that should play it.
5. Save the routine, then say "Alexa, adhan time" once to check that it plays.

### Connect it to Muslim Assistant

1. Go to **Muslim Assistant → Configure → Audio & Speaker Settings**.
2. Set **Alexa / Echo behavior** to **Run an Alexa routine**.
3. In **Alexa routine for the Adhan**, type the routine's voice phrase exactly, for example `adhan time`.
4. Keep at least one Echo in **Target Speakers**. Muslim Assistant uses it to start the routine.
5. Make sure **Configure → Automations → Play Adhan at every prayer time** is on.

---

## 5. Play the Adhan on several Echos at once

### With "Announce the prayer name"

Select all the Echos you want in **Target Speakers**. Every selected Echo makes the announcement.

### With "Run an Alexa routine"

The routine decides which Echos play, not the **Target Speakers** list. Muslim Assistant starts the routine **once**, however many Echos are selected, so the Adhan doesn't play twice.

To play on several Echos together, use a speaker group:

1. In the Alexa app, go to **Devices → + → Combine Speakers → Multi-room music**.
2. Pick the Echos, for example Kitchen, Main Bedroom and Kids Room, and name the group, for example `Adhan Speakers`. If a group like **Everywhere** already has the right speakers, use that one.
3. Edit your Adhan routine and use a **Music & Podcasts** action to play the Adhan.
4. Set that action's **From** to the speaker group. All the speakers in the group play the Adhan together.

The **Customized** action can only play on one device. If you prefer it, add one **Customized** action per Echo, each with its own **From** device. They start a second or two apart rather than exactly together.

---

## 6. Test it

1. Go to **Developer Tools → Actions** (called **Tools → Actions** in newer versions).
2. Choose **`muslim_assistant.play_adhan`**. You can fill in **Prayer**, for example `Dhuhr`, to hear the prayer name in announcements.
3. Click **Perform Action**.

Your Echos should announce the prayer or start your routine, depending on the option you chose.

---

## 7. Troubleshooting

| Problem | What to check |
|---|---|
| Alexa still says "I can't play that" | You're on an older version. In HACS, open Muslim Assistant → ⋮ → **Redownload**, pick **`main`**, then restart Home Assistant. |
| HACS redownload fails with a 404 | You picked an old commit such as `3eac45f` in the version list. Pick **`main`** instead. |
| My Echos aren't in **Target Speakers** | Install **Alexa Media Player** ([section 1](#1-connect-your-echo-devices-to-home-assistant)). The built-in Alexa Devices integration doesn't provide them yet. |
| Announce mode is silent | Check that the `notify.alexa_media` action exists in **Developer Tools → Actions**. If it doesn't, Alexa Media Player isn't set up. Home Assistant's log shows a Muslim Assistant warning when this happens. |
| Routine mode does nothing | The text in **Alexa routine for the Adhan** must match the routine's voice phrase exactly. Say the phrase to Alexa to confirm the routine works on its own. |
| Adhan plays on one Echo only | The routine plays where its action's **From** points. Set it to a speaker group ([section 5](#5-play-the-adhan-on-several-echos-at-once)). |
| Quran doesn't play on my Echo | Expected. Echos can't stream the recitation. Add a Google, Sonos or phone speaker to **Target Speakers** for Quran audio. |
