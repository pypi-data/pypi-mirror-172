from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DlinearizeCls:
	"""Dlinearize commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dlinearize", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.CalPowDetLinMode:
		"""SCPI: CALibration:LEVel:DLINearize:MODE \n
		Snippet: value: enums.CalPowDetLinMode = driver.calibration.level.dlinearize.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:DLINearize:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.CalPowDetLinMode)

	def set_mode(self, mode: enums.CalPowDetLinMode) -> None:
		"""SCPI: CALibration:LEVel:DLINearize:MODE \n
		Snippet: driver.calibration.level.dlinearize.set_mode(mode = enums.CalPowDetLinMode.AUTO) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.CalPowDetLinMode)
		self._core.io.write(f'CALibration:LEVel:DLINearize:MODE {param}')
