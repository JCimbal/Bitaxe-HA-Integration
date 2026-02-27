"""Constants for the BitAxe integration."""

DOMAIN = "bitaxe"
PLATFORMS: list[str] = ["sensor", "button", "switch", "number", "select", "text"]
DEFAULT_SCAN_INTERVAL = 30  # seconds

# Valid frequency options per ASIC model (MHz)
ASIC_FREQUENCY: dict[str, list[str]] = {
    "BM1397": ["400", "425", "450", "475", "485", "500", "525", "550", "575", "600"],
    "BM1366": ["400", "425", "450", "475", "485", "500", "525", "550", "575"],
    "BM1368": ["400", "425", "450", "475", "485", "490", "500", "525", "550", "575"],
    "BM1370": ["400", "490", "525", "550", "600", "625"],
    "BM1370XP": ["350", "375", "380", "400", "410"],
}

# Valid core voltage options per ASIC model (mV)
ASIC_VOLTAGE: dict[str, list[str]] = {
    "BM1397": ["1100", "1150", "1200", "1250", "1300", "1350", "1400", "1450", "1500"],
    "BM1366": ["1100", "1150", "1200", "1250", "1300"],
    "BM1368": ["1100", "1150", "1166", "1200", "1250", "1300"],
    "BM1370": ["1000", "1060", "1100", "1150", "1200", "1250"],
    "BM1370XP": ["1000", "1060", "1100", "1150", "1200", "1250"],
}

# Display sleep options: label → API value (seconds), -1 = always on, 0 = always off
DISPLAY_SLEEP_OPTIONS: dict[str, int] = {
    "Always off": 0,
    "1 minute": 60,
    "2 minutes": 120,
    "5 minutes": 300,
    "15 minutes": 900,
    "30 minutes": 1800,
    "1 hour": 3600,
    "2 hours": 7200,
    "4 hours": 14400,
    "8 hours": 28800,
    "Always on": -1,
}
DISPLAY_SLEEP_VALUE_TO_LABEL: dict[int, str] = {v: k for k, v in DISPLAY_SLEEP_OPTIONS.items()}
