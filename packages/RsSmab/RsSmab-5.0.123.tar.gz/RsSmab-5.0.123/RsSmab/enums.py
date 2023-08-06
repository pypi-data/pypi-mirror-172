from enum import Enum


# noinspection SpellCheckingInspection
class AcDc(Enum):
	"""2 Members, AC ... DC"""
	AC = 0
	DC = 1


# noinspection SpellCheckingInspection
class AlcOffMode(Enum):
	"""2 Members, SHOLd ... TABLe"""
	SHOLd = 0
	TABLe = 1


# noinspection SpellCheckingInspection
class AlcOnOffAuto(Enum):
	"""9 Members, _0 ... PRESet"""
	_0 = 0
	_1 = 1
	AUTO = 2
	OFF = 3
	OFFTable = 4
	ON = 5
	ONSample = 6
	ONTable = 7
	PRESet = 8


# noinspection SpellCheckingInspection
class AmMode(Enum):
	"""2 Members, NORMal ... SCAN"""
	NORMal = 0
	SCAN = 1


# noinspection SpellCheckingInspection
class AmType(Enum):
	"""2 Members, EXPonential ... LINear"""
	EXPonential = 0
	LINear = 1


# noinspection SpellCheckingInspection
class AutoManStep(Enum):
	"""3 Members, AUTO ... STEP"""
	AUTO = 0
	MANual = 1
	STEP = 2


# noinspection SpellCheckingInspection
class AutoManualMode(Enum):
	"""2 Members, AUTO ... MANual"""
	AUTO = 0
	MANual = 1


# noinspection SpellCheckingInspection
class AutoStep(Enum):
	"""2 Members, AUTO ... STEP"""
	AUTO = 0
	STEP = 1


# noinspection SpellCheckingInspection
class AvionicCarrFreqMode(Enum):
	"""3 Members, DECimal ... USER"""
	DECimal = 0
	ICAO = 1
	USER = 2


# noinspection SpellCheckingInspection
class AvionicCarrFreqModeMrkBcn(Enum):
	"""2 Members, PREDefined ... USER"""
	PREDefined = 0
	USER = 1


# noinspection SpellCheckingInspection
class AvionicComIdTimeSchem(Enum):
	"""2 Members, STD ... USER"""
	STD = 0
	USER = 1


# noinspection SpellCheckingInspection
class AvionicDdmStep(Enum):
	"""2 Members, DECimal ... PREDefined"""
	DECimal = 0
	PREDefined = 1


# noinspection SpellCheckingInspection
class AvionicExtAm(Enum):
	"""2 Members, EXT ... INT"""
	EXT = 0
	INT = 1


# noinspection SpellCheckingInspection
class AvionicIlsDdmCoup(Enum):
	"""2 Members, FIXed ... SDM"""
	FIXed = 0
	SDM = 1


# noinspection SpellCheckingInspection
class AvionicIlsDdmPol(Enum):
	"""2 Members, P150_90 ... P90_150"""
	P150_90 = 0
	P90_150 = 1


# noinspection SpellCheckingInspection
class AvionicIlsGsMode(Enum):
	"""3 Members, LLOBe ... ULOBe"""
	LLOBe = 0
	NORM = 1
	ULOBe = 2


# noinspection SpellCheckingInspection
class AvionicIlsIcaoChan(Enum):
	"""40 Members, CH18X ... CH56Y"""
	CH18X = 0
	CH18Y = 1
	CH20X = 2
	CH20Y = 3
	CH22X = 4
	CH22Y = 5
	CH24X = 6
	CH24Y = 7
	CH26X = 8
	CH26Y = 9
	CH28X = 10
	CH28Y = 11
	CH30X = 12
	CH30Y = 13
	CH32X = 14
	CH32Y = 15
	CH34X = 16
	CH34Y = 17
	CH36X = 18
	CH36Y = 19
	CH38X = 20
	CH38Y = 21
	CH40X = 22
	CH40Y = 23
	CH42X = 24
	CH42Y = 25
	CH44X = 26
	CH44Y = 27
	CH46X = 28
	CH46Y = 29
	CH48X = 30
	CH48Y = 31
	CH50X = 32
	CH50Y = 33
	CH52X = 34
	CH52Y = 35
	CH54X = 36
	CH54Y = 37
	CH56X = 38
	CH56Y = 39


# noinspection SpellCheckingInspection
class AvionicIlsLocMode(Enum):
	"""3 Members, LLOBe ... RLOBe"""
	LLOBe = 0
	NORM = 1
	RLOBe = 2


