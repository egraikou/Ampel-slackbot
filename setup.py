#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-slackbot/setup.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 21.08.2021
# Last Modified Date: 21.08.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from setuptools import setup, find_namespace_packages # type: ignore[import]

package_data = {
	'': ['*.json', 'py.typed'],
	'conf': [
		'ampel-slackbot/*.yaml', 'ampel-slackbot/*.yml', 'ampel-slackbot/*.json',
		'ampel-slackbot/**/*.yaml', 'ampel-slackbot/**/*.yml', 'ampel-slackbot/**/*.json',
	],
}

install_requires = ['ampel-core', 'ampel-interface', 'ampel-plots']

setup(
    name = 'ampel-slackbot',
    version = '0.8.0',
    description = 'Asynchronous and Modular Platform with Execution Layers',
    author = 'Valery Brinnel',
    maintainer = 'Jakob van Santen',
    maintainer_email = 'jakob.van.santen@desy.de',
    url = 'https://ampelproject.github.io',
    zip_safe=False,
    packages = find_namespace_packages(),
    package_data = package_data,
    install_requires = install_requires,
    python_requires = '>=3.9,<4.0'
)
