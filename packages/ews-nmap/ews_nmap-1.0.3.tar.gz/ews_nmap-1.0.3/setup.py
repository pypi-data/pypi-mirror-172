# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ews_nmap']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'python-libnmap>=0.7.3,<0.8.0']

entry_points = \
{'console_scripts': ['ewsnmap = ewsnmap:main']}

setup_kwargs = {
    'name': 'ews-nmap',
    'version': '1.0.3',
    'description': 'Extract web servers from an Nmap XML file',
    'long_description': '<h1 align="center">\n    <img src="https://raw.githubusercontent.com/cybersecsi/ews-nmap/main/assets/logo-light-mode.png" alt= "ews-nmap" width="300px">\n</h1>\n\n<h2 align="center">\n    <b>ews-nmap</b>\n<h2>\n<p align="center">\n    <b>E</b>xtract <b>W</b>eb <b>S</b>ervers from Nmap\n</p>\n\n<p align="center">\n  <a href="https://github.com/cybersecsi/ews-nmap/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>\n  <a href="https://github.com/cybersecsi/ews-nmap/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache2-blue.svg"></a>\n</p>\n\n## Table of Contents\n- [Overview](#overview)\n- [Getting Started](#getting-started)\n  - [Example](#example)\n  - [Install & Run](#install--run)\n  - [Run without installing](#run-without-installing)\n    - [Prerequisites](#prerequisites)\n- [Contributing](#contributing)\n- [Credits](#credits)\n- [License](#license)\n\n## Overview\n``ews-nmap`` (**E**xtract **W**eb **S**ervers from Nmap) is a simple script that allows you to easily find all web servers from the XML output of Nmap. \nThe script performs a simple scraping of the informations in the XML file and identifies HTTP/S services.\n\n##  Getting Started  \nRun ``nmap``  and save XML output, for example:   \n```  \nnmap -sV -oX <nmap_output.xml>  \n```  \n\n### Example\nThe output of the tool is like the following:\n![Execution example](https://github.com/cybersecsi/ews-nmap/raw/main/assets/usage.png)\n\n### Install & Run\nTo install it you just need to run:\n```\npip install ews-nmap\n```\n\n### Run without installing\n\n#### Prerequisites   \nInstall dependencies by using the following command:   \n``` \npip install -r requirements.txt\nchmod +x ewsnmap/ewsnmap.py\n```\n\n```   \nUsage: ewsnmap.py NMAP_XML_FILE <flags>\n  optional flags:        --output-dir | --output\n  \n```  \n\nTo run the parser:   \n```  \newsnmap.py <nmap_output.xml>   \n``` \n\nthe script will generate a file ``output.txt`` in ``ewsnmap-output`` dir. If you want to set the output file and the output dir:   \n```   \newsnmap.py <nmap_output.xml>  --output <output_csv_file> --dir <output_directory>\n``` \n\n## Contributing\n\nContributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n## Credits\n``ews-nmap`` is proudly developed [@SecSI](https://secsi.io) by:\n- [Angelo Delicato](https://github.com/thelicato)\n\n## License\nDistributed under Apache 2 License. See `LICENSE` for more information. ',
    'author': 'SecSI',
    'author_email': 'dev@secsi.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
