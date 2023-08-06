from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LinearCls:
	"""Linear commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("linear", core, parent)

	def set(self, depth_lin: float, generatorIx=repcap.GeneratorIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:AM<CH>:DEPTh:LINear \n
		Snippet: driver.source.am.depth.linear.set(depth_lin = 1.0, generatorIx = repcap.GeneratorIx.Default) \n
		Sets the depth of the linear amplitude modulation in percent / volt. \n
			:param depth_lin: float Range: 0 to 100
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
		"""
		param = Conversions.decimal_value_to_str(depth_lin)
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		self._core.io.write(f'SOURce<HwInstance>:AM{generatorIx_cmd_val}:DEPTh:LINear {param}')

	def get(self, generatorIx=repcap.GeneratorIx.Default) -> float:
		"""SCPI: [SOURce<HW>]:AM<CH>:DEPTh:LINear \n
		Snippet: value: float = driver.source.am.depth.linear.get(generatorIx = repcap.GeneratorIx.Default) \n
		Sets the depth of the linear amplitude modulation in percent / volt. \n
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
			:return: depth_lin: float Range: 0 to 100"""
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AM{generatorIx_cmd_val}:DEPTh:LINear?')
		return Conversions.str_to_float(response)
