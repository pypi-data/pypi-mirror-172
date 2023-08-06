from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FproportionalCls:
	"""Fproportional commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fproportional", core, parent)

	# noinspection PyTypeChecker
	def get_scale(self) -> enums.SelOutpVxAxis:
		"""SCPI: OUTPut:FPRoportional:SCALe \n
		Snippet: value: enums.SelOutpVxAxis = driver.output.fproportional.get_scale() \n
		Selects the mode the voltage is supplied depending on the frequency. The R&S SMA100B supplies the signal at the V/GHz
		X-Axis connector. \n
			:return: outp_sel_scale: S0V25| S0V5| S1V0| XAXis S0V25|S0V5|S1V0 Supplies the voltage proportional to the set frequency, derived from the selected setting. XAXis Supplies a voltage range from 0 V to 10 V proportional to the frequency sweep range, set with[:SOURcehw]:FREQuency:STARt and [:SOURcehw]:FREQuency:STOP.
		"""
		response = self._core.io.query_str('OUTPut:FPRoportional:SCALe?')
		return Conversions.str_to_scalar_enum(response, enums.SelOutpVxAxis)

	def set_scale(self, outp_sel_scale: enums.SelOutpVxAxis) -> None:
		"""SCPI: OUTPut:FPRoportional:SCALe \n
		Snippet: driver.output.fproportional.set_scale(outp_sel_scale = enums.SelOutpVxAxis.S0V25) \n
		Selects the mode the voltage is supplied depending on the frequency. The R&S SMA100B supplies the signal at the V/GHz
		X-Axis connector. \n
			:param outp_sel_scale: S0V25| S0V5| S1V0| XAXis S0V25|S0V5|S1V0 Supplies the voltage proportional to the set frequency, derived from the selected setting. XAXis Supplies a voltage range from 0 V to 10 V proportional to the frequency sweep range, set with[:SOURcehw]:FREQuency:STARt and [:SOURcehw]:FREQuency:STOP.
		"""
		param = Conversions.enum_scalar_to_str(outp_sel_scale, enums.SelOutpVxAxis)
		self._core.io.write(f'OUTPut:FPRoportional:SCALe {param}')
