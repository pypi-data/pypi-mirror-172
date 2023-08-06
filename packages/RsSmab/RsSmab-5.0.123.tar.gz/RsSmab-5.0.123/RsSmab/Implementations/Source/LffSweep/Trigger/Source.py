from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	# noinspection PyTypeChecker
	def get_advanced(self) -> enums.TrigSweepImmBusExt:
		"""SCPI: [SOURce<HW>]:LFFSweep:TRIGger:SOURce:ADVanced \n
		Snippet: value: enums.TrigSweepImmBusExt = driver.source.lffSweep.trigger.source.get_advanced() \n
		No command help available \n
			:return: lf_trig_source_adv: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFFSweep:TRIGger:SOURce:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSweepImmBusExt)

	def set_advanced(self, lf_trig_source_adv: enums.TrigSweepImmBusExt) -> None:
		"""SCPI: [SOURce<HW>]:LFFSweep:TRIGger:SOURce:ADVanced \n
		Snippet: driver.source.lffSweep.trigger.source.set_advanced(lf_trig_source_adv = enums.TrigSweepImmBusExt.BUS) \n
		No command help available \n
			:param lf_trig_source_adv: No help available
		"""
		param = Conversions.enum_scalar_to_str(lf_trig_source_adv, enums.TrigSweepImmBusExt)
		self._core.io.write(f'SOURce<HwInstance>:LFFSweep:TRIGger:SOURce:ADVanced {param}')
