from setuptools import setup

setup(
    name='tracelog',
    version='0.0.3',
    packages=['tracelog'],
    install_requires=[
        'requests',
        'importlib; python_version == "3.8"',
    ],
)