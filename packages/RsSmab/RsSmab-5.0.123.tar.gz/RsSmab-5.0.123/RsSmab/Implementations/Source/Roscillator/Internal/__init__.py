from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InternalCls:
	"""Internal commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("internal", core, parent)

	@property
	def tuning(self):
		"""tuning commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tuning'):
			from .Tuning import TuningCls
			self._tuning = TuningCls(self._core, self._cmd_group)
		return self._tuning

	@property
	def adjust(self):
		"""adjust commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_adjust'):
			from .Adjust import AdjustCls
			self._adjust = AdjustCls(self._core, self._cmd_group)
		return self._adjust

	def clone(self) -> 'InternalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InternalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
