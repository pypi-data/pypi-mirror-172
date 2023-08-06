from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RepetitionCls:
	"""Repetition commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("repetition", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:REPetition:POINts \n
		Snippet: value: int = driver.source.pulm.train.hopping.repetition.get_points() \n
		No command help available \n
			:return: points: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:HOPPing:REPetition:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[int]:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:REPetition \n
		Snippet: value: List[int] = driver.source.pulm.train.hopping.repetition.get_value() \n
		No command help available \n
			:return: repetition: No help available
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SOURce<HwInstance>:PULM:TRAin:HOPPing:REPetition?')
		return response

	def set_value(self, repetition: List[int]) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:REPetition \n
		Snippet: driver.source.pulm.train.hopping.repetition.set_value(repetition = [1, 2, 3]) \n
		No command help available \n
			:param repetition: No help available
		"""
		param = Conversions.list_to_csv_str(repetition)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRAin:HOPPing:REPetition {param}')
