from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DdmCls:
	"""Ddm commands group definition. 8 total commands, 0 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ddm", core, parent)

	# noinspection PyTypeChecker
	def get_coupling(self) -> enums.AvionicIlsDdmCoup:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:COUPling \n
		Snippet: value: enums.AvionicIlsDdmCoup = driver.source.ils.localizer.ddm.get_coupling() \n
		Selects if the DDM value is fixed or is changed with a change of sum of modulation depths (SDM,
		see [:SOURce<hw>]:ILS:LOCalizer:SDM) . \n
			:return: coupling: FIXed| SDM
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:DDM:COUPling?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsDdmCoup)

	def set_coupling(self, coupling: enums.AvionicIlsDdmCoup) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:COUPling \n
		Snippet: driver.source.ils.localizer.ddm.set_coupling(coupling = enums.AvionicIlsDdmCoup.FIXed) \n
		Selects if the DDM value is fixed or is changed with a change of sum of modulation depths (SDM,
		see [:SOURce<hw>]:ILS:LOCalizer:SDM) . \n
			:param coupling: FIXed| SDM
		"""
		param = Conversions.enum_scalar_to_str(coupling, enums.AvionicIlsDdmCoup)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:DDM:COUPling {param}')

	def get_current(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:CURRent \n
		Snippet: value: float = driver.source.ils.localizer.ddm.get_current() \n
		Sets the DDM value alternatively as a current by means of the ILS indicating instrument. The instrument current is
		calculated according to: DDM µA = DDM × 857,1 µA A variation of the instrument current automatically leads to a variation
		of the DDM value and the DDM value in dB. \n
			:return: current: float Range: -9.6775E-4 to 9.6775E-4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:DDM:CURRent?')
		return Conversions.str_to_float(response)

	def set_current(self, current: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:CURRent \n
		Snippet: driver.source.ils.localizer.ddm.set_current(current = 1.0) \n
		Sets the DDM value alternatively as a current by means of the ILS indicating instrument. The instrument current is
		calculated according to: DDM µA = DDM × 857,1 µA A variation of the instrument current automatically leads to a variation
		of the DDM value and the DDM value in dB. \n
			:param current: float Range: -9.6775E-4 to 9.6775E-4
		"""
		param = Conversions.decimal_value_to_str(current)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:DDM:CURRent {param}')

	# noinspection PyTypeChecker
	def get_direction(self) -> enums.LeftRightDirection:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:DIRection \n
		Snippet: value: enums.LeftRightDirection = driver.source.ils.localizer.ddm.get_direction() \n
		Sets the simulation mode for the ILS-LOC modulation signal. A change of the setting automatically changes the sign of the
		DDM value. \n
			:return: direction: LEFT| RIGHt LEFT The 150 Hz modulation signal is predominant, the DDM value is negative (the airplane is too far to the right, it must turn to the left) . RIGHT The 90 Hz modulation signal is predominant, the DDM value is positive (the airplane is too far to the left, it must turn to the right) .
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:DDM:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.LeftRightDirection)

	def set_direction(self, direction: enums.LeftRightDirection) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:DIRection \n
		Snippet: driver.source.ils.localizer.ddm.set_direction(direction = enums.LeftRightDirection.LEFT) \n
		Sets the simulation mode for the ILS-LOC modulation signal. A change of the setting automatically changes the sign of the
		DDM value. \n
			:param direction: LEFT| RIGHt LEFT The 150 Hz modulation signal is predominant, the DDM value is negative (the airplane is too far to the right, it must turn to the left) . RIGHT The 90 Hz modulation signal is predominant, the DDM value is positive (the airplane is too far to the left, it must turn to the right) .
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.LeftRightDirection)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:DDM:DIRection {param}')

	def get_logarithmic(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:LOGarithmic \n
		Snippet: value: float = driver.source.ils.localizer.ddm.get_logarithmic() \n
		Sets the modulation depth in dB for ILS localizer modulation. See also [:SOURce<hw>]:ILS:LOCalizer:DDM[:DEPTh]. \n
			:return: logarithmic: float Range: -999.9 to 999.9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:DDM:LOGarithmic?')
		return Conversions.str_to_float(response)

	def set_logarithmic(self, logarithmic: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:LOGarithmic \n
		Snippet: driver.source.ils.localizer.ddm.set_logarithmic(logarithmic = 1.0) \n
		Sets the modulation depth in dB for ILS localizer modulation. See also [:SOURce<hw>]:ILS:LOCalizer:DDM[:DEPTh]. \n
			:param logarithmic: float Range: -999.9 to 999.9
		"""
		param = Conversions.decimal_value_to_str(logarithmic)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:DDM:LOGarithmic {param}')

	def get_pct(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:PCT \n
		Snippet: value: float = driver.source.ils.localizer.ddm.get_pct() \n
		Sets the difference in depth of modulation between the signal of the left lobe (90 Hz) and the right lobe (150 Hz) . The
		maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone.
		See also [:SOURce<hw>]:ILS:LOCalizer:DDM[:DEPTh]. \n
			:return: pct: float Range: -80.0 to 80.0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:DDM:PCT?')
		return Conversions.str_to_float(response)

	def set_pct(self, pct: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:PCT \n
		Snippet: driver.source.ils.localizer.ddm.set_pct(pct = 1.0) \n
		Sets the difference in depth of modulation between the signal of the left lobe (90 Hz) and the right lobe (150 Hz) . The
		maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone.
		See also [:SOURce<hw>]:ILS:LOCalizer:DDM[:DEPTh]. \n
			:param pct: float Range: -80.0 to 80.0
		"""
		param = Conversions.decimal_value_to_str(pct)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:DDM:PCT {param}')

	# noinspection PyTypeChecker
	def get_polarity(self) -> enums.AvionicIlsDdmPol:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:POLarity \n
		Snippet: value: enums.AvionicIlsDdmPol = driver.source.ils.localizer.ddm.get_polarity() \n
		Sets the polarity for DDM calculation (see [:SOURce<hw>]:ILS:LOCalizer:DDM[:DEPTh]) . The DDM depth calculation depends
		on the selected polarity:
			INTRO_CMD_HELP: The effect depends on the selected mode: \n
			- Polarity 90 Hz - 150 Hz (default setting) : DDM = [ AM (90 Hz) - AM (150 Hz) ] / 100%
			- Polarity 150 Hz - 90 Hz: DDM = [ AM (150 Hz) - AM (90 Hz) ] / 100% \n
			:return: polarity: P90_150| P150_90
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:DDM:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicIlsDdmPol)

	def set_polarity(self, polarity: enums.AvionicIlsDdmPol) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:POLarity \n
		Snippet: driver.source.ils.localizer.ddm.set_polarity(polarity = enums.AvionicIlsDdmPol.P150_90) \n
		Sets the polarity for DDM calculation (see [:SOURce<hw>]:ILS:LOCalizer:DDM[:DEPTh]) . The DDM depth calculation depends
		on the selected polarity:
			INTRO_CMD_HELP: The effect depends on the selected mode: \n
			- Polarity 90 Hz - 150 Hz (default setting) : DDM = [ AM (90 Hz) - AM (150 Hz) ] / 100%
			- Polarity 150 Hz - 90 Hz: DDM = [ AM (150 Hz) - AM (90 Hz) ] / 100% \n
			:param polarity: P90_150| P150_90
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.AvionicIlsDdmPol)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:DDM:POLarity {param}')

	# noinspection PyTypeChecker
	def get_step(self) -> enums.AvionicDdmStep:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:STEP \n
		Snippet: value: enums.AvionicDdmStep = driver.source.ils.localizer.ddm.get_step() \n
		Sets the variation step of the DDM values. \n
			:return: ddm_step: DECimal| PREDefined
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:DDM:STEP?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDdmStep)

	def set_step(self, ddm_step: enums.AvionicDdmStep) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:STEP \n
		Snippet: driver.source.ils.localizer.ddm.set_step(ddm_step = enums.AvionicDdmStep.DECimal) \n
		Sets the variation step of the DDM values. \n
			:param ddm_step: DECimal| PREDefined
		"""
		param = Conversions.enum_scalar_to_str(ddm_step, enums.AvionicDdmStep)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:DDM:STEP {param}')

	def get_depth(self) -> float:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:[DEPTh] \n
		Snippet: value: float = driver.source.ils.localizer.ddm.get_depth() \n
		Sets the difference in depth of modulation between the signal of the upper/left lobe (90 Hz) and the lower/right lobe
		(150 Hz) . The maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone.The following is
		true: ILS:LOC:DDM:DEPTh = (AM(90Hz) - AM(150Hz) )/100% A variation of the DDM value automatically leads to a variation of
		the DDM value in dB and the value of the instrument current. \n
			:return: depth: float Range: -0.4 to 0.4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:DDM:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""SCPI: [SOURce<HW>]:ILS:LOCalizer:DDM:[DEPTh] \n
		Snippet: driver.source.ils.localizer.ddm.set_depth(depth = 1.0) \n
		Sets the difference in depth of modulation between the signal of the upper/left lobe (90 Hz) and the lower/right lobe
		(150 Hz) . The maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone.The following is
		true: ILS:LOC:DDM:DEPTh = (AM(90Hz) - AM(150Hz) )/100% A variation of the DDM value automatically leads to a variation of
		the DDM value in dB and the value of the instrument current. \n
			:param depth: float Range: -0.4 to 0.4
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:DDM:DEPTh {param}')
