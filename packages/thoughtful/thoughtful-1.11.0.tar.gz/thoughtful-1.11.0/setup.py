# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supervisor', 'supervisor.reporting']

package_data = \
{'': ['*']}

install_requires = \
['aws-requests-auth>=0.4.3,<0.5.0',
 'boto3>=1.24.64,<2.0.0',
 'chevron>=0.14.0,<0.15.0',
 'isodate>=0.6.1,<0.7.0',
 'moto>=4.0.5,<5.0.0',
 'pre-commit>=2.17.0,<3.0.0',
 'pyconfs>=0.5.5,<0.6.0',
 'pydantic-yaml>=0.6.3,<0.7.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyyaml>=5.4.1']

setup_kwargs = {
    'name': 'thoughtful',
    'version': '1.11.0',
    'description': 'Supervisor is a Workflow Engine for Digital Workers that generates a detailed telemetric log at runtime called a Work Report',
    'long_description': '# 👷 Supervisor\n\n<img\n  title="Supervisor"\n  alt="Supervisor — Github Header"\n  width="262px"\n  height="179.5px"\n  align="right"\n  src="https://user-images.githubusercontent.com/1096881/147704110-3116d1e3-c278-45d6-b99a-209faf2b17e0.png"\n/>\n\n> **:warning: NOTE**: *Supervisor* is quite new.\n> We welcome and encourage you to help shape future\n> development by [reporting issues][git:issues] and\n> [making suggestions][url:notion-feedback] 💖\n\n---\n<big>Supervisor is a <u>Workflow Engine</u> for Digital Workers that constructs\nand broadcasts a detailed and structured telemetric log, called the <u>Run Report</u>.\n\nSupervisor is quick and easy to implement:</big>\n\n```python\nfrom supervisor import step, step_scope, supervise, set_step_status\n\n\n# using the step decorator\n@step("2")\ndef step_2(name: str) -> bool:\n    print(f\'Hello {name}\')\n    return True # some condition\n\ndef main() -> None:\n    # using the step_scope context manager\n    with step_scope(\'1\') as step_context:\n        try:\n            print("Getting credentials")\n            # ...\n        except Exception as e:\n            # set step status using method\n            step_context.set_status("warning")\n\n    if not step_2():\n        # set step status using function\n        set_step_status("2", "fail")\n\nif __name__ == \'__main__\':\n    with supervise():\n        main()\n```\n\n[![pre-commit](https://github.com/thoughtful-automation/supervisor/workflows/pre-commit/badge.svg?event=push)](https://github.com/thoughtful-automation/supervisor/actions?query=workflow%3Apre-commit+event%3Apush)\n[![test](https://github.com/thoughtful-automation/supervisor/workflows/test/badge.svg?event=push)](https://github.com/thoughtful-automation/supervisor/actions?query=workflow%3Atest+event%3Apush)\n\n<small>Supervisor supports `Python ≥ 3.7.5`</small>\n\n:books: 👉️ **[Read the Docs][url:readthedocs]**\n\n## Table of Contents\n\n- [Install](#install)\n- [Documentation](#documentation)\n- [Contributing](#contributing)\n- [Resources](#resources)\n\n## Installing Supervisor\n\nAt this time, Supervisor is a private package hosted only on CodeArtifact.\n\n1. Authenticate with `CodeArtifact`:\n\n   ```bash\n   aws codeartifact login \\\n     --tool pip \\\n     --repository thoughtful-automation \\\n     --domain thoughtful-automation \\\n     --domain-owner XXXXXXXXXXXX \\\n     --region us-east-1\n   ```\n\n2. Pip install\n\n   ```bash\n   pip install t-supervisor\n   ```\n\n   > or install a specific version: `pip install "t-supervisor==0.4.0"`\n\n## Documentation available on [Read the Docs][url:readthedocs]\n\nSee the [Read the Docs][url:readthedocs].\n\n## Contributing\n\nContributions to Supervisor are welcomed!\n\nTo get started, see the [contributing guide](CONTRIBUTING.md).\n\n## Resources\n\nLinks to related code, documentation, and applications.\n\n[**🖥 Empower**][url:dwm]\n\n> The digital Workforce Manager (*DWM*)\n\n[**👷 Supervisor**][url:supervisor] (this repo)\n\n> The Workflow Engine for Digital Workers that constructs\nand broadcasts a detailed and structured telemetric log, called the Work Report\n\n[**:robot: Foundry**][url:otto]\n\n> The initialization tool for Digital Workers.\n\n[**🔀 Prospector**][url:prospector]\n\n> The design tool for Digital Workers.\n\n[**:books: Schema Library**][url:schema-lib]\n\n  > The JSON-Schema-defined documents used to validate the **Manifest** and the\n  > runtime **Work Report**\n\n[**:eagle: Department of Digital\n  Labor**][url:dodl]\n\n> Documentation and Specifications for building Digital Workers in *TA\'s\n> ecosystem*, and **Empower**\n\n---\n\n<div align="center">\n\n  Made with ❤️ by\n\n  [![Thoughtful Automation](https://user-images.githubusercontent.com/1096881/141985289-317c2e72-3c2d-4e6b-800a-0def1a05f599.png)][url:ta]\n\n</div>\n\n<!--  Link References -->\n\n[url:ta]: https://www.thoughtfulautomation.com/\n[url:dwm]: https://app.thoughtfulautomation.com/\n[url:supervisor]: https://github.com/Thoughtful-Automation/supervisor\n[url:otto]: https://github.com/Thoughtful-Automation/otto\n[url:prospector]: https://github.com/Thoughtful-Automation/prospector\n[url:dodl]: https://github.com/Thoughtful-Automation/dodl\n[url:schema-lib]: https://github.com/Thoughtful-Automation/schemas\n[url:notion-feedback]:\n    https://www.notion.so/thoughtfulautomation/Feedback-Feature-Requests-5716a73769ea4e0cba398e921eab44b5\n[git:issues]: https://github.com/Thoughtful-Automation/supervisor/issues\n[url:readthedocs]: https://thoughtful-supervisor.readthedocs-hosted.com/en/latest/\n',
    'author': 'Thoughtful Automation',
    'author_email': 'engineering@thoughtfulautomation.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://thoughtfulautomation.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
