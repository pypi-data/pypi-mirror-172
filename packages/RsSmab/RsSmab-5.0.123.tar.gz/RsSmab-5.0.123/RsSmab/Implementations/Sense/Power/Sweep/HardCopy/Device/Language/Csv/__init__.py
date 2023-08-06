from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsvCls:
	"""Csv commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csv", core, parent)

	@property
	def column(self):
		"""column commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_column'):
			from .Column import ColumnCls
			self._column = ColumnCls(self._core, self._cmd_group)
		return self._column

	# noinspection PyTypeChecker
	def get_dpoint(self) -> enums.DecimalSeparator:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage:CSV:DPOint \n
		Snippet: value: enums.DecimalSeparator = driver.sense.power.sweep.hardCopy.device.language.csv.get_dpoint() \n
		Defines which character is used as the decimal point of the values, either dot or comma. \n
			:return: dpoint: DOT| COMMa
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage:CSV:DPOint?')
		return Conversions.str_to_scalar_enum(response, enums.DecimalSeparator)

	def set_dpoint(self, dpoint: enums.DecimalSeparator) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage:CSV:DPOint \n
		Snippet: driver.sense.power.sweep.hardCopy.device.language.csv.set_dpoint(dpoint = enums.DecimalSeparator.COMMa) \n
		Defines which character is used as the decimal point of the values, either dot or comma. \n
			:param dpoint: DOT| COMMa
		"""
		param = Conversions.enum_scalar_to_str(dpoint, enums.DecimalSeparator)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage:CSV:DPOint {param}')

	# noinspection PyTypeChecker
	def get_header(self) -> enums.MeasRespHcOpCsvhEader:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage:CSV:HEADer \n
		Snippet: value: enums.MeasRespHcOpCsvhEader = driver.sense.power.sweep.hardCopy.device.language.csv.get_header() \n
		Defines whether each row (or column depending on the orientation) should be preceded by a header containing information
		about the trace (see also method RsSmab.Sense.Power.Sweep.HardCopy.data) . \n
			:return: header: OFF| STANdard
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage:CSV:HEADer?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespHcOpCsvhEader)

	def set_header(self, header: enums.MeasRespHcOpCsvhEader) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage:CSV:HEADer \n
		Snippet: driver.sense.power.sweep.hardCopy.device.language.csv.set_header(header = enums.MeasRespHcOpCsvhEader.OFF) \n
		Defines whether each row (or column depending on the orientation) should be preceded by a header containing information
		about the trace (see also method RsSmab.Sense.Power.Sweep.HardCopy.data) . \n
			:param header: OFF| STANdard
		"""
		param = Conversions.enum_scalar_to_str(header, enums.MeasRespHcOpCsvhEader)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage:CSV:HEADer {param}')

	# noinspection PyTypeChecker
	def get_orientation(self) -> enums.MeasRespHcOpCsvoRient:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage:CSV:ORIentation \n
		Snippet: value: enums.MeasRespHcOpCsvoRient = driver.sense.power.sweep.hardCopy.device.language.csv.get_orientation() \n
		Defines the orientation of the X/Y value pairs. \n
			:return: orientation: HORizontal| VERTical
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage:CSV:ORIentation?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespHcOpCsvoRient)

	def set_orientation(self, orientation: enums.MeasRespHcOpCsvoRient) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:LANGuage:CSV:ORIentation \n
		Snippet: driver.sense.power.sweep.hardCopy.device.language.csv.set_orientation(orientation = enums.MeasRespHcOpCsvoRient.HORizontal) \n
		Defines the orientation of the X/Y value pairs. \n
			:param orientation: HORizontal| VERTical
		"""
		param = Conversions.enum_scalar_to_str(orientation, enums.MeasRespHcOpCsvoRient)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:DEVice:LANGuage:CSV:ORIentation {param}')

	def clone(self) -> 'CsvCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsvCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
