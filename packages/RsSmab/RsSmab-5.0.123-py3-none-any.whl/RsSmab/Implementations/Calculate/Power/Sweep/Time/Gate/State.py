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

	def set(self, state: bool, gate=repcap.Gate.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:STATe \n
		Snippet: driver.calculate.power.sweep.time.gate.state.set(state = False, gate = repcap.Gate.Default) \n
		Activates the gate settings for the selected trace. The measurement is started with command SENS:POW:INIT. Both gates are
		active at one time. \n
			:param state: 0| 1| OFF| ON
			:param gate: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
		"""
		param = Conversions.bool_to_str(state)
		gate_cmd_val = self._cmd_group.get_repcap_cmd_value(gate, repcap.Gate)
		self._core.io.write(f'CALCulate:POWer:SWEep:TIME:GATE{gate_cmd_val}:STATe {param}')

	def get(self, gate=repcap.Gate.Default) -> bool:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:STATe \n
		Snippet: value: bool = driver.calculate.power.sweep.time.gate.state.get(gate = repcap.Gate.Default) \n
		Activates the gate settings for the selected trace. The measurement is started with command SENS:POW:INIT. Both gates are
		active at one time. \n
			:param gate: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
			:return: state: 0| 1| OFF| ON"""
		gate_cmd_val = self._cmd_group.get_repcap_cmd_value(gate, repcap.Gate)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:GATE{gate_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
