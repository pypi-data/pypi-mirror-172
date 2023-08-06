from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def get_continuous(self) -> bool:
		"""SCPI: INITiate:LIST:MODE:CONTinuous \n
		Snippet: value: bool = driver.initiate.listPy.mode.get_continuous() \n
		No command help available \n
			:return: list_mode_adv_stat: No help available
		"""
		response = self._core.io.query_str('INITiate:LIST:MODE:CONTinuous?')
		return Conversions.str_to_bool(response)

	def set_continuous(self, list_mode_adv_stat: bool) -> None:
		"""SCPI: INITiate:LIST:MODE:CONTinuous \n
		Snippet: driver.initiate.listPy.mode.set_continuous(list_mode_adv_stat = False) \n
		No command help available \n
			:param list_mode_adv_stat: No help available
		"""
		param = Conversions.bool_to_str(list_mode_adv_stat)
		self._core.io.write(f'INITiate:LIST:MODE:CONTinuous {param}')
