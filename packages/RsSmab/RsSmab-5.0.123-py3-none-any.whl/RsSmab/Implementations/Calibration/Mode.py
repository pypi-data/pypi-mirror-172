from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def get_configuration(self) -> str:
		"""SCPI: CALibration:MODE:CONFiguration \n
		Snippet: value: str = driver.calibration.mode.get_configuration() \n
		No command help available \n
			:return: cal_conf_xml: No help available
		"""
		response = self._core.io.query_str('CALibration:MODE:CONFiguration?')
		return trim_str_response(response)

	def set_configuration(self, cal_conf_xml: str) -> None:
		"""SCPI: CALibration:MODE:CONFiguration \n
		Snippet: driver.calibration.mode.set_configuration(cal_conf_xml = '1') \n
		No command help available \n
			:param cal_conf_xml: No help available
		"""
		param = Conversions.value_to_quoted_str(cal_conf_xml)
		self._core.io.write(f'CALibration:MODE:CONFiguration {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.CalAdjMode:
		"""SCPI: CALibration:MODE \n
		Snippet: value: enums.CalAdjMode = driver.calibration.mode.get_value() \n
		No command help available \n
			:return: cal_mode: No help available
		"""
		response = self._core.io.query_str('CALibration:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.CalAdjMode)

	def set_value(self, cal_mode: enums.CalAdjMode) -> None:
		"""SCPI: CALibration:MODE \n
		Snippet: driver.calibration.mode.set_value(cal_mode = enums.CalAdjMode.BURNin) \n
		No command help available \n
			:param cal_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(cal_mode, enums.CalAdjMode)
		self._core.io.write(f'CALibration:MODE {param}')
