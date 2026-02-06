"""Constants for Muslim Assistant integration."""

DOMAIN = "muslim_assistant"
NAME = "Muslim Assistant"
VERSION = "2.0.0"

# Configuration keys
CONF_CALC_METHOD = "calculation_method"
CONF_SCHOOL = "school"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_FAJR_OFFSET = "fajr_offset"
CONF_DHUHR_OFFSET = "dhuhr_offset"
CONF_ASR_OFFSET = "asr_offset"
CONF_MAGHRIB_OFFSET = "maghrib_offset"
CONF_ISHA_OFFSET = "isha_offset"
CONF_QURAN_RECITER = "quran_reciter"
CONF_ADHAN_SOUND = "adhan_sound"
CONF_TARGET_PLAYER = "target_media_player"

# Defaults
DEFAULT_CALC_METHOD = "ISNA"
DEFAULT_SCHOOL = "Standard"

# Calculation Methods (from Aladhan API)
CALC_METHODS = {
    "Shia Ithna-Ansari": 0,
    "University of Islamic Sciences, Karachi": 1,
    "Islamic Society of North America (ISNA)": 2,
    "Muslim World League": 3,
    "Umm Al-Qura University, Makkah": 4,
    "Egyptian General Authority of Survey": 5,
    "Institute of Geophysics, University of Tehran": 7,
    "Gulf Region": 8,
    "Kuwait": 9,
    "Qatar": 10,
    "Majlis Ugama Islam Singapura, Singapore": 11,
    "Union Organization Islamic de France": 12,
    "Diyanet Isleri Baskanligi, Turkey": 13,
    "Spiritual Administration of Muslims of Russia": 14,
    "Moonsighting Committee Worldwide": 15,
    "Dubai": 16,
}

CALC_METHOD_MAP = {
    "Shia Ithna-Ansari": 0,
    "Karachi": 1,
    "ISNA": 2,
    "MWL": 3,
    "Makkah": 4,
    "Egypt": 5,
    "Tehran": 7,
    "Gulf": 8,
    "Kuwait": 9,
    "Qatar": 10,
    "Singapore": 11,
    "France": 12,
    "Turkey": 13,
    "Russia": 14,
    "Moonsighting": 15,
    "Dubai": 16,
}

# Schools
SCHOOL_STANDARD = 0  # Shafi, Maliki, Hanbali
SCHOOL_HANAFI = 1

SCHOOLS = {
    "Standard": SCHOOL_STANDARD,
    "Hanafi": SCHOOL_HANAFI,
}

# Prayer names
PRAYER_FAJR = "Fajr"
PRAYER_SUNRISE = "Sunrise"
PRAYER_DHUHR = "Dhuhr"
PRAYER_ASR = "Asr"
PRAYER_MAGHRIB = "Maghrib"
PRAYER_ISHA = "Isha"
PRAYER_MIDNIGHT = "Midnight"

PRAYERS = [
    PRAYER_FAJR,
    PRAYER_SUNRISE,
    PRAYER_DHUHR,
    PRAYER_ASR,
    PRAYER_MAGHRIB,
    PRAYER_ISHA,
]

ADJUSTABLE_PRAYERS = [
    PRAYER_FAJR,
    PRAYER_DHUHR,
    PRAYER_ASR,
    PRAYER_MAGHRIB,
    PRAYER_ISHA,
]

# API endpoints
ALADHAN_API_BASE = "https://api.aladhan.com/v1"
QURAN_API_BASE = "https://api.alquran.cloud/v1"
QURAN_CDN_BASE = "https://cdn.islamic.network/quran"
OVERPASS_API = "https://overpass-api.de/api/interpreter"

# Update intervals (seconds)
UPDATE_INTERVAL_PRAYER = 300  # 5 minutes
UPDATE_INTERVAL_HIJRI = 3600  # 1 hour
UPDATE_INTERVAL_QURAN = 86400  # 24 hours

# Platforms
PLATFORMS = ["sensor", "media_player"]

# ── Quran Reciters (API edition identifiers) ──────────────────────

QURAN_RECITERS = {
    "Mishary Rashid Alafasy": "ar.alafasy",
    "Abdul Rahman Al-Sudais": "ar.abdurrahmaansudais",
    "Abdul Basit (Murattal)": "ar.abdulbasitmurattal",
    "Abdul Basit (Mujawwad)": "ar.abdulbasitmujawwad",
    "Mohamed Siddiq Al-Minshawi": "ar.minshawi",
    "Mahmoud Khalil Al-Husary": "ar.husary",
    "Abu Bakr Al-Shatri": "ar.shaatree",
    "Saad Al-Ghamdi": "ar.saadalghamidi",
    "Maher Al-Muaiqly": "ar.maaboralmuaiqly",
    "Hani Ar-Rifai": "ar.hanaborifai",
    "Ahmed ibn Ali Al-Ajamy": "ar.ahmedajamy",
}

