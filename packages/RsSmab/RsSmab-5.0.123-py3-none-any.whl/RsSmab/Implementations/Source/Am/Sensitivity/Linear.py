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

	def set(self, sensitivity: float, generatorIx=repcap.GeneratorIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:AM<CH>:SENSitivity:[LINear] \n
		Snippet: driver.source.am.sensitivity.linear.set(sensitivity = 1.0, generatorIx = repcap.GeneratorIx.Default) \n
		For [:SOURce<hw>]:AM:TYPE LIN, sets the sensitivity of the external signal source for amplitude modulation. \n
			:param sensitivity: float Range: 0 to 100
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
		"""
		param = Conversions.decimal_value_to_str(sensitivity)
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		self._core.io.write(f'SOURce<HwInstance>:AM{generatorIx_cmd_val}:SENSitivity:LINear {param}')

	def get(self, generatorIx=repcap.GeneratorIx.Default) -> float:
		"""SCPI: [SOURce<HW>]:AM<CH>:SENSitivity:[LINear] \n
		Snippet: value: float = driver.source.am.sensitivity.linear.get(generatorIx = repcap.GeneratorIx.Default) \n
		For [:SOURce<hw>]:AM:TYPE LIN, sets the sensitivity of the external signal source for amplitude modulation. \n
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
			:return: sensitivity: float Range: 0 to 100"""
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AM{generatorIx_cmd_val}:SENSitivity:LINear?')
		return Conversions.str_to_float(response)
