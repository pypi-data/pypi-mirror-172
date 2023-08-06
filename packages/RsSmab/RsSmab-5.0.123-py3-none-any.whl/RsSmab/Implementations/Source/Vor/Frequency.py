from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicCarrFreqMode:
		"""SCPI: [SOURce<HW>]:VOR:FREQuency:MODE \n
		Snippet: value: enums.AvionicCarrFreqMode = driver.source.vor.frequency.get_mode() \n
		Sets the mode for the carrier frequency of the signal. \n
			:return: mode: DECimal| ICAO DECimal Activates user-defined variation of the carrier frequency. ICAO Activates variation in predefined steps according to standard VOR transmitting frequencies (see Table 'VOR ICAO standard frequencies (MHz) and channels') .
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicCarrFreqMode)

	def set_mode(self, mode: enums.AvionicCarrFreqMode) -> None:
		"""SCPI: [SOURce<HW>]:VOR:FREQuency:MODE \n
		Snippet: driver.source.vor.frequency.set_mode(mode = enums.AvionicCarrFreqMode.DECimal) \n
		Sets the mode for the carrier frequency of the signal. \n
			:param mode: DECimal| ICAO DECimal Activates user-defined variation of the carrier frequency. ICAO Activates variation in predefined steps according to standard VOR transmitting frequencies (see Table 'VOR ICAO standard frequencies (MHz) and channels') .
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicCarrFreqMode)
		self._core.io.write(f'SOURce<HwInstance>:VOR:FREQuency:MODE {param}')

	# noinspection PyTypeChecker
	def get_step(self) -> enums.AvionicKnobStep:
		"""SCPI: [SOURce<HW>]:VOR:FREQuency:STEP \n
		Snippet: value: enums.AvionicKnobStep = driver.source.vor.frequency.get_step() \n
		No command help available \n
			:return: step: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:FREQuency:STEP?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicKnobStep)

	def set_step(self, step: enums.AvionicKnobStep) -> None:
		"""SCPI: [SOURce<HW>]:VOR:FREQuency:STEP \n
		Snippet: driver.source.vor.frequency.set_step(step = enums.AvionicKnobStep.DECimal) \n
		No command help available \n
			:param step: No help available
		"""
		param = Conversions.enum_scalar_to_str(step, enums.AvionicKnobStep)
		self._core.io.write(f'SOURce<HwInstance>:VOR:FREQuency:STEP {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:FREQuency \n
		Snippet: value: float = driver.source.vor.frequency.get_value() \n
		Sets the carrier frequency of the signal. \n
			:return: carrier_freq: float Range: 100E3 to 6E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:FREQuency?')
		return Conversions.str_to_float(response)

	def set_value(self, carrier_freq: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:FREQuency \n
		Snippet: driver.source.vor.frequency.set_value(carrier_freq = 1.0) \n
		Sets the carrier frequency of the signal. \n
			:param carrier_freq: float Range: 100E3 to 6E9
		"""
		param = Conversions.decimal_value_to_str(carrier_freq)
		self._core.io.write(f'SOURce<HwInstance>:VOR:FREQuency {param}')
