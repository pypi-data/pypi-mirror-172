from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GsCls:
	"""Gs commands group definition. 20 total commands, 5 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gs", core, parent)

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
	def ulobe(self):
		"""ulobe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulobe'):
			from .Ulobe import UlobeCls
			self._ulobe = UlobeCls(self._core, self._cmd_group)
		return self._ulobe

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:ILS:GS:PRESet \n
		Snippet: driver.source.ils.gs.preset() \n
		Sets the parameters of the ILS glide slope component to their default values (*RST values specified for the commands) .
		For other ILS preset commands, see [:SOURce<hw>]:ILS:PRESet. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:GS:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:ILS:GS:PRESet \n
		Snippet: driver.source.ils.gs.preset_with_opc() \n
		Sets the parameters of the ILS glide slope component to their default values (*RST values specified for the commands) .
		For other ILS preset commands, see [:SOURce<hw>]:ILS:PRESet. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:GS:PRESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:ILS:GS:STATe \n
		Snippet: value: bool = driver.source.ils.gs.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:ILS:GS:STATe \n
		Snippet: driver.source.ils.gs.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GS:STATe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicIlsGsMode:
		"""SCPI: [SOURce<HW>]:ILS:[GS]:MODE \n
		Snippet: value: enums.AvionicIlsGsMode = driver.source.ils.gs.get_mode() \n
		Sets the operating mode for the ILS glide slope modulation signal. \n
			:return: mode: NORM| ULOBe| LLOBe NORM ILS glide slope modulation is active. ULOBe Amplitude modulation of the output signal with the upper lobe (90Hz) signal component of the ILS glide slope signal is active. LLOBe Amplitude modulation of the output signal with the lower lobe (150Hz) signal component of the ILS glide slope signal is active.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GS:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsGsMode)

	def set_mode(self, mode: enums.AvionicIlsGsMode) -> None:
		"""SCPI: [SOURce<HW>]:ILS:[GS]:MODE \n
		Snippet: driver.source.ils.gs.set_mode(mode = enums.AvionicIlsGsMode.LLOBe) \n
		Sets the operating mode for the ILS glide slope modulation signal. \n
			:param mode: NORM| ULOBe| LLOBe NORM ILS glide slope modulation is active. ULOBe Amplitude modulation of the output signal with the upper lobe (90Hz) signal component of the ILS glide slope signal is active. LLOBe Amplitude modulation of the output signal with the lower lobe (150Hz) signal component of the ILS glide slope signal is active.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicIlsGsMode)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GS:MODE {param}')

	def get_phase(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:[GS]:PHASe \n
		Snippet: value: float = driver.source.ils.gs.get_phase() \n
		Sets the phase between the modulation signals of the upper and lower antenna lobe of the ILS glide slope signal.
		Zero crossing of the lower lobe (150Hz) signal serves as a reference. The angle refers to the period of the signal of the
		right antenna lobe. \n
			:return: phase: float Range: -60 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GS:PHASe?')
		return Conversions.str_to_float(response)

	def set_phase(self, phase: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:[GS]:PHASe \n
		Snippet: driver.source.ils.gs.set_phase(phase = 1.0) \n
		Sets the phase between the modulation signals of the upper and lower antenna lobe of the ILS glide slope signal.
		Zero crossing of the lower lobe (150Hz) signal serves as a reference. The angle refers to the period of the signal of the
		right antenna lobe. \n
			:param phase: float Range: -60 to 120
		"""
		param = Conversions.decimal_value_to_str(phase)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GS:PHASe {param}')

	def get_sdm(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:[GS]:SDM \n
		Snippet: value: float = driver.source.ils.gs.get_sdm() \n
		Sets the arithmetic sum of the modulation depths of the upper lobe (90 Hz) and lower lobe (150 Hz) for the ILS glide
		slope signal contents. The RMS modulation depth of the sum signal depends on the phase setting of both modulation tones. \n
			:return: sdm: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GS:SDM?')
		return Conversions.str_to_float(response)

	def set_sdm(self, sdm: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:[GS]:SDM \n
		Snippet: driver.source.ils.gs.set_sdm(sdm = 1.0) \n
		Sets the arithmetic sum of the modulation depths of the upper lobe (90 Hz) and lower lobe (150 Hz) for the ILS glide
		slope signal contents. The RMS modulation depth of the sum signal depends on the phase setting of both modulation tones. \n
			:param sdm: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(sdm)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GS:SDM {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.AvionicExtAm:
		"""SCPI: [SOURce<HW>]:ILS:[GS]:SOURce \n
		Snippet: value: enums.AvionicExtAm = driver.source.ils.gs.get_source() \n
		Sets the modulation source for the avionic standard modulation. If external modulation source is set, the external signal
		is added to the internal signal. Switching off the internal modulation source is not possible. \n
			:return: ils_gs_source: INT| EXT| INT,EXT INT Internal modulation source is used. EXT|INT,EXT An external modulation source is used, additional to the internal modulation source. The external signal is input at the Ext connector.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GS:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicExtAm)

	def set_source(self, ils_gs_source: enums.AvionicExtAm) -> None:
		"""SCPI: [SOURce<HW>]:ILS:[GS]:SOURce \n
		Snippet: driver.source.ils.gs.set_source(ils_gs_source = enums.AvionicExtAm.EXT) \n
		Sets the modulation source for the avionic standard modulation. If external modulation source is set, the external signal
		is added to the internal signal. Switching off the internal modulation source is not possible. \n
			:param ils_gs_source: INT| EXT| INT,EXT INT Internal modulation source is used. EXT|INT,EXT An external modulation source is used, additional to the internal modulation source. The external signal is input at the Ext connector.
		"""
		param = Conversions.enum_scalar_to_str(ils_gs_source, enums.AvionicExtAm)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GS:SOURce {param}')

	def clone(self) -> 'GsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
