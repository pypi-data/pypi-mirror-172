from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)

	@property
	def immediate(self):
		"""immediate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_immediate'):
			from .Immediate import ImmediateCls
			self._immediate = ImmediateCls(self._core, self._cmd_group)
		return self._immediate

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PulsTrigModeWithSingle:
		"""SCPI: [SOURce<HW>]:CHIRp:TRIGger:MODE \n
		Snippet: value: enums.PulsTrigModeWithSingle = driver.source.chirp.trigger.get_mode() \n
		Selects the trigger mode for the chirp modulation signal. \n
			:return: mode: AUTO| EXTernal| EGATe| SINGle| ESINgle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:TRIGger:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PulsTrigModeWithSingle)

	def set_mode(self, mode: enums.PulsTrigModeWithSingle) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:TRIGger:MODE \n
		Snippet: driver.source.chirp.trigger.set_mode(mode = enums.PulsTrigModeWithSingle.AUTO) \n
		Selects the trigger mode for the chirp modulation signal. \n
			:param mode: AUTO| EXTernal| EGATe| SINGle| ESINgle
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PulsTrigModeWithSingle)
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:TRIGger:MODE {param}')

	def clone(self) -> 'TriggerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TriggerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
