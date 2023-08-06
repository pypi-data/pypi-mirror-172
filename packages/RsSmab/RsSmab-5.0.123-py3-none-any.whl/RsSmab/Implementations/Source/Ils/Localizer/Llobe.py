from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LlobeCls:
	"""Llobe commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("llobe", core, parent)

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:LLOBe:[FREQuency] \n
		Snippet: value: float = driver.source.ils.localizer.llobe.get_frequency() \n
		Sets the modulation frequency of the antenna lobe arranged at the bottom viewed from the air plane for the ILS localizer
		modulation signal. \n
			:return: frequency: float Range: 60 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:LLOBe:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:LLOBe:[FREQuency] \n
		Snippet: driver.source.ils.localizer.llobe.set_frequency(frequency = 1.0) \n
		Sets the modulation frequency of the antenna lobe arranged at the bottom viewed from the air plane for the ILS localizer
		modulation signal. \n
			:param frequency: float Range: 60 to 120
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:LLOBe:FREQuency {param}')
