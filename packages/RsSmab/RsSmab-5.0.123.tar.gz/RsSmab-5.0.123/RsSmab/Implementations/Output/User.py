from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	# noinspection PyTypeChecker
	def get_marker(self) -> enums.SelOutpMarkUser:
		"""SCPI: OUTPut:USER:MARKer \n
		Snippet: value: enums.SelOutpMarkUser = driver.output.user.get_marker() \n
		Selects the signal for output at the Marker User1 connector. \n
			:return: sel_user_marker: MARK| USER MARK Assigns a marker signal to the output. USER Intended for future use.
		"""
		response = self._core.io.query_str('OUTPut:USER:MARKer?')
		return Conversions.str_to_scalar_enum(response, enums.SelOutpMarkUser)

	def set_marker(self, sel_user_marker: enums.SelOutpMarkUser) -> None:
		"""SCPI: OUTPut:USER:MARKer \n
		Snippet: driver.output.user.set_marker(sel_user_marker = enums.SelOutpMarkUser.MARK) \n
		Selects the signal for output at the Marker User1 connector. \n
			:param sel_user_marker: MARK| USER MARK Assigns a marker signal to the output. USER Intended for future use.
		"""
		param = Conversions.enum_scalar_to_str(sel_user_marker, enums.SelOutpMarkUser)
		self._core.io.write(f'OUTPut:USER:MARKer {param}')
