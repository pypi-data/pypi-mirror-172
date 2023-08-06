from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbCls:
	"""Bb commands group definition. 17 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bb", core, parent)

	@property
	def dme(self):
		"""dme commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_dme'):
			from .Dme import DmeCls
			self._dme = DmeCls(self._core, self._cmd_group)
		return self._dme

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	@property
	def vor(self):
		"""vor commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_vor'):
			from .Vor import VorCls
			self._vor = VorCls(self._core, self._cmd_group)
		return self._vor

	@property
	def ils(self):
		"""ils commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_ils'):
			from .Ils import IlsCls
			self._ils = IlsCls(self._core, self._cmd_group)
		return self._ils

	def clone(self) -> 'BbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
