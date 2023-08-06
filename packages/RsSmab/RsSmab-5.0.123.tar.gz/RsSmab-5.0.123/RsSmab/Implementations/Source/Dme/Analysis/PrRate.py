from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrRateCls:
	"""PrRate commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prRate", core, parent)

	def get_ok(self) -> bool:
		"""SCPI: [SOURce<HW>]:DME:ANALysis:PRRate:OK \n
		Snippet: value: bool = driver.source.dme.analysis.prRate.get_ok() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:ANALysis:PRRate:OK?')
		return Conversions.str_to_bool(response)

	def set_ok(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:DME:ANALysis:PRRate:OK \n
		Snippet: driver.source.dme.analysis.prRate.set_ok(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:DME:ANALysis:PRRate:OK {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:DME:ANALysis:PRRate:STATe \n
		Snippet: value: bool = driver.source.dme.analysis.prRate.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:ANALysis:PRRate:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:DME:ANALysis:PRRate:STATe \n
		Snippet: driver.source.dme.analysis.prRate.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:DME:ANALysis:PRRate:STATe {param}')