# noinspection SpellCheckingInspection
class AvionicIlsType(Enum):
	"""4 Members, GS ... MBEacon"""
	GS = 0
	GSLope = 1
	LOCalize = 2
	MBEacon = 3


# noinspection SpellCheckingInspection
class AvionicKnobStep(Enum):
	"""2 Members, DECimal ... ICAO"""
	DECimal = 0
	ICAO = 1


# noinspection SpellCheckingInspection
class AvionicVorDir(Enum):
	"""2 Members, FROM ... TO"""
	FROM = 0
	TO = 1


# noinspection SpellCheckingInspection
class AvionicVorIcaoChan(Enum):
	"""160 Members, CH100X ... CH99Y"""
	CH100X = 0
	CH100Y = 1
	CH101X = 2
	CH101Y = 3
	CH102X = 4
	CH102Y = 5
	CH103X = 6
	CH103Y = 7
	CH104X = 8
	CH104Y = 9
	CH105X = 10
	CH105Y = 11
	CH106X = 12
	CH106Y = 13
	CH107X = 14
	CH107Y = 15
	CH108X = 16
	CH108Y = 17
	CH109X = 18
	CH109Y = 19
	CH110X = 20
	CH110Y = 21
	CH111X = 22
	CH111Y = 23
	CH112X = 24
	CH112Y = 25
	CH113X = 26
	CH113Y = 27
	CH114X = 28
	CH114Y = 29
	CH115X = 30
	CH115Y = 31
	CH116X = 32
	CH116Y = 33
	CH117X = 34
	CH117Y = 35
	CH118X = 36
	CH118Y = 37
	CH119X = 38
	CH119Y = 39
	CH120X = 40
	CH120Y = 41
	CH121X = 42
	CH121Y = 43
	CH122X = 44
	CH122Y = 45
	CH123X = 46
	CH123Y = 47
	CH124X = 48
	CH124Y = 49
	CH125X = 50
	CH125Y = 51
	CH126X = 52
	CH126Y = 53
	CH17X = 54
	CH17Y = 55
	CH19X = 56
	CH19Y = 57
	CH21X = 58
	CH21Y = 59
	CH23X = 60
	CH23Y = 61
	CH25X = 62
	CH25Y = 63
	CH27X = 64
	CH27Y = 65
	CH29X = 66
	CH29Y = 67
	CH31X = 68
	CH31Y = 69
	CH33X = 70
	CH33Y = 71
	CH35X = 72
	CH35Y = 73
	CH37X = 74
	CH37Y = 75
	CH39X = 76
	CH39Y = 77
	CH41X = 78
	CH41Y = 79
	CH43X = 80
	CH43Y = 81
	CH45X = 82
	CH45Y = 83
	CH47X = 84
	CH47Y = 85
	CH49X = 86
	CH49Y = 87
	CH51X = 88
	CH51Y = 89
	CH53X = 90
	CH53Y = 91
	CH55X = 92
	CH55Y = 93
	CH57X = 94
	CH57Y = 95
	CH58X = 96
	CH58Y = 97
	CH59X = 98
	CH59Y = 99
	CH70X = 100
	CH70Y = 101
	CH71X = 102
	CH71Y = 103
	CH72X = 104
	CH72Y = 105
	CH73X = 106
	CH73Y = 107
	CH74X = 108
	CH74Y = 109
	CH75X = 110
	CH75Y = 111
	CH76X = 112
	CH76Y = 113
	CH77X = 114
	CH77Y = 115
	CH78X = 116
	CH78Y = 117
	CH79X = 118
	CH79Y = 119
	CH80X = 120
	CH80Y = 121
	CH81X = 122
	CH81Y = 123
	CH82X = 124
	CH82Y = 125
	CH83X = 126
	CH83Y = 127
	CH84X = 128
	CH84Y = 129
	CH85X = 130
	CH85Y = 131
	CH86X = 132
	CH86Y = 133
	CH87X = 134
	CH87Y = 135
	CH88X = 136
	CH88Y = 137
	CH89X = 138
	CH89Y = 139
	CH90X = 140
	CH90Y = 141
	CH91X = 142
	CH91Y = 143
	CH92X = 144
	CH92Y = 145
	CH93X = 146
	CH93Y = 147
	CH94X = 148
	CH94Y = 149
	CH95X = 150
	CH95Y = 151
	CH96X = 152
	CH96Y = 153
	CH97X = 154
	CH97Y = 155
	CH98X = 156
	CH98Y = 157
	CH99X = 158
	CH99Y = 159


