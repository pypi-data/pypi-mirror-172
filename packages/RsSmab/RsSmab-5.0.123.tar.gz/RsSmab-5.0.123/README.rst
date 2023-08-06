==================================
 RsSmab
==================================

.. image:: https://img.shields.io/pypi/v/RsSmab.svg
   :target: https://pypi.org/project/ RsSmab/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsSmab.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsSmab.svg
   :target: https://pypi.python.org/pypi/RsSmab/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsSmab.svg
   :target: https://pypi.python.org/pypi/RsSmab/

Rohde & Schwarz SMA100B Microwave Signal Generator RsSmab instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsSmab import *

    instr = RsSmab('TCPIP::192.168.56.101::HISLIP', reset=True)
    idn = instr.query_str('*IDN?')
    print('Hello, I am: ' + idn)

Check out the full documentation on `ReadTheDocs <https://RsSmab.readthedocs.io//>`_

Supported instruments: SMA100B

The package is hosted here: https://pypi.org/project/RsSmab/

Examples: https://github.com/Rohde-Schwarz/Examples/tree/main/SignalGenerators/Python/RsSmab_ScpiPackage


Version history
----------------

    Latest release notes summary: Update for FW 5.0

    Version 5.0.123.21
		- Update for FW 5.0

	Version 4.70.300.19
		- Fixed bug in interfaces with the name 'base', new docu format

	Version 4.70.300.16
		- Fixed several misspelled arguments and command headers

	Version 4.70.300.15
		- Complete rework of the Repeated capabilities. Before, the driver used extensively the RepCaps Channel, Stream, Subframe, User, Group. Now, they have more fitting names, and also proper ranges and default values.
		- All the repcaps ending with Null have ranges starting with 0. 0 is also their default value. For example, ChannelNull starts from 0, while Channel starts from 1. Since this is a breaking change, please make sure your code written in the previous version of the driver is compatible with this new version. This change was necessary in order to assure all the possible settings.

	Version 4.70.205.9
		- Added Documentation
		- Added method RsSmab.list_resources()

	Version 4.70.205.8
		- Default HwInterface repcap is 0 (empty command suffix)

	Version 4.70.205.7
		- Second build, fixed enum names

	Version 4.70.205.1
		- First released version
