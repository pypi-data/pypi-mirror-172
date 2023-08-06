from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LanguageCls:
	"""Language commands group definition. 5 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("language", core, parent)

	@property
	def csv(self):
		"""csv commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_csv'):
			from .Csv import CsvCls
			self._csv = CsvCls(self._core, self._cmd_group)
		return self._csv

	# noinspection PyTypeChecker
	def get_value(self) -> enums.MeasRespHcOpFileFormat:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage \n
		Snippet: value: enums.MeasRespHcOpFileFormat = driver.sense.power.sweep.hardCopy.device.language.get_value() \n
		Selects the bitmap graphic format for the screenshot of the power analysis trace. In addition, ASCII file format *.csv is
		offered. If file format *.csv is selected, the trace data is saved as an ASCII file with comma separated values. It is
		also possible to directly retrieve the data using command method RsSmab.Sense.Power.Sweep.HardCopy.data \n
			:return: language: BMP| JPG| XPM| PNG| CSV
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespHcOpFileFormat)

	def set_value(self, language: enums.MeasRespHcOpFileFormat) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage \n
		Snippet: driver.sense.power.sweep.hardCopy.device.language.set_value(language = enums.MeasRespHcOpFileFormat.BMP) \n
		Selects the bitmap graphic format for the screenshot of the power analysis trace. In addition, ASCII file format *.csv is
		offered. If file format *.csv is selected, the trace data is saved as an ASCII file with comma separated values. It is
		also possible to directly retrieve the data using command method RsSmab.Sense.Power.Sweep.HardCopy.data \n
			:param language: BMP| JPG| XPM| PNG| CSV
		"""
		param = Conversions.enum_scalar_to_str(language, enums.MeasRespHcOpFileFormat)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage {param}')

	def clone(self) -> 'LanguageCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LanguageCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
