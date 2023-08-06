from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PllCls:
	"""Pll commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pll", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FreqPllModeF:
		"""SCPI: [SOURce<HW>]:FREQuency:PLL:MODE \n
		Snippet: value: enums.FreqPllModeF = driver.source.frequency.pll.get_mode() \n
		Selects the PLL (Phase Locked Loop) bandwidth of the main synthesizer. \n
			:return: mode: NORMal| NARRow NORMal Maximum modulation bandwidth and FM/PhiM deviation. NARRow Narrow PLL bandwidth
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:PLL:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqPllModeF)

	def set_mode(self, mode: enums.FreqPllModeF) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:PLL:MODE \n
		Snippet: driver.source.frequency.pll.set_mode(mode = enums.FreqPllModeF.NARRow) \n
		Selects the PLL (Phase Locked Loop) bandwidth of the main synthesizer. \n
			:param mode: NORMal| NARRow NORMal Maximum modulation bandwidth and FM/PhiM deviation. NARRow Narrow PLL bandwidth
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FreqPllModeF)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:PLL:MODE {param}')
