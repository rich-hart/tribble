from setuptools import setup, find_packages

ENTRY_POINTS = """\
[console_scripts]
tribify = tribble.batch_process:main
"""

setup(name='tribify',
      version='0.0.0',
      description='Star trek special effects',
      url='https://github.com/rich-hart/tribble',
      author='Richard Hart',
      author_email='richhohart@gmail.com',
      python_requires='<=3.6.5',
      entry_points=ENTRY_POINTS,
      include_package_data=True,
)
