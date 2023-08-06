from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 14 total commands, 6 Subgroups, 0 group commands
	Repeated Capability: InputIx, default value after init: InputIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_inputIx_get', 'repcap_inputIx_set', repcap.InputIx.Nr1)

	def repcap_inputIx_set(self, inputIx: repcap.InputIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to InputIx.Default
		Default value after init: InputIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(inputIx)

	def repcap_inputIx_get(self) -> repcap.InputIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def fpSweep(self):
		"""fpSweep commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fpSweep'):
			from .FpSweep import FpSweepCls
			self._fpSweep = FpSweepCls(self._core, self._cmd_group)
		return self._fpSweep

	@property
	def freqSweep(self):
		"""freqSweep commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqSweep'):
			from .FreqSweep import FreqSweepCls
			self._freqSweep = FreqSweepCls(self._core, self._cmd_group)
		return self._freqSweep

	@property
	def lffSweep(self):
		"""lffSweep commands group. 2 Sub-classes, 1 commands."""
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
		"""psweep commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_psweep'):
			from .Psweep import PsweepCls
			self._psweep = PsweepCls(self._core, self._cmd_group)
		return self._psweep

	@property
	def sweep(self):
		"""sweep commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sweep'):
			from .Sweep import SweepCls
			self._sweep = SweepCls(self._core, self._cmd_group)
		return self._sweep

	def clone(self) -> 'TriggerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TriggerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
