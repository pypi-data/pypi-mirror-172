from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubcarrierCls:
	"""Subcarrier commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subcarrier", core, parent)

	def get_depth(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:SUBCarrier:DEPTh \n
		Snippet: value: float = driver.source.vor.subcarrier.get_depth() \n
		Sets the AM modulation depth of the FM carrier. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:SUBCarrier:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:SUBCarrier:DEPTh \n
		Snippet: driver.source.vor.subcarrier.set_depth(depth = 1.0) \n
		Sets the AM modulation depth of the FM carrier. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:VOR:SUBCarrier:DEPTh {param}')

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:SUBCarrier:[FREQuency] \n
		Snippet: value: float = driver.source.vor.subcarrier.get_frequency() \n
		Sets the frequency of the FM carrier. \n
			:return: frequency: float Range: 5E3 to 15E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:SUBCarrier:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:SUBCarrier:[FREQuency] \n
		Snippet: driver.source.vor.subcarrier.set_frequency(frequency = 1.0) \n
		Sets the frequency of the FM carrier. \n
			:param frequency: float Range: 5E3 to 15E3
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:VOR:SUBCarrier:FREQuency {param}')
