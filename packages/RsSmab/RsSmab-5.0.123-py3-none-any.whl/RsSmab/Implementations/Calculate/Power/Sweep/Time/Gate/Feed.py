from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FeedCls:
	"""Feed commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("feed", core, parent)

	def set(self, feed: enums.MeasRespTimeGate, gate=repcap.Gate.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:FEED \n
		Snippet: driver.calculate.power.sweep.time.gate.feed.set(feed = enums.MeasRespTimeGate.TRAC1, gate = repcap.Gate.Default) \n
		Selects the trace for time gated measurement. Both gates are assigned to the same trace. \n
			:param feed: TRAC1| TRAC2| TRAC3| TRACe1| TRACe2| TRACe3| TRAC4| TRACe4
			:param gate: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
		"""
		param = Conversions.enum_scalar_to_str(feed, enums.MeasRespTimeGate)
		gate_cmd_val = self._cmd_group.get_repcap_cmd_value(gate, repcap.Gate)
		self._core.io.write(f'CALCulate:POWer:SWEep:TIME:GATE{gate_cmd_val}:FEED {param}')

	# noinspection PyTypeChecker
	def get(self, gate=repcap.Gate.Default) -> enums.MeasRespTimeGate:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:FEED \n
		Snippet: value: enums.MeasRespTimeGate = driver.calculate.power.sweep.time.gate.feed.get(gate = repcap.Gate.Default) \n
		Selects the trace for time gated measurement. Both gates are assigned to the same trace. \n
			:param gate: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
			:return: feed: TRAC1| TRAC2| TRAC3| TRACe1| TRACe2| TRACe3| TRAC4| TRACe4"""
		gate_cmd_val = self._cmd_group.get_repcap_cmd_value(gate, repcap.Gate)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:GATE{gate_cmd_val}:FEED?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTimeGate)
