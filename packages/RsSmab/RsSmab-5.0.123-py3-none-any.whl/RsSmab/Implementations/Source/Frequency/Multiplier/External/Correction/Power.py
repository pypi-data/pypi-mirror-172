from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:POWer:POINts \n
		Snippet: value: int = driver.source.frequency.multiplier.external.correction.power.get_points() \n
		No command help available \n
			:return: points: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:POWer:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[float]:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:POWer \n
		Snippet: value: List[float] = driver.source.frequency.multiplier.external.correction.power.get_value() \n
		No command help available \n
			:return: list_pow: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:POWer?')
		return response

	def set_value(self, list_pow: List[float]) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:POWer \n
		Snippet: driver.source.frequency.multiplier.external.correction.power.set_value(list_pow = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param list_pow: No help available
		"""
		param = Conversions.list_to_csv_str(list_pow)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:POWer {param}')
