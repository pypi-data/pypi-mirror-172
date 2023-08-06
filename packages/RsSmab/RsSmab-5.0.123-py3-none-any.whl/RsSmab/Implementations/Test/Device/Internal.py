from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InternalCls:
	"""Internal commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("internal", core, parent)

	# noinspection PyTypeChecker
	def get(self, argument: str) -> enums.Test:
		"""SCPI: TEST:DEVice:INTernal \n
		Snippet: value: enums.Test = driver.test.device.internal.get(argument = '1') \n
		No command help available \n
			:param argument: No help available
			:return: result: No help available"""
		param = Conversions.value_to_quoted_str(argument)
		response = self._core.io.query_str(f'TEST:DEVice:INTernal? {param}')
		return Conversions.str_to_scalar_enum(response, enums.Test)
