from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 30 total commands, 3 Subgroups, 15 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	@property
	def correction(self):
		"""correction commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def firmware(self):
		"""firmware commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_firmware'):
			from .Firmware import FirmwareCls
			self._firmware = FirmwareCls(self._core, self._cmd_group)
		return self._firmware

	@property
	def loader(self):
		"""loader commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_loader'):
			from .Loader import LoaderCls
			self._loader = LoaderCls(self._core, self._cmd_group)
		return self._loader

	def get_dac_0(self) -> int:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:DAC0 \n
		Snippet: value: int = driver.source.frequency.multiplier.external.get_dac_0() \n
		No command help available \n
			:return: dac_0_value: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:DAC0?')
		return Conversions.str_to_int(response)

	def set_dac_0(self, dac_0_value: int) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:DAC0 \n
		Snippet: driver.source.frequency.multiplier.external.set_dac_0(dac_0_value = 1) \n
		No command help available \n
			:param dac_0_value: No help available
		"""
		param = Conversions.decimal_value_to_str(dac_0_value)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:DAC0 {param}')

	def get_dac_1(self) -> int:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:DAC1 \n
		Snippet: value: int = driver.source.frequency.multiplier.external.get_dac_1() \n
		No command help available \n
			:return: dac_1_value: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:DAC1?')
		return Conversions.str_to_int(response)

	def get_fmaximum(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:FMAXimum \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_fmaximum() \n
		No command help available \n
			:return: fmax: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:FMAXimum?')
		return Conversions.str_to_float(response)

	def get_fminimum(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:FMINimum \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_fminimum() \n
		No command help available \n
			:return: fmin: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:FMINimum?')
		return Conversions.str_to_float(response)

	def get_ipmax(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:IPMax \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_ipmax() \n
		No command help available \n
			:return: input_power_max: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:IPMax?')
		return Conversions.str_to_float(response)

	def get_ipower(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:IPOWer \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_ipower() \n
		No command help available \n
			:return: input_power: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:IPOWer?')
		return Conversions.str_to_float(response)

	def get_multiplier(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:MULTiplier \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_multiplier() \n
		No command help available \n
			:return: multiplier: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:MULTiplier?')
		return Conversions.str_to_float(response)

	def get_padjust(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:PADJust \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_padjust() \n
		No command help available \n
			:return: power_adjust: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:PADJust?')
		return Conversions.str_to_float(response)

	def get_pmaximum(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:PMAXimum \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_pmaximum() \n
		No command help available \n
			:return: pmax: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:PMAXimum?')
		return Conversions.str_to_float(response)

	def get_pminimum(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:PMINimum \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_pminimum() \n
		No command help available \n
			:return: pmin: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:PMINimum?')
		return Conversions.str_to_float(response)

	def get_psd_minimum(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:PSDMinimum \n
		Snippet: value: float = driver.source.frequency.multiplier.external.get_psd_minimum() \n
		No command help available \n
			:return: power_sweep_dwell: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:PSDMinimum?')
		return Conversions.str_to_float(response)

	def get_revision(self) -> str:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:REVision \n
		Snippet: value: str = driver.source.frequency.multiplier.external.get_revision() \n
		No command help available \n
			:return: revision: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:REVision?')
		return trim_str_response(response)

	def get_snumber(self) -> str:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:SNUMber \n
		Snippet: value: str = driver.source.frequency.multiplier.external.get_snumber() \n
		No command help available \n
			:return: serial_number: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:SNUMber?')
		return trim_str_response(response)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:STATe \n
		Snippet: value: bool = driver.source.frequency.multiplier.external.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:STATe?')
		return Conversions.str_to_bool(response)

	def get_type_py(self) -> str:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:TYPE \n
		Snippet: value: str = driver.source.frequency.multiplier.external.get_type_py() \n
		No command help available \n
			:return: type_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:TYPE?')
		return trim_str_response(response)

	def clone(self) -> 'ExternalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExternalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
