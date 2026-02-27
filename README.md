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

### Mining Settings
| Setting | Type | Range | Description |
|---------|------|-------|-------------|
| Frequency | Select | Model-specific | ASIC clock frequency (options depend on ASIC model) |
| Core Voltage | Select | Model-specific | ASIC core voltage (options depend on ASIC model) |
| Automatic Fan Control | Switch | On/Off | Toggle between automatic and manual fan control |
| Target Temperature | Number | 30–90 °C | Target temperature for auto fan control |
| Minimum Fan Speed | Number | 0–100% | Minimum fan speed |

### Display Settings
| Setting | Type | Range | Description |
|---------|------|-------|-------------|
| Display Sleep | Select | Always off – Always on | Display sleep timeout |
| Display Rotation | Select | 0°, 90°, 180°, 270° | On-device display orientation (requires restart to take effect) |
| Invert Display Colors | Switch | On/Off | Invert the on-device display colors |

### Other Settings
| Setting | Type | Description |
|---------|------|-------------|
| Hostname | Text | Device hostname on the network |
| Overclock Enabled | Switch | Enable/disable overclocking (required for voltage/frequency changes) |

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
