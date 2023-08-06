from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DirectoryCls:
	"""Directory commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("directory", core, parent)

	def clear(self) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:DIRectory:CLEar \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.auto.directory.clear() \n
		Deletes all files with extensions bmp , img, png, xpm and csv in the directory set for automatic naming. \n
		"""
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:DIRectory:CLEar')

	def clear_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:DIRectory:CLEar \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.auto.directory.clear_with_opc() \n
		Deletes all files with extensions bmp , img, png, xpm and csv in the directory set for automatic naming. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:DIRectory:CLEar', opc_timeout_ms)

	def get_value(self) -> str:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:DIRectory \n
		Snippet: value: str = driver.sense.power.sweep.hardCopy.file.name.auto.directory.get_value() \n
		Defines the directory into which the hardcopy files are stored if auto naming is activated (SENS:SWE:HCOP:FILE:AUTO:STAT
		ON) . \n
			:return: directory: string
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:DIRectory?')
		return trim_str_response(response)

	def set_value(self, directory: str) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:DIRectory \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.auto.directory.set_value(directory = '1') \n
		Defines the directory into which the hardcopy files are stored if auto naming is activated (SENS:SWE:HCOP:FILE:AUTO:STAT
		ON) . \n
			:param directory: string
		"""
		param = Conversions.value_to_quoted_str(directory)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:DIRectory {param}')
