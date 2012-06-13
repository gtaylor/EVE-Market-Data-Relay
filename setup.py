try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

    def find_packages(exclude=None):
        """
        Just stub this. If you're packaging EMDS, you need setuptools. If
        you're installing, not so much.
        """
        return

import emdr

required = [
    'bottle',
    'ujson',
    'gevent',
    'requests',
    'python-dateutil<2.0',
    'pyzmq',
    'pytz',
    'cython',
    'emds',
]

scripts = [
    'bin/emdr-announcer',
    'bin/emdr-gateway',
    'bin/emdr-relay',
    'bin/emdr-snooper',
]

setup(
    name='emdr',
    version=emdr.__version__,
    description='EVE Market Data Relay',
    long_description=open('README.rst').read(),
    author='Greg Taylor',
    author_email='gtaylor@gc-taylor.com',
    url='https://github.com/gtaylor/EVE-Market-Data-Relay',
    packages=find_packages(exclude=['tests', 'emds']),
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
