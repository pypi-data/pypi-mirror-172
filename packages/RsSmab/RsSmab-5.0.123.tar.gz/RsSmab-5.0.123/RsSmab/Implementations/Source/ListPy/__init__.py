from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPyCls:
	"""ListPy commands group definition. 34 total commands, 8 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("listPy", core, parent)

	@property
	def dexchange(self):
		"""dexchange commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_dexchange'):
			from .Dexchange import DexchangeCls
			self._dexchange = DexchangeCls(self._core, self._cmd_group)
		return self._dexchange

	@property
	def dwell(self):
		"""dwell commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_dwell'):
			from .Dwell import DwellCls
			self._dwell = DwellCls(self._core, self._cmd_group)
		return self._dwell

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_index'):
			from .Index import IndexCls
			self._index = IndexCls(self._core, self._cmd_group)
		return self._index

	@property
	def learn(self):
		"""learn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_learn'):
			from .Learn import LearnCls
			self._learn = LearnCls(self._core, self._cmd_group)
		return self._learn

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def trigger(self):
		"""trigger commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:LIST:CATalog \n
		Snippet: value: List[str] = driver.source.listPy.get_catalog() \n
		Queries the available list files in the specified directory. \n
			:return: catalog: string List of list filenames, separated by commas
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:LIST:DELete \n
		Snippet: driver.source.listPy.delete(filename = '1') \n
		Deletes the specified list. Refer to 'Accessing files in the default or in a specified directory' for general information
		on file handling in the default and in a specific directory. \n
			:param filename: string Filename or complete file path; file extension is optional.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:LIST:DELete {param}')

	def delete_all(self) -> None:
		"""SCPI: [SOURce<HW>]:LIST:DELete:ALL \n
		Snippet: driver.source.listPy.delete_all() \n
		Deletes all lists in the set directory.
			INTRO_CMD_HELP: This command can only be executed, if: \n
			- No list file is selected.
			- List mode is disabled. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:LIST:DELete:ALL')

	def delete_all_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:LIST:DELete:ALL \n
		Snippet: driver.source.listPy.delete_all_with_opc() \n
		Deletes all lists in the set directory.
			INTRO_CMD_HELP: This command can only be executed, if: \n
			- No list file is selected.
			- List mode is disabled. \n
		Same as delete_all, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:LIST:DELete:ALL', opc_timeout_ms)

	def get_free(self) -> int:
		"""SCPI: [SOURce<HW>]:LIST:FREE \n
		Snippet: value: int = driver.source.listPy.get_free() \n
		Queries the amount of free memory (in bytes) for list mode lists. \n
			:return: free: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:FREE?')
		return Conversions.str_to_int(response)

	def reset(self) -> None:
		"""SCPI: [SOURce<HW>]:LIST:RESet \n
		Snippet: driver.source.listPy.reset() \n
		Jumps to the beginning of the list. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:LIST:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:LIST:RESet \n
		Snippet: driver.source.listPy.reset_with_opc() \n
		Jumps to the beginning of the list. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:LIST:RESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.LmodRunMode:
		"""SCPI: [SOURce<HW>]:LIST:RMODe \n
		Snippet: value: enums.LmodRunMode = driver.source.listPy.get_rmode() \n
		No command help available \n
			:return: rmode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.LmodRunMode)

	def set_rmode(self, rmode: enums.LmodRunMode) -> None:
		"""SCPI: [SOURce<HW>]:LIST:RMODe \n
		Snippet: driver.source.listPy.set_rmode(rmode = enums.LmodRunMode.LEARned) \n
		No command help available \n
			:param rmode: No help available
		"""
		param = Conversions.enum_scalar_to_str(rmode, enums.LmodRunMode)
		self._core.io.write(f'SOURce<HwInstance>:LIST:RMODe {param}')

	def get_running(self) -> bool:
		"""SCPI: [SOURce<HW>]:LIST:RUNNing \n
		Snippet: value: bool = driver.source.listPy.get_running() \n
		Queries the current state of the list mode. \n
			:return: state: 1| ON| 0| OFF 1 Signal generation based on the list mode is active.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:RUNNing?')
		return Conversions.str_to_bool(response)

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:LIST:SELect \n
		Snippet: value: str = driver.source.listPy.get_select() \n
		Selects or creates a data list in list mode. If the list with the selected name does not exist, a new list is created. \n
			:return: filename: string Filename or complete file path; file extension can be omitted.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:LIST:SELect \n
		Snippet: driver.source.listPy.set_select(filename = '1') \n
		Selects or creates a data list in list mode. If the list with the selected name does not exist, a new list is created. \n
			:param filename: string Filename or complete file path; file extension can be omitted.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:LIST:SELect {param}')

	def clone(self) -> 'ListPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ListPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
