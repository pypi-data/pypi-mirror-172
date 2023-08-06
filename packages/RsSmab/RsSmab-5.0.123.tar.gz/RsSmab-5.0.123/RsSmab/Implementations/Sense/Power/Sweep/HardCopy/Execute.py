from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExecuteCls:
	"""Execute commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:[EXECute] \n
		Snippet: driver.sense.power.sweep.hardCopy.execute.set() \n
		Triggers the generation of a hardcopy of the current measurement diagram. The data is written into the file
		selected/created with the method RsSmab.Sense.Power.Sweep.HardCopy.File.Name.value command. \n
		"""
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:EXECute')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:[EXECute] \n
		Snippet: driver.sense.power.sweep.hardCopy.execute.set_with_opc() \n
		Triggers the generation of a hardcopy of the current measurement diagram. The data is written into the file
		selected/created with the method RsSmab.Sense.Power.Sweep.HardCopy.File.Name.value command. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SENSe:POWer:SWEep:HCOPy:EXECute', opc_timeout_ms)
