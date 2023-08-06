from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VorCls:
	"""Vor commands group definition. 31 total commands, 8 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vor", core, parent)

	@property
	def comid(self):
		"""comid commands group. 1 Sub-classes, 10 commands."""
		if not hasattr(self, '_comid'):
			from .Comid import ComidCls
			self._comid = ComidCls(self._core, self._cmd_group)
		return self._comid

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
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import ReferenceCls
			self._reference = ReferenceCls(self._core, self._cmd_group)
		return self._reference

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def subcarrier(self):
		"""subcarrier commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_subcarrier'):
			from .Subcarrier import SubcarrierCls
			self._subcarrier = SubcarrierCls(self._core, self._cmd_group)
		return self._subcarrier

	@property
	def var(self):
		"""var commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_var'):
			from .Var import VarCls
			self._var = VarCls(self._core, self._cmd_group)
		return self._var

	@property
	def bangle(self):
		"""bangle commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bangle'):
			from .Bangle import BangleCls
			self._bangle = BangleCls(self._core, self._cmd_group)
		return self._bangle

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicVorMode:
		"""SCPI: [SOURce<HW>]:VOR:MODE \n
		Snippet: value: enums.AvionicVorMode = driver.source.vor.get_mode() \n
		Sets the operating mode for the VOR modulation signal. \n
			:return: mode: NORM| VAR| SUBCarrier| FMSubcarrier NORM VOR modulation is active. VAR Amplitude modulation of the output signal with the variable signal component (30Hz signal content) of the VOR signal. The modulation depth of the 30 Hz signal can be set with [:SOURcehw]:VOR:VAR[:DEPTh]. SUBCarrier Amplitude modulation of the output signal with the unmodulated FM carrier (9960Hz) of the VOR signal. The modulation depth of the 30 Hz signal can be set with [:SOURcehw]:VOR:SUBCarrier:DEPTh. FMSubcarrier Amplitude modulation of the output signal with the frequency modulated FM carrier (9960Hz) of the VOR signal. The modulation depth of the 30 Hz signal can be set with [:SOURcehw]:VOR:SUBCarrier:DEPTh. The frequency deviation can be set with [:SOURcehw]:VOR:REFerence[:DEViation].
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicVorMode)

	def set_mode(self, mode: enums.AvionicVorMode) -> None:
		"""SCPI: [SOURce<HW>]:VOR:MODE \n
		Snippet: driver.source.vor.set_mode(mode = enums.AvionicVorMode.FMSubcarrier) \n
		Sets the operating mode for the VOR modulation signal. \n
			:param mode: NORM| VAR| SUBCarrier| FMSubcarrier NORM VOR modulation is active. VAR Amplitude modulation of the output signal with the variable signal component (30Hz signal content) of the VOR signal. The modulation depth of the 30 Hz signal can be set with [:SOURcehw]:VOR:VAR[:DEPTh]. SUBCarrier Amplitude modulation of the output signal with the unmodulated FM carrier (9960Hz) of the VOR signal. The modulation depth of the 30 Hz signal can be set with [:SOURcehw]:VOR:SUBCarrier:DEPTh. FMSubcarrier Amplitude modulation of the output signal with the frequency modulated FM carrier (9960Hz) of the VOR signal. The modulation depth of the 30 Hz signal can be set with [:SOURcehw]:VOR:SUBCarrier:DEPTh. The frequency deviation can be set with [:SOURcehw]:VOR:REFerence[:DEViation].
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicVorMode)
		self._core.io.write(f'SOURce<HwInstance>:VOR:MODE {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:VOR:PRESet \n
		Snippet: driver.source.vor.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:VOR:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:VOR:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:VOR:PRESet \n
		Snippet: driver.source.vor.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:VOR:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:VOR:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.AvionicExtAm:
		"""SCPI: [SOURce<HW>]:VOR:SOURce \n
		Snippet: value: enums.AvionicExtAm = driver.source.vor.get_source() \n
		Sets the modulation source for the avionic standard modulation. If external modulation source is set, the external signal
		is added to the internal signal. Switching off the internal modulation source is not possible. \n
			:return: vor_source_sel: INT| EXT| INT,EXT INT Internal modulation source is used. EXT|INT,EXT An external modulation source is used, additional to the internal modulation source. The external signal is input at the Ext connector.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicExtAm)

	def set_source(self, vor_source_sel: enums.AvionicExtAm) -> None:
		"""SCPI: [SOURce<HW>]:VOR:SOURce \n
		Snippet: driver.source.vor.set_source(vor_source_sel = enums.AvionicExtAm.EXT) \n
		Sets the modulation source for the avionic standard modulation. If external modulation source is set, the external signal
		is added to the internal signal. Switching off the internal modulation source is not possible. \n
			:param vor_source_sel: INT| EXT| INT,EXT INT Internal modulation source is used. EXT|INT,EXT An external modulation source is used, additional to the internal modulation source. The external signal is input at the Ext connector.
		"""
		param = Conversions.enum_scalar_to_str(vor_source_sel, enums.AvionicExtAm)
		self._core.io.write(f'SOURce<HwInstance>:VOR:SOURce {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:VOR:STATe \n
		Snippet: value: bool = driver.source.vor.get_state() \n
		Activates/deactivates the VOR modulation. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:VOR:STATe \n
		Snippet: driver.source.vor.set_state(state = False) \n
		Activates/deactivates the VOR modulation. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:VOR:STATe {param}')

	def clone(self) -> 'VorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = VorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
