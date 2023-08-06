from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OntimeCls:
	"""Ontime commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ontime", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:ONTime:POINts \n
		Snippet: value: int = driver.source.pulm.train.hopping.ontime.get_points() \n
		No command help available \n
			:return: points: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:HOPPing:ONTime:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[float]:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:ONTime \n
		Snippet: value: List[float] = driver.source.pulm.train.hopping.ontime.get_value() \n
		No command help available \n
			:return: ontime: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:PULM:TRAin:HOPPing:ONTime?')
		return response

	def set_value(self, ontime: List[float]) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:ONTime \n
		Snippet: driver.source.pulm.train.hopping.ontime.set_value(ontime = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param ontime: No help available
		"""
		param = Conversions.list_to_csv_str(ontime)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRAin:HOPPing:ONTime {param}')
