from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IlsCls:
	"""Ils commands group definition. 96 total commands, 5 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ils", core, parent)

	@property
	def gs(self):
		"""gs commands group. 5 Sub-classes, 6 commands."""
		if not hasattr(self, '_gs'):
			from .Gs import GsCls
			self._gs = GsCls(self._core, self._cmd_group)
		return self._gs

	@property
	def gslope(self):
		"""gslope commands group. 5 Sub-classes, 6 commands."""
		if not hasattr(self, '_gslope'):
			from .Gslope import GslopeCls
			self._gslope = GslopeCls(self._core, self._cmd_group)
		return self._gslope

	@property
	def localizer(self):
		"""localizer commands group. 6 Sub-classes, 6 commands."""
		if not hasattr(self, '_localizer'):
			from .Localizer import LocalizerCls
			self._localizer = LocalizerCls(self._core, self._cmd_group)
		return self._localizer

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def mbeacon(self):
		"""mbeacon commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_mbeacon'):
			from .Mbeacon import MbeaconCls
			self._mbeacon = MbeaconCls(self._core, self._cmd_group)
		return self._mbeacon

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:ILS:PRESet \n
		Snippet: driver.source.ils.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:VOR:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:ILS:PRESet \n
		Snippet: driver.source.ils.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:VOR:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:PRESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:ILS:STATe \n
		Snippet: value: bool = driver.source.ils.get_state() \n
		Activates/deactivates the VOR modulation. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:ILS:STATe \n
		Snippet: driver.source.ils.set_state(state = False) \n
		Activates/deactivates the VOR modulation. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ILS:STATe {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.AvionicIlsType:
		"""SCPI: [SOURce<HW>]:ILS:TYPE \n
		Snippet: value: enums.AvionicIlsType = driver.source.ils.get_type_py() \n
		Selects the ILS modulation type. \n
			:return: type_py: GS| LOCalize| GSLope| MBEacon
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsType)

	def set_type_py(self, type_py: enums.AvionicIlsType) -> None:
		"""SCPI: [SOURce<HW>]:ILS:TYPE \n
		Snippet: driver.source.ils.set_type_py(type_py = enums.AvionicIlsType.GS) \n
		Selects the ILS modulation type. \n
			:param type_py: GS| LOCalize| GSLope| MBEacon
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.AvionicIlsType)
		self._core.io.write(f'SOURce<HwInstance>:ILS:TYPE {param}')

	def clone(self) -> 'IlsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IlsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
