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
    'version': '1.0.0',
    'description': 'Control an Airton AC device over LAN.',
    'long_description': '# airton-ac\n\n[![tests](https://github.com/gpajot/airton-ac/workflows/Test/badge.svg?branch=main&event=push)](https://github.com/gpajot/airton-ac/actions?query=workflow%3ATest+branch%3Amain+event%3Apush)\n[![version](https://img.shields.io/pypi/v/airton-ac?label=stable)](https://pypi.org/project/airton-ac/)\n[![python](https://img.shields.io/pypi/pyversions/airton-ac)](https://pypi.org/project/airton-ac/)\n\nControl an Airton AC device over the local area network without using any cloud.\nThis requires having the [wifi module](https://eu.airton.shop/en/products/kit-module-wifi-pour-climatiseurs-airton-en-wifi-ready).\n\n## Usage\nYou can use this library to control a device programmatically with `airton_ac.Device` or through the Domoticz plugin.\n\n### Requirements\nTo control a device you will need these 3 things:\n- the device ID\n- the device local IP address\n- the device local key (encryption key generated upon pairing)\n\nTo get those, follow instructions from [TinyTuya](https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys).\n> ⚠️ Important considerations:\n> - After pairing the devices, assign static IPs in your router.\n> - Data center should be `Central Europe Data Center`.\n\nAfter having run the wizard, you can run `python -m tinytuya scan` to get a summary of devices.\nOnce you have the information you can unlink the devices from the SmartLife app and delete your accounts.\n\n> ⚠️ Keep in mind that if you reset or re-pair devices the local key will change.\n\n### Domoticz plugin\nThe plugin requires having fetched device information using instructions above.\nMake sure to read [plugin instructions](https://www.domoticz.com/wiki/Using_Python_plugins) first.\nThe Domoticz version should be `2022.1` or higher.\n\n```shell\npython3 -m pip install airton-ac\npython3 -m airton_ac.domoticz.install\n```\n\nRestart Domoticz and create a new Hardware using `AirtonAC`. You will need one per device, fill in information and add.\nThe hardware will create 10 devices to control the AC (all prefixed with hardware name):\n- `power`: to turn on or off\n- `set point`: to set the target temperature\n- `temperature`: to record curent temperature as measured by the unit\n- `mode`: to control operating mode\n- `fan`: to control fan speed\n- `eco`: toggle low heat when heating and eco-mode when cooling\n- `light`: toggle display on the unit\n- `swing`: toggle swing mode\n- `sleep`: toggle sleep mode\n- `health`: toggle health mode\n',
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
