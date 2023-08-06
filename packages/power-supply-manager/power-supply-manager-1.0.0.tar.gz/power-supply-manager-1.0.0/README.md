# Power Supply Manager


![](./power_supply_manager_1.png)
![](./power_supply_manager_2.png)

## Description
Control multiple networked power supplies from the same graphical application. Features:

* Connect to multiple bench-top power supply units over Ethernet (VXI11 or LXI protocols)
* Four ways to control power output:
  * Individual channels
  * Group any combination of channels to power simultaneously
  * Define power on/off sequences with configurable time delays in between
  * Power all channels on/off simultaneously
* Real-time plots showing voltage and current measurements from each channel.
* Set voltage, current, over-voltage protection, over-current protection, and 4-wire control settings.
* Log voltage and current measurements to CSV files.
* Save and load multi-device configuration files to quickly restore settings.

## Installation

### Install from PyPI (recommended)

1. Install pip package:
  ```
  pip install power-supply-manager
  ```

  Make sure the pip installation directory is on your system PATH:
  * Linux / MacOS: Typically `$HOME/.local/bin`, `/usr/bin`, or `/usr/local/bin`
  * Windows: Typically `<Python install dir>\Scripts` or `C:\Users\<username>\AppData\Roaming\Python\Python<vers>\Scripts`

2. Run application:
  ```
  power-supply-manager
  ```

### Install from GitLab

1. Install the repository:

  ```
  git clone https://gitlab.com/d7406/power-supply-manager.git
  ```
2. Install [Poetry](https://python-poetry.org)
3. Setup virtual environment using Poetry:
  ```
  poetry install
  ```
4. Run application:
  ```
  poetry run python power_supply_manager/power_supply_manager.py
  ```

## Contributing
We welcome contributions and suggestions to improve this application. Please submit an issue or merge request [here](https://gitlab.com/d7406/power-supply-manager)

## Authors and acknowledgment
[DevBuildZero, LLC](http://devbuildzero.com)

## License
This software is provided for free under the MIT open source license:

Copyright 2022 DevBuildZero, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
