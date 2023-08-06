from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ProtectionCls:
	"""Protection commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("protection", core, parent)

	def clear(self) -> None:
		"""SCPI: OUTPut<HW>:PROTection:CLEar \n
		Snippet: driver.output.protection.clear() \n
		Resets the protective circuit after it has been tripped. To define the output state, use the command method RsSmab.Output.
		State.value. \n
		"""
		self._core.io.write(f'OUTPut<HwInstance>:PROTection:CLEar')

	def clear_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: OUTPut<HW>:PROTection:CLEar \n
		Snippet: driver.output.protection.clear_with_opc() \n
		Resets the protective circuit after it has been tripped. To define the output state, use the command method RsSmab.Output.
		State.value. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'OUTPut<HwInstance>:PROTection:CLEar', opc_timeout_ms)

	def get_tripped(self) -> bool:
		"""SCPI: OUTPut<HW>:PROTection:TRIPped \n
		Snippet: value: bool = driver.output.protection.get_tripped() \n
		Queries the state of the protective circuit. \n
			:return: tripped: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:PROTection:TRIPped?')
		return Conversions.str_to_bool(response)
