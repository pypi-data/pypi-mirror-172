from distutils.core import setup

setup(
    name='pySCOrchestrator',
    version='0.0.1',
    author='davidwallis',
    author_email='david@wallis2000.co.uk',
    packages=['pySCOrchestrator'],
    url='https://github.com/davidwallis3101/pySCOrchestrator',
    license='Apache License',
    description='A simple client for calling System Center Orchestrator runbooks in python',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests >= 2.0.0",
        "requests_ntlm",
        "xmltodict"
    ],
)
