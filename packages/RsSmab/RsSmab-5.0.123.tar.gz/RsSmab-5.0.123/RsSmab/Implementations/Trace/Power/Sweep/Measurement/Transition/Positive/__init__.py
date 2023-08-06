from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PositiveCls:
	"""Positive commands group definition. 6 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("positive", core, parent)

	@property
	def duration(self):
		"""duration commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def occurrence(self):
		"""occurrence commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_occurrence'):
			from .Occurrence import OccurrenceCls
			self._occurrence = OccurrenceCls(self._core, self._cmd_group)
		return self._occurrence

	@property
	def overshoot(self):
		"""overshoot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_overshoot'):
			from .Overshoot import OvershootCls
			self._overshoot = OvershootCls(self._core, self._cmd_group)
		return self._overshoot

	def clone(self) -> 'PositiveCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PositiveCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
