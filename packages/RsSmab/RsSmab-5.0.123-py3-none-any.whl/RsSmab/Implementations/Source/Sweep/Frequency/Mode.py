from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	# noinspection PyTypeChecker
	def get_advanced(self) -> enums.AutoManualMode:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MODE:ADVanced \n
		Snippet: value: enums.AutoManualMode = driver.source.sweep.frequency.mode.get_advanced() \n
		No command help available \n
			:return: adv_freq_mode_sel: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:MODE:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_advanced(self, adv_freq_mode_sel: enums.AutoManualMode) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MODE:ADVanced \n
		Snippet: driver.source.sweep.frequency.mode.set_advanced(adv_freq_mode_sel = enums.AutoManualMode.AUTO) \n
		No command help available \n
			:param adv_freq_mode_sel: No help available
		"""
		param = Conversions.enum_scalar_to_str(adv_freq_mode_sel, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:MODE:ADVanced {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.AutoManStep:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MODE \n
		Snippet: value: enums.AutoManStep = driver.source.sweep.frequency.mode.get_value() \n
		Sets the cycle mode for the frequency sweep. \n
			:return: mode: AUTO| MANual| STEP AUTO Each trigger event triggers exactly one complete sweep. MANual The trigger system is not active. You can trigger every step individually by input of the frequencies with the command [:SOURcehw]:FREQuency:MANual. STEP Each trigger event triggers one sweep step. The frequency increases by the value entered with [:SOURcehw]:SWEep[:FREQuency]:STEP[:LINear] (linear spacing) or [:SOURcehw]:SWEep[:FREQuency]:STEP:LOGarithmic (logarithmic spacing) .
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManStep)

	def set_value(self, mode: enums.AutoManStep) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MODE \n
		Snippet: driver.source.sweep.frequency.mode.set_value(mode = enums.AutoManStep.AUTO) \n
		Sets the cycle mode for the frequency sweep. \n
			:param mode: AUTO| MANual| STEP AUTO Each trigger event triggers exactly one complete sweep. MANual The trigger system is not active. You can trigger every step individually by input of the frequencies with the command [:SOURcehw]:FREQuency:MANual. STEP Each trigger event triggers one sweep step. The frequency increases by the value entered with [:SOURcehw]:SWEep[:FREQuency]:STEP[:LINear] (linear spacing) or [:SOURcehw]:SWEep[:FREQuency]:STEP:LOGarithmic (logarithmic spacing) .
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AutoManStep)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:MODE {param}')
