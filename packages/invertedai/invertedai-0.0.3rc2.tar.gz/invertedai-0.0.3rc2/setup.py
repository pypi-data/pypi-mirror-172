# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invertedai', 'invertedai.api']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=5.2.3,<6.0.0',
 'carla>=0.9.13,<0.10.0',
 'furo>=2022.9.29,<2023.0.0',
 'ipython>=7.34,<8.0',
 'ipywidgets>=8.0.2,<9.0.0',
 'jupyterlab>=3.3,<4.0',
 'matplotlib>=3.5,<4.0',
 'myst-parser>=0.18.1,<0.19.0',
 'nbsphinx>=0.8.9,<0.9.0',
 'numpy>=1.17.0,<2.0.0',
 'pydata-sphinx-theme>=0.10.1,<0.11.0',
 'requests>=2.28.1,<3.0.0',
 'sphinx-autobuild>=2021.3.14,<2022.0.0',
 'sphinx-copybutton>=0.5.0,<0.6.0',
 'sphinx_design>=0.3.0,<0.4.0',
 'sphinxcontrib-applehelp>=1.0.2,<2.0.0',
 'sphinxcontrib-devhelp>=1.0.2,<2.0.0',
 'sphinxcontrib-htmlhelp>=2.0.0,<3.0.0',
 'sphinxcontrib-jsmath>=1.0.1,<2.0.0',
 'sphinxcontrib-qthelp>=1.0.3,<2.0.0',
 'sphinxcontrib-serializinghtml>=1.1.5,<2.0.0',
 'twine>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'invertedai',
    'version': '0.0.3rc2',
    'description': 'Client SDK for InvertedAI',
    'long_description': "[pypi-badge]: https://badge.fury.io/py/invertedai.svg\n[pypi-link]: https://pypi.org/project/invertedai/\n[colab-badge]: https://colab.research.google.com/assets/colab-badge.svg\n[colab-link]: https://colab.research.google.com/github/inverted-ai/invertedai-drive/blob/develop/examples/Colab-Demo.ipynb\n\n\n[![Documentation Status](https://readthedocs.org/projects/inverted-ai/badge/?version=latest)](https://inverted-ai.readthedocs.io/en/latest/?badge=latest)\n[![PyPI][pypi-badge]][pypi-link]\n[![Open In Colab][colab-badge]][colab-link]\n\n# InvertedAI\n\n## Overview\n<!-- start elevator-pitch -->\nInverted AI provides an API for controlling non-playable characters (NPCs) in autonomous driving simulations,\navailable as either a REST API or a Python library built on top of it. Using the API requires an access key -\n[contact us](mailto:sales@inverted.ai) to get yours. This page describes how to get started quickly. For more in-depth understanding,\nsee the [API usage guide](userguide.md), and detailed documentation for the [REST API](apireference.md) and the\n[Python library](pythonapi/index.md).\nTo understand the underlying technology and why it's necessary for autonomous driving simulations, visit the\n[Inverted AI website](https://www.inverted.ai/).\n<!-- end elevator-pitch -->\n\n![](docs/images/top_camera.gif)\n\n# Get Started\n<!-- start quickstart -->\n## Installation\nFor installing the Python package from [PyPI][pypi-link]:\n\n```bash\npip install invertedai\n```\n\nThe Python client library is [open source](https://github.com/inverted-ai/invertedai),\nso you can also download it and build locally.\n\n\n## Minimal example\n\nConceptually, the API is used to establish synchronous co-simulation between your own simulator running locally on\nyour machine and the NPC engine running on Inverted AI servers. The basic integration in Python looks like this.\n\n```python\nimport invertedai as iai\n\niai.add_apikey('')  # specify your key here or through the IAI_API_KEY variable\n\niai_simulation = iai.Simulation(  # instantiate a stateful wrapper for Inverted AI API\n    location='canada:vancouver:ubc_roundabout',  # select one of available locations\n    agent_count=5,  #  how many vehicles in total to use in the simulation\n    ego_agent_mask=[True, False, False, False, False]  # first vehicle is ego, rest are NPCs\n)\nfor _ in range(100):  # how many simulation steps to execute (10 steps is 1 second)\n    # collect predictions for the next time step\n    predicted_npc_behavior = iai_simulation.npc_states()\n    # execute predictions in your simulator, using your actions for the ego vehicle\n    updated_ego_agent_state = step_local_simulator(predicted_npc_behavior)\n    # query the API for subsequent NPC predictions, informing it how the ego vehicle acted\n    iai_simulation.step(updated_ego_agent_state)\n```\n\nIn order to execute this code, you need to connect a simulator locally. To quickly check out how Inverted AI NPCs\nbehave, try our\n[Colab](https://colab.research.google.com/github/inverted-ai/invertedai-drive/blob/develop/examples/Colab-Demo.ipynb),\nwhere all agents are NPCs, or go to our\n[github repository](https://github.com/inverted-ai/invertedai/examples) to execute it locally.\nWhen you're ready to try our NPCs with a real simulator, see the example [CARLA integration](examples/carlasim.md).\nThe examples are currently only provided in Python, but if you want to use the API from another language,\nyou can use the [REST API](apireference.md) directly.\n\n<!-- end quickstart -->\n",
    'author': 'Inverted AI',
    'author_email': 'info@inverted.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
