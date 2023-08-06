from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ContinuousCls:
	"""Continuous commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("continuous", core, parent)

	def get_high(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:PHASe:CONTinuous:HIGH \n
		Snippet: value: float = driver.source.frequency.phase.continuous.get_high() \n
		Queries the maximum frequency of the frequency range for phase continuous settings. The maximum frequency of the
		frequency range depends on the mode selected with the command [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:MODE. \n
			:return: high: float Range: 1E5 to 6E9, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:PHASe:CONTinuous:HIGH?')
		return Conversions.str_to_float(response)

	def get_low(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:PHASe:CONTinuous:LOW \n
		Snippet: value: float = driver.source.frequency.phase.continuous.get_low() \n
		Queries the minimum frequency of the frequency range for phase continuous settings. The minimum frequency of the
		frequency range depends on the mode selected with the command [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:MODE. \n
			:return: low: float Range: 1E5 to 6E9, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:PHASe:CONTinuous:LOW?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FilterWidth:
		"""SCPI: [SOURce<HW>]:FREQuency:PHASe:CONTinuous:MODE \n
		Snippet: value: enums.FilterWidth = driver.source.frequency.phase.continuous.get_mode() \n
		Selects the mode that determines the frequency range for the phase continuity. To query the frequency range, use the
		commands [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:HIGH? and [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:LOW? \n
			:return: mode: NARRow| WIDE NARRow Small frequency range, asymmetrically around the RF frequency. WIDE Large frequency range, symmetrically around the RF frequency.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:PHASe:CONTinuous:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FilterWidth)

	def set_mode(self, mode: enums.FilterWidth) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:PHASe:CONTinuous:MODE \n
		Snippet: driver.source.frequency.phase.continuous.set_mode(mode = enums.FilterWidth.NARRow) \n
		Selects the mode that determines the frequency range for the phase continuity. To query the frequency range, use the
		commands [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:HIGH? and [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:LOW? \n
			:param mode: NARRow| WIDE NARRow Small frequency range, asymmetrically around the RF frequency. WIDE Large frequency range, symmetrically around the RF frequency.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FilterWidth)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:PHASe:CONTinuous:MODE {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:FREQuency:PHASe:CONTinuous:STATe \n
		Snippet: value: bool = driver.source.frequency.phase.continuous.get_state() \n
		Activates phase continuity of the RF frequency. The frequency range is limited and varies depending on the set RF
		frequency. You can query the range with the commands [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:HIGH?
		and [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:LOW?. Note: Restricted structure of command line. In phase continuous mode,
		the R&S SMA100B only processes the first command of a command line and ignores further commands if they are on the same
		line. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:PHASe:CONTinuous:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:PHASe:CONTinuous:STATe \n
		Snippet: driver.source.frequency.phase.continuous.set_state(state = False) \n
		Activates phase continuity of the RF frequency. The frequency range is limited and varies depending on the set RF
		frequency. You can query the range with the commands [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:HIGH?
		and [:SOURce<hw>]:FREQuency:PHASe:CONTinuous:LOW?. Note: Restricted structure of command line. In phase continuous mode,
		the R&S SMA100B only processes the first command of a command line and ignores further commands if they are on the same
		line. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:PHASe:CONTinuous:STATe {param}')
