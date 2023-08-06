from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class YvaluesCls:
	"""Yvalues commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("yvalues", core, parent)

	def get(self, trace=repcap.Trace.Default) -> List[float]:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:DATA:YVALues \n
		Snippet: value: List[float] = driver.trace.power.sweep.data.yvalues.get(trace = repcap.Trace.Default) \n
		Queries the measurement (y-axis) values of the selected trace of the current power analysis. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: yvalues: string"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_bin_or_ascii_float_list(f'TRACe{trace_cmd_val}:POWer:SWEep:DATA:YVALues?')
		return response
