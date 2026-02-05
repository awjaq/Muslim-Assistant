"""Constants for Muslim Assistant integration."""

DOMAIN = "muslim_assistant"

# Configuration keys
CONF_CALC_METHOD = "calculation_method"
CONF_SCHOOL = "school"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"

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
    "Diyanet İşleri Başkanlığı, Turkey": 13,
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

# API endpoints
ALADHAN_API_BASE = "https://api.aladhan.com/v1"
ALADHAN_TIMINGS = f"{ALADHAN_API_BASE}/timings"
ALADHAN_CALENDAR = f"{ALADHAN_API_BASE}/calendar"
ALADHAN_QIBLA = f"{ALADHAN_API_BASE}/qibla"
QURAN_API_BASE = "https://api.alquran.cloud/v1"

# Update intervals (seconds)
UPDATE_INTERVAL_PRAYER = 300  # 5 minutes
UPDATE_INTERVAL_HIJRI = 3600  # 1 hour
UPDATE_INTERVAL_QURAN = 86400  # 24 hours

# Platforms
PLATFORMS = ["sensor"]

# Sensor types
SENSOR_PRAYER_TIMES = "prayer_times"
SENSOR_NEXT_PRAYER = "next_prayer"
SENSOR_QIBLA = "qibla"
SENSOR_HIJRI_DATE = "hijri_date"
SENSOR_DAILY_DUA = "daily_dua"
SENSOR_RAMADAN = "ramadan"

# Duas collection
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
        "arabic": "لاَ إِلَهَ إِلاَّ اللَّهُ الْعَظِيمُ الْحَلِيمُ، لاَ إِلَهَ إِلاَّ اللَّهُ رَبُّ الْعَرْشِ الْعَظِيمِ، لاَ إِلَهَ إِلاَّ اللَّهُ رَبُّ السَّمَوَاتِ وَرَبُّ الأَرْضِ وَرَبُّ الْعَرْشِ الْكَرِيمِ",
        "transliteration": "La ilaha illallahul-'Adhimul-Halim, la ilaha illallahu Rabbul-'Arshil-'Adhim, la ilaha illallahu Rabbus-samawati wa Rabbul-ardi wa Rabbul-'Arshil-Karim",
        "translation": "None has the right to be worshipped except Allah, the Mighty, the Forbearing. None has the right to be worshipped except Allah, Lord of the magnificent throne. None has the right to be worshipped except Allah, Lord of the heavens, Lord of the earth, and Lord of the noble throne.",
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

# Quran Surah names
SURAH_COUNT = 114