# noinspection SpellCheckingInspection
class AvionicVorMode(Enum):
	"""4 Members, FMSubcarrier ... VAR"""
	FMSubcarrier = 0
	NORM = 1
	SUBCarrier = 2
	VAR = 3


# noinspection SpellCheckingInspection
class ByteOrder(Enum):
	"""2 Members, NORMal ... SWAPped"""
	NORMal = 0
	SWAPped = 1


# noinspection SpellCheckingInspection
class CalAdjMode(Enum):
	"""2 Members, BURNin ... FULL"""
	BURNin = 0
	FULL = 1


# noinspection SpellCheckingInspection
class CalDataMode(Enum):
	"""2 Members, CUSTomer ... FACTory"""
	CUSTomer = 0
	FACTory = 1


# noinspection SpellCheckingInspection
class CalDataUpdate(Enum):
	"""6 Members, BBFRC ... RFFRC"""
	BBFRC = 0
	FREQuency = 1
	IALL = 2
	LEVel = 3
	LEVForced = 4
	RFFRC = 5


# noinspection SpellCheckingInspection
class CalPowActorLinMode(Enum):
	"""2 Members, AUTO ... OFF"""
	AUTO = 0
	OFF = 1


# noinspection SpellCheckingInspection
class CalPowAmpDetMode(Enum):
	"""13 Members, AMP ... OPU"""
	AMP = 0
	AT20 = 1
	AT40 = 2
	AT6 = 3
	ATT = 4
	AUTO = 5
	FIXed = 6
	HP = 7
	HP6 = 8
	OP20 = 9
	OP40 = 10
	OP6 = 11
	OPU = 12


# noinspection SpellCheckingInspection
class CalPowAttMode(Enum):
	"""2 Members, NEW ... OLD"""
	NEW = 0
	OLD = 1


# noinspection SpellCheckingInspection
class CalPowBandwidth(Enum):
	"""3 Members, AUTO ... LOW"""
	AUTO = 0
	HIGH = 1
	LOW = 2


# noinspection SpellCheckingInspection
class CalPowDetLinMode(Enum):
	"""4 Members, AUTO ... USER2"""
	AUTO = 0
	OFF = 1
	USER1 = 2
	USER2 = 3


# noinspection SpellCheckingInspection
class CalPowOpuLconMode(Enum):
	"""6 Members, AM ... USER2"""
	AM = 0
	AUTO = 1
	CW = 2
	DAM = 3
	USER1 = 4
	USER2 = 5


# noinspection SpellCheckingInspection
class ClkSynOutType(Enum):
	"""4 Members, CMOS ... SESine"""
	CMOS = 0
	DSINe = 1
	DSQuare = 2
	SESine = 3


# noinspection SpellCheckingInspection
class Colour(Enum):
	"""4 Members, GREen ... YELLow"""
	GREen = 0
	NONE = 1
	RED = 2
	YELLow = 3


# noinspection SpellCheckingInspection
class DecimalSeparator(Enum):
	"""2 Members, COMMa ... DOT"""
	COMMa = 0
	DOT = 1


# noinspection SpellCheckingInspection
class DevExpFormat(Enum):
	"""4 Members, CGPRedefined ... XML"""
	CGPRedefined = 0
	CGUSer = 1
	SCPI = 2
	XML = 3


# noinspection SpellCheckingInspection
class DexchExtension(Enum):
	"""2 Members, CSV ... TXT"""
	CSV = 0
	TXT = 1


# noinspection SpellCheckingInspection
class DexchMode(Enum):
	"""2 Members, EXPort ... IMPort"""
	EXPort = 0
	IMPort = 1


# noinspection SpellCheckingInspection
class DexchSepCol(Enum):
	"""4 Members, COMMa ... TABulator"""
	COMMa = 0
	SEMicolon = 1
	SPACe = 2
	TABulator = 3


# noinspection SpellCheckingInspection
class DiagBgColor(Enum):
	"""2 Members, BLACk ... WHITe"""
	BLACk = 0
	WHITe = 1


# noinspection SpellCheckingInspection
class DispKeybLockMode(Enum):
	"""5 Members, DISabled ... VNConly"""
	DISabled = 0
	DONLy = 1
	ENABled = 2
	TOFF = 3
	VNConly = 4


