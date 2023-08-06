from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	def get_ok(self) -> bool:
		"""SCPI: [SOURce<HW>]:DME:ANALysis:POWer:OK \n
		Snippet: value: bool = driver.source.dme.analysis.power.get_ok() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:ANALysis:POWer:OK?')
		return Conversions.str_to_bool(response)

	def set_ok(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:DME:ANALysis:POWer:OK \n
		Snippet: driver.source.dme.analysis.power.set_ok(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:DME:ANALysis:POWer:OK {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:DME:ANALysis:POWer:STATe \n
		Snippet: value: bool = driver.source.dme.analysis.power.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:ANALysis:POWer:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:DME:ANALysis:POWer:STATe \n
		Snippet: driver.source.dme.analysis.power.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:DME:ANALysis:POWer:STATe {param}')
