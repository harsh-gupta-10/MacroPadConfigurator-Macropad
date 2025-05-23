# MacroPad Configurator

## Introduction

The MacroPad Configurator is a software tool designed to customize and configure a DIY macro pad built using the Raspberry Pi Pico RP2040. This tool allows you to program custom keystrokes, shortcuts, and actions for each button on your macro pad, enhancing your workflow and productivity.

![MacroPad Hardware](/img/macropad.jpg)
![MacroPad Configurator Software](/img/screenshot.png)

### Project Links
- [MacroPad Configurator Software (This Repository)](https://github.com/harsh-gupta-10/MacroPadConfigurator-Macropad)
- [MacroPad Hardware Code (CircuitPython)](https://github.com/harsh-gupta-10/macropad-rp2040)

## Features

- Intuitive GUI for macro configuration
- Support for key combinations and shortcuts
- Multiple profiles for different applications
- Real-time communication with the macro pad
- Save and load configurations

## Installation

### Prerequisites
- Python 3.10 or higher
- Git (for cloning the repository)

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/harsh-gupta-10/MacroPadConfigurator-Macropad.git
   cd MacroPadConfigurator-Macropad
   ```

2. Install required dependencies:
   ```
   pip install pyserial
   pip install pyinstaller
   ```

3. Run the application:
   ```
   python main.py
   ```

### Building Executable

To create a standalone executable file:

```
python -m PyInstaller main.py --onefile --name MacroPadConfigurator-v2.0 --icon=icon.ico --noconsole
```

The executable will be generated in the `dist` folder.

## Usage

1. Connect your macro pad to your computer via USB
2. Launch the MacroPad Configurator
3. Select the correct serial port
4. Configure your desired macros for each key
5. Save your configuration
6. Press keys on your macro pad to trigger the programmed actions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- The CircuitPython team for their excellent microcontroller support
- Contributors to the PySerial library