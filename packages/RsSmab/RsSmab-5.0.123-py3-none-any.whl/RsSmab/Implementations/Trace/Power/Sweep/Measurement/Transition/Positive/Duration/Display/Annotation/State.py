from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, trace=repcap.Trace.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:MEASurement:TRANsition:POSitive:DURation:DISPlay:ANNotation:[STATe] \n
		Snippet: driver.trace.power.sweep.measurement.transition.positive.duration.display.annotation.state.set(state = False, trace = repcap.Trace.Default) \n
		The above listed commands select the pulse parameters which are indicated in the display and hardcopy file.
		Only six parameters can be indicated at a time. Note: These commands are only available in time measurement mode and with
		R&S NRP-Z81 power sensors. \n
			:param state: 0| 1| OFF| ON
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
		"""
		param = Conversions.bool_to_str(state)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'TRACe{trace_cmd_val}:POWer:SWEep:MEASurement:TRANsition:POSitive:DURation:DISPlay:ANNotation:STATe {param}')

	def get(self, trace=repcap.Trace.Default) -> bool:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:MEASurement:TRANsition:POSitive:DURation:DISPlay:ANNotation:[STATe] \n
		Snippet: value: bool = driver.trace.power.sweep.measurement.transition.positive.duration.display.annotation.state.get(trace = repcap.Trace.Default) \n
		The above listed commands select the pulse parameters which are indicated in the display and hardcopy file.
		Only six parameters can be indicated at a time. Note: These commands are only available in time measurement mode and with
		R&S NRP-Z81 power sensors. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: state: 0| 1| OFF| ON"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:MEASurement:TRANsition:POSitive:DURation:DISPlay:ANNotation:STATe?')
		return Conversions.str_to_bool(response)
