from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	# noinspection PyTypeChecker
	def get_advanced(self) -> enums.TrigSweepImmBusExt:
		"""SCPI: [SOURce<HW>]:LIST:TRIGger:SOURce:ADVanced \n
		Snippet: value: enums.TrigSweepImmBusExt = driver.source.listPy.trigger.source.get_advanced() \n
		No command help available \n
			:return: trig_point_adv: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:TRIGger:SOURce:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSweepImmBusExt)

	def set_advanced(self, trig_point_adv: enums.TrigSweepImmBusExt) -> None:
		"""SCPI: [SOURce<HW>]:LIST:TRIGger:SOURce:ADVanced \n
		Snippet: driver.source.listPy.trigger.source.set_advanced(trig_point_adv = enums.TrigSweepImmBusExt.BUS) \n
		No command help available \n
			:param trig_point_adv: No help available
		"""
		param = Conversions.enum_scalar_to_str(trig_point_adv, enums.TrigSweepImmBusExt)
		self._core.io.write(f'SOURce<HwInstance>:LIST:TRIGger:SOURce:ADVanced {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.TrigSweepSourNoHopExtAuto:
		"""SCPI: [SOURce<HW>]:LIST:TRIGger:SOURce \n
		Snippet: value: enums.TrigSweepSourNoHopExtAuto = driver.source.listPy.trigger.source.get_value() \n
		Selects the trigger source for processing lists. The designation of the parameters correspond to those in sweep mode.
		SCPI standard uses other designations for the parameters, which are also accepted by the instrument. The SCPI designation
		should be used if compatibility is an important consideration. For an overview, see the following table:
			Table Header: Rohde & Schwarz parameter / SCPI parameter / Applies to the list mode parameters: \n
			- AUTO / IMMediate / [:SOURce<hw>]:LIST:MODE AUTO
			- SINGle / BUS / [:SOURce<hw>]:LIST:MODE AUTO or [:SOURce<hw>]:LIST:MODE STEP
			- EXTernal / EXTernal / [:SOURce<hw>]:LIST:MODE AUTO or [:SOURce<hw>]:LIST:MODE STEP \n
			:return: source: AUTO| IMMediate| SINGle| BUS| EXTernal AUTO|IMMediate The trigger is free-running, i.e. the trigger condition is fulfilled continuously. The selected list is restarted as soon as it is finished. SINGle|BUS The list is triggered by the command [:SOURcehw]:LIST:TRIGger:EXECute. The list is executed once. EXTernal The list is triggered externally and executed once.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSweepSourNoHopExtAuto)

	def set_value(self, source: enums.TrigSweepSourNoHopExtAuto) -> None:
		"""SCPI: [SOURce<HW>]:LIST:TRIGger:SOURce \n
		Snippet: driver.source.listPy.trigger.source.set_value(source = enums.TrigSweepSourNoHopExtAuto.AUTO) \n
		Selects the trigger source for processing lists. The designation of the parameters correspond to those in sweep mode.
		SCPI standard uses other designations for the parameters, which are also accepted by the instrument. The SCPI designation
		should be used if compatibility is an important consideration. For an overview, see the following table:
			Table Header: Rohde & Schwarz parameter / SCPI parameter / Applies to the list mode parameters: \n
			- AUTO / IMMediate / [:SOURce<hw>]:LIST:MODE AUTO
			- SINGle / BUS / [:SOURce<hw>]:LIST:MODE AUTO or [:SOURce<hw>]:LIST:MODE STEP
			- EXTernal / EXTernal / [:SOURce<hw>]:LIST:MODE AUTO or [:SOURce<hw>]:LIST:MODE STEP \n
			:param source: AUTO| IMMediate| SINGle| BUS| EXTernal AUTO|IMMediate The trigger is free-running, i.e. the trigger condition is fulfilled continuously. The selected list is restarted as soon as it is finished. SINGle|BUS The list is triggered by the command [:SOURcehw]:LIST:TRIGger:EXECute. The list is executed once. EXTernal The list is triggered externally and executed once.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.TrigSweepSourNoHopExtAuto)
		self._core.io.write(f'SOURce<HwInstance>:LIST:TRIGger:SOURce {param}')
