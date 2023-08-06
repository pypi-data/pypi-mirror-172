from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExponentialCls:
	"""Exponential commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("exponential", core, parent)

	def set(self, depth_exp: float, generatorIx=repcap.GeneratorIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:AM<CH>:DEPTh:EXPonential \n
		Snippet: driver.source.am.depth.exponential.set(depth_exp = 1.0, generatorIx = repcap.GeneratorIx.Default) \n
		Sets the depth of the exponential amplitude modulation in dB/volt. \n
			:param depth_exp: float Range: 0 to 100
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
		"""
		param = Conversions.decimal_value_to_str(depth_exp)
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		self._core.io.write(f'SOURce<HwInstance>:AM{generatorIx_cmd_val}:DEPTh:EXPonential {param}')

	def get(self, generatorIx=repcap.GeneratorIx.Default) -> float:
		"""SCPI: [SOURce<HW>]:AM<CH>:DEPTh:EXPonential \n
		Snippet: value: float = driver.source.am.depth.exponential.get(generatorIx = repcap.GeneratorIx.Default) \n
		Sets the depth of the exponential amplitude modulation in dB/volt. \n
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
			:return: depth_exp: float Range: 0 to 100"""
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AM{generatorIx_cmd_val}:DEPTh:EXPonential?')
		return Conversions.str_to_float(response)