DEFAULT_RECITER = "Mishary Rashid Alafasy"

# ── Adhan Audio ───────────────────────────────────────────────────
# Al Quran Cloud CDN has adhan audio; these are reciter-based audio IDs.
# Users play Adhan through any HA media_player (Alexa, Google, Sonos, etc.)

ADHAN_SOUNDS = {
    "Makkah (Mishary Alafasy)": "mishary",
    "Madinah": "madinah",
    "Al-Aqsa": "alaqsa",
    "Egypt (Abdul Basit)": "abdulbasit",
}

DEFAULT_ADHAN = "Makkah (Mishary Alafasy)"

# Audio bitrate for CDN
AUDIO_BITRATE = 128

# Makkah Live Stream
MAKKAH_LIVE_STREAM_URL = "https://www.youtube.com/@saudiqurantv/live"

# ── Duas collection ───────────────────────────────────────────────

DAILY_DUAS = [
    {
        "name": "Morning Remembrance",
        "arabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَهَ إِلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ",
        "transliteration": "Asbahna wa asbahal-mulku lillah, walhamdu lillah, la ilaha illallahu wahdahu la sharika lah",
        "translation": "We have reached the morning and at this very time all sovereignty belongs to Allah. All praise is for Allah. None has the right to be worshipped except Allah, alone, without partner.",
    },
    {
        "name": "Evening Remembrance",
        "arabic": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَهَ إِلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ",
        "transliteration": "Amsayna wa amsal-mulku lillah, walhamdu lillah, la ilaha illallahu wahdahu la sharika lah",
        "translation": "We have reached the evening and at this very time all sovereignty belongs to Allah. All praise is for Allah. None has the right to be worshipped except Allah, alone, without partner.",
    },
    {
        "name": "Before Sleeping",
        "arabic": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
        "transliteration": "Bismika Allahumma amootu wa ahya",
        "translation": "In Your name O Allah, I live and die.",
    },
    {
        "name": "Upon Waking Up",
        "arabic": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ",
        "transliteration": "Alhamdu lillahil-ladhi ahyana ba'da ma amatana wa ilayhin-nushur",
        "translation": "All praise is for Allah who gave us life after having taken it from us and unto Him is the resurrection.",
    },
    {
        "name": "Before Eating",
        "arabic": "بِسْمِ اللَّهِ",
        "transliteration": "Bismillah",
        "translation": "In the name of Allah.",
    },
    {
        "name": "After Eating",
        "arabic": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلاَ قُوَّةٍ",
        "transliteration": "Alhamdu lillahil-ladhi at'amani hadha wa razaqanihi min ghayri hawlin minni wa la quwwah",
        "translation": "All praise is for Allah who fed me this and provided it for me without any might or power from myself.",
    },
    {
        "name": "Entering the Mosque",
        "arabic": "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ",
        "transliteration": "Allaahum-maf-tah lee abwaaba rahmatika",
        "translation": "O Allah, open the gates of Your mercy for me.",
    },
    {
        "name": "Leaving the Mosque",
        "arabic": "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ",
        "transliteration": "Allaahumma 'innee 'as'aluka min fadhlika",
        "translation": "O Allah, I ask You from Your favour.",
    },
    {
        "name": "Before Wudu (Ablution)",
        "arabic": "بِسْمِ اللَّهِ",
        "transliteration": "Bismillah",
        "translation": "In the name of Allah.",
    },
    {
        "name": "After Wudu (Ablution)",
        "arabic": "أَشْهَدُ أَنْ لاَ إِلَهَ إِلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ، وَأَشْهَدُ أَنَّ مُحَمَّداً عَبْدُهُ وَرَسُولُهُ",
        "transliteration": "Ashhadu an la ilaha illallahu wahdahu la sharika lahu, wa ashhadu anna Muhammadan 'abduhu wa rasuluh",
        "translation": "I bear witness that none has the right to be worshipped except Allah, alone without partner, and I bear witness that Muhammad is His slave and Messenger.",
    },
    {
        "name": "Entering the Home",
        "arabic": "بِسْمِ اللَّهِ وَلَجْنَا، وَبِسْمِ اللَّهِ خَرَجْنَا، وَعَلَى رَبِّنَا تَوَكَّلْنَا",
        "transliteration": "Bismillahi walajna, wa bismillahi kharajna, wa 'ala Rabbina tawakkalna",
        "translation": "In the name of Allah we enter and in the name of Allah we leave, and upon our Lord we place our trust.",
    },
    {
        "name": "Leaving the Home",
        "arabic": "بِسْمِ اللَّهِ، تَوَكَّلْتُ عَلَى اللَّهِ، وَلاَ حَوْلَ وَلاَ قُوَّةَ إِلاَّ بِاللَّهِ",
        "transliteration": "Bismillah, tawakkaltu 'alallah, wa la hawla wa la quwwata illa billah",
        "translation": "In the name of Allah, I place my trust in Allah, and there is no might nor power except with Allah.",
    },
    {
        "name": "Istikhara (Seeking Guidance)",
        "arabic": "اللَّهُمَّ إِنِّي أَسْتَخِيرُكَ بِعِلْمِكَ، وَأَسْتَقْدِرُكَ بِقُدْرَتِكَ، وَأَسْأَلُكَ مِنْ فَضْلِكَ الْعَظِيمِ",
        "transliteration": "Allahumma inni astakhiruka bi'ilmika, wa astaqdiruka biqudratika, wa as'aluka min fadlikal-'azim",
        "translation": "O Allah, I seek Your guidance by virtue of Your knowledge, and I seek ability by virtue of Your power, and I ask You of Your great bounty.",
    },
    {
        "name": "For Travel",
        "arabic": "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ",
        "transliteration": "Subhanal-ladhi sakh-khara lana hadha wa ma kunna lahu muqrinin, wa inna ila Rabbina lamunqalibun",
        "translation": "How perfect He is, the One Who has placed this (transport) at our service and we ourselves would not have been capable of that, and to our Lord is our final destiny.",
    },
    {
        "name": "When in Distress",
        "arabic": "لاَ إِلَهَ إِلاَّ اللَّهُ الْعَظِيمُ الْحَلِيمُ، لاَ إِلَهَ إِلاَّ اللَّهُ رَبُّ الْعَرْشِ الْعَظِيمِ",
        "transliteration": "La ilaha illallahul-'Adhimul-Halim, la ilaha illallahu Rabbul-'Arshil-'Adhim",
        "translation": "None has the right to be worshipped except Allah, the Mighty, the Forbearing. None has the right to be worshipped except Allah, Lord of the magnificent throne.",
    },
    {
        "name": "Dhikr - SubhanAllah",
        "arabic": "سُبْحَانَ اللَّهِ",
        "transliteration": "SubhanAllah",
        "translation": "Glory be to Allah. (Recite 33 times)",
    },
    {
        "name": "Dhikr - Alhamdulillah",
        "arabic": "الْحَمْدُ لِلَّهِ",
        "transliteration": "Alhamdulillah",
        "translation": "All praise is for Allah. (Recite 33 times)",
    },
    {
        "name": "Dhikr - Allahu Akbar",
        "arabic": "اللَّهُ أَكْبَرُ",
        "transliteration": "Allahu Akbar",
        "translation": "Allah is the Greatest. (Recite 34 times)",
    },
    {
        "name": "Seeking Forgiveness",
        "arabic": "أَسْتَغْفِرُ اللَّهَ",
        "transliteration": "Astaghfirullah",
        "translation": "I seek forgiveness from Allah.",
    },
    {
        "name": "Salawat upon the Prophet",
        "arabic": "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ",
        "transliteration": "Allahumma salli 'ala Muhammadin wa 'ala ali Muhammad",
        "translation": "O Allah, send prayers upon Muhammad and the family of Muhammad.",
    },
]

