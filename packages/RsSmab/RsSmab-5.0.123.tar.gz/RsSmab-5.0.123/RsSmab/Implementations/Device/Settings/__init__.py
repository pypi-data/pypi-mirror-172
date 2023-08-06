from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingsCls:
	"""Settings commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("settings", core, parent)

	@property
	def backup(self):
		"""backup commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_backup'):
			from .Backup import BackupCls
			self._backup = BackupCls(self._core, self._cmd_group)
		return self._backup

	@property
	def restore(self):
		"""restore commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_restore'):
			from .Restore import RestoreCls
			self._restore = RestoreCls(self._core, self._cmd_group)
		return self._restore

	def clone(self) -> 'SettingsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SettingsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
