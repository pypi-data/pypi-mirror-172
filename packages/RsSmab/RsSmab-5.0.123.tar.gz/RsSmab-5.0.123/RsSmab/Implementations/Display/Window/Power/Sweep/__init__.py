from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SweepCls:
	"""Sweep commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sweep", core, parent)

	@property
	def background(self):
		"""background commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_background'):
			from .Background import BackgroundCls
			self._background = BackgroundCls(self._core, self._cmd_group)
		return self._background

	@property
	def grid(self):
		"""grid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_grid'):
			from .Grid import GridCls
			self._grid = GridCls(self._core, self._cmd_group)
		return self._grid

	def clone(self) -> 'SweepCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SweepCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
