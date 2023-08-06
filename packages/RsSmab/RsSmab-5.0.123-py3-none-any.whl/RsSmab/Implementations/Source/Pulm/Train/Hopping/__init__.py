from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HoppingCls:
	"""Hopping commands group definition. 13 total commands, 5 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hopping", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def offTime(self):
		"""offTime commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_offTime'):
			from .OffTime import OffTimeCls
			self._offTime = OffTimeCls(self._core, self._cmd_group)
		return self._offTime

	@property
	def ontime(self):
		"""ontime commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ontime'):
			from .Ontime import OntimeCls
			self._ontime = OntimeCls(self._core, self._cmd_group)
		return self._ontime

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def repetition(self):
		"""repetition commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_repetition'):
			from .Repetition import RepetitionCls
			self._repetition = RepetitionCls(self._core, self._cmd_group)
		return self._repetition

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:CATalog \n
		Snippet: value: List[str] = driver.source.pulm.train.hopping.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:HOPPing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:DELete \n
		Snippet: driver.source.pulm.train.hopping.delete(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRAin:HOPPing:DELete {param}')

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:SELect \n
		Snippet: value: str = driver.source.pulm.train.hopping.get_select() \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:HOPPing:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:SELect \n
		Snippet: driver.source.pulm.train.hopping.set_select(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRAin:HOPPing:SELect {param}')

	def clone(self) -> 'HoppingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HoppingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
