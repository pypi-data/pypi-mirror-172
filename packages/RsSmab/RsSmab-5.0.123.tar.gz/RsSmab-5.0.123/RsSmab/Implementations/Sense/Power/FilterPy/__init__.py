from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPyCls:
	"""FilterPy commands group definition. 6 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def length(self):
		"""length commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_length'):
			from .Length import LengthCls
			self._length = LengthCls(self._core, self._cmd_group)
		return self._length

	@property
	def nsRatio(self):
		"""nsRatio commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsRatio'):
			from .NsRatio import NsRatioCls
			self._nsRatio = NsRatioCls(self._core, self._cmd_group)
		return self._nsRatio

	@property
	def sonce(self):
		"""sonce commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sonce'):
			from .Sonce import SonceCls
			self._sonce = SonceCls(self._core, self._cmd_group)
		return self._sonce

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'FilterPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
