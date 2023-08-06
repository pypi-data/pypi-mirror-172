from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TuningCls:
	"""Tuning commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tuning", core, parent)

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.LowHigh:
		"""SCPI: [SOURce]:ROSCillator:INTernal:TUNing:SLOPe \n
		Snippet: value: enums.LowHigh = driver.source.roscillator.internal.tuning.get_slope() \n
		Sets the sensitivity of the external tuning volatge. \n
			:return: state: LOW| HIGH
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:INTernal:TUNing:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_slope(self, state: enums.LowHigh) -> None:
		"""SCPI: [SOURce]:ROSCillator:INTernal:TUNing:SLOPe \n
		Snippet: driver.source.roscillator.internal.tuning.set_slope(state = enums.LowHigh.HIGH) \n
		Sets the sensitivity of the external tuning volatge. \n
			:param state: LOW| HIGH
		"""
		param = Conversions.enum_scalar_to_str(state, enums.LowHigh)
		self._core.io.write(f'SOURce:ROSCillator:INTernal:TUNing:SLOPe {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce]:ROSCillator:INTernal:TUNing:[STATe] \n
		Snippet: value: bool = driver.source.roscillator.internal.tuning.get_state() \n
		Activates the EFC (external frequency control) . \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:INTernal:TUNing:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce]:ROSCillator:INTernal:TUNing:[STATe] \n
		Snippet: driver.source.roscillator.internal.tuning.set_state(state = False) \n
		Activates the EFC (external frequency control) . \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:ROSCillator:INTernal:TUNing:STATe {param}')
