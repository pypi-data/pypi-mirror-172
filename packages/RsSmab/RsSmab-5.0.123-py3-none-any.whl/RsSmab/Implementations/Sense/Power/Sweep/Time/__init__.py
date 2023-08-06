from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 30 total commands, 5 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_average'):
			from .Average import AverageCls
			self._average = AverageCls(self._core, self._cmd_group)
		return self._average

	@property
	def reference(self):
		"""reference commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import ReferenceCls
			self._reference = ReferenceCls(self._core, self._cmd_group)
		return self._reference

	@property
	def spacing(self):
		"""spacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spacing'):
			from .Spacing import SpacingCls
			self._spacing = SpacingCls(self._core, self._cmd_group)
		return self._spacing

	@property
	def yscale(self):
		"""yscale commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_yscale'):
			from .Yscale import YscaleCls
			self._yscale = YscaleCls(self._core, self._cmd_group)
		return self._yscale

	@property
	def sensor(self):
		"""sensor commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sensor'):
			from .Sensor import SensorCls
			self._sensor = SensorCls(self._core, self._cmd_group)
		return self._sensor

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.RepeatMode:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:RMODe \n
		Snippet: value: enums.RepeatMode = driver.sense.power.sweep.time.get_rmode() \n
		Selects single or continuous mode for measurement mode time in power analysis. \n
			:return: rmode: SINGle| CONTinuous
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.RepeatMode)

	def set_rmode(self, rmode: enums.RepeatMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:RMODe \n
		Snippet: driver.sense.power.sweep.time.set_rmode(rmode = enums.RepeatMode.CONTinuous) \n
		Selects single or continuous mode for measurement mode time in power analysis. \n
			:param rmode: SINGle| CONTinuous
		"""
		param = Conversions.enum_scalar_to_str(rmode, enums.RepeatMode)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:RMODe {param}')

	def get_start(self) -> float:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:STARt \n
		Snippet: value: float = driver.sense.power.sweep.time.get_start() \n
		Sets the start time for the power versus time measurement. Value 0 defines the trigger point. By choosing a negative time
		value, the trace can be shifted in the diagram. It is possible, that the measurement cannot be performed over the
		complete time range because of limitations due to sensor settings. In this case, an error message is output. \n
			:return: start: float Range: -1 to 1
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start: float) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:STARt \n
		Snippet: driver.sense.power.sweep.time.set_start(start = 1.0) \n
		Sets the start time for the power versus time measurement. Value 0 defines the trigger point. By choosing a negative time
		value, the trace can be shifted in the diagram. It is possible, that the measurement cannot be performed over the
		complete time range because of limitations due to sensor settings. In this case, an error message is output. \n
			:param start: float Range: -1 to 1
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:STARt {param}')

	def get_steps(self) -> int:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:STEPs \n
		Snippet: value: int = driver.sense.power.sweep.time.get_steps() \n
		Sets the number of measurement steps for the power versus time measurement. Value 0 defines the trigger point. \n
			:return: steps: integer Range: 10 to 1000
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:STEPs?')
		return Conversions.str_to_int(response)

	def set_steps(self, steps: int) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:STEPs \n
		Snippet: driver.sense.power.sweep.time.set_steps(steps = 1) \n
		Sets the number of measurement steps for the power versus time measurement. Value 0 defines the trigger point. \n
			:param steps: integer Range: 10 to 1000
		"""
		param = Conversions.decimal_value_to_str(steps)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:STEPs {param}')

	def get_stop(self) -> float:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:STOP \n
		Snippet: value: float = driver.sense.power.sweep.time.get_stop() \n
		Sets the stop time for the power versus time measurement. \n
			:return: stop: float Range: 0 to 2
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, stop: float) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:STOP \n
		Snippet: driver.sense.power.sweep.time.set_stop(stop = 1.0) \n
		Sets the stop time for the power versus time measurement. \n
			:param stop: float Range: 0 to 2
		"""
		param = Conversions.decimal_value_to_str(stop)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:STOP {param}')

	# noinspection PyTypeChecker
	def get_tevents(self) -> enums.MeasRespYsCaleEvents:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:TEVents \n
		Snippet: value: enums.MeasRespYsCaleEvents = driver.sense.power.sweep.time.get_tevents() \n
		Determines, whether the measurement data processing starts with a trigger event in one of the sensors (Logical OR) , or
		whether all channels have to be triggered (logical AND) . Each sensor evaluates a trigger event according to its setting
		independently. This function supports the internal or external trigger modes with multi-channel time measurements. \n
			:return: trigger_tevents: AND| OR
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:TEVents?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespYsCaleEvents)

	def set_tevents(self, trigger_tevents: enums.MeasRespYsCaleEvents) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:TEVents \n
		Snippet: driver.sense.power.sweep.time.set_tevents(trigger_tevents = enums.MeasRespYsCaleEvents.AND) \n
		Determines, whether the measurement data processing starts with a trigger event in one of the sensors (Logical OR) , or
		whether all channels have to be triggered (logical AND) . Each sensor evaluates a trigger event according to its setting
		independently. This function supports the internal or external trigger modes with multi-channel time measurements. \n
			:param trigger_tevents: AND| OR
		"""
		param = Conversions.enum_scalar_to_str(trigger_tevents, enums.MeasRespYsCaleEvents)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:TEVents {param}')

	def clone(self) -> 'TimeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TimeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
