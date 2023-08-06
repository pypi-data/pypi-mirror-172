from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RoscillatorCls:
	"""Roscillator commands group definition. 3 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("roscillator", core, parent)

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def store(self):
		"""store commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_store'):
			from .Store import StoreCls
			self._store = StoreCls(self._core, self._cmd_group)
		return self._store

	def clone(self) -> 'RoscillatorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RoscillatorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
