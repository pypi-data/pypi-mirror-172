from setuptools import setup

setup(
    name='nolk-dwh-logs',
    version='0.0.6',
    packages=['dwh-logs'],
    install_requires=[
        'requests',
        'importlib; python_version == "3.8"',
    ],
)