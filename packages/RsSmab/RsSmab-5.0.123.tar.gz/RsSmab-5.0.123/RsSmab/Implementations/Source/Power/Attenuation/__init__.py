from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AttenuationCls:
	"""Attenuation commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attenuation", core, parent)

	@property
	def rfOff(self):
		"""rfOff commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfOff'):
			from .RfOff import RfOffCls
			self._rfOff = RfOffCls(self._core, self._cmd_group)
		return self._rfOff

	def get_max_level(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:MAXLevel \n
		Snippet: value: float = driver.source.power.attenuation.get_max_level() \n
		No command help available \n
			:return: level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ATTenuation:MAXLevel?')
		return Conversions.str_to_float(response)

	def set_max_level(self, level: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:MAXLevel \n
		Snippet: driver.source.power.attenuation.set_max_level(level = 1.0) \n
		No command help available \n
			:param level: No help available
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ATTenuation:MAXLevel {param}')

	# noinspection PyTypeChecker
	def get_pattenuator(self) -> enums.PowAttStepArt:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:PATTenuator \n
		Snippet: value: enums.PowAttStepArt = driver.source.power.attenuation.get_pattenuator() \n
		Selects the type of step attenuator used below 20 GHz. \n
			:return: step_att_sel: MECHanical| ELECtronic MECHanical Uses the mechanical step attenuator at all frequencies. ELECtronic Uses the electronic step attenuator up to 20 GHz.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ATTenuation:PATTenuator?')
		return Conversions.str_to_scalar_enum(response, enums.PowAttStepArt)

	def set_pattenuator(self, step_att_sel: enums.PowAttStepArt) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:PATTenuator \n
		Snippet: driver.source.power.attenuation.set_pattenuator(step_att_sel = enums.PowAttStepArt.ELECtronic) \n
		Selects the type of step attenuator used below 20 GHz. \n
			:param step_att_sel: MECHanical| ELECtronic MECHanical Uses the mechanical step attenuator at all frequencies. ELECtronic Uses the electronic step attenuator up to 20 GHz.
		"""
		param = Conversions.enum_scalar_to_str(step_att_sel, enums.PowAttStepArt)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ATTenuation:PATTenuator {param}')

	def get_stage(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:STAGe \n
		Snippet: value: float = driver.source.power.attenuation.get_stage() \n
		No command help available \n
			:return: stage: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ATTenuation:STAGe?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'AttenuationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AttenuationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
