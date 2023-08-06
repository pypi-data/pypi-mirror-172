# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_forms']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.13,<3.0']

setup_kwargs = {
    'name': 'aiogram-forms',
    'version': '0.3.0',
    'description': 'Forms for aiogram',
    'long_description': '# aiogram-forms\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram-forms)\n![PyPI](https://img.shields.io/pypi/v/aiogram-forms)\n![GitHub](https://img.shields.io/github/license/13g10n/aiogram-forms)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/aiogram-forms?label=installs)\n\n## Introduction\n`aiogram-forms` is an addition for `aiogram` which allows you to create different forms and process user input step by step easily.\n\n## Installation\n```bash\npip install aiogram-forms\n```\n\n## Usage\nCreate form you need by subclassing `aiogram_forms.forms.Form`. Fields can be added with `aiogram_forms.fields.Field`. For more examples refer to `examples` folder.\n```python\nclass UserProfileForm(forms.Form):\n    """Example of user details form."""\n\n    # Simple field usage\n    name = fields.StringField(\'Name\')\n    # Using custom validators\n    username = fields.StringField(\n        \'Username\', validators=[validators.RegexValidator(r\'^[a-z0-9_-]{3,15}$\')]\n    )\n    # Custom reply keyboard with validation\n    language = fields.ChoicesField(\n        \'Language\', LANGUAGE_CHOICES, reply_keyboard=LANGUAGE_KEYBOARD\n    )\n    # Custom validation message\n    email = fields.EmailField(\n        \'Email\', validation_error_message=\'Wrong email format!\'\n    )\n    # Allow user to share contact as reply\n    phone = fields.PhoneNumberField(\n        \'Phone\', share_contact=True, share_contact_label=\'Share your contact\'\n    )\n```\n\n## History\nAll notable changes to this project will be documented in [CHANGELOG](CHANGELOG.md) file.\n\n',
    'author': 'Ivan Borisenko',
    'author_email': 'i.13g10n@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/aiogram-forms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
