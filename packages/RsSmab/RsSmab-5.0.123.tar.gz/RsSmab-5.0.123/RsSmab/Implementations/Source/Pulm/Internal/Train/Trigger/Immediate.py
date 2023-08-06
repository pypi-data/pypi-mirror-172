from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImmediateCls:
	"""Immediate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("immediate", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce]:PULM:[INTernal]:[TRAin]:TRIGger:IMMediate \n
		Snippet: driver.source.pulm.internal.train.trigger.immediate.set() \n
		If [:SOURce<hw>]:PULM:TRIGger:MODESINGle, triggers the pulse generator. \n
		"""
		self._core.io.write(f'SOURce:PULM:INTernal:TRAin:TRIGger:IMMediate')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce]:PULM:[INTernal]:[TRAin]:TRIGger:IMMediate \n
		Snippet: driver.source.pulm.internal.train.trigger.immediate.set_with_opc() \n
		If [:SOURce<hw>]:PULM:TRIGger:MODESINGle, triggers the pulse generator. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce:PULM:INTernal:TRAin:TRIGger:IMMediate', opc_timeout_ms)
