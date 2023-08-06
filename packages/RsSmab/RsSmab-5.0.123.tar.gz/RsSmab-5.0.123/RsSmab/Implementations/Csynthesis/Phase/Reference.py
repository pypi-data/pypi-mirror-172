from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReferenceCls:
	"""Reference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)

	def set(self) -> None:
		"""SCPI: CSYNthesis:PHASe:REFerence \n
		Snippet: driver.csynthesis.phase.reference.set() \n
		Resets the delta phase value. \n
		"""
		self._core.io.write(f'CSYNthesis:PHASe:REFerence')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CSYNthesis:PHASe:REFerence \n
		Snippet: driver.csynthesis.phase.reference.set_with_opc() \n
		Resets the delta phase value. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CSYNthesis:PHASe:REFerence', opc_timeout_ms)
