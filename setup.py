try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import emdr

required = [
    'bottle',
    'simplejson',
    'gevent',
    'gevent-zeromq',
    'python-dateutil<2.0',
]

packages = [
    'emdr',
    'emdr.conf',
    'emdr.core', 'emdr.core.serialization',
    'emdr.daemons', 'emdr.daemons.broker', 'emdr.daemons.gateway',
    'emdr.daemons.processor', 'emdr.daemons.relay'
]

scripts = [
    'bin/emdr-broker',
    'bin/emdr-processor',
    'bin/emdr-relay',
]

setup(
    name='emdr',
    version=emdr.__version__,
    description='EVE Market Data Relay',
    long_description=open('README.rst').read(),
    author='Greg Taylor',
    author_email='gtaylor@gc-taylor.com',
    url='https://github.com/gtaylor/EVE-Market-Data-Relay',
    packages=packages,
    scripts=scripts,
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=required,
    license='BSD',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        ),
    )
