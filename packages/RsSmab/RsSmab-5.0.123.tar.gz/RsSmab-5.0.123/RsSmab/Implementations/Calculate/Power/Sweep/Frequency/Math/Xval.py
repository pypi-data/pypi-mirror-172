from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class XvalCls:
	"""Xval commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("xval", core, parent)

	def set(self, xval: float, math=repcap.Math.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:FREQuency:MATH<CH>:XVAL \n
		Snippet: driver.calculate.power.sweep.frequency.math.xval.set(xval = 1.0, math = repcap.Math.Default) \n
		Sets the x-axis values for calculating the reference curve in frequency measurement mode. To determine two points ('Point
		A'/'Point B') , set suffix 1 and 2 in keyword MATH<ch>. \n
			:param xval: float Range: 0 to 1E12
			:param math: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')
		"""
		param = Conversions.decimal_value_to_str(xval)
		math_cmd_val = self._cmd_group.get_repcap_cmd_value(math, repcap.Math)
		self._core.io.write(f'CALCulate:POWer:SWEep:FREQuency:MATH{math_cmd_val}:XVAL {param}')

	def get(self, math=repcap.Math.Default) -> float:
		"""SCPI: CALCulate:[POWer]:SWEep:FREQuency:MATH<CH>:XVAL \n
		Snippet: value: float = driver.calculate.power.sweep.frequency.math.xval.get(math = repcap.Math.Default) \n
		Sets the x-axis values for calculating the reference curve in frequency measurement mode. To determine two points ('Point
		A'/'Point B') , set suffix 1 and 2 in keyword MATH<ch>. \n
			:param math: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')
			:return: xval: float Range: 0 to 1E12"""
		math_cmd_val = self._cmd_group.get_repcap_cmd_value(math, repcap.Math)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:FREQuency:MATH{math_cmd_val}:XVAL?')
		return Conversions.str_to_float(response)
