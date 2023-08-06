from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CorrectionCls:
	"""Correction commands group definition. 10 total commands, 3 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("correction", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def sensor(self):
		"""sensor commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sensor'):
			from .Sensor import SensorCls
			self._sensor = SensorCls(self._core, self._cmd_group)
		return self._sensor

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:CATalog \n
		Snippet: value: List[str] = driver.source.frequency.multiplier.external.correction.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_closs(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:CLOSs \n
		Snippet: value: float = driver.source.frequency.multiplier.external.correction.get_closs() \n
		No command help available \n
			:return: cable_loss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:CLOSs?')
		return Conversions.str_to_float(response)

	def set_closs(self, cable_loss: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:CLOSs \n
		Snippet: driver.source.frequency.multiplier.external.correction.set_closs(cable_loss = 1.0) \n
		No command help available \n
			:param cable_loss: No help available
		"""
		param = Conversions.decimal_value_to_str(cable_loss)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:CLOSs {param}')

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:DELete \n
		Snippet: driver.source.frequency.multiplier.external.correction.delete(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:DELete {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.RfFreqMultCcorMode:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:MODE \n
		Snippet: value: enums.RfFreqMultCcorMode = driver.source.frequency.multiplier.external.correction.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.RfFreqMultCcorMode)

	def set_mode(self, mode: enums.RfFreqMultCcorMode) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:MODE \n
		Snippet: driver.source.frequency.multiplier.external.correction.set_mode(mode = enums.RfFreqMultCcorMode.HPRecision) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.RfFreqMultCcorMode)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:MODE {param}')

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:SELect \n
		Snippet: value: str = driver.source.frequency.multiplier.external.correction.get_select() \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:SELect \n
		Snippet: driver.source.frequency.multiplier.external.correction.set_select(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:SELect {param}')

	def clone(self) -> 'CorrectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CorrectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
