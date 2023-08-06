from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StartCls:
	"""Start commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("start", core, parent)

	def set(self, start: float, gate=repcap.Gate.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:STARt \n
		Snippet: driver.calculate.power.sweep.time.gate.start.set(start = 1.0, gate = repcap.Gate.Default) \n
		Sets the start time of the selected gate. Insert value and unit. \n
			:param start: float
			:param gate: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
		"""
		param = Conversions.decimal_value_to_str(start)
		gate_cmd_val = self._cmd_group.get_repcap_cmd_value(gate, repcap.Gate)
		self._core.io.write(f'CALCulate:POWer:SWEep:TIME:GATE{gate_cmd_val}:STARt {param}')

	def get(self, gate=repcap.Gate.Default) -> float:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:STARt \n
		Snippet: value: float = driver.calculate.power.sweep.time.gate.start.get(gate = repcap.Gate.Default) \n
		Sets the start time of the selected gate. Insert value and unit. \n
			:param gate: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
			:return: start: No help available"""
		gate_cmd_val = self._cmd_group.get_repcap_cmd_value(gate, repcap.Gate)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:GATE{gate_cmd_val}:STARt?')
		return Conversions.str_to_float(response)
