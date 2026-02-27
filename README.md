# Bitaxe Home Assistant Integration

[![HACS](https://img.shields.io/badge/HACS-Custom-blue.svg)](https://hacs.xyz/)
[![Latest Release](https://img.shields.io/github/v/release/JCimbal/Bitaxe-HA-Integration)](https://github.com/JCimbal/Bitaxe-HA-Integration/releases)
[![Stars](https://img.shields.io/github/stars/JCimbal/Bitaxe-HA-Integration)](https://github.com/JCimbal/Bitaxe-HA-Integration/stargazers)

A custom Home Assistant integration for monitoring and controlling [BitAxe](https://github.com/skot/bitaxe) open-source bitcoin miners.

## Installation

### HACS (Recommended)

1. Open the HACS section in your Home Assistant.
2. Go to **Integrations** and select **Add Repository**.
3. Enter the repository URL: `https://github.com/JCimbal/Bitaxe-HA-Integration`.
4. Install the integration and restart Home Assistant.

### Manual

1. Navigate to your Home Assistant configuration directory (usually `/config`).
2. Clone the repository into the `custom_components` folder:
   ```bash
   mkdir -p custom_components
   git clone https://github.com/JCimbal/Bitaxe-HA-Integration.git /config/custom_components/bitaxe
   ```
3. Restart Home Assistant.

## Configuration

1. Go to **Settings > Devices & Services > Add Integration**.
2. Search for **Bitaxe** and select it.
3. Enter the IP address of your BitAxe miner (the integration will verify connectivity).
4. Choose a name for your device.
5. Complete the setup.

All sensors, controls, and settings will appear automatically under your device.

## Features

### Real-time Monitoring (Sensors)
| Sensor | Unit | Description |
|--------|------|-------------|
| Power Consumption | W | Current power draw |
| Temperature ASIC | °C | ASIC chip temperature |
| Temperature VR | °C | Voltage regulator temperature |
| Hash Rate | GH/s | Current hashing speed |
| All-Time Best Difficulty | — | Highest difficulty share ever found (formatted, e.g. "1.23 T") |
| Best Difficulty Since Boot | — | Highest difficulty share since last reboot |
| Shares Accepted | — | Total accepted shares |
| Shares Rejected | — | Total rejected shares |
| Fan Speed | % | Current fan speed percentage |
| Fan RPM | RPM | Current fan speed in RPM |
| Uptime | s | Time since last reboot |

### Device Controls (Buttons)
| Button | Description |
|--------|-------------|
| Restart | Restart the BitAxe device |
| Identify | Make the device blink to identify it |

### Configuration Switches
| Switch | Description |
|--------|-------------|
| Use Fallback Stratum | Enable/disable the fallback mining pool |
| Overclock Enabled | Enable/disable overclocking (required for voltage/frequency changes) |
| Auto Fan Speed | Toggle between automatic and manual fan control |
| Invert Display | Invert the on-device display |
| Overheat Mode | Enable/disable overheat protection mode |

### Numeric Settings
| Setting | Range | Description |
|---------|-------|-------------|
| Stratum Port | 1–65535 | Mining pool port |
| Fallback Stratum Port | 1–65535 | Fallback pool port |
| Core Voltage | 1000–1500 mV | ASIC core voltage |
| ASIC Frequency | 100–800 MHz | ASIC clock frequency |
| Fan Speed Setting | 0–100% | Manual fan speed (when auto fan is off) |
| Target Temperature | 30–90 °C | Target temperature for auto fan control |
| Display Timeout | -1–3600 s | Display timeout (-1 = always on, 0 = always off) |
| Stats Logging Interval | 1–3600 s | Frequency of stats logging |

### Selection Settings
| Setting | Options | Description |
|---------|---------|-------------|
| Display Rotation | 0°, 90°, 180°, 270° | On-device display orientation |

### Text Settings
| Setting | Description |
|---------|-------------|
| Stratum URL | Mining pool URL |
| Stratum User | Mining pool username |
| Fallback Stratum URL | Fallback mining pool URL |
| Fallback Stratum User | Fallback pool username |
| Hostname | Device hostname on the network |

## Screenshots

### Setup Screen
<img src="custom_components/bitaxe/images/Setup.png" alt="Setup Screen" style="max-width: 100%; height: auto;">

### Sensor Data Screen
<img src="custom_components/bitaxe/images/Sensor.png" alt="Sensor Data Screen" style="max-width: 100%; height: auto;">

## Credits

This project is a fork of the [original Bitaxe HA Integration](https://github.com/DerMiika/Bitaxe-HA-Integration) by [DerMiika](https://github.com/DerMiika), extended with device controls and configuration management.

It communicates with [BitAxe](https://github.com/skot/bitaxe) open-source miners via their local REST API. BitAxe is an open-source bitcoin miner project by [skot](https://github.com/skot).

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
