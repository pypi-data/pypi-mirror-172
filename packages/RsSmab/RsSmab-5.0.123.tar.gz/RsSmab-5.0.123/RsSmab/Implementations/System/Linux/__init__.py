from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LinuxCls:
	"""Linux commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("linux", core, parent)

	@property
	def kernel(self):
		"""kernel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kernel'):
			from .Kernel import KernelCls
			self._kernel = KernelCls(self._core, self._cmd_group)
		return self._kernel

	def clone(self) -> 'LinuxCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LinuxCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
