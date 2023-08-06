from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 17 total commands, 8 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	@property
	def alinearize(self):
		"""alinearize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alinearize'):
			from .Alinearize import AlinearizeCls
			self._alinearize = AlinearizeCls(self._core, self._cmd_group)
		return self._alinearize

	@property
	def amplifier(self):
		"""amplifier commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_amplifier'):
			from .Amplifier import AmplifierCls
			self._amplifier = AmplifierCls(self._core, self._cmd_group)
		return self._amplifier

	@property
	def attenuator(self):
		"""attenuator commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_attenuator'):
			from .Attenuator import AttenuatorCls
			self._attenuator = AttenuatorCls(self._core, self._cmd_group)
		return self._attenuator

	@property
	def detAtt(self):
		"""detAtt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_detAtt'):
			from .DetAtt import DetAttCls
			self._detAtt = DetAttCls(self._core, self._cmd_group)
		return self._detAtt

	@property
	def dlinearize(self):
		"""dlinearize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlinearize'):
			from .Dlinearize import DlinearizeCls
			self._dlinearize = DlinearizeCls(self._core, self._cmd_group)
		return self._dlinearize

	@property
	def opu(self):
		"""opu commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_opu'):
			from .Opu import OpuCls
			self._opu = OpuCls(self._core, self._cmd_group)
		return self._opu

	@property
	def swAmplifier(self):
		"""swAmplifier commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swAmplifier'):
			from .SwAmplifier import SwAmplifierCls
			self._swAmplifier = SwAmplifierCls(self._core, self._cmd_group)
		return self._swAmplifier

	@property
	def measure(self):
		"""measure commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_measure'):
			from .Measure import MeasureCls
			self._measure = MeasureCls(self._core, self._cmd_group)
		return self._measure

	# noinspection PyTypeChecker
	def get_bandwidth(self) -> enums.CalPowBandwidth:
		"""SCPI: CALibration:LEVel:BWIDth \n
		Snippet: value: enums.CalPowBandwidth = driver.calibration.level.get_bandwidth() \n
		No command help available \n
			:return: bandwidth: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:BWIDth?')
		return Conversions.str_to_scalar_enum(response, enums.CalPowBandwidth)

	def set_bandwidth(self, bandwidth: enums.CalPowBandwidth) -> None:
		"""SCPI: CALibration:LEVel:BWIDth \n
		Snippet: driver.calibration.level.set_bandwidth(bandwidth = enums.CalPowBandwidth.AUTO) \n
		No command help available \n
			:param bandwidth: No help available
		"""
		param = Conversions.enum_scalar_to_str(bandwidth, enums.CalPowBandwidth)
		self._core.io.write(f'CALibration:LEVel:BWIDth {param}')

	# noinspection PyTypeChecker
	def get_state(self) -> enums.StateExtended:
		"""SCPI: CALibration<HW>:LEVel:STATe \n
		Snippet: value: enums.StateExtended = driver.calibration.level.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:LEVel:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.StateExtended)

	def set_state(self, state: enums.StateExtended) -> None:
		"""SCPI: CALibration<HW>:LEVel:STATe \n
		Snippet: driver.calibration.level.set_state(state = enums.StateExtended._0) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.enum_scalar_to_str(state, enums.StateExtended)
		self._core.io.write(f'CALibration<HwInstance>:LEVel:STATe {param}')

	def clone(self) -> 'LevelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LevelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
