from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SweepCls:
	"""Sweep commands group definition. 36 total commands, 4 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sweep", core, parent)

	@property
	def combined(self):
		"""combined commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_combined'):
			from .Combined import CombinedCls
			self._combined = CombinedCls(self._core, self._cmd_group)
		return self._combined

	@property
	def marker(self):
		"""marker commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	@property
	def power(self):
		"""power commands group. 4 Sub-classes, 6 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def frequency(self):
		"""frequency commands group. 5 Sub-classes, 7 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	# noinspection PyTypeChecker
	def get_generation(self) -> enums.FreqSweepType:
		"""SCPI: [SOURce<HW>]:SWEep:GENeration \n
		Snippet: value: enums.FreqSweepType = driver.source.sweep.get_generation() \n
		Selects frequency sweep type. \n
			:return: sweep_type: STEPped| ANALog STEPped Performs a frequency sweep. ANALog Performs a continuous analog frequency sweep (ramp) , synchronized with the sweep time [:SOURcehw]:SWEep[:FREQuency]:TIME.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:GENeration?')
		return Conversions.str_to_scalar_enum(response, enums.FreqSweepType)

	def set_generation(self, sweep_type: enums.FreqSweepType) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:GENeration \n
		Snippet: driver.source.sweep.set_generation(sweep_type = enums.FreqSweepType.ANALog) \n
		Selects frequency sweep type. \n
			:param sweep_type: STEPped| ANALog STEPped Performs a frequency sweep. ANALog Performs a continuous analog frequency sweep (ramp) , synchronized with the sweep time [:SOURcehw]:SWEep[:FREQuency]:TIME.
		"""
		param = Conversions.enum_scalar_to_str(sweep_type, enums.FreqSweepType)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:GENeration {param}')

	def reset_all(self) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:RESet:[ALL] \n
		Snippet: driver.source.sweep.reset_all() \n
		Resets all active sweeps to the starting point. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:SWEep:RESet:ALL')

	def reset_all_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:RESet:[ALL] \n
		Snippet: driver.source.sweep.reset_all_with_opc() \n
		Resets all active sweeps to the starting point. \n
		Same as reset_all, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:SWEep:RESet:ALL', opc_timeout_ms)

	def clone(self) -> 'SweepCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SweepCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
