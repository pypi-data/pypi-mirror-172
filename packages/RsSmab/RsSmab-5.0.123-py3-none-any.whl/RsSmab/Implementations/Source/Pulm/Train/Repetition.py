from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RepetitionCls:
	"""Repetition commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("repetition", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:REPetition:POINts \n
		Snippet: value: int = driver.source.pulm.train.repetition.get_points() \n
		Queries the number of on and off time entries and repetitions in the selected list. \n
			:return: points: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:REPetition:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[int]:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:REPetition \n
		Snippet: value: List[int] = driver.source.pulm.train.repetition.get_value() \n
		Sets the number of repetitions for each pulse on/off time value pair. \n
			:return: repetition: Repetition#1{, Repetition#2, ...} 0 = ignore value pair Set 'Repetition = 0' to skip a particular pulse without deleting the pulse on/off time value pair Range: 0 to 65535
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SOURce<HwInstance>:PULM:TRAin:REPetition?')
		return response

	def set_value(self, repetition: List[int]) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:REPetition \n
		Snippet: driver.source.pulm.train.repetition.set_value(repetition = [1, 2, 3]) \n
		Sets the number of repetitions for each pulse on/off time value pair. \n
			:param repetition: Repetition#1{, Repetition#2, ...} 0 = ignore value pair Set 'Repetition = 0' to skip a particular pulse without deleting the pulse on/off time value pair Range: 0 to 65535
		"""
		param = Conversions.list_to_csv_str(repetition)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRAin:REPetition {param}')