# noinspection SpellCheckingInspection
class ErFpowSensMapping(Enum):
	"""9 Members, SENS1 ... UNMapped"""
	SENS1 = 0
	SENS2 = 1
	SENS3 = 2
	SENS4 = 3
	SENSor1 = 4
	SENSor2 = 5
	SENSor3 = 6
	SENSor4 = 7
	UNMapped = 8


# noinspection SpellCheckingInspection
class FilterWidth(Enum):
	"""2 Members, NARRow ... WIDE"""
	NARRow = 0
	WIDE = 1


# noinspection SpellCheckingInspection
class FmMode(Enum):
	"""2 Members, HBANdwidth ... LNOise"""
	HBANdwidth = 0
	LNOise = 1


# noinspection SpellCheckingInspection
class FmSour(Enum):
	"""7 Members, EXT1 ... NOISe"""
	EXT1 = 0
	EXT2 = 1
	EXTernal = 2
	INTernal = 3
	LF1 = 4
	LF2 = 5
	NOISe = 6


# noinspection SpellCheckingInspection
class FormData(Enum):
	"""2 Members, ASCii ... PACKed"""
	ASCii = 0
	PACKed = 1


# noinspection SpellCheckingInspection
class FormStatReg(Enum):
	"""4 Members, ASCii ... OCTal"""
	ASCii = 0
	BINary = 1
	HEXadecimal = 2
	OCTal = 3


# noinspection SpellCheckingInspection
class FreqMode(Enum):
	"""5 Members, COMBined ... SWEep"""
	COMBined = 0
	CW = 1
	FIXed = 2
	LIST = 3
	SWEep = 4


# noinspection SpellCheckingInspection
class FreqPllModeF(Enum):
	"""2 Members, NARRow ... NORMal"""
	NARRow = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class FreqStepMode(Enum):
	"""2 Members, DECimal ... USER"""
	DECimal = 0
	USER = 1


# noinspection SpellCheckingInspection
class FreqSweepType(Enum):
	"""2 Members, ANALog ... STEPped"""
	ANALog = 0
	STEPped = 1


# noinspection SpellCheckingInspection
class HardCopyImageFormat(Enum):
	"""4 Members, BMP ... XPM"""
	BMP = 0
	JPG = 1
	PNG = 2
	XPM = 3


# noinspection SpellCheckingInspection
class HardCopyRegion(Enum):
	"""2 Members, ALL ... DIALog"""
	ALL = 0
	DIALog = 1


# noinspection SpellCheckingInspection
class HcopyDestination(Enum):
	"""2 Members, FILE ... PRINter"""
	FILE = 0
	PRINter = 1


# noinspection SpellCheckingInspection
class IecDevId(Enum):
	"""2 Members, AUTO ... USER"""
	AUTO = 0
	USER = 1


# noinspection SpellCheckingInspection
class IecTermMode(Enum):
	"""2 Members, EOI ... STANdard"""
	EOI = 0
	STANdard = 1


# noinspection SpellCheckingInspection
class Imp(Enum):
	"""3 Members, G50 ... HIGH"""
	G50 = 0
	G600 = 1
	HIGH = 2


# noinspection SpellCheckingInspection
class InclExcl(Enum):
	"""2 Members, EXCLude ... INCLude"""
	EXCLude = 0
	INCLude = 1


# noinspection SpellCheckingInspection
class InpImpRf(Enum):
	"""3 Members, G10K ... G50"""
	G10K = 0
	G1K = 1
	G50 = 2


# noinspection SpellCheckingInspection
class KbLayout(Enum):
	"""20 Members, CHINese ... SWEDish"""
	CHINese = 0
	DANish = 1
	DUTBe = 2
	DUTCh = 3
	ENGLish = 4
	ENGUK = 5
	ENGUS = 6
	FINNish = 7
	FREBe = 8
	FRECa = 9
	FRENch = 10
	GERMan = 11
	ITALian = 12
	JAPanese = 13
	KORean = 14
	NORWegian = 15
	PORTuguese = 16
	RUSSian = 17
	SPANish = 18
	SWEDish = 19


# noinspection SpellCheckingInspection
class LeftRightDirection(Enum):
	"""2 Members, LEFT ... RIGHt"""
	LEFT = 0
	RIGHt = 1


# noinspection SpellCheckingInspection
class LfBwidth(Enum):
	"""2 Members, BW0M2 ... BW10m"""
	BW0M2 = 0
	BW10m = 1


