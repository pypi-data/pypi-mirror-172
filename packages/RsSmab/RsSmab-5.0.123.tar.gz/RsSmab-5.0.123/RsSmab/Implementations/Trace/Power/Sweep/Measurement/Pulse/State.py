from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def get(self, trace=repcap.Trace.Default) -> bool:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:MEASurement:PULSe:STATe \n
		Snippet: value: bool = driver.trace.power.sweep.measurement.pulse.state.get(trace = repcap.Trace.Default) \n
		The above listed commands query the measured pulse parameter values. Note: These commands are only available in time
		measurement mode and with R&S NRP-Z81 power sensors. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: state: float Range: 0 to 100"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:MEASurement:PULSe:STATe?')
		return Conversions.str_to_bool(response)
