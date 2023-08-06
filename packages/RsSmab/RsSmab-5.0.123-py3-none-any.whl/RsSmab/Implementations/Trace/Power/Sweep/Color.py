from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ColorCls:
	"""Color commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("color", core, parent)

	def set(self, color: enums.MeasRespTraceColor, trace=repcap.Trace.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:COLor \n
		Snippet: driver.trace.power.sweep.color.set(color = enums.MeasRespTraceColor.BLUE, trace = repcap.Trace.Default) \n
		Defines the color of a trace. \n
			:param color: INVers| GRAY| YELLow| BLUE| GREen| RED| MAGenta
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
		"""
		param = Conversions.enum_scalar_to_str(color, enums.MeasRespTraceColor)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'TRACe{trace_cmd_val}:POWer:SWEep:COLor {param}')

	# noinspection PyTypeChecker
	def get(self, trace=repcap.Trace.Default) -> enums.MeasRespTraceColor:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:COLor \n
		Snippet: value: enums.MeasRespTraceColor = driver.trace.power.sweep.color.get(trace = repcap.Trace.Default) \n
		Defines the color of a trace. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: color: INVers| GRAY| YELLow| BLUE| GREen| RED| MAGenta"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:COLor?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTraceColor)