# noinspection SpellCheckingInspection
class LfFreqMode(Enum):
	"""3 Members, CW ... SWEep"""
	CW = 0
	FIXed = 1
	SWEep = 2


# noinspection SpellCheckingInspection
class LfShapeBfAmily(Enum):
	"""5 Members, PULSe ... TRIangle"""
	PULSe = 0
	SINE = 1
	SQUare = 2
	TRAPeze = 3
	TRIangle = 4


# noinspection SpellCheckingInspection
class LfSource(Enum):
	"""17 Members, AM ... NOISe"""
	AM = 0
	AMA = 1
	AMB = 2
	EXT1 = 3
	EXT2 = 4
	FMPM = 5
	FMPMA = 6
	FMPMB = 7
	LF1 = 8
	LF1A = 9
	LF1B = 10
	LF2 = 11
	LF2A = 12
	LF2B = 13
	NOISA = 14
	NOISB = 15
	NOISe = 16


# noinspection SpellCheckingInspection
class LfSweepSource(Enum):
	"""2 Members, LF1 ... LF2"""
	LF1 = 0
	LF2 = 1


# noinspection SpellCheckingInspection
class LmodRunMode(Enum):
	"""2 Members, LEARned ... LIVE"""
	LEARned = 0
	LIVE = 1


# noinspection SpellCheckingInspection
class LowHigh(Enum):
	"""2 Members, HIGH ... LOW"""
	HIGH = 0
	LOW = 1


# noinspection SpellCheckingInspection
class MeasRespHcOpCsvcLmSep(Enum):
	"""4 Members, BLANk ... TABulator"""
	BLANk = 0
	COMMa = 1
	SEMicolon = 2
	TABulator = 3


# noinspection SpellCheckingInspection
class MeasRespHcOpCsvhEader(Enum):
	"""2 Members, OFF ... STANdard"""
	OFF = 0
	STANdard = 1


# noinspection SpellCheckingInspection
class MeasRespHcOpCsvoRient(Enum):
	"""2 Members, HORizontal ... VERTical"""
	HORizontal = 0
	VERTical = 1


# noinspection SpellCheckingInspection
class MeasRespHcOpFileFormat(Enum):
	"""5 Members, BMP ... XPM"""
	BMP = 0
	CSV = 1
	JPG = 2
	PNG = 3
	XPM = 4


# noinspection SpellCheckingInspection
class MeasRespMath(Enum):
	"""20 Members, T1REf ... T4T4"""
	T1REf = 0
	T1T1 = 1
	T1T2 = 2
	T1T3 = 3
	T1T4 = 4
	T2REf = 5
	T2T1 = 6
	T2T2 = 7
	T2T3 = 8
	T2T4 = 9
	T3REf = 10
	T3T1 = 11
	T3T2 = 12
	T3T3 = 13
	T3T4 = 14
	T4REf = 15
	T4T1 = 16
	T4T2 = 17
	T4T3 = 18
	T4T4 = 19


# noinspection SpellCheckingInspection
class MeasRespMode(Enum):
	"""3 Members, FREQuency ... TIME"""
	FREQuency = 0
	POWer = 1
	TIME = 2


# noinspection SpellCheckingInspection
class MeasRespPulsThrBase(Enum):
	"""2 Members, POWer ... VOLTage"""
	POWer = 0
	VOLTage = 1


# noinspection SpellCheckingInspection
class MeasRespSpacingMode(Enum):
	"""2 Members, LINear ... LOGarithmic"""
	LINear = 0
	LOGarithmic = 1


# noinspection SpellCheckingInspection
class MeasRespTimeAverage(Enum):
	"""11 Members, _1 ... _8"""
	_1 = 0
	_1024 = 1
	_128 = 2
	_16 = 3
	_2 = 4
	_256 = 5
	_32 = 6
	_4 = 7
	_512 = 8
	_64 = 9
	_8 = 10


# noinspection SpellCheckingInspection
class MeasRespTimeGate(Enum):
	"""8 Members, TRAC1 ... TRACe4"""
	TRAC1 = 0
	TRAC2 = 1
	TRAC3 = 2
	TRAC4 = 3
	TRACe1 = 4
	TRACe2 = 5
	TRACe3 = 6
	TRACe4 = 7


# noinspection SpellCheckingInspection
class MeasRespTimingMode(Enum):
	"""2 Members, FAST ... NORMal"""
	FAST = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class MeasRespTraceColor(Enum):
	"""7 Members, BLUE ... YELLow"""
	BLUE = 0
	GRAY = 1
	GREen = 2
	INVers = 3
	MAGenta = 4
	RED = 5
	YELLow = 6


