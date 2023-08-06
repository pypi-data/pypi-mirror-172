# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bmm150']

package_data = \
{'': ['*']}

install_requires = \
['smbus2>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'bmm150',
    'version': '0.1.4',
    'description': 'A pure python API for the bmm150 magnetic sensor',
    'long_description': '# BMM150\n\nA pure python API for the bmm150 magnetic sensor.\n\n> Note : Most code logic comes from one of the following repos : [Seed-Studio/Grove_3_Axis_Compass_V2.0_BMM150](https://github.com/Seeed-Studio/Grove_3_Axis_Compass_V2.0_BMM150) or [BoschSensortec/BMM150-Sensor-API](https://github.com/BoschSensortec/BMM150-Sensor-API) . This is mostly a transpilation and a python packaging of this code.\n\n# Installation\n\nThe easiest way to install this library is using pip:\n\n```bash\npip install bmm150\n```\n\n# Documentation\n\nThe documentation is built using sphinx and the readthedocs theme. You can find it on the [readthedocs official website](https://bmm150.readthedocs.io/).\n\n# Usage\n\nThe following code initializes the sensor, and prints the magnetic field values for x, y and z.\nThen, using the `atan2` function from the `math` standard library, it retrieves the heading of the sensor.\n\n```python\nimport bmm150\nimport math\n\ndevice = bmm150.BMM150(bus_number=1)  # Bus number will default to 1\n\ndevice.initialize()\n\nx, y, z = device.read_mag_data()\n\nheading_rads = math.atan2(x, y)\n\nif heading_rads < 0:\n    heading_rads += 2*math.pi\nif heading_rads > 2*math.pi:\n    heading_rads -= 2*math.pi\n\nheading_degs = heading_rads * 180 / math.pi\n\nprint(f"X : {x:.2f}µT")\nprint(f"Y : {y:.2f}µT")\nprint(f"Z : {z:.2f}µT")\n\nprint(f"Heading: {heading_degs:.2f}°")\n```\n\n# Development\n\nThis library uses poetry as a development tool.\n\nYou can start development by running :\n\n```bash\npoetry install\n```\n\n# Testing\n\nYou can test this library using :\n\n```bash\npoetry run pytest\n```\n\n# Tox\n\nYou cant test multiple python versions using tox :\n\n```bash\npoetry run tox\n```',
    'author': 'Ulysse Moreau',
    'author_email': 'ulysse.moreau@gmx.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/umoreau/bmm150',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
