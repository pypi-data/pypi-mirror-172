from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SweepCls:
	"""Sweep commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sweep", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.SweepType:
		"""SCPI: SWEep:TYPE \n
		Snippet: value: enums.SweepType = driver.sweep.get_type_py() \n
		Provided for compatibility between SCPI and Rohde & Schwarz commands. \n
			:return: sweep_type: ADVanced| STANdard
		"""
		response = self._core.io.query_str('SWEep:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.SweepType)

	def set_type_py(self, sweep_type: enums.SweepType) -> None:
		"""SCPI: SWEep:TYPE \n
		Snippet: driver.sweep.set_type_py(sweep_type = enums.SweepType.ADVanced) \n
		Provided for compatibility between SCPI and Rohde & Schwarz commands. \n
			:param sweep_type: ADVanced| STANdard
		"""
		param = Conversions.enum_scalar_to_str(sweep_type, enums.SweepType)
		self._core.io.write(f'SWEep:TYPE {param}')
