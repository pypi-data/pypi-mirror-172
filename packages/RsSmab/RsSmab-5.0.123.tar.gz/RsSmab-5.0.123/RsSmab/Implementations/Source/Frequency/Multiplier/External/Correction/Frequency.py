from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:FREQuency:POINts \n
		Snippet: value: int = driver.source.frequency.multiplier.external.correction.frequency.get_points() \n
		No command help available \n
			:return: points: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:FREQuency:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[float]:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:FREQuency \n
		Snippet: value: List[float] = driver.source.frequency.multiplier.external.correction.frequency.get_value() \n
		No command help available \n
			:return: list_freq: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:FREQuency?')
		return response

	def set_value(self, list_freq: List[float]) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:CORRection:FREQuency \n
		Snippet: driver.source.frequency.multiplier.external.correction.frequency.set_value(list_freq = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param list_freq: No help available
		"""
		param = Conversions.list_to_csv_str(list_freq)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:CORRection:FREQuency {param}')
