# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nmapvulners2csv']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'bs4>=0.0.1,<0.0.2',
 'elementpath>=3.0.2,<4.0.0',
 'fire>=0.4.0,<0.5.0',
 'six>=1.16.0,<2.0.0',
 'soupsieve>=2.3.2.post1,<3.0.0',
 'termcolor>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['nmapvulners2csv = nmapvulners2csv:main']}

setup_kwargs = {
    'name': 'nmapvulners2csv',
    'version': '1.0.4',
    'description': 'Convert Nmap Vulners script output to CSV',
    'long_description': '<h1 align="center">\n    <img src="https://raw.githubusercontent.com/cybersecsi/nmapvulners2csv/main/assets/logo-light-mode.png" alt= "nmapvulners2csv" width="300px">\n</h1>\n\n<p align="center">\n    <b>nmapvulners2csv</b>\n<p>\n\n\n<p align="center">\n  <a href="https://github.com/cybersecsi/nmapvulners2csv/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>\n  <a href="https://github.com/cybersecsi/nmapvulners2csv/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache2-blue.svg"></a>\n</p>\n\n## Table of Contents\n- [Getting Started](#getting-started)\n  - [Install](#install)\n  - [Run without installing](#run-without-installing)\n    - [Prerequisites](#prerequisites)\n  - [Evidences Description](#evidences-description)\n- [Contributing](#contributing)\n- [Credits](#credits)\n- [License](#license)\n\n##  Getting Started  \nRun nmap with enabled script Vulners and save xml output, for example:   \n```  \nnmap -sV --script vulners -oX <nmap_output.xml>  \n```  \n\n### Example\nThe output of the tool is like the following:\n![Execution example](https://github.com/cybersecsi/nmapvulners2csv/raw/main/assets/usage.png)\n\n### Install & Run\nTo install it you just need to run:\n```\npip install nmapvulners2csv\n```\n\n### Run without installing\n\n#### Prerequisites   \nInstall dependencies by using the following command:   \n``` \npip install -r requirements.txt\nchmod +x nmapvulners2csv/nmapvulners2csv.py\n```\n\n```   \nUsage: nmapvulners2csv.py NMAP_XML_FILE <flags>\n  optional flags:        --output | --descr\n  \n```  \n\nTo run the converter:   \n```  \nnmapvulners2csv.py <nmap_output.xml>   \n``` \n\nthe script will generate a file output.csv in output dir. If you want to set the output file:   \n```   \nnmapvulners2csv.py <nmap_output.xml>  --output <output_csv_file> --dir <output_directory>\n``` \nFor multiple data:   \n```  \nfor i in `ls -1 vulners*`; do python nmapvulners2csv.py $i ${i%%.xml}.csv ; done   \n``` \n\n### Evidences Description  \n``nmapvulners2csv`` does not generate descriptions for vulnerabilities. You can add `--descr` flag to add descriptions in CSV.  The script scrapes description information from Vulners site. The command is more time-expensive and send several HTTP requests against Vulners website. Not tested for IP ban and network issues.     \n\n## Contributing\n\nContributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n## Credits\n``nmapvulners2csv`` is proudly developed [@SecSI](https://secsi.io) by:\n- [Gaetano Perrone](https://github.com/giper45)\n- [NdA994](https://github.com/NdA994)\n- [Angelo Delicato](https://github.com/thelicato)\n\n## License\nDistributed under Apache 2 License. See `LICENSE` for more information. ',
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
