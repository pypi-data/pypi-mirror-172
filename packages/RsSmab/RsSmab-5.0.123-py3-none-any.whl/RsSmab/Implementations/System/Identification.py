from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IdentificationCls:
	"""Identification commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("identification", core, parent)

	def preset(self) -> None:
		"""SCPI: SYSTem:IDENtification:PRESet \n
		Snippet: driver.system.identification.preset() \n
		Sets the *IDN and *OPT strings in user defined mode to default values. \n
		"""
		self._core.io.write(f'SYSTem:IDENtification:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:IDENtification:PRESet \n
		Snippet: driver.system.identification.preset_with_opc() \n
		Sets the *IDN and *OPT strings in user defined mode to default values. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:IDENtification:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_value(self) -> enums.IecDevId:
		"""SCPI: SYSTem:IDENtification \n
		Snippet: value: enums.IecDevId = driver.system.identification.get_value() \n
		Selects the mode to determine the 'IDN String' and the 'OPT String' for the instrument, selected with command method
		RsSmab.System.language. Note: While working in an emulation mode, the R&S SMA100B specific command set is disabled, that
		is, the SCPI command method RsSmab.System.Identification.value is discarded. \n
			:return: identification: AUTO| USER AUTO Automatically determines the strings. USER User-defined strings can be selected.
		"""
		response = self._core.io.query_str('SYSTem:IDENtification?')
		return Conversions.str_to_scalar_enum(response, enums.IecDevId)

	def set_value(self, identification: enums.IecDevId) -> None:
		"""SCPI: SYSTem:IDENtification \n
		Snippet: driver.system.identification.set_value(identification = enums.IecDevId.AUTO) \n
		Selects the mode to determine the 'IDN String' and the 'OPT String' for the instrument, selected with command method
		RsSmab.System.language. Note: While working in an emulation mode, the R&S SMA100B specific command set is disabled, that
		is, the SCPI command method RsSmab.System.Identification.value is discarded. \n
			:param identification: AUTO| USER AUTO Automatically determines the strings. USER User-defined strings can be selected.
		"""
		param = Conversions.enum_scalar_to_str(identification, enums.IecDevId)
		self._core.io.write(f'SYSTem:IDENtification {param}')
