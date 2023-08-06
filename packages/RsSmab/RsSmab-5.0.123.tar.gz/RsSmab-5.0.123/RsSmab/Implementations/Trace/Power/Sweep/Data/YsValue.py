from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class YsValueCls:
	"""YsValue commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ysValue", core, parent)

	def get(self, xvalue: float, trace=repcap.Trace.Default) -> float:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:DATA:YSValue \n
		Snippet: value: float = driver.trace.power.sweep.data.ysValue.get(xvalue = 1.0, trace = repcap.Trace.Default) \n
		For a given x-axis value, queries the measurement (y-axis) value of the selected trace of the current power analysis. \n
			:param xvalue: float
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: ys_value: float"""
		param = Conversions.decimal_value_to_str(xvalue)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:DATA:YSValue? {param}')
		return Conversions.str_to_float(response)
