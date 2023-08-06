# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tracking_numbers', 'tracking_numbers.helpers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tracking-numbers',
    'version': '0.1.3',
    'description': 'Parse tracking numbers from couriers with no external dependencies',
    'long_description': '<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n<!-- DON\'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*\n\n- [tracking-numbers](#tracking-numbers)\n  - [Why?](#why)\n  - [Installation](#installation)\n  - [Usage](#usage)\n    - [`get_tracking_number(number)`](#get_tracking_numbernumber)\n    - [`get_definition(product_name)`](#get_definitionproduct_name)\n  - [Testing](#testing)\n\n<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n\n# tracking-numbers\n\nA library that parses tracking numbers and provides common types.\nThe data is sourced from [`tracking_number_data`](https://github.com/jkeen/tracking_number_data/) and the definitions are code-generated.\n\n## Why?\n\nThe typical shipping tracking number has a lot of data encoded within.\nWhile some couriers share similar logic (serial number, check digit, etc), others have entirely different ways of representing tracking numbers.\n\nInstead of hand-rolling parsing code for all of these cases, the author of [`tracking_number_data`](https://github.com/jkeen/tracking_number_data/) has put together a repo that serves as a language-agnostic source of knowledge for various couriers and their shipping products.\n\nThis library uses that data to code-generate definitions to create python bindings for parsing tracking numbers.\n\nThe library itself has no external dependencies, and can be used to decode basic tracking data without the need of an API or external data source at runtime.\n\n## Installation\n\nInstall the tracking-numbers library using pypi\n\n```sh\npip install tracking-numbers\n```\n\n## Usage\n\nHere are the main public functions to use:\n\n### `get_tracking_number(number)`\n\nParses the `number` and returns the `TrackingNumber` dataclass, if detected, or none otherwise.\n\n```python\nfrom tracking_numbers import get_tracking_number\n\ntracking_number = get_tracking_number("1ZY0X1930320121606")\n\n# => TrackingNumber(\n#       valid=False,\n#       number=\'1ZY0X1930320121606\',\n#       serial_number=[6, 0, 5, 1, 9, 3, 0, 3, 2, 0, 1, 2, 1, 6, 0],\n#       tracking_url=\'https://wwwapps.ups.com/WebTracking/track?track=yes&trackNums=1ZY0X1930320121604\',\n#       courier=Courier(code=\'ups\', name=\'UPS\'),\n#       product=Product(name=\'UPS\'),\n#    )\n```\n\n### `get_definition(product_name)`\n\nGiven a product name, gets the `TrackingNumberDefinition` associated.\nYou can call `definition.test(number)` to parse a number for that specific product.\n\n```python\nfrom tracking_numbers import get_definition\n\nups_definition = get_definition(\'UPS\')\ntracking_number = ups_definition.test("1ZY0X1930320121606")\n\n# => TrackingNumber(\n#       valid=False,\n#       number=\'1ZY0X1930320121606\',\n#       serial_number=[6, 0, 5, 1, 9, 3, 0, 3, 2, 0, 1, 2, 1, 6, 0],\n#       tracking_url=\'https://wwwapps.ups.com/WebTracking/track?track=yes&trackNums=1ZY0X1930320121604\',\n#       courier=Courier(code=\'ups\', name=\'UPS\'),\n#       product=Product(name=\'UPS\'),\n#    )\n\ntracking_number = ups_definition.test(\'some_valid_fedex_number\')\n\n# => None\n```\n\n## Testing\n\nWe use the test cases defined in the courier data to generate pytest test cases.\nIn this way, we can be confident that the logic for parsing tracking numbers is working properly.\n',
    'author': 'Jonathan Como',
    'author_email': 'public@jcomo.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jcomo/tracking-numbers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