# noinspection SpellCheckingInspection
class MeasRespTraceCopyDest(Enum):
	"""1 Members, REFerence ... REFerence"""
	REFerence = 0


# noinspection SpellCheckingInspection
class MeasRespTraceFeed(Enum):
	"""10 Members, NONE ... SENSor4"""
	NONE = 0
	REFerence = 1
	SENS1 = 2
	SENS2 = 3
	SENS3 = 4
	SENS4 = 5
	SENSor1 = 6
	SENSor2 = 7
	SENSor3 = 8
	SENSor4 = 9


# noinspection SpellCheckingInspection
class MeasRespTraceState(Enum):
	"""3 Members, HOLD ... ON"""
	HOLD = 0
	OFF = 1
	ON = 2


# noinspection SpellCheckingInspection
class MeasRespTrigAutoSet(Enum):
	"""1 Members, ONCE ... ONCE"""
	ONCE = 0


# noinspection SpellCheckingInspection
class MeasRespTrigMode(Enum):
	"""4 Members, AUTO ... INTernal"""
	AUTO = 0
	EXTernal = 1
	FREE = 2
	INTernal = 3


# noinspection SpellCheckingInspection
class MeasRespYsCaleEvents(Enum):
	"""2 Members, AND ... OR"""
	AND = 0
	OR = 1


# noinspection SpellCheckingInspection
class MeasRespYsCaleMode(Enum):
	"""5 Members, CEXPanding ... OFF"""
	CEXPanding = 0
	CFLoating = 1
	FEXPanding = 2
	FFLoating = 3
	OFF = 4


# noinspection SpellCheckingInspection
class ModulationDevMode(Enum):
	"""3 Members, RATio ... UNCoupled"""
	RATio = 0
	TOTal = 1
	UNCoupled = 2


# noinspection SpellCheckingInspection
class NetMode(Enum):
	"""2 Members, AUTO ... STATic"""
	AUTO = 0
	STATic = 1


# noinspection SpellCheckingInspection
class NoisDistrib(Enum):
	"""4 Members, EQUal ... UNIForm"""
	EQUal = 0
	GAUSs = 1
	NORMal = 2
	UNIForm = 3


# noinspection SpellCheckingInspection
class NormalInverted(Enum):
	"""2 Members, INVerted ... NORMal"""
	INVerted = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class ParameterSetMode(Enum):
	"""2 Members, GLOBal ... LIST"""
	GLOBal = 0
	LIST = 1


# noinspection SpellCheckingInspection
class Parity(Enum):
	"""3 Members, EVEN ... ODD"""
	EVEN = 0
	NONE = 1
	ODD = 2


# noinspection SpellCheckingInspection
class PmMode(Enum):
	"""3 Members, HBANdwidth ... LNOise"""
	HBANdwidth = 0
	HDEViation = 1
	LNOise = 2


# noinspection SpellCheckingInspection
class PowAlcDetSensitivity(Enum):
	"""5 Members, AUTO ... MEDium"""
	AUTO = 0
	FIXed = 1
	HIGH = 2
	LOW = 3
	MEDium = 4


# noinspection SpellCheckingInspection
class PowAlcStateWithExtAlc(Enum):
	"""10 Members, _0 ... PRESet"""
	_0 = 0
	_1 = 1
	AUTO = 2
	EALC = 3
	OFF = 4
	OFFTable = 5
	ON = 6
	ONSample = 7
	ONTable = 8
	PRESet = 9


# noinspection SpellCheckingInspection
class PowAttMode(Enum):
	"""5 Members, AUTO ... NORMal"""
	AUTO = 0
	FIXed = 1
	HPOWer = 2
	MANual = 3
	NORMal = 4


# noinspection SpellCheckingInspection
class PowAttModeOut(Enum):
	"""2 Members, AUTO ... FIXed"""
	AUTO = 0
	FIXed = 1


# noinspection SpellCheckingInspection
class PowAttRfOffMode(Enum):
	"""2 Members, FATTenuation ... UNCHanged"""
	FATTenuation = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class PowAttStepArt(Enum):
	"""2 Members, ELECtronic ... MECHanical"""
	ELECtronic = 0
	MECHanical = 1


# noinspection SpellCheckingInspection
class PowCntrlSelect(Enum):
	"""8 Members, SENS1 ... SENSor4"""
	SENS1 = 0
	SENS2 = 1
	SENS3 = 2
	SENS4 = 3
	SENSor1 = 4
	SENSor2 = 5
	SENSor3 = 6
	SENSor4 = 7


