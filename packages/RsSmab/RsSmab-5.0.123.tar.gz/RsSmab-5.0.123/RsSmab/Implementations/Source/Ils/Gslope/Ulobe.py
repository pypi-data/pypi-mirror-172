from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UlobeCls:
	"""Ulobe commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ulobe", core, parent)

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:[GSLope]:ULOBe:[FREQuency] \n
		Snippet: value: float = driver.source.ils.gslope.ulobe.get_frequency() \n
		No command help available \n
			:return: frequency: float Range: 60 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GSLope:ULOBe:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:[GSLope]:ULOBe:[FREQuency] \n
		Snippet: driver.source.ils.gslope.ulobe.set_frequency(frequency = 1.0) \n
		No command help available \n
			:param frequency: float Range: 60 to 120
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GSLope:ULOBe:FREQuency {param}')
