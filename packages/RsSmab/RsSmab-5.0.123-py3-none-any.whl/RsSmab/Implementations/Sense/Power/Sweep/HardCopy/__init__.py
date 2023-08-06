from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HardCopyCls:
	"""HardCopy commands group definition. 24 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hardCopy", core, parent)

	@property
	def device(self):
		"""device commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_device'):
			from .Device import DeviceCls
			self._device = DeviceCls(self._core, self._cmd_group)
		return self._device

	@property
	def file(self):
		"""file commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	def get_data(self) -> bytes:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DATA \n
		Snippet: value: bytes = driver.sense.power.sweep.hardCopy.get_data() \n
		Queries the measurement data directly. The data is transferred to the remote client as data stream. Readable ASCII data
		is available for hardcopy language CSV. The representation of the values depends on the selected orientation for the CSV
		format. \n
			:return: data: block data
		"""
		response = self._core.io.query_bin_block('SENSe:POWer:SWEep:HCOPy:DATA?')
		return response

	def clone(self) -> 'HardCopyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HardCopyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
