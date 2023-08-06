from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PulseCls:
	"""Pulse commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pulse", core, parent)

	@property
	def base(self):
		"""base commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_base'):
			from .Base import BaseCls
			self._base = BaseCls(self._core, self._cmd_group)
		return self._base

	@property
	def top(self):
		"""top commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_top'):
			from .Top import TopCls
			self._top = TopCls(self._core, self._cmd_group)
		return self._top

	def clone(self) -> 'PulseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PulseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
