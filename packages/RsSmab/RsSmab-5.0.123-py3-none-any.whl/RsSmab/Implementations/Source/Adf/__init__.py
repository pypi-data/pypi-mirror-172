from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdfCls:
	"""Adf commands group definition. 16 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("adf", core, parent)

	@property
	def comid(self):
		"""comid commands group. 0 Sub-classes, 10 commands."""
		if not hasattr(self, '_comid'):
			from .Comid import ComidCls
			self._comid = ComidCls(self._core, self._cmd_group)
		return self._comid

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:ADF:PRESet \n
		Snippet: driver.source.adf.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:VOR:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ADF:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:ADF:PRESet \n
		Snippet: driver.source.adf.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:VOR:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ADF:PRESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:ADF:STATe \n
		Snippet: value: bool = driver.source.adf.get_state() \n
		Activates/deactivates the VOR modulation. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:ADF:STATe \n
		Snippet: driver.source.adf.set_state(state = False) \n
		Activates/deactivates the VOR modulation. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ADF:STATe {param}')

	def clone(self) -> 'AdfCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AdfCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
