from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, math=repcap.Math.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:POWer:MATH<CH>:STATe \n
		Snippet: driver.calculate.power.sweep.power.math.state.set(state = False, math = repcap.Math.Default) \n
		Activates the trace mathematics mode for 'Power' measurement. This feature enables you to calculate the difference
		between the measurement values of two traces. For further calculation, a math result can also be assigned to a trace. \n
			:param state: 0| 1| OFF| ON
			:param math: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')
		"""
		param = Conversions.bool_to_str(state)
		math_cmd_val = self._cmd_group.get_repcap_cmd_value(math, repcap.Math)
		self._core.io.write(f'CALCulate:POWer:SWEep:POWer:MATH{math_cmd_val}:STATe {param}')

	def get(self, math=repcap.Math.Default) -> bool:
		"""SCPI: CALCulate:[POWer]:SWEep:POWer:MATH<CH>:STATe \n
		Snippet: value: bool = driver.calculate.power.sweep.power.math.state.get(math = repcap.Math.Default) \n
		Activates the trace mathematics mode for 'Power' measurement. This feature enables you to calculate the difference
		between the measurement values of two traces. For further calculation, a math result can also be assigned to a trace. \n
			:param math: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')
			:return: state: 0| 1| OFF| ON"""
		math_cmd_val = self._cmd_group.get_repcap_cmd_value(math, repcap.Math)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:POWer:MATH{math_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
