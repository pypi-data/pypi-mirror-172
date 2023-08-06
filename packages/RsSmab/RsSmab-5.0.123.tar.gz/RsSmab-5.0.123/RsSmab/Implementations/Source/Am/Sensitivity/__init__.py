from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SensitivityCls:
	"""Sensitivity commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sensitivity", core, parent)

	@property
	def exponential(self):
		"""exponential commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_exponential'):
			from .Exponential import ExponentialCls
			self._exponential = ExponentialCls(self._core, self._cmd_group)
		return self._exponential

	@property
	def linear(self):
		"""linear commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_linear'):
			from .Linear import LinearCls
			self._linear = LinearCls(self._core, self._cmd_group)
		return self._linear

	def clone(self) -> 'SensitivityCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SensitivityCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
