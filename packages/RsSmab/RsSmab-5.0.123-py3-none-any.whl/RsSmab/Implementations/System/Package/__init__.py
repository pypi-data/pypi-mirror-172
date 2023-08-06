from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PackageCls:
	"""Package commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("package", core, parent)

	@property
	def chartDisplay(self):
		"""chartDisplay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chartDisplay'):
			from .ChartDisplay import ChartDisplayCls
			self._chartDisplay = ChartDisplayCls(self._core, self._cmd_group)
		return self._chartDisplay

	@property
	def guiFramework(self):
		"""guiFramework commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_guiFramework'):
			from .GuiFramework import GuiFrameworkCls
			self._guiFramework = GuiFrameworkCls(self._core, self._cmd_group)
		return self._guiFramework

	@property
	def qt(self):
		"""qt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qt'):
			from .Qt import QtCls
			self._qt = QtCls(self._core, self._cmd_group)
		return self._qt

	def clone(self) -> 'PackageCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PackageCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
