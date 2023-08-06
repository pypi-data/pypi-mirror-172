# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airton_ac', 'airton_ac.domoticz', 'airton_ac.domoticz.units']

package_data = \
{'': ['*']}

install_requires = \
['tinytuya==1.7.1']

setup_kwargs = {
    'name': 'airton-ac',
    'version': '0.1.0',
    'description': 'Control an Airton AC device over LAN.',
    'long_description': '# airton-ac\nControl an Airton AC device over LAN.\nThis requires having the [wifi module](https://eu.airton.shop/en/products/kit-module-wifi-pour-climatiseurs-airton-en-wifi-ready).\n\n## Usage\nYou can use this library to control a device programmatically with `airton_ac.Device` or through the Domoticz plugin.\n\n### Requirements\nTo control a device you will need these 3 things:\n- the device ID\n- the device local IP address\n- the device local key (encryption key generated upon pairing)\n\nTo get those, follow instructions from [TinyTuya](https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys).\n> ⚠️ Data center should be `Central Europe Data Center`.\n\nAfter having run the wizard, you can run `python -m tinytuya scan` to get a summary of devices.\nOnce you have the information you can unlink the devices from the SmartLife app and delete your accounts.\n\n> ⚠️ Keep in mind that if you reset or re-pair devices the local key will change.\n\n### Domoticz plugin\nThe plugin requires having fetched device information using instructions above.\nMake sure to read [plugin instructions](https://www.domoticz.com/wiki/Using_Python_plugins) first.\nThe Domoticz version should be `2022.1` or higher.\n\n```shell\npython3 -m pip install airton_ac\npython3 -m airton_ac.domoticz.install\n```\n\nRestart Domoticz and create a new Hardware using `AirtonAC`. You will need one per device, fill in information and add.\nThe hardware will create several devices to control the AC (all prefixed with hardware name):\n- `Power`: to turn on or off\n- `Mode`: to control operating mode\n- `Fan`: to control fan speed\n- `Set point`: to set the target temperature\n- `Temperature`: to record curent temperature as measured by the unit\n- `Low heat`: to turn on low heat\n',
    'author': 'Gabriel Pajot',
    'author_email': 'gab@les-cactus.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpajot/airton-ac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
