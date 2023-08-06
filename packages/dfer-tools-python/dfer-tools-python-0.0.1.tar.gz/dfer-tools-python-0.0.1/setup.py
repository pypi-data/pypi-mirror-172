#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'dfer-tools-python'
DESCRIPTION = 'python常用的工具库'
URL = 'https://gitcode.net/dofun333/dfer_tools_python'
EMAIL = 'df_business@qq.com'
AUTHOR = 'dfer.top'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None
PROJECT_ROOT='src';

# What packages are required for this module to be executed?
REQUIRED = [
				# 'requests', 'maya', 'records',
]

# What packages are optional?
EXTRAS = {
				# 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
				with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
								long_description = '\n' + f.read()
except FileNotFoundError:
				long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
if not VERSION:
				with open(os.path.join(here, PROJECT_ROOT, '__version__.py')) as f:
								exec(f.read(), about)
else:
				about['__version__'] = VERSION
				
				
"""Support setup.py upload."""
class UploadCommand(Command):
				description = '生成、发布python包'
				user_options = []

				@staticmethod
				def status(s):
								"""Prints things in bold."""
								print('>>>{0}<<<'.format(s))

				def initialize_options(self):
								pass

				def finalize_options(self):
								pass

				def run(self):
								try:
												self.status('移除之前生成的发布文件…')
												rmtree(os.path.join(here, 'dist'))
												rmtree(os.path.join(here, '{0}.egg-info'.format(project_slug)))
								except OSError:
												pass

								self.status('生成新的发布文件…')
								# print('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))
								# os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))
								os.system('{0} setup.py sdist'.format(sys.executable))
								self.status('上传到python库…')
								os.system('twine upload dist/* --verbose -u dfer -p lifeisfuckingmovie')
								
								# 自动上传git
								self.status('添加标签，上传git …')       
								os.system('git add *')
								os.system('git commit -m v{0}'.format(about['__version__']))
								os.system('git tag v{0}'.format(about['__version__']))
								# 删除本地tag
								# os.system('git tag -d v{0}'.format(about['__version__']))
								os.system('git push --tags')
								# os.system('git push')
								self.status('完成')
								sys.exit()


# Where the magic happens:
setup(
				name=NAME,
				version=about['__version__'],
				description=DESCRIPTION,
				long_description=long_description,
				long_description_content_type='text/markdown',
				author=AUTHOR,
				author_email=EMAIL,
				python_requires=REQUIRES_PYTHON,
				url=URL,
				project_urls={
								"Bug Tracker": "{0}/issues".format(URL),
				},
				# package_dir={"": PROJECT_ROOT},
				packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
				# If your package is a single module, use this instead of 'packages':
				# py_modules=['mypackage'],

				# entry_points={
				#     'console_scripts': ['mycli=mymodule:cli'],
				# },
				install_requires=REQUIRED,
				extras_require=EXTRAS,
				include_package_data=True,
				license='MIT',
				classifiers=[
								# Trove classifiers
								# Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
								'License :: OSI Approved :: MIT License',
								'Programming Language :: Python',
								'Programming Language :: Python :: 3',
								'Programming Language :: Python :: 3.6',
								'Programming Language :: Python :: Implementation :: CPython',
								'Programming Language :: Python :: Implementation :: PyPy'
				],
				# $ setup.py publish support.
				cmdclass={
								'upload': UploadCommand,
				},
)
