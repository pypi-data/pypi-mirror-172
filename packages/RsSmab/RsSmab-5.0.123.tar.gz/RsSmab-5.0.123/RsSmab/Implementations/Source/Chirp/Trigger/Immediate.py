from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImmediateCls:
	"""Immediate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("immediate", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:TRIGger:IMMediate \n
		Snippet: driver.source.chirp.trigger.immediate.set() \n
		Immediately starts the chirp signal generation. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:TRIGger:IMMediate')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:TRIGger:IMMediate \n
		Snippet: driver.source.chirp.trigger.immediate.set_with_opc() \n
		Immediately starts the chirp signal generation. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CHIRp:TRIGger:IMMediate', opc_timeout_ms)
