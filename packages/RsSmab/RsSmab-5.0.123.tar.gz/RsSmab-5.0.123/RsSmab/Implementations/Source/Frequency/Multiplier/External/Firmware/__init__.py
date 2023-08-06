from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FirmwareCls:
	"""Firmware commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("firmware", core, parent)

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Update import UpdateCls
			self._update = UpdateCls(self._core, self._cmd_group)
		return self._update

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:FIRMware:CATalog \n
		Snippet: value: List[str] = driver.source.frequency.multiplier.external.firmware.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:FIRMware:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:FIRMware:SELect \n
		Snippet: value: str = driver.source.frequency.multiplier.external.firmware.get_select() \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:FIRMware:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:FIRMware:SELect \n
		Snippet: driver.source.frequency.multiplier.external.firmware.set_select(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:FIRMware:SELect {param}')

	def get_version(self) -> str:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:FIRMware:VERSion \n
		Snippet: value: str = driver.source.frequency.multiplier.external.firmware.get_version() \n
		No command help available \n
			:return: firmware_version: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:FIRMware:VERSion?')
		return trim_str_response(response)

	def clone(self) -> 'FirmwareCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FirmwareCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
