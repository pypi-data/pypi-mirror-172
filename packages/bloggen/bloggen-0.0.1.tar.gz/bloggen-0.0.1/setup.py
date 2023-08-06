# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bloggen']

package_data = \
{'': ['*'], 'bloggen': ['.bloggen/*']}

install_requires = \
['Markdown>=3.4.1,<4.0.0',
 'argparse>=1.4,<2.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'google-cloud>=0.34.0,<0.35.0',
 'pathlib>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['bloggen = bloggen.__main__:main']}

setup_kwargs = {
    'name': 'bloggen',
    'version': '0.0.1',
    'description': 'Deploy a dir of md files as a static site',
    'long_description': "# Bloggen\n\nPoint bloggen to a hosting location, give it your markdown, then watch it deploy a static site.\n\n# Use\n\n## A parable:\n\nLee creates a GCP credentials json:\n\n1.  Lee gets a service token JSON from GCP. He follows this guide https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication'\n2.  Lee saves the JSON to his machine and remembers the path for later. Bloggen is going to save the path to that JSON into an environment variable\n3.  Lee will need to tell Bloggen the path to the json by configuring a Bloggen profile\n\nLee configures a profile:\n\n1. Lee runs `bloggen --config` and supplies the following information:\n\n   - Name\n   - Path to GCP credentials json\n   - Name of GCP bucket to use\n\n1. Lee writes 5 md notes into a dir\n1. Lee runs `bloggen --generate path_to_md_dir`\n1. Lee sees a new dir appear. It is named static-site and can be found at ../path_to_md_dir\n1. Lee runs `bloggen --publish path_to_static_site`\n1. Lee learns that his notes are available as a static site on GCP\n\n## Generate\n\n_generates static webpage_\nUser provides a directory of markdown to be converted to html\n\n`bloggen generate --path=path_to_dir`\n\n## Sync\n\n_Sync directory of markdown files with existing static site_\n`bloggen sync --path=path_to_dir_of_md_files`\n\n## Add\n\n_Add file to static site_\n_Convert given markdown file to html and add to site_\n`bloggen add --path=path_to_md_file`\n\n## Remove\n\n_Remove named page from static site_\n`bloggen remove --name=name_of_file`\n\n## Destroy\n\n_Destroy site and bucket_\n`bloggen destroy`\n",
    'author': 'Lee Harrold',
    'author_email': 'halzinnia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