# noinspection SpellCheckingInspection
class PowHarmMode(Enum):
	"""3 Members, _1 ... ON"""
	_1 = 0
	AUTO = 1
	ON = 2


# noinspection SpellCheckingInspection
class PowLevBehaviour(Enum):
	"""7 Members, AUTO ... USER"""
	AUTO = 0
	CPHase = 1
	CVSWr = 2
	HDUN = 3
	MONotone = 4
	UNINterrupted = 5
	USER = 6


# noinspection SpellCheckingInspection
class PowLevMode(Enum):
	"""3 Members, LOWDistortion ... NORMal"""
	LOWDistortion = 0
	LOWNoise = 1
	NORMal = 2


# noinspection SpellCheckingInspection
class PowSensDisplayPriority(Enum):
	"""2 Members, AVERage ... PEAK"""
	AVERage = 0
	PEAK = 1


# noinspection SpellCheckingInspection
class PowSensFiltType(Enum):
	"""3 Members, AUTO ... USER"""
	AUTO = 0
	NSRatio = 1
	USER = 2


# noinspection SpellCheckingInspection
class PowSensSource(Enum):
	"""4 Members, A ... USER"""
	A = 0
	B = 1
	RF = 2
	USER = 3


# noinspection SpellCheckingInspection
class PulsMode(Enum):
	"""4 Members, DOUBle ... SINGle"""
	DOUBle = 0
	PHOPptrain = 1
	PTRain = 2
	SINGle = 3


# noinspection SpellCheckingInspection
class PulsTransType(Enum):
	"""2 Members, FAST ... SMOothed"""
	FAST = 0
	SMOothed = 1


# noinspection SpellCheckingInspection
class PulsTrigModeWithSingle(Enum):
	"""5 Members, AUTO ... SINGle"""
	AUTO = 0
	EGATe = 1
	ESINgle = 2
	EXTernal = 3
	SINGle = 4


# noinspection SpellCheckingInspection
class RecScpiCmdMode(Enum):
	"""4 Members, AUTO ... OFF"""
	AUTO = 0
	DAUTo = 1
	MANual = 2
	OFF = 3


# noinspection SpellCheckingInspection
class RepeatMode(Enum):
	"""2 Members, CONTinuous ... SINGle"""
	CONTinuous = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class RfFreqMultCcorMode(Enum):
	"""3 Members, HPRecision ... STANdard"""
	HPRecision = 0
	NONE = 1
	STANdard = 2


# noinspection SpellCheckingInspection
class Rosc1GoUtpFreqMode(Enum):
	"""3 Members, DER1G ... OFF"""
	DER1G = 0
	LOOPthrough = 1
	OFF = 2


# noinspection SpellCheckingInspection
class RoscFreqExt(Enum):
	"""4 Members, _100MHZ ... VARiable"""
	_100MHZ = 0
	_10MHZ = 1
	_1GHZ = 2
	VARiable = 3


# noinspection SpellCheckingInspection
class RoscOutpFreqMode(Enum):
	"""4 Members, DER100M ... OFF"""
	DER100M = 0
	DER10M = 1
	LOOPthrough = 2
	OFF = 3


# noinspection SpellCheckingInspection
class Rs232BdRate(Enum):
	"""7 Members, _115200 ... _9600"""
	_115200 = 0
	_19200 = 1
	_2400 = 2
	_38400 = 3
	_4800 = 4
	_57600 = 5
	_9600 = 6


# noinspection SpellCheckingInspection
class Rs232StopBits(Enum):
	"""2 Members, _1 ... _2"""
	_1 = 0
	_2 = 1


# noinspection SpellCheckingInspection
class SelftLev(Enum):
	"""3 Members, CUSTomer ... SERVice"""
	CUSTomer = 0
	PRODuction = 1
	SERVice = 2


# noinspection SpellCheckingInspection
class SelftLevWrite(Enum):
	"""4 Members, CUSTomer ... SERVice"""
	CUSTomer = 0
	NONE = 1
	PRODuction = 2
	SERVice = 3


# noinspection SpellCheckingInspection
class SelOutpMarkUser(Enum):
	"""2 Members, MARK ... USER"""
	MARK = 0
	USER = 1


