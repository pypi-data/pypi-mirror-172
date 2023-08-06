from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 11 total commands, 4 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def spacing(self):
		"""spacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spacing'):
			from .Spacing import SpacingCls
			self._spacing = SpacingCls(self._core, self._cmd_group)
		return self._spacing

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_step'):
			from .Step import StepCls
			self._step = StepCls(self._core, self._cmd_group)
		return self._step

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.PowAttMode:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:AMODe \n
		Snippet: value: enums.PowAttMode = driver.source.sweep.power.get_amode() \n
		No command help available \n
			:return: amode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.PowAttMode)

	def set_amode(self, amode: enums.PowAttMode) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:AMODe \n
		Snippet: driver.source.sweep.power.set_amode(amode = enums.PowAttMode.AUTO) \n
		No command help available \n
			:param amode: No help available
		"""
		param = Conversions.enum_scalar_to_str(amode, enums.PowAttMode)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:AMODe {param}')

	def get_dwell(self) -> float:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:DWELl \n
		Snippet: value: float = driver.source.sweep.power.get_dwell() \n
		Sets the dwell time for a level sweep step. \n
			:return: dwell: float Range: 0.001 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:DWELl?')
		return Conversions.str_to_float(response)

	def set_dwell(self, dwell: float) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:DWELl \n
		Snippet: driver.source.sweep.power.set_dwell(dwell = 1.0) \n
		Sets the dwell time for a level sweep step. \n
			:param dwell: float Range: 0.001 to 100
		"""
		param = Conversions.decimal_value_to_str(dwell)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:DWELl {param}')

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:POINts \n
		Snippet: value: int = driver.source.sweep.power.get_points() \n
		Sets the number of steps within the RF level sweep range. See 'Correlating parameters in sweep mode'. \n
			:return: points: integer Range: 2 to Max
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:POINts?')
		return Conversions.str_to_int(response)

	def set_points(self, points: int) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:POINts \n
		Snippet: driver.source.sweep.power.set_points(points = 1) \n
		Sets the number of steps within the RF level sweep range. See 'Correlating parameters in sweep mode'. \n
			:param points: integer Range: 2 to Max
		"""
		param = Conversions.decimal_value_to_str(points)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:POINts {param}')

	def get_retrace(self) -> bool:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:RETRace \n
		Snippet: value: bool = driver.source.sweep.power.get_retrace() \n
		Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. You can
		enable this feature, when you are working with sawtooth shapes in sweep mode 'Single' or 'External Single'. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:RETRace?')
		return Conversions.str_to_bool(response)

	def set_retrace(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:RETRace \n
		Snippet: driver.source.sweep.power.set_retrace(state = False) \n
		Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. You can
		enable this feature, when you are working with sawtooth shapes in sweep mode 'Single' or 'External Single'. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:RETRace {param}')

	def get_running(self) -> bool:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:RUNNing \n
		Snippet: value: bool = driver.source.sweep.power.get_running() \n
		Queries the current sweep state. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:RUNNing?')
		return Conversions.str_to_bool(response)

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.SweCyclMode:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:SHAPe \n
		Snippet: value: enums.SweCyclMode = driver.source.sweep.power.get_shape() \n
		Determines the waveform shape for a frequency sweep sequence. \n
			:return: shape: SAWTooth| TRIangle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.SweCyclMode)

	def set_shape(self, shape: enums.SweCyclMode) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:POWer:SHAPe \n
		Snippet: driver.source.sweep.power.set_shape(shape = enums.SweCyclMode.SAWTooth) \n
		Determines the waveform shape for a frequency sweep sequence. \n
			:param shape: SAWTooth| TRIangle
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.SweCyclMode)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:SHAPe {param}')

	def clone(self) -> 'PowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
