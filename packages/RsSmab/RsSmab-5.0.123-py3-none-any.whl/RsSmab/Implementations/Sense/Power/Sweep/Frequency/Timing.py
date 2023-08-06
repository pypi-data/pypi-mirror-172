from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimingCls:
	"""Timing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("timing", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.MeasRespTimingMode:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:TIMing:[MODE] \n
		Snippet: value: enums.MeasRespTimingMode = driver.sense.power.sweep.frequency.timing.get_mode() \n
		Selects the mode in terms of speed and precision of the response of a measurement. \n
			:return: mode: FAST| NORMal| HPRecision | FAST| NORMal FAST Selection FAST leads to a fast measurement with a short integration time for each measurement step. NORMal NORMal leads to a longer but more precise measurement due to a higher integration time for each step.
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:FREQuency:TIMing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTimingMode)

	def set_mode(self, mode: enums.MeasRespTimingMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:TIMing:[MODE] \n
		Snippet: driver.sense.power.sweep.frequency.timing.set_mode(mode = enums.MeasRespTimingMode.FAST) \n
		Selects the mode in terms of speed and precision of the response of a measurement. \n
			:param mode: FAST| NORMal| HPRecision | FAST| NORMal FAST Selection FAST leads to a fast measurement with a short integration time for each measurement step. NORMal NORMal leads to a longer but more precise measurement due to a higher integration time for each step.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.MeasRespTimingMode)
		self._core.io.write(f'SENSe:POWer:SWEep:FREQuency:TIMing:MODE {param}')
