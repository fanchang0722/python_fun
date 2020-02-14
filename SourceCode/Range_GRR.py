import numpy as np
import pandas as pd


def GRR(df, LSL, USL):
	columns = df.columns
	"""columns[0]=SN"""
	dfPartMean = df.groupby(columns[0]).mean()

	"""columns[1]=Operator"""
	dfMean = df.groupby([columns[1], columns[0]]).mean()

	"""columns[2]=Metrics"""
	Xbar = dfMean.groupby(columns[1])[columns[2]].mean()

	dfMax = df.groupby([columns[1], columns[0]]).max()
	dfMin = df.groupby([columns[1], columns[0]]).min()
	Range = dfMax[columns[2]] - dfMin[columns[2]]
	Rbar = Range.groupby(columns[1]).mean()
	Rbarbar = Rbar.mean()
	Xbardiff = Xbar.max() - Xbar.min()
	RP = (dfPartMean.max() - dfPartMean.min())[columns[2]]
	D4 = 2.58
	UCL = D4 * Rbarbar
	K1 = 0.5908
	EV = Rbarbar * K1
	numOfparts = 10
	numOftrials = 3
	K2 = 0.5231
	#     print Xbardiff
	#     print "(Xbardiff*K2)**2-EV**2/(numOfparts*numOftrials) : ",(Xbardiff*K2)**2-EV**2/(numOfparts*numOftrials)
	AV = np.sqrt((Xbardiff * K2) ** 2 - EV ** 2 / (numOfparts * numOftrials))
	if np.isnan(AV):
		AV = 0
	GRR = np.sqrt(EV ** 2 + AV ** 2)
	if np.isnan(GRR):
		GRR = 0
	K3 = 0.3146
	PV = RP * K3
	TV = np.sqrt(GRR ** 2 + PV ** 2)

	#
	# print dfPartMean
	# print dfMean
	# print Xbar
	# print dfMax[columns[2]]-dfMin[columns[2]]
	# print Range
	# print Xbar
	# print Rbar
	# print Rbarbar
	# print Xbardiff
	# print UCL
	# print RP
	print 'EV -->', EV
	print 'AV -->', AV
	print 'GRR -->', GRR
	print 'PV -->', PV
	print 'TV -->', TV
	print 'ndc -->', 1.41 * PV / GRR
	ndc = np.ceil(1.41 * PV / GRR)
	if np.isnan(ndc):
		ndc = 0
	print 'precision/tolerance ratio --> ', round(600 * GRR / (USL - LSL), 3)
	if np.isnan(round(600 * GRR / (USL - LSL), 3)):
		return EV, AV, GRR, PV, TV, ndc, 0
	else:
		return EV, AV, GRR, PV, TV, ndc, round(600 * GRR / (USL - LSL), 3)


if __name__ == '__main__':
	filename = r'/Users/liaoying/Documents/workspace/ComboGrr/clifford_phase/calibration_phase_01_out.csv'
	df = pd.read_csv(filename)
	# print df.head(5)
	print df
	columns = df.columns
	print columns
	print len(columns)
	newdf = df[df.columns[[1, 2, 3]]]
	print newdf
	GRR(newdf, .34, 1)
