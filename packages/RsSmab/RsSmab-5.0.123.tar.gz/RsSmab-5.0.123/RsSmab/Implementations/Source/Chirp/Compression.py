from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CompressionCls:
	"""Compression commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("compression", core, parent)

	def get_ratio(self) -> float:
		"""SCPI: [SOURce<HW>]:CHIRp:COMPression:RATio \n
		Snippet: value: float = driver.source.chirp.compression.get_ratio() \n
		Queries the pulse compression ratio (= product of pulse width (s) and bandwidth (Hz) ). \n
			:return: ratio: float Range: 0 to 80E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:COMPression:RATio?')
		return Conversions.str_to_float(response)
