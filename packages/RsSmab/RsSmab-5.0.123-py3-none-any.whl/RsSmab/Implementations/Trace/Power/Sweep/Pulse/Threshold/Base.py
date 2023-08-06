from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BaseCls:
	"""Base commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("base", core, parent)

	# noinspection PyTypeChecker
	def get(self, trace=repcap.Trace.Default) -> enums.MeasRespPulsThrBase:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:PULSe:THReshold:BASE \n
		Snippet: value: enums.MeasRespPulsThrBase = driver.trace.power.sweep.pulse.threshold.base.get(trace = repcap.Trace.Default) \n
		Queries how the threshold parameters are calculated. Note: This parameter is only avalaible in time measurement mode and
		R&S NRP-Z81 power sensors. \n
			:param trace: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: base: VOLTage| POWer"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'TRACe{trace_cmd_val}:POWer:SWEep:PULSe:THReshold:BASE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespPulsThrBase)
