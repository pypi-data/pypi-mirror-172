from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReferenceCls:
	"""Reference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)

	def set(self, reference: float, trace=repcap.Trace.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:PULSe:THReshold:POWer:REFerence \n
		Snippet: driver.trace.power.sweep.pulse.threshold.power.reference.set(reference = 1.0, trace = repcap.Trace.Default) \n
		Queries the medial threshold level of the overall pulse level. This level is used to define the pulse width and pulse
		period. Note: This parameter is only avalaible in time measurement mode and R&S NRP-Z81 power sensors. \n
			:param reference: float Range: 0.0 to 100.0
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
		"""
		param = Conversions.decimal_value_to_str(reference)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'TRACe{trace_cmd_val}:POWer:SWEep:PULSe:THReshold:POWer:REFerence {param}')

	def get(self, trace=repcap.Trace.Default) -> float:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:PULSe:THReshold:POWer:REFerence \n
		Snippet: value: float = driver.trace.power.sweep.pulse.threshold.power.reference.get(trace = repcap.Trace.Default) \n
		Queries the medial threshold level of the overall pulse level. This level is used to define the pulse width and pulse
		period. Note: This parameter is only avalaible in time measurement mode and R&S NRP-Z81 power sensors. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: reference: float Range: 0.0 to 100.0"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:PULSe:THReshold:POWer:REFerence?')
		return Conversions.str_to_float(response)
