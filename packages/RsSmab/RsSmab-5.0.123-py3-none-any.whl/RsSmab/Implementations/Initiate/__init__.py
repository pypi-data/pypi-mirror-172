from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InitiateCls:
	"""Initiate commands group definition. 5 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("initiate", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, channel: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._cmd_group.set_repcap_enum_value(channel)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def freqSweep(self):
		"""freqSweep commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqSweep'):
			from .FreqSweep import FreqSweepCls
			self._freqSweep = FreqSweepCls(self._core, self._cmd_group)
		return self._freqSweep

	@property
	def lffSweep(self):
		"""lffSweep commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lffSweep'):
			from .LffSweep import LffSweepCls
			self._lffSweep = LffSweepCls(self._core, self._cmd_group)
		return self._lffSweep

	@property
	def listPy(self):
		"""listPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def psweep(self):
		"""psweep commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_psweep'):
			from .Psweep import PsweepCls
			self._psweep = PsweepCls(self._core, self._cmd_group)
		return self._psweep

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	def clone(self) -> 'InitiateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InitiateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
