from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PulseCls:
	"""Pulse commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pulse", core, parent)

	def get_period(self) -> float:
		"""SCPI: [SOURce<HW>]:CHIRp:PULSe:PERiod \n
		Snippet: value: float = driver.source.chirp.pulse.get_period() \n
		Sets the period of the generated modulation chirp. The period determines the repetition frequency of the internal signal. \n
			:return: period: float Range: 5E-6 (2E-7 with K23) to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:PULSe:PERiod?')
		return Conversions.str_to_float(response)

	def set_period(self, period: float) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:PULSe:PERiod \n
		Snippet: driver.source.chirp.pulse.set_period(period = 1.0) \n
		Sets the period of the generated modulation chirp. The period determines the repetition frequency of the internal signal. \n
			:param period: float Range: 5E-6 (2E-7 with K23) to 100
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:PULSe:PERiod {param}')

	def get_width(self) -> float:
		"""SCPI: [SOURce<HW>]:CHIRp:PULSe:WIDTh \n
		Snippet: value: float = driver.source.chirp.pulse.get_width() \n
		Sets the width of the generated pulse. The pulse width must be at least 1us less than the set pulse period. \n
			:return: width: float Range: 2E-6 (1E-7 with K23) to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:PULSe:WIDTh?')
		return Conversions.str_to_float(response)

	def set_width(self, width: float) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:PULSe:WIDTh \n
		Snippet: driver.source.chirp.pulse.set_width(width = 1.0) \n
		Sets the width of the generated pulse. The pulse width must be at least 1us less than the set pulse period. \n
			:param width: float Range: 2E-6 (1E-7 with K23) to 100
		"""
		param = Conversions.decimal_value_to_str(width)
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:PULSe:WIDTh {param}')
