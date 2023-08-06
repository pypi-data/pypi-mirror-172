from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TemporaryCls:
	"""Temporary commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("temporary", core, parent)

	def delete(self) -> None:
		"""SCPI: SYSTem:FILes:TEMPorary:DELete \n
		Snippet: driver.system.files.temporary.delete() \n
		Deletes the temporary files from the internal memory or, if installed, from the SD card slot. \n
		"""
		self._core.io.write(f'SYSTem:FILes:TEMPorary:DELete')

	def delete_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:FILes:TEMPorary:DELete \n
		Snippet: driver.system.files.temporary.delete_with_opc() \n
		Deletes the temporary files from the internal memory or, if installed, from the SD card slot. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:FILes:TEMPorary:DELete', opc_timeout_ms)