# Quran Surah info
SURAH_COUNT = 114

# ── 99 Names of Allah (Asma ul Husna) ────────────────────────────

NAMES_OF_ALLAH = [
    {"number": 1, "name": "Ar-Rahman", "arabic": "الرَّحْمَنُ", "meaning": "The Most Gracious"},
    {"number": 2, "name": "Ar-Rahim", "arabic": "الرَّحِيمُ", "meaning": "The Most Merciful"},
    {"number": 3, "name": "Al-Malik", "arabic": "الْمَلِكُ", "meaning": "The King"},
    {"number": 4, "name": "Al-Quddus", "arabic": "الْقُدُّوسُ", "meaning": "The Most Holy"},
    {"number": 5, "name": "As-Salam", "arabic": "السَّلاَمُ", "meaning": "The Source of Peace"},
    {"number": 6, "name": "Al-Mu'min", "arabic": "الْمُؤْمِنُ", "meaning": "The Guardian of Faith"},
    {"number": 7, "name": "Al-Muhaymin", "arabic": "الْمُهَيْمِنُ", "meaning": "The Protector"},
    {"number": 8, "name": "Al-Aziz", "arabic": "الْعَزِيزُ", "meaning": "The Almighty"},
    {"number": 9, "name": "Al-Jabbar", "arabic": "الْجَبَّارُ", "meaning": "The Compeller"},
    {"number": 10, "name": "Al-Mutakabbir", "arabic": "الْمُتَكَبِّرُ", "meaning": "The Greatest"},
    {"number": 11, "name": "Al-Khaliq", "arabic": "الْخَالِقُ", "meaning": "The Creator"},
    {"number": 12, "name": "Al-Bari'", "arabic": "الْبَارِئُ", "meaning": "The Maker of Order"},
    {"number": 13, "name": "Al-Musawwir", "arabic": "الْمُصَوِّرُ", "meaning": "The Shaper of Beauty"},
    {"number": 14, "name": "Al-Ghaffar", "arabic": "الْغَفَّارُ", "meaning": "The Forgiving"},
    {"number": 15, "name": "Al-Qahhar", "arabic": "الْقَهَّارُ", "meaning": "The Subduer"},
    {"number": 16, "name": "Al-Wahhab", "arabic": "الْوَهَّابُ", "meaning": "The Giver of All"},
    {"number": 17, "name": "Ar-Razzaq", "arabic": "الرَّزَّاقُ", "meaning": "The Sustainer"},
    {"number": 18, "name": "Al-Fattah", "arabic": "الْفَتَّاحُ", "meaning": "The Opener"},
    {"number": 19, "name": "Al-'Alim", "arabic": "الْعَلِيمُ", "meaning": "The Knower of All"},
    {"number": 20, "name": "Al-Qabid", "arabic": "الْقَابِضُ", "meaning": "The Constrictor"},
    {"number": 21, "name": "Al-Basit", "arabic": "الْبَاسِطُ", "meaning": "The Reliever"},
    {"number": 22, "name": "Al-Khafid", "arabic": "الْخَافِضُ", "meaning": "The Abaser"},
    {"number": 23, "name": "Ar-Rafi'", "arabic": "الرَّافِعُ", "meaning": "The Exalter"},
    {"number": 24, "name": "Al-Mu'izz", "arabic": "الْمُعِزُّ", "meaning": "The Bestower of Honours"},
    {"number": 25, "name": "Al-Mudhill", "arabic": "المُذِلُّ", "meaning": "The Humiliator"},
    {"number": 26, "name": "As-Sami'", "arabic": "السَّمِيعُ", "meaning": "The Hearer of All"},
    {"number": 27, "name": "Al-Basir", "arabic": "الْبَصِيرُ", "meaning": "The Seer of All"},
    {"number": 28, "name": "Al-Hakam", "arabic": "الْحَكَمُ", "meaning": "The Judge"},
    {"number": 29, "name": "Al-'Adl", "arabic": "الْعَدْلُ", "meaning": "The Just"},
    {"number": 30, "name": "Al-Latif", "arabic": "اللَّطِيفُ", "meaning": "The Subtle One"},
    {"number": 31, "name": "Al-Khabir", "arabic": "الْخَبِيرُ", "meaning": "The All-Aware"},
    {"number": 32, "name": "Al-Halim", "arabic": "الْحَلِيمُ", "meaning": "The Forbearing"},
    {"number": 33, "name": "Al-'Azim", "arabic": "الْعَظِيمُ", "meaning": "The Magnificent"},
    {"number": 34, "name": "Al-Ghafur", "arabic": "الْغَفُورُ", "meaning": "The Forgiver and Hider of Faults"},
    {"number": 35, "name": "Ash-Shakur", "arabic": "الشَّكُورُ", "meaning": "The Rewarder of Thankfulness"},
    {"number": 36, "name": "Al-'Ali", "arabic": "الْعَلِيُّ", "meaning": "The Highest"},
    {"number": 37, "name": "Al-Kabir", "arabic": "الْكَبِيرُ", "meaning": "The Greatest"},
    {"number": 38, "name": "Al-Hafiz", "arabic": "الْحَفِيظُ", "meaning": "The Preserver"},
    {"number": 39, "name": "Al-Muqit", "arabic": "المُقِيتُ", "meaning": "The Nourisher"},
    {"number": 40, "name": "Al-Hasib", "arabic": "الْحسِيبُ", "meaning": "The Accounter"},
    {"number": 41, "name": "Al-Jalil", "arabic": "الْجَلِيلُ", "meaning": "The Mighty"},
    {"number": 42, "name": "Al-Karim", "arabic": "الْكَرِيمُ", "meaning": "The Generous"},
    {"number": 43, "name": "Ar-Raqib", "arabic": "الرَّقِيبُ", "meaning": "The Watchful One"},
    {"number": 44, "name": "Al-Mujib", "arabic": "الْمُجِيبُ", "meaning": "The Responder to Prayer"},
    {"number": 45, "name": "Al-Wasi'", "arabic": "الْوَاسِعُ", "meaning": "The All-Comprehending"},
    {"number": 46, "name": "Al-Hakim", "arabic": "الْحَكِيمُ", "meaning": "The Perfectly Wise"},
    {"number": 47, "name": "Al-Wadud", "arabic": "الْوَدُودُ", "meaning": "The Loving One"},
    {"number": 48, "name": "Al-Majid", "arabic": "الْمَجِيدُ", "meaning": "The Majestic One"},
    {"number": 49, "name": "Al-Ba'ith", "arabic": "الْبَاعِثُ", "meaning": "The Resurrector"},
    {"number": 50, "name": "Ash-Shahid", "arabic": "الشَّهِيدُ", "meaning": "The Witness"},
    {"number": 51, "name": "Al-Haqq", "arabic": "الْحَقُّ", "meaning": "The Truth"},
    {"number": 52, "name": "Al-Wakil", "arabic": "الْوَكِيلُ", "meaning": "The Trustee"},
    {"number": 53, "name": "Al-Qawiyy", "arabic": "الْقَوِيُّ", "meaning": "The Possessor of All Strength"},
    {"number": 54, "name": "Al-Matin", "arabic": "الْمَتِينُ", "meaning": "The Forceful One"},
    {"number": 55, "name": "Al-Waliyy", "arabic": "الْوَلِيُّ", "meaning": "The Governor"},
    {"number": 56, "name": "Al-Hamid", "arabic": "الْحَمِيدُ", "meaning": "The Praised One"},
    {"number": 57, "name": "Al-Muhsi", "arabic": "الْمُحْصِي", "meaning": "The Appraiser"},
    {"number": 58, "name": "Al-Mubdi'", "arabic": "الْمُبْدِئُ", "meaning": "The Originator"},
    {"number": 59, "name": "Al-Mu'id", "arabic": "الْمُعِيدُ", "meaning": "The Restorer"},
    {"number": 60, "name": "Al-Muhyi", "arabic": "الْمُحْيِي", "meaning": "The Giver of Life"},
    {"number": 61, "name": "Al-Mumit", "arabic": "الْمُمِيتُ", "meaning": "The Taker of Life"},
    {"number": 62, "name": "Al-Hayy", "arabic": "الْحَيُّ", "meaning": "The Ever Living One"},
    {"number": 63, "name": "Al-Qayyum", "arabic": "الْقَيُّومُ", "meaning": "The Self-Existing One"},
    {"number": 64, "name": "Al-Wajid", "arabic": "الْوَاجِدُ", "meaning": "The Finder"},
    {"number": 65, "name": "Al-Majid", "arabic": "الْمَاجِدُ", "meaning": "The Glorious"},
    {"number": 66, "name": "Al-Wahid", "arabic": "الْوَاحِدُ", "meaning": "The One"},
    {"number": 67, "name": "Al-Ahad", "arabic": "الأَحَدُ", "meaning": "The Unique"},
    {"number": 68, "name": "As-Samad", "arabic": "الصَّمَدُ", "meaning": "The Satisfier of All Needs"},
    {"number": 69, "name": "Al-Qadir", "arabic": "الْقَادِرُ", "meaning": "The All Powerful"},
    {"number": 70, "name": "Al-Muqtadir", "arabic": "الْمُقْتَدِرُ", "meaning": "The Creator of All Power"},
    {"number": 71, "name": "Al-Muqaddim", "arabic": "الْمُقَدِّمُ", "meaning": "The Expediter"},
    {"number": 72, "name": "Al-Mu'akhkhir", "arabic": "الْمُؤَخِّرُ", "meaning": "The Delayer"},
    {"number": 73, "name": "Al-Awwal", "arabic": "الأوَّلُ", "meaning": "The First"},
    {"number": 74, "name": "Al-Akhir", "arabic": "الآخِرُ", "meaning": "The Last"},
    {"number": 75, "name": "Az-Zahir", "arabic": "الظَّاهِرُ", "meaning": "The Manifest One"},
    {"number": 76, "name": "Al-Batin", "arabic": "الْبَاطِنُ", "meaning": "The Hidden One"},
    {"number": 77, "name": "Al-Wali", "arabic": "الْوَالِي", "meaning": "The Protecting Friend"},
    {"number": 78, "name": "Al-Muta'ali", "arabic": "الْمُتَعَالِي", "meaning": "The Supreme One"},
    {"number": 79, "name": "Al-Barr", "arabic": "الْبَرُّ", "meaning": "The Doer of Good"},
    {"number": 80, "name": "At-Tawwab", "arabic": "التَّوَّابُ", "meaning": "The Guide to Repentance"},
    {"number": 81, "name": "Al-Muntaqim", "arabic": "الْمُنْتَقِمُ", "meaning": "The Avenger"},
    {"number": 82, "name": "Al-'Afuww", "arabic": "العَفُوُّ", "meaning": "The Forgiver"},
    {"number": 83, "name": "Ar-Ra'uf", "arabic": "الرَّؤُوفُ", "meaning": "The Clement"},
    {"number": 84, "name": "Malik-ul-Mulk", "arabic": "مَالِكُ الْمُلْكِ", "meaning": "The Owner of All"},
    {"number": 85, "name": "Dhul-Jalali-Wal-Ikram", "arabic": "ذُوالْجَلاَلِ وَالإكْرَامِ", "meaning": "The Lord of Majesty and Bounty"},
    {"number": 86, "name": "Al-Muqsit", "arabic": "الْمُقْسِطُ", "meaning": "The Equitable One"},
    {"number": 87, "name": "Al-Jami'", "arabic": "الْجَامِعُ", "meaning": "The Gatherer"},
    {"number": 88, "name": "Al-Ghani", "arabic": "الْغَنِيُّ", "meaning": "The Rich One"},
    {"number": 89, "name": "Al-Mughni", "arabic": "الْمُغْنِي", "meaning": "The Enricher"},
    {"number": 90, "name": "Al-Mani'", "arabic": "الْمَانِعُ", "meaning": "The Preventer of Harm"},
    {"number": 91, "name": "Ad-Darr", "arabic": "الضَّارَّ", "meaning": "The Creator of the Harmful"},
    {"number": 92, "name": "An-Nafi'", "arabic": "النَّافِعُ", "meaning": "The Creator of Good"},
    {"number": 93, "name": "An-Nur", "arabic": "النُّورُ", "meaning": "The Light"},
    {"number": 94, "name": "Al-Hadi", "arabic": "الْهَادِي", "meaning": "The Guide"},
    {"number": 95, "name": "Al-Badi'", "arabic": "الْبَدِيعُ", "meaning": "The Originator"},
    {"number": 96, "name": "Al-Baqi", "arabic": "الْبَاقِي", "meaning": "The Everlasting One"},
    {"number": 97, "name": "Al-Warith", "arabic": "الْوَارِثُ", "meaning": "The Inheritor of All"},
    {"number": 98, "name": "Ar-Rashid", "arabic": "الرَّشِيدُ", "meaning": "The Righteous Teacher"},
    {"number": 99, "name": "As-Sabur", "arabic": "الصَّبُورُ", "meaning": "The Patient One"},
]

