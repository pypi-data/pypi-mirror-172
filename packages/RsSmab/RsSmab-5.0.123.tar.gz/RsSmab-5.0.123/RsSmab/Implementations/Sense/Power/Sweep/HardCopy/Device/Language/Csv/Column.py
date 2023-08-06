from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ColumnCls:
	"""Column commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("column", core, parent)

	# noinspection PyTypeChecker
	def get_separator(self) -> enums.MeasRespHcOpCsvcLmSep:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage:CSV:[COLumn]:SEParator \n
		Snippet: value: enums.MeasRespHcOpCsvcLmSep = driver.sense.power.sweep.hardCopy.device.language.csv.column.get_separator() \n
		Defines which character is to separate the values, either tabulator, semicolon, comma or blank. \n
			:return: separator: TABulator| SEMicolon| COMMa| BLANk
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage:CSV:COLumn:SEParator?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespHcOpCsvcLmSep)

	def set_separator(self, separator: enums.MeasRespHcOpCsvcLmSep) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage:CSV:[COLumn]:SEParator \n
		Snippet: driver.sense.power.sweep.hardCopy.device.language.csv.column.set_separator(separator = enums.MeasRespHcOpCsvcLmSep.BLANk) \n
		Defines which character is to separate the values, either tabulator, semicolon, comma or blank. \n
			:param separator: TABulator| SEMicolon| COMMa| BLANk
		"""
		param = Conversions.enum_scalar_to_str(separator, enums.MeasRespHcOpCsvcLmSep)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage:CSV:COLumn:SEParator {param}')
