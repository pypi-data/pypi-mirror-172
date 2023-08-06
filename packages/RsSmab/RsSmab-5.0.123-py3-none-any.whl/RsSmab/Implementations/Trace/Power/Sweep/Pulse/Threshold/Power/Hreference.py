from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HreferenceCls:
	"""Hreference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hreference", core, parent)

	def set(self, hreference: float, trace=repcap.Trace.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:PULSe:THReshold:POWer:HREFerence \n
		Snippet: driver.trace.power.sweep.pulse.threshold.power.hreference.set(hreference = 1.0, trace = repcap.Trace.Default) \n
		Queries the upper threshold level of the overall pulse level. The distal power defines the end of the rising edge and the
		start of the falling edge of the pulse. Note: This parameter is only avalaible in time measurement mode and R&S NRP-Z81
		power sensors. \n
			:param hreference: float Range: 0.0 to 100.0
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
		"""
		param = Conversions.decimal_value_to_str(hreference)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'TRACe{trace_cmd_val}:POWer:SWEep:PULSe:THReshold:POWer:HREFerence {param}')

	def get(self, trace=repcap.Trace.Default) -> float:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:PULSe:THReshold:POWer:HREFerence \n
		Snippet: value: float = driver.trace.power.sweep.pulse.threshold.power.hreference.get(trace = repcap.Trace.Default) \n
		Queries the upper threshold level of the overall pulse level. The distal power defines the end of the rising edge and the
		start of the falling edge of the pulse. Note: This parameter is only avalaible in time measurement mode and R&S NRP-Z81
		power sensors. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: hreference: float Range: 0.0 to 100.0"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:PULSe:THReshold:POWer:HREFerence?')
		return Conversions.str_to_float(response)
