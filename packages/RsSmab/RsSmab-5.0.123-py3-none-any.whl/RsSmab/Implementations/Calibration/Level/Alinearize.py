from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlinearizeCls:
	"""Alinearize commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alinearize", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.CalPowActorLinMode:
		"""SCPI: CALibration:LEVel:ALINearize:MODE \n
		Snippet: value: enums.CalPowActorLinMode = driver.calibration.level.alinearize.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:ALINearize:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.CalPowActorLinMode)

	def set_mode(self, mode: enums.CalPowActorLinMode) -> None:
		"""SCPI: CALibration:LEVel:ALINearize:MODE \n
		Snippet: driver.calibration.level.alinearize.set_mode(mode = enums.CalPowActorLinMode.AUTO) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.CalPowActorLinMode)
		self._core.io.write(f'CALibration:LEVel:ALINearize:MODE {param}')
