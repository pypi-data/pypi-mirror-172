from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LconCls:
	"""Lcon commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lcon", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.CalPowOpuLconMode:
		"""SCPI: CALibration:LEVel:OPU:LCON:MODE \n
		Snippet: value: enums.CalPowOpuLconMode = driver.calibration.level.opu.lcon.get_mode() \n
		No command help available \n
			:return: lcon_mode: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:OPU:LCON:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.CalPowOpuLconMode)

	def set_mode(self, lcon_mode: enums.CalPowOpuLconMode) -> None:
		"""SCPI: CALibration:LEVel:OPU:LCON:MODE \n
		Snippet: driver.calibration.level.opu.lcon.set_mode(lcon_mode = enums.CalPowOpuLconMode.AM) \n
		No command help available \n
			:param lcon_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(lcon_mode, enums.CalPowOpuLconMode)
		self._core.io.write(f'CALibration:LEVel:OPU:LCON:MODE {param}')
