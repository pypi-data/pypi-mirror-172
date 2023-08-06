from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrcCls:
	"""Src commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("src", core, parent)

	def set(self, pow_source: enums.TraceSourceAll, trace=repcap.Trace.Default) -> None:
		"""SCPI: TRACe<CH>:POW:SWEep:SRC \n
		Snippet: driver.trace.pow.sweep.src.set(pow_source = enums.TraceSourceAll.HOLD, trace = repcap.Trace.Default) \n
		Determines the trace source of a trace for display in power measurement mode. \n
			:param pow_source: OFF| SEN1| SEN2| SEN3| SEN4| HOLD| REF| ON ON|OFF Activates ofr deactivates the display of a trace. SEN1|SEN2|SEN3|SEN4 Activates the measurement results display of the sensor that is assigned to the trace. REF Selects a reference trace. HOLD Freezes the measurement results display of the sensor that is assigned to the trace.
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
		"""
		param = Conversions.enum_scalar_to_str(pow_source, enums.TraceSourceAll)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'TRACe{trace_cmd_val}:POW:SWEep:SRC {param}')

	# noinspection PyTypeChecker
	def get(self, trace=repcap.Trace.Default) -> enums.TraceSourceAll:
		"""SCPI: TRACe<CH>:POW:SWEep:SRC \n
		Snippet: value: enums.TraceSourceAll = driver.trace.pow.sweep.src.get(trace = repcap.Trace.Default) \n
		Determines the trace source of a trace for display in power measurement mode. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: pow_source: OFF| SEN1| SEN2| SEN3| SEN4| HOLD| REF| ON ON|OFF Activates ofr deactivates the display of a trace. SEN1|SEN2|SEN3|SEN4 Activates the measurement results display of the sensor that is assigned to the trace. REF Selects a reference trace. HOLD Freezes the measurement results display of the sensor that is assigned to the trace."""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POW:SWEep:SRC?')
		return Conversions.str_to_scalar_enum(response, enums.TraceSourceAll)
