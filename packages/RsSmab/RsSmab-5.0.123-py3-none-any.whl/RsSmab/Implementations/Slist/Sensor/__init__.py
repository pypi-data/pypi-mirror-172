from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SensorCls:
	"""Sensor commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sensor", core, parent)

	@property
	def map(self):
		"""map commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_map'):
			from .Map import MapCls
			self._map = MapCls(self._core, self._cmd_group)
		return self._map

	def clone(self) -> 'SensorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SensorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
