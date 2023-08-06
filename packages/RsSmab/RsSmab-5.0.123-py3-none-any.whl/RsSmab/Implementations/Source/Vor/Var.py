from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VarCls:
	"""Var commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("var", core, parent)

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:VAR:FREQuency \n
		Snippet: value: float = driver.source.vor.var.get_frequency() \n
		Sets the frequency of the variable and the reference signal. As the two signals must have the same frequency, the setting
		is valid for both signals. \n
			:return: frequency: float Range: 10 to 60
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:VAR:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:VAR:FREQuency \n
		Snippet: driver.source.vor.var.set_frequency(frequency = 1.0) \n
		Sets the frequency of the variable and the reference signal. As the two signals must have the same frequency, the setting
		is valid for both signals. \n
			:param frequency: float Range: 10 to 60
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:VOR:VAR:FREQuency {param}')

	def get_depth(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:VAR:[DEPTh] \n
		Snippet: value: float = driver.source.vor.var.get_depth() \n
		Sets the AM modulation depth of the 30Hz variable signal. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:VAR:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:VAR:[DEPTh] \n
		Snippet: driver.source.vor.var.set_depth(depth = 1.0) \n
		Sets the AM modulation depth of the 30Hz variable signal. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:VOR:VAR:DEPTh {param}')
