from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class YvalCls:
	"""Yval commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("yval", core, parent)

	def set(self, yval: float, math=repcap.Math.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:MATH<CH>:YVAL \n
		Snippet: driver.calculate.power.sweep.time.math.yval.set(yval = 1.0, math = repcap.Math.Default) \n
		Sets the y-axis values for calculating the reference curve in time measurement mode. To determine two points ('Point
		A'/'Point B') , set suffix 1 and 2 in keyword MATH<ch>. \n
			:param yval: float Range: -200 to 100
			:param math: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')
		"""
		param = Conversions.decimal_value_to_str(yval)
		math_cmd_val = self._cmd_group.get_repcap_cmd_value(math, repcap.Math)
		self._core.io.write(f'CALCulate:POWer:SWEep:TIME:MATH{math_cmd_val}:YVAL {param}')

	def get(self, math=repcap.Math.Default) -> float:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:MATH<CH>:YVAL \n
		Snippet: value: float = driver.calculate.power.sweep.time.math.yval.get(math = repcap.Math.Default) \n
		Sets the y-axis values for calculating the reference curve in time measurement mode. To determine two points ('Point
		A'/'Point B') , set suffix 1 and 2 in keyword MATH<ch>. \n
			:param math: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')
			:return: yval: float Range: -200 to 100"""
		math_cmd_val = self._cmd_group.get_repcap_cmd_value(math, repcap.Math)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:MATH{math_cmd_val}:YVAL?')
		return Conversions.str_to_float(response)
