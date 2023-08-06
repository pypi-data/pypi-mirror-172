from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnalysisCls:
	"""Analysis commands group definition. 8 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("analysis", core, parent)

	@property
	def efficiency(self):
		"""efficiency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_efficiency'):
			from .Efficiency import EfficiencyCls
			self._efficiency = EfficiencyCls(self._core, self._cmd_group)
		return self._efficiency

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def prRate(self):
		"""prRate commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_prRate'):
			from .PrRate import PrRateCls
			self._prRate = PrRateCls(self._core, self._cmd_group)
		return self._prRate

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	def clone(self) -> 'AnalysisCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AnalysisCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
