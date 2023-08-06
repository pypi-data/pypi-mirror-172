from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MeasurementCls:
	"""Measurement commands group definition. 43 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measurement", core, parent)

	@property
	def fullscreen(self):
		"""fullscreen commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fullscreen'):
			from .Fullscreen import FullscreenCls
			self._fullscreen = FullscreenCls(self._core, self._cmd_group)
		return self._fullscreen

	@property
	def gate(self):
		"""gate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gate'):
			from .Gate import GateCls
			self._gate = GateCls(self._core, self._cmd_group)
		return self._gate

	@property
	def marker(self):
		"""marker commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	@property
	def power(self):
		"""power commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def pulse(self):
		"""pulse commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_pulse'):
			from .Pulse import PulseCls
			self._pulse = PulseCls(self._core, self._cmd_group)
		return self._pulse

	@property
	def standard(self):
		"""standard commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_standard'):
			from .Standard import StandardCls
			self._standard = StandardCls(self._core, self._cmd_group)
		return self._standard

	@property
	def transition(self):
		"""transition commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_transition'):
			from .Transition import TransitionCls
			self._transition = TransitionCls(self._core, self._cmd_group)
		return self._transition

	def clone(self) -> 'MeasurementCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MeasurementCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
