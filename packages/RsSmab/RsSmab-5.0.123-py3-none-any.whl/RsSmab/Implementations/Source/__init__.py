from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 500 total commands, 29 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def adf(self):
		"""adf commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_adf'):
			from .Adf import AdfCls
			self._adf = AdfCls(self._core, self._cmd_group)
		return self._adf

	@property
	def am(self):
		"""am commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_am'):
			from .Am import AmCls
			self._am = AmCls(self._core, self._cmd_group)
		return self._am

	@property
	def bb(self):
		"""bb commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bb'):
			from .Bb import BbCls
			self._bb = BbCls(self._core, self._cmd_group)
		return self._bb

	@property
	def chirp(self):
		"""chirp commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_chirp'):
			from .Chirp import ChirpCls
			self._chirp = ChirpCls(self._core, self._cmd_group)
		return self._chirp

	@property
	def combined(self):
		"""combined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_combined'):
			from .Combined import CombinedCls
			self._combined = CombinedCls(self._core, self._cmd_group)
		return self._combined

	@property
	def correction(self):
		"""correction commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def dme(self):
		"""dme commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_dme'):
			from .Dme import DmeCls
			self._dme = DmeCls(self._core, self._cmd_group)
		return self._dme

	@property
	def fm(self):
		"""fm commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_fm'):
			from .Fm import FmCls
			self._fm = FmCls(self._core, self._cmd_group)
		return self._fm

	@property
	def frequency(self):
		"""frequency commands group. 6 Sub-classes, 8 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def freqSweep(self):
		"""freqSweep commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqSweep'):
			from .FreqSweep import FreqSweepCls
			self._freqSweep = FreqSweepCls(self._core, self._cmd_group)
		return self._freqSweep

	@property
	def ils(self):
		"""ils commands group. 5 Sub-classes, 3 commands."""
		if not hasattr(self, '_ils'):
			from .Ils import IlsCls
			self._ils = IlsCls(self._core, self._cmd_group)
		return self._ils

	@property
	def inputPy(self):
		"""inputPy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def lffSweep(self):
		"""lffSweep commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lffSweep'):
			from .LffSweep import LffSweepCls
			self._lffSweep = LffSweepCls(self._core, self._cmd_group)
		return self._lffSweep

	@property
	def lfOutput(self):
		"""lfOutput commands group. 8 Sub-classes, 2 commands."""
		if not hasattr(self, '_lfOutput'):
			from .LfOutput import LfOutputCls
			self._lfOutput = LfOutputCls(self._core, self._cmd_group)
		return self._lfOutput

	@property
	def listPy(self):
		"""listPy commands group. 8 Sub-classes, 8 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def mbeacon(self):
		"""mbeacon commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mbeacon'):
			from .Mbeacon import MbeaconCls
			self._mbeacon = MbeaconCls(self._core, self._cmd_group)
		return self._mbeacon

	@property
	def modulation(self):
		"""modulation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def noise(self):
		"""noise commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_noise'):
			from .Noise import NoiseCls
			self._noise = NoiseCls(self._core, self._cmd_group)
		return self._noise

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	@property
	def pgenerator(self):
		"""pgenerator commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pgenerator'):
			from .Pgenerator import PgeneratorCls
			self._pgenerator = PgeneratorCls(self._core, self._cmd_group)
		return self._pgenerator

	@property
	def phase(self):
		"""phase commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def pm(self):
		"""pm commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_pm'):
			from .Pm import PmCls
			self._pm = PmCls(self._core, self._cmd_group)
		return self._pm

	@property
	def power(self):
		"""power commands group. 8 Sub-classes, 8 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def psweep(self):
		"""psweep commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_psweep'):
			from .Psweep import PsweepCls
			self._psweep = PsweepCls(self._core, self._cmd_group)
		return self._psweep

	@property
	def pulm(self):
		"""pulm commands group. 4 Sub-classes, 10 commands."""
		if not hasattr(self, '_pulm'):
			from .Pulm import PulmCls
			self._pulm = PulmCls(self._core, self._cmd_group)
		return self._pulm

	@property
	def roscillator(self):
		"""roscillator commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_roscillator'):
			from .Roscillator import RoscillatorCls
			self._roscillator = RoscillatorCls(self._core, self._cmd_group)
		return self._roscillator

	@property
	def sweep(self):
		"""sweep commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_sweep'):
			from .Sweep import SweepCls
			self._sweep = SweepCls(self._core, self._cmd_group)
		return self._sweep

	@property
	def valRf(self):
		"""valRf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_valRf'):
			from .ValRf import ValRfCls
			self._valRf = ValRfCls(self._core, self._cmd_group)
		return self._valRf

	@property
	def vor(self):
		"""vor commands group. 8 Sub-classes, 4 commands."""
		if not hasattr(self, '_vor'):
			from .Vor import VorCls
			self._vor = VorCls(self._core, self._cmd_group)
		return self._vor

	def preset(self) -> None:
		"""SCPI: SOURce<HW>:PRESet \n
		Snippet: driver.source.preset() \n
		Presets all parameters which are related to the selected signal path. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SOURce<HW>:PRESet \n
		Snippet: driver.source.preset_with_opc() \n
		Presets all parameters which are related to the selected signal path. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:PRESet', opc_timeout_ms)

	def clone(self) -> 'SourceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SourceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
