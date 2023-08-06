from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 10 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	@property
	def gate(self):
		"""gate commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_gate'):
			from .Gate import GateCls
			self._gate = GateCls(self._core, self._cmd_group)
		return self._gate

	@property
	def math(self):
		"""math commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_math'):
			from .Math import MathCls
			self._math = MathCls(self._core, self._cmd_group)
		return self._math

	def clone(self) -> 'TimeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TimeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
