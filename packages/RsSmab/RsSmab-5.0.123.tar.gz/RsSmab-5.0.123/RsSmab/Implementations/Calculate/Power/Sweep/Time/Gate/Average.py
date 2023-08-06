from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	def get(self, gate=repcap.Gate.Default) -> float:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:AVERage \n
		Snippet: value: float = driver.calculate.power.sweep.time.gate.average.get(gate = repcap.Gate.Default) \n
		Queries the average power value of the time gated measurement. \n
			:param gate: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
			:return: average: float Range: -1000 to 1000"""
		gate_cmd_val = self._cmd_group.get_repcap_cmd_value(gate, repcap.Gate)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:GATE{gate_cmd_val}:AVERage?')
		return Conversions.str_to_float(response)