# ── Islamic Inspirational Quotes ──────────────────────────────────

ISLAMIC_QUOTES = [
    {"quote": "Verily, with hardship comes ease.", "source": "Quran 94:6", "arabic": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا"},
    {"quote": "And He found you lost and guided you.", "source": "Quran 93:7", "arabic": "وَوَجَدَكَ ضَالًّا فَهَدَىٰ"},
    {"quote": "So remember Me; I will remember you.", "source": "Quran 2:152", "arabic": "فَاذْكُرُونِي أَذْكُرْكُمْ"},
    {"quote": "And Allah is the best of providers.", "source": "Quran 62:11", "arabic": "وَاللَّهُ خَيْرُ الرَّازِقِينَ"},
    {"quote": "My mercy encompasses all things.", "source": "Quran 7:156", "arabic": "وَرَحْمَتِي وَسِعَتْ كُلَّ شَيْءٍ"},
    {"quote": "And whoever puts their trust in Allah, then He will suffice him.", "source": "Quran 65:3", "arabic": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ"},
    {"quote": "Indeed, Allah does not burden a soul beyond that it can bear.", "source": "Quran 2:286", "arabic": "لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا"},
    {"quote": "Call upon Me; I will respond to you.", "source": "Quran 40:60", "arabic": "ادْعُونِي أَسْتَجِبْ لَكُمْ"},
    {"quote": "And He is with you wherever you are.", "source": "Quran 57:4", "arabic": "وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ"},
    {"quote": "Do not lose hope, nor be sad.", "source": "Quran 3:139", "arabic": "وَلَا تَهِنُوا وَلَا تَحْزَنُوا"},
    {"quote": "The best of you are those who learn the Quran and teach it.", "source": "Sahih Bukhari", "arabic": "خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ"},
    {"quote": "Whoever believes in Allah and the Last Day, let him speak good or remain silent.", "source": "Sahih Bukhari & Muslim", "arabic": "مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ"},
    {"quote": "None of you truly believes until he loves for his brother what he loves for himself.", "source": "Sahih Bukhari & Muslim", "arabic": "لاَ يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ"},
    {"quote": "The most beloved deeds to Allah are those done consistently, even if they are small.", "source": "Sahih Bukhari & Muslim", "arabic": "أَحَبُّ الأَعْمَالِ إِلَى اللَّهِ أَدْوَمُهَا وَإِنْ قَلَّ"},
    {"quote": "Be in this world as though you were a stranger or a traveler.", "source": "Sahih Bukhari", "arabic": "كُنْ فِي الدُّنْيَا كَأَنَّكَ غَرِيبٌ أَوْ عَابِرُ سَبِيلٍ"},
    {"quote": "Smiling in the face of your brother is charity.", "source": "Jami at-Tirmidhi", "arabic": "تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ لَكَ صَدَقَةٌ"},
    {"quote": "And whoever fears Allah - He will make for him a way out.", "source": "Quran 65:2", "arabic": "وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا"},
    {"quote": "Indeed, the patient will be given their reward without account.", "source": "Quran 39:10", "arabic": "إِنَّمَا يُوَفَّى الصَّابِرُونَ أَجْرَهُم بِغَيْرِ حِسَابٍ"},
    {"quote": "Perhaps you hate a thing and it is good for you.", "source": "Quran 2:216", "arabic": "وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ"},
    {"quote": "Spread peace, feed the hungry, and pray at night when people are sleeping, you will enter Paradise in peace.", "source": "Sunan Ibn Majah", "arabic": "أَفْشُوا السَّلاَمَ وَأَطْعِمُوا الطَّعَامَ وَصَلُّوا بِاللَّيْلِ وَالنَّاسُ نِيَامٌ تَدْخُلُوا الْجَنَّةَ بِسَلاَمٍ"},
]

# ── Hajj & Umrah Guides ──────────────────────────────────────────

HAJJ_GUIDE = {
    "pillars": [
        {"step": 1, "name": "Ihram", "name_arabic": "الإحرام", "description": "Enter the state of Ihram at the Miqat. Wear the prescribed garments (two white unstitched cloths for men). Make the intention for Hajj and recite the Talbiyah: Labbayk Allahumma labbayk.", "tips": "Ensure you are clean and have performed Ghusl before wearing Ihram. Women can wear any modest clothing."},
        {"step": 2, "name": "Tawaf al-Qudum", "name_arabic": "طواف القدوم", "description": "Upon arriving in Makkah, perform Tawaf around the Kaaba seven times counter-clockwise, starting from the Black Stone.", "tips": "Try to touch or kiss the Black Stone if possible, otherwise point towards it."},
        {"step": 3, "name": "Sa'i", "name_arabic": "السعي", "description": "Walk between the hills of Safa and Marwah seven times, commemorating Hajar's search for water for her son Ismail.", "tips": "Start from Safa and end at Marwah."},
        {"step": 4, "name": "Day of Tarwiyah (8th Dhul Hijjah)", "name_arabic": "يوم التروية", "description": "Travel to Mina and spend the night there. Pray Dhuhr, Asr, Maghrib, Isha, and Fajr.", "tips": "Use this time for dhikr, dua, and preparation."},
        {"step": 5, "name": "Day of Arafah (9th Dhul Hijjah)", "name_arabic": "يوم عرفة", "description": "Stand at the plain of Arafah from noon until sunset. This is the most important pillar of Hajj.", "tips": "The Prophet said: 'Hajj is Arafah.' Make as many duas as possible."},
        {"step": 6, "name": "Muzdalifah", "name_arabic": "المزدلفة", "description": "After sunset at Arafah, travel to Muzdalifah. Pray Maghrib and Isha combined. Collect pebbles for stoning.", "tips": "Collect 49 pebbles (or 70 to be safe)."},
        {"step": 7, "name": "Ramy al-Jamarat (10th Dhul Hijjah)", "name_arabic": "رمي الجمرات", "description": "Stone the largest pillar with seven pebbles, saying Allahu Akbar with each throw. Then perform the animal sacrifice.", "tips": "After sacrifice, shave or trim hair, then remove Ihram."},
        {"step": 8, "name": "Tawaf al-Ifadah", "name_arabic": "طواف الإفاضة", "description": "Return to Makkah and perform Tawaf al-Ifadah. This is a pillar of Hajj. Follow with Sa'i.", "tips": "This can be done on the 10th, 11th, or 12th of Dhul Hijjah."},
        {"step": 9, "name": "Days of Tashreeq (11th-13th)", "name_arabic": "أيام التشريق", "description": "Return to Mina and stone all three pillars each day (7 pebbles each).", "tips": "You may leave on the 12th after stoning if you wish."},
        {"step": 10, "name": "Tawaf al-Wada", "name_arabic": "طواف الوداع", "description": "Before leaving Makkah, perform the Farewell Tawaf as the last act of Hajj.", "tips": "This should be the very last thing you do in Makkah."},
    ],
}

UMRAH_GUIDE = {
    "steps": [
        {"step": 1, "name": "Ihram", "name_arabic": "الإحرام", "description": "Assume Ihram at the designated Miqat. Perform Ghusl, wear Ihram garments, make intention for Umrah, and begin reciting the Talbiyah."},
        {"step": 2, "name": "Tawaf", "name_arabic": "الطواف", "description": "Perform Tawaf around the Kaaba seven times counter-clockwise, starting and ending at the Black Stone."},
        {"step": 3, "name": "Salah behind Maqam Ibrahim", "name_arabic": "صلاة خلف مقام إبراهيم", "description": "After completing Tawaf, pray two rak'ahs behind Maqam Ibrahim, or anywhere in the Haram."},
        {"step": 4, "name": "Sa'i between Safa and Marwah", "name_arabic": "السعي بين الصفا والمروة", "description": "Walk between the hills of Safa and Marwah seven times, starting from Safa."},
        {"step": 5, "name": "Halq or Taqsir", "name_arabic": "الحلق أو التقصير", "description": "Men shave (Halq) or shorten (Taqsir) their hair. Women cut a fingertip's length. This completes the Umrah."},
    ],
}

# ── Zakat ─────────────────────────────────────────────────────────

ZAKAT_NISAB_GOLD_GRAMS = 87.48
ZAKAT_NISAB_SILVER_GRAMS = 612.36
ZAKAT_RATE = 0.025  # 2.5%

# ── Islamic Greeting Card Templates ───────────────────────────────

GREETING_TEMPLATES = [
    {"occasion": "Eid ul-Fitr", "greeting": "Eid Mubarak! May Allah accept our fasts and prayers. Taqabbal Allahu minna wa minkum.", "arabic": "عيد مبارك! تقبل الله منا ومنكم"},
    {"occasion": "Eid ul-Adha", "greeting": "Eid Mubarak! May Allah accept your sacrifice and bless you with His mercy.", "arabic": "عيد أضحى مبارك! تقبل الله منا ومنكم"},
    {"occasion": "Ramadan", "greeting": "Ramadan Mubarak! May this holy month bring you peace, blessings, and forgiveness.", "arabic": "رمضان مبارك! كل عام وأنتم بخير"},
    {"occasion": "Jummah (Friday)", "greeting": "Jummah Mubarak! May Allah bless your Friday with peace and barakah.", "arabic": "جمعة مباركة"},
    {"occasion": "New Islamic Year", "greeting": "Happy Islamic New Year! May this year bring you closer to Allah.", "arabic": "كل عام هجري وأنتم بخير"},
    {"occasion": "Mawlid an-Nabi", "greeting": "On this blessed day, we celebrate the birth of Prophet Muhammad (PBUH).", "arabic": "مولد نبوي سعيد"},
    {"occasion": "Isra and Mi'raj", "greeting": "On this night of Isra and Mi'raj, may Allah elevate your status.", "arabic": "ذكرى الإسراء والمعراج"},
    {"occasion": "Laylat al-Qadr", "greeting": "May Allah bless you on this Night of Power, better than a thousand months.", "arabic": "ليلة القدر خير من ألف شهر"},
    {"occasion": "Wedding", "greeting": "Barakallahu lakuma wa baraka alaikuma wa jama'a bainakuma fi khair.", "arabic": "بارك الله لكما وبارك عليكما وجمع بينكما في خير"},
    {"occasion": "New Baby", "greeting": "Congratulations! May Allah make the child a source of joy and righteousness.", "arabic": "بارك الله لك في الموهوب لك"},
    {"occasion": "General", "greeting": "Assalamu Alaikum wa Rahmatullahi wa Barakatuh.", "arabic": "السلام عليكم ورحمة الله وبركاته"},
    {"occasion": "Condolence", "greeting": "Inna lillahi wa inna ilayhi raji'un. May Allah grant the deceased Jannatul Firdaus.", "arabic": "إنا لله وإنا إليه راجعون"},
]
