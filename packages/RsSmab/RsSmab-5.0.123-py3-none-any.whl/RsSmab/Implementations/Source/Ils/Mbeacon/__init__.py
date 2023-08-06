from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MbeaconCls:
	"""Mbeacon commands group definition. 17 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mbeacon", core, parent)

	@property
	def comid(self):
		"""comid commands group. 1 Sub-classes, 9 commands."""
		if not hasattr(self, '_comid'):
			from .Comid import ComidCls
			self._comid = ComidCls(self._core, self._cmd_group)
		return self._comid

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:PRESet \n
		Snippet: driver.source.ils.mbeacon.preset() \n
		Sets the parameters of the ILS marker beacons component to their default values (*RST values specified for the commands) .
		For other ILS preset commands, see [:SOURce<hw>]:ILS:PRESet. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:PRESet \n
		Snippet: driver.source.ils.mbeacon.preset_with_opc() \n
		Sets the parameters of the ILS marker beacons component to their default values (*RST values specified for the commands) .
		For other ILS preset commands, see [:SOURce<hw>]:ILS:PRESet. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:MBEacon:PRESet', opc_timeout_ms)

	def clone(self) -> 'MbeaconCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MbeaconCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
