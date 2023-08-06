from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	def get_count(self) -> enums.MeasRespTimeAverage:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:AVERage:[COUNt] \n
		Snippet: value: enums.MeasRespTimeAverage = driver.sense.power.sweep.time.average.get_count() \n
		Selects the averaging factor in time mode. The count number determines how many measurement cycles are used to form a
		measurement result. Higher averaging counts reduce noise but increase the measurement time. Averaging requires a stable
		trigger event so that the measurement cycles have the same timing. \n
			:return: count: 1| 2| 4| 8| 16| 32| 64| 128| 256| 512| 1024
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:AVERage:COUNt?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTimeAverage)

	def set_count(self, count: enums.MeasRespTimeAverage) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:AVERage:[COUNt] \n
		Snippet: driver.sense.power.sweep.time.average.set_count(count = enums.MeasRespTimeAverage._1) \n
		Selects the averaging factor in time mode. The count number determines how many measurement cycles are used to form a
		measurement result. Higher averaging counts reduce noise but increase the measurement time. Averaging requires a stable
		trigger event so that the measurement cycles have the same timing. \n
			:param count: 1| 2| 4| 8| 16| 32| 64| 128| 256| 512| 1024
		"""
		param = Conversions.enum_scalar_to_str(count, enums.MeasRespTimeAverage)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:AVERage:COUNt {param}')
