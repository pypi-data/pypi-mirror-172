from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LoaderCls:
	"""Loader commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("loader", core, parent)

	def get_version(self) -> str:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:LOADer:VERSion \n
		Snippet: value: str = driver.source.frequency.multiplier.external.loader.get_version() \n
		No command help available \n
			:return: loader_version: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:LOADer:VERSion?')
		return trim_str_response(response)
