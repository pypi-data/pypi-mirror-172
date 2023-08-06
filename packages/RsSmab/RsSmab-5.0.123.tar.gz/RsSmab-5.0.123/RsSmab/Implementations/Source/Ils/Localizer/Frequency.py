from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicCarrFreqMode:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:FREQuency:MODE \n
		Snippet: value: enums.AvionicCarrFreqMode = driver.source.ils.localizer.frequency.get_mode() \n
		Sets the mode for the carrier frequency of the signal. \n
			:return: ils_loc_freq_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicCarrFreqMode)

	def set_mode(self, ils_loc_freq_mode: enums.AvionicCarrFreqMode) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:FREQuency:MODE \n
		Snippet: driver.source.ils.localizer.frequency.set_mode(ils_loc_freq_mode = enums.AvionicCarrFreqMode.DECimal) \n
		Sets the mode for the carrier frequency of the signal. \n
			:param ils_loc_freq_mode: DECimal| ICAO DECimal Activates user-defined variation of the carrier frequency. ICAO Activates variation in predefined steps according to standard ILS transmitting frequencies (see Table 'ILS glide slope and localizer ICAO standard frequencies (MHz) and channels') .
		"""
		param = Conversions.enum_scalar_to_str(ils_loc_freq_mode, enums.AvionicCarrFreqMode)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:FREQuency:MODE {param}')

	# noinspection PyTypeChecker
	def get_step(self) -> enums.AvionicCarrFreqMode:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:FREQuency:STEP \n
		Snippet: value: enums.AvionicCarrFreqMode = driver.source.ils.localizer.frequency.get_step() \n
		No command help available \n
			:return: ils_loc_freq_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:FREQuency:STEP?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicCarrFreqMode)

	def set_step(self, ils_loc_freq_mode: enums.AvionicCarrFreqMode) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:FREQuency:STEP \n
		Snippet: driver.source.ils.localizer.frequency.set_step(ils_loc_freq_mode = enums.AvionicCarrFreqMode.DECimal) \n
		No command help available \n
			:param ils_loc_freq_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(ils_loc_freq_mode, enums.AvionicCarrFreqMode)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:FREQuency:STEP {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:FREQuency \n
		Snippet: value: float = driver.source.ils.localizer.frequency.get_value() \n
		Sets the carrier frequency of the signal. \n
			:return: carrier_freq: float Range: 100E3 to 6E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:FREQuency?')
		return Conversions.str_to_float(response)

	def set_value(self, carrier_freq: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:FREQuency \n
		Snippet: driver.source.ils.localizer.frequency.set_value(carrier_freq = 1.0) \n
		Sets the carrier frequency of the signal. \n
			:param carrier_freq: float Range: 100E3 to 6E9
		"""
		param = Conversions.decimal_value_to_str(carrier_freq)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:FREQuency {param}')
