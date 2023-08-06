from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EdetectorCls:
	"""Edetector commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("edetector", core, parent)

	def get_factor(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:ALC:EDETector:FACTor \n
		Snippet: value: float = driver.source.power.alc.edetector.get_factor() \n
		Sets the attenuation value of the RF coupler. \n
			:return: detector_fact: float Range: -200 to 200
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:EDETector:FACTor?')
		return Conversions.str_to_float(response)

	def get_level(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:ALC:EDETector:LEVel \n
		Snippet: value: float = driver.source.power.alc.edetector.get_level() \n
		Sets the maximum power level at the RF output required for compensating the external ALC coupler and cable losses. \n
			:return: req_gen_lev: float Range: -145 to 40
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:EDETector:LEVel?')
		return Conversions.str_to_float(response)
