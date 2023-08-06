from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	@property
	def hreference(self):
		"""hreference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hreference'):
			from .Hreference import HreferenceCls
			self._hreference = HreferenceCls(self._core, self._cmd_group)
		return self._hreference

	@property
	def lreference(self):
		"""lreference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lreference'):
			from .Lreference import LreferenceCls
			self._lreference = LreferenceCls(self._core, self._cmd_group)
		return self._lreference

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import ReferenceCls
			self._reference = ReferenceCls(self._core, self._cmd_group)
		return self._reference

	def clone(self) -> 'PowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
