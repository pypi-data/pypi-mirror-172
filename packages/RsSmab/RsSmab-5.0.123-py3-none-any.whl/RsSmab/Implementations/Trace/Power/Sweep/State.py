from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: enums.MeasRespTraceState, trace=repcap.Trace.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:STATe \n
		Snippet: driver.trace.power.sweep.state.set(state = enums.MeasRespTraceState.HOLD, trace = repcap.Trace.Default) \n
		Activates the selected trace. \n
			:param state: OFF| ON| HOLD
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
		"""
		param = Conversions.enum_scalar_to_str(state, enums.MeasRespTraceState)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'TRACe{trace_cmd_val}:POWer:SWEep:STATe {param}')

	# noinspection PyTypeChecker
	def get(self, trace=repcap.Trace.Default) -> enums.MeasRespTraceState:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:STATe \n
		Snippet: value: enums.MeasRespTraceState = driver.trace.power.sweep.state.get(trace = repcap.Trace.Default) \n
		Activates the selected trace. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: state: OFF| ON| HOLD"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTraceState)
