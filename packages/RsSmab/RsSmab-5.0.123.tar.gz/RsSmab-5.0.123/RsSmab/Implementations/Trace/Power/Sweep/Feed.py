from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FeedCls:
	"""Feed commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("feed", core, parent)

	def set(self, feed: enums.MeasRespTraceFeed, trace=repcap.Trace.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:FEED \n
		Snippet: driver.trace.power.sweep.feed.set(feed = enums.MeasRespTraceFeed.NONE, trace = repcap.Trace.Default) \n
		Selects the source for the trace data. \n
			:param feed: SENS1| SENS2| SENS3| REFerence| NONE| SENSor1| SENSor2| SENSor3| SENS4| SENSor4
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
		"""
		param = Conversions.enum_scalar_to_str(feed, enums.MeasRespTraceFeed)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'TRACe{trace_cmd_val}:POWer:SWEep:FEED {param}')

	# noinspection PyTypeChecker
	def get(self, trace=repcap.Trace.Default) -> enums.MeasRespTraceFeed:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:FEED \n
		Snippet: value: enums.MeasRespTraceFeed = driver.trace.power.sweep.feed.get(trace = repcap.Trace.Default) \n
		Selects the source for the trace data. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: feed: SENS1| SENS2| SENS3| REFerence| NONE| SENSor1| SENSor2| SENSor3| SENS4| SENSor4"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:FEED?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTraceFeed)
