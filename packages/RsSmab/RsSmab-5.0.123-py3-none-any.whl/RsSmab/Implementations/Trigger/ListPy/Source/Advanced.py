from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdvancedCls:
	"""Advanced commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("advanced", core, parent)

	def set(self, start_trig_adv: enums.TrigSweepImmBusExt, inputIx=repcap.InputIx.Default) -> None:
		"""SCPI: TRIGger<HW>:LIST:SOURce:ADVanced \n
		Snippet: driver.trigger.listPy.source.advanced.set(start_trig_adv = enums.TrigSweepImmBusExt.BUS, inputIx = repcap.InputIx.Default) \n
		No command help available \n
			:param start_trig_adv: No help available
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trigger')
		"""
		param = Conversions.enum_scalar_to_str(start_trig_adv, enums.TrigSweepImmBusExt)
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		self._core.io.write(f'TRIGger{inputIx_cmd_val}:LIST:SOURce:ADVanced {param}')

	# noinspection PyTypeChecker
	def get(self, inputIx=repcap.InputIx.Default) -> enums.TrigSweepImmBusExt:
		"""SCPI: TRIGger<HW>:LIST:SOURce:ADVanced \n
		Snippet: value: enums.TrigSweepImmBusExt = driver.trigger.listPy.source.advanced.get(inputIx = repcap.InputIx.Default) \n
		No command help available \n
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trigger')
			:return: start_trig_adv: No help available"""
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		response = self._core.io.query_str(f'TRIGger{inputIx_cmd_val}:LIST:SOURce:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSweepImmBusExt)
