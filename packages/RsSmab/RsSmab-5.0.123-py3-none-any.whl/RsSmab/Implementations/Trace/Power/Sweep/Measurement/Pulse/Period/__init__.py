from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PeriodCls:
	"""Period commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("period", core, parent)

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_display'):
			from .Display import DisplayCls
			self._display = DisplayCls(self._core, self._cmd_group)
		return self._display

	def get(self, trace=repcap.Trace.Default) -> float:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:MEASurement:PULSe:PERiod \n
		Snippet: value: float = driver.trace.power.sweep.measurement.pulse.period.get(trace = repcap.Trace.Default) \n
		The above listed commands query the measured pulse parameter values. Note: These commands are only available in time
		measurement mode and with R&S NRP-Z81 power sensors. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: period: float Range: 0 to 100"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:MEASurement:PULSe:PERiod?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'PeriodCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PeriodCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
