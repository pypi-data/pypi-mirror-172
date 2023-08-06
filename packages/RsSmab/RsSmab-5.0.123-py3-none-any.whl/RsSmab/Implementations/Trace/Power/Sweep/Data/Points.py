from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PointsCls:
	"""Points commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("points", core, parent)

	def get(self, trace=repcap.Trace.Default) -> int:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:DATA:POINts \n
		Snippet: value: int = driver.trace.power.sweep.data.points.get(trace = repcap.Trace.Default) \n
		Queries the number of measurement points of the selected trace of the current power analysis. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: points: integer Range: 10 to 1000"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:DATA:POINts?')
		return Conversions.str_to_int(response)
