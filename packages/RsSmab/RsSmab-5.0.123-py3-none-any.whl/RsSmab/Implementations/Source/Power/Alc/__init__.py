from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlcCls:
	"""Alc commands group definition. 8 total commands, 2 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alc", core, parent)

	@property
	def edetector(self):
		"""edetector commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_edetector'):
			from .Edetector import EdetectorCls
			self._edetector = EdetectorCls(self._core, self._cmd_group)
		return self._edetector

	@property
	def sonce(self):
		"""sonce commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sonce'):
			from .Sonce import SonceCls
			self._sonce = SonceCls(self._core, self._cmd_group)
		return self._sonce

	# noinspection PyTypeChecker
	def get_dsensitivity(self) -> enums.PowAlcDetSensitivity:
		"""SCPI: [SOURce<HW>]:POWer:ALC:DSENsitivity \n
		Snippet: value: enums.PowAlcDetSensitivity = driver.source.power.alc.get_dsensitivity() \n
		Sets the sensitivity of the ALC detector. \n
			:return: sensitivity: AUTO| FIXed AUTO Selects the optimum sensitivity automatically. FIXed Fixes the internal level detector.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:DSENsitivity?')
		return Conversions.str_to_scalar_enum(response, enums.PowAlcDetSensitivity)

	def set_dsensitivity(self, sensitivity: enums.PowAlcDetSensitivity) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:DSENsitivity \n
		Snippet: driver.source.power.alc.set_dsensitivity(sensitivity = enums.PowAlcDetSensitivity.AUTO) \n
		Sets the sensitivity of the ALC detector. \n
			:param sensitivity: AUTO| FIXed AUTO Selects the optimum sensitivity automatically. FIXed Fixes the internal level detector.
		"""
		param = Conversions.enum_scalar_to_str(sensitivity, enums.PowAlcDetSensitivity)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:DSENsitivity {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AlcOnOffAuto:
		"""SCPI: [SOURce<HW>]:POWer:ALC:MODE \n
		Snippet: value: enums.AlcOnOffAuto = driver.source.power.alc.get_mode() \n
		Queries the currently set ALC mode. See [:SOURce<hw>]:POWer:ALC[:STATe]. \n
			:return: pow_alc_mode: 0| AUTO| 1| PRESet| OFFTable| ON| OFF| ONSample| ONTable
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AlcOnOffAuto)

	# noinspection PyTypeChecker
	def get_omode(self) -> enums.AlcOffMode:
		"""SCPI: [SOURce<HW>]:POWer:ALC:OMODe \n
		Snippet: value: enums.AlcOffMode = driver.source.power.alc.get_omode() \n
		No command help available \n
			:return: off_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:OMODe?')
		return Conversions.str_to_scalar_enum(response, enums.AlcOffMode)

	def set_omode(self, off_mode: enums.AlcOffMode) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:OMODe \n
		Snippet: driver.source.power.alc.set_omode(off_mode = enums.AlcOffMode.SHOLd) \n
		No command help available \n
			:param off_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(off_mode, enums.AlcOffMode)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:OMODe {param}')

	def get_search(self) -> bool:
		"""SCPI: [SOURce<HW>]:POWer:ALC:SEARch \n
		Snippet: value: bool = driver.source.power.alc.get_search() \n
		No command help available \n
			:return: search: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:SEARch?')
		return Conversions.str_to_bool(response)

	def set_search(self, search: bool) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:SEARch \n
		Snippet: driver.source.power.alc.set_search(search = False) \n
		No command help available \n
			:param search: No help available
		"""
		param = Conversions.bool_to_str(search)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:SEARch {param}')

	# noinspection PyTypeChecker
	def get_state(self) -> enums.PowAlcStateWithExtAlc:
		"""SCPI: [SOURce<HW>]:POWer:ALC:[STATe] \n
		Snippet: value: enums.PowAlcStateWithExtAlc = driver.source.power.alc.get_state() \n
		No command help available \n
			:return: state: 0| OFF| AUTO| 1| ON| ONTable| PRESet| OFFTable | EALC AUTO Adjusts the output level to the operating conditions automatically. 1|ON Activates internal level control permanently. OFFTable Controls the level using attenuation values of the internal ALC table. 0|OFF Provided only for backward compatibility with other Rohde & Schwarz signal generators. The R&S SMA100B accepts these values and maps them automatically as follows: 0|OFF = OFFTable ONTable Starts with the attenuation setting from the table and continues with automatic level control. EALC Activates external ALC mode.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.PowAlcStateWithExtAlc)

	def set_state(self, state: enums.PowAlcStateWithExtAlc) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:[STATe] \n
		Snippet: driver.source.power.alc.set_state(state = enums.PowAlcStateWithExtAlc._0) \n
		No command help available \n
			:param state: 0| OFF| AUTO| 1| ON| ONTable| PRESet| OFFTable | EALC AUTO Adjusts the output level to the operating conditions automatically. 1|ON Activates internal level control permanently. OFFTable Controls the level using attenuation values of the internal ALC table. 0|OFF Provided only for backward compatibility with other Rohde & Schwarz signal generators. The R&S SMA100B accepts these values and maps them automatically as follows: 0|OFF = OFFTable ONTable Starts with the attenuation setting from the table and continues with automatic level control. EALC Activates external ALC mode.
		"""
		param = Conversions.enum_scalar_to_str(state, enums.PowAlcStateWithExtAlc)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:STATe {param}')

	def clone(self) -> 'AlcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AlcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
