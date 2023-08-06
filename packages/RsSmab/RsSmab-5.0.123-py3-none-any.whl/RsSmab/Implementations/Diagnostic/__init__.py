from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DiagnosticCls:
	"""Diagnostic commands group definition. 20 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("diagnostic", core, parent)

	@property
	def bgInfo(self):
		"""bgInfo commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bgInfo'):
			from .BgInfo import BgInfoCls
			self._bgInfo = BgInfoCls(self._core, self._cmd_group)
		return self._bgInfo

	@property
	def debug(self):
		"""debug commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_debug'):
			from .Debug import DebugCls
			self._debug = DebugCls(self._core, self._cmd_group)
		return self._debug

	@property
	def eeprom(self):
		"""eeprom commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_eeprom'):
			from .Eeprom import EepromCls
			self._eeprom = EepromCls(self._core, self._cmd_group)
		return self._eeprom

	@property
	def info(self):
		"""info commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_info'):
			from .Info import InfoCls
			self._info = InfoCls(self._core, self._cmd_group)
		return self._info

	@property
	def point(self):
		"""point commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_point'):
			from .Point import PointCls
			self._point = PointCls(self._core, self._cmd_group)
		return self._point

	@property
	def service(self):
		"""service commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_service'):
			from .Service import ServiceCls
			self._service = ServiceCls(self._core, self._cmd_group)
		return self._service

	@property
	def measure(self):
		"""measure commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_measure'):
			from .Measure import MeasureCls
			self._measure = MeasureCls(self._core, self._cmd_group)
		return self._measure

	def clone(self) -> 'DiagnosticCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DiagnosticCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
