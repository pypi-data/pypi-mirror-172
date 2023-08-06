from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LocalizerCls:
	"""Localizer commands group definition. 32 total commands, 6 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("localizer", core, parent)

	@property
	def comid(self):
		"""comid commands group. 1 Sub-classes, 10 commands."""
		if not hasattr(self, '_comid'):
			from .Comid import ComidCls
			self._comid = ComidCls(self._core, self._cmd_group)
		return self._comid

	@property
	def ddm(self):
		"""ddm commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_ddm'):
			from .Ddm import DdmCls
			self._ddm = DdmCls(self._core, self._cmd_group)
		return self._ddm

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def icao(self):
		"""icao commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icao'):
			from .Icao import IcaoCls
			self._icao = IcaoCls(self._core, self._cmd_group)
		return self._icao

	@property
	def llobe(self):
		"""llobe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_llobe'):
			from .Llobe import LlobeCls
			self._llobe = LlobeCls(self._core, self._cmd_group)
		return self._llobe

	@property
	def rlobe(self):
		"""rlobe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rlobe'):
			from .Rlobe import RlobeCls
			self._rlobe = RlobeCls(self._core, self._cmd_group)
		return self._rlobe

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicIlsLocMode:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:MODE \n
		Snippet: value: enums.AvionicIlsLocMode = driver.source.ils.localizer.get_mode() \n
		Sets the operating mode for the ILS localizer modulation signal. \n
			:return: mode: NORM| LLOBe| RLOBe NORM ILS localizer modulation is active. LLOBe Amplitude modulation of the output signal with the left lobe (90Hz) signal component of the ILS localizer signal is active. RLOBe Amplitude modulation of the output signal with the right lobe (150Hz) signal component of the ILS localizer signal is active.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsLocMode)

	def set_mode(self, mode: enums.AvionicIlsLocMode) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:MODE \n
		Snippet: driver.source.ils.localizer.set_mode(mode = enums.AvionicIlsLocMode.LLOBe) \n
		Sets the operating mode for the ILS localizer modulation signal. \n
			:param mode: NORM| LLOBe| RLOBe NORM ILS localizer modulation is active. LLOBe Amplitude modulation of the output signal with the left lobe (90Hz) signal component of the ILS localizer signal is active. RLOBe Amplitude modulation of the output signal with the right lobe (150Hz) signal component of the ILS localizer signal is active.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicIlsLocMode)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:MODE {param}')

	def get_phase(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:PHASe \n
		Snippet: value: float = driver.source.ils.localizer.get_phase() \n
		Sets the phase between the modulation signals of the left and right antenna lobe of the ILS localizer signal. The zero
		crossing of the right lobe (150Hz) signal serves as a reference. The angle refers to the period of the signal of the
		right antenna lobe. \n
			:return: phase: float Range: -60 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:PHASe?')
		return Conversions.str_to_float(response)

	def set_phase(self, phase: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:PHASe \n
		Snippet: driver.source.ils.localizer.set_phase(phase = 1.0) \n
		Sets the phase between the modulation signals of the left and right antenna lobe of the ILS localizer signal. The zero
		crossing of the right lobe (150Hz) signal serves as a reference. The angle refers to the period of the signal of the
		right antenna lobe. \n
			:param phase: float Range: -60 to 120
		"""
		param = Conversions.decimal_value_to_str(phase)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:PHASe {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:PRESet \n
		Snippet: driver.source.ils.localizer.preset() \n
		Sets the parameters of the ILS localizer component to their default values (*RST values specified for the commands) . For
		other ILS preset commands, see [:SOURce<hw>]:ILS:PRESet. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:PRESet \n
		Snippet: driver.source.ils.localizer.preset_with_opc() \n
		Sets the parameters of the ILS localizer component to their default values (*RST values specified for the commands) . For
		other ILS preset commands, see [:SOURce<hw>]:ILS:PRESet. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:LOCalizer:PRESet', opc_timeout_ms)

	def get_sdm(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:SDM \n
		Snippet: value: float = driver.source.ils.localizer.get_sdm() \n
		Sets the arithmetic sum of the modulation depths of the left lobe (90 Hz) and right lobe (150 Hz) for the ILS localizer
		signal contents. The RMS modulation depth of the sum signal depends on the phase setting of both modulation tones. \n
			:return: sdm: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:SDM?')
		return Conversions.str_to_float(response)

	def set_sdm(self, sdm: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:SDM \n
		Snippet: driver.source.ils.localizer.set_sdm(sdm = 1.0) \n
		Sets the arithmetic sum of the modulation depths of the left lobe (90 Hz) and right lobe (150 Hz) for the ILS localizer
		signal contents. The RMS modulation depth of the sum signal depends on the phase setting of both modulation tones. \n
			:param sdm: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(sdm)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:SDM {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.AvionicExtAm:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:SOURce \n
		Snippet: value: enums.AvionicExtAm = driver.source.ils.localizer.get_source() \n
		Sets the modulation source for the avionic standard modulation. If external modulation source is set, the external signal
		is added to the internal signal. Switching off the internal modulation source is not possible. \n
			:return: ils_loc_source: INT| EXT| INT,EXT INT Internal modulation source is used. EXT|INT,EXT An external modulation source is used, additional to the internal modulation source. The external signal is input at the Ext connector.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicExtAm)

	def set_source(self, ils_loc_source: enums.AvionicExtAm) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:SOURce \n
		Snippet: driver.source.ils.localizer.set_source(ils_loc_source = enums.AvionicExtAm.EXT) \n
		Sets the modulation source for the avionic standard modulation. If external modulation source is set, the external signal
		is added to the internal signal. Switching off the internal modulation source is not possible. \n
			:param ils_loc_source: INT| EXT| INT,EXT INT Internal modulation source is used. EXT|INT,EXT An external modulation source is used, additional to the internal modulation source. The external signal is input at the Ext connector.
		"""
		param = Conversions.enum_scalar_to_str(ils_loc_source, enums.AvionicExtAm)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:SOURce {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:STATe \n
		Snippet: value: bool = driver.source.ils.localizer.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:STATe \n
		Snippet: driver.source.ils.localizer.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:STATe {param}')

	def clone(self) -> 'LocalizerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LocalizerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