# noinspection SpellCheckingInspection
class SelOutpVxAxis(Enum):
	"""4 Members, S0V25 ... XAXis"""
	S0V25 = 0
	S0V5 = 1
	S1V0 = 2
	XAXis = 3


# noinspection SpellCheckingInspection
class SingExtAuto(Enum):
	"""8 Members, AUTO ... SINGle"""
	AUTO = 0
	BUS = 1
	DHOP = 2
	EAUTo = 3
	EXTernal = 4
	HOP = 5
	IMMediate = 6
	SINGle = 7


# noinspection SpellCheckingInspection
class SlopeType(Enum):
	"""2 Members, NEGative ... POSitive"""
	NEGative = 0
	POSitive = 1


# noinspection SpellCheckingInspection
class SourceInt(Enum):
	"""2 Members, EXTernal ... INTernal"""
	EXTernal = 0
	INTernal = 1


# noinspection SpellCheckingInspection
class Spacing(Enum):
	"""3 Members, LINear ... RAMP"""
	LINear = 0
	LOGarithmic = 1
	RAMP = 2


# noinspection SpellCheckingInspection
class StagMode(Enum):
	"""3 Members, AUTO ... USER"""
	AUTO = 0
	FIXed = 1
	USER = 2


# noinspection SpellCheckingInspection
class StateExtended(Enum):
	"""6 Members, _0 ... ON"""
	_0 = 0
	_1 = 1
	_2 = 2
	DEFault = 3
	OFF = 4
	ON = 5


# noinspection SpellCheckingInspection
class SweCyclMode(Enum):
	"""2 Members, SAWTooth ... TRIangle"""
	SAWTooth = 0
	TRIangle = 1


# noinspection SpellCheckingInspection
class SweepType(Enum):
	"""2 Members, ADVanced ... STANdard"""
	ADVanced = 0
	STANdard = 1


# noinspection SpellCheckingInspection
class SweMarkActive(Enum):
	"""11 Members, M01 ... NONE"""
	M01 = 0
	M02 = 1
	M03 = 2
	M04 = 3
	M05 = 4
	M06 = 5
	M07 = 6
	M08 = 7
	M09 = 8
	M10 = 9
	NONE = 10


# noinspection SpellCheckingInspection
class Test(Enum):
	"""4 Members, _0 ... STOPped"""
	_0 = 0
	_1 = 1
	RUNning = 2
	STOPped = 3


# noinspection SpellCheckingInspection
class TestCalSelected(Enum):
	"""2 Members, _0 ... _1"""
	_0 = 0
	_1 = 1


# noinspection SpellCheckingInspection
class TraceSourceAll(Enum):
	"""8 Members, HOLD ... SEN4"""
	HOLD = 0
	OFF = 1
	ON = 2
	REF = 3
	SEN1 = 4
	SEN2 = 5
	SEN3 = 6
	SEN4 = 7


# noinspection SpellCheckingInspection
class TrigSweepImmBusExt(Enum):
	"""3 Members, BUS ... IMMediate"""
	BUS = 0
	EXTernal = 1
	IMMediate = 2


# noinspection SpellCheckingInspection
class TrigSweepSourNoHopExtAuto(Enum):
	"""5 Members, AUTO ... SINGle"""
	AUTO = 0
	BUS = 1
	EXTernal = 2
	IMMediate = 3
	SINGle = 4


# noinspection SpellCheckingInspection
class UnchOff(Enum):
	"""2 Members, OFF ... UNCHanged"""
	OFF = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class UnitAngle(Enum):
	"""3 Members, DEGree ... RADian"""
	DEGree = 0
	DEGRee = 1
	RADian = 2


# noinspection SpellCheckingInspection
class UnitPower(Enum):
	"""3 Members, DBM ... V"""
	DBM = 0
	DBUV = 1
	V = 2


# noinspection SpellCheckingInspection
class UnitPowSens(Enum):
	"""3 Members, DBM ... WATT"""
	DBM = 0
	DBUV = 1
	WATT = 2


# noinspection SpellCheckingInspection
class UnitSpeed(Enum):
	"""4 Members, KMH ... NMPH"""
	KMH = 0
	MPH = 1
	MPS = 2
	NMPH = 3


# noinspection SpellCheckingInspection
class UpDownDirection(Enum):
	"""2 Members, DOWN ... UP"""
	DOWN = 0
	UP = 1


# noinspection SpellCheckingInspection
class UpdPolicyMode(Enum):
	"""3 Members, CONFirm ... STRict"""
	CONFirm = 0
	IGNore = 1
	STRict = 2
