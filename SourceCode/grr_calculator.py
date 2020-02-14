#!/usr/bin/env python
# -*- coding: utf-8 -*-  

"""
@desc:  
@version: python2.7
@author: Xiaosu Liao
@license: LGPL Licence 
@contact: xsliao@colibri.com.cn
@site: 
@software: PyCharm Community Edition
@file: grr_calculator.py
@time: 2018/5/8 9:15
"""

import os

import numpy as np
import pandas as pd
import psutil

from Range_GRR import GRR


# import objgraph

def memory_usage():
	"""Return the memory usage of the current python process."""
	return psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2


class GrrCalculator(object):
	def __init__(self, raw_df, num_parts=10, num_operators=3, num_trials=3):
		self._op_num = num_operators  # number of operators
		self._part_num = num_parts  # number of parts/ sample size
		self._trials_num = num_trials  #
		try:
			self._raw_df = self._normalize(raw_df)
		except Exception:
			return
		# self._raw_df = raw_df
		self._sns = set(self._raw_df['SN'])
		self._ops = set(self._raw_df['Operator'])

		self._init_args()

	def _init_args(self):
		# TODO(xsliao:) Those constants should be lookup in the table
		# TODO(2018-5-8) according to the numbers of appraisers/parts/trials
		self.d2_star_EV = 1.693
		self.d2_star_AV = 1.91
		self.d2_star_PV = 3.18
		self.d4 = 2.575  # trials = 3
		self.a2 = 1.023  # trials = 3

		self.UCL_x = 0.0
		self.LCL_x = 0.0
		self.UCL_r = 0.0
		self.LCL_r = 0.0

		# list for every op
		self._app_a_ave = []
		self._app_b_ave = []
		self._app_c_ave = []
		self._app_a_range = []
		self._app_b_range = []
		self._app_c_range = []
		self._part_ave = []

		self._xbar_a = 0.0
		self._xbar_b = 0.0
		self._xbar_c = 0.0
		self.xbar_diff = 0.0
		self._rbar_a = 0.0
		self._rbar_b = 0.0
		self._rbar_c = 0.0

		self.x_double_bar = 0.0
		self.r_double_bar = 0.0
		self.rp = 0.0  # Range parts
		self.ro = 0.0  # Range operators

	def _normalize(self, df):
		self._tmp_df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()) if not x.dtype == object else x)
		return self._tmp_df

	def _get_average_by_appraiser_and_part(self, item, op, sn):
		self._curdata = self._raw_df[item][(self._raw_df['Operator'] == op) & (self._raw_df['SN'] == sn)]
		retval = self._curdata.mean()
		return retval

	def _get_range_by_appraiser_and_part(self, item, op, sn):
		self._curdata = self._raw_df[item][(self._raw_df['Operator'] == op) & (self._raw_df['SN'] == sn)]
		retval = self._curdata.ptp()
		return retval

	def _get_averages_by_operator(self, item, op):
		"Reference: Table: VariablegaugeRandR: App(A/B/C)Ave"
		retlist = []
		for sn in self._sns:
			rstval = self._get_average_by_appraiser_and_part(item, op, sn)
			retlist.append(rstval)

		return retlist

	def _get_ranges_by_operator(self, item, op):
		"Reference: Table: VariablegaugeRandR: App(A/B/C)Range"
		retlist = []
		for sn in self._sns:
			rstval = self._get_range_by_appraiser_and_part(item, op, sn)
			retlist.append(rstval)

		return retlist

	def _get_xbar_by_operator(self, item, op):
		"Reference: Table: VariablegaugeRandR: Xbar(A/B/C)"
		rstlist = self._get_averages_by_operator(item, op)
		retval = np.mean(rstlist)
		return retval

	def _get_rbar_by_operator(self, item, op):
		"Reference: Table: VariablegaugeRandR: Rbar(A/B/C)"
		rstlist = self._get_ranges_by_operator(item, op)
		retval = np.mean(rstlist)
		return retval

	def _cal_parts_average(self, item):
		"Reference: Table: VariablegaugeRandR: Part Average"
		rstlist = []
		for sn in self._sns:
			tmplist = []
			for op in self._ops:
				rstval = self._get_average_by_appraiser_and_part(item, op, sn)
				tmplist.append(rstval)
			rstlist.append(np.mean(tmplist))

		self._part_ave = rstlist

	def _cal_x_doublebar(self, item):
		self.x_double_bar = np.mean(self._part_ave)

	def _cal_r_doublebar(self, item):
		self.r_double_bar = np.sum([self._rbar_a, self._rbar_b, self._rbar_c]) / self._op_num

	def _cal_rp(self, item):
		self.rp = np.ptp(self._part_ave)

	def _cal_ro(self, item):
		self.ro = np.ptp([self._xbar_a, self._xbar_b, self._xbar_c])

	def _cal_x_bar_diff(self, item):
		xbarmin = np.min([self._xbar_a, self._xbar_b, self._xbar_c])
		xbarmax = np.max([self._xbar_a, self._xbar_b, self._xbar_c])
		self.xbar_diff = xbarmax - xbarmin

	def calculate_grr(self, item, df, lsl, uls):
		self._init_args()

		self._app_a_ave = self._get_averages_by_operator(item, 'OP1')
		self._app_b_ave = self._get_averages_by_operator(item, 'OP2')
		self._app_c_ave = self._get_averages_by_operator(item, 'OP3')

		self._app_a_range = self._get_ranges_by_operator(item, 'OP1')
		self._app_b_range = self._get_ranges_by_operator(item, 'OP2')
		self._app_c_range = self._get_ranges_by_operator(item, 'OP3')

		self._cal_parts_average(item)

		self._xbar_a = self._get_xbar_by_operator(item, 'OP1')
		self._xbar_b = self._get_xbar_by_operator(item, 'OP2')
		self._xbar_c = self._get_xbar_by_operator(item, 'OP3')
		self._cal_x_bar_diff(item)

		self._rbar_a = self._get_rbar_by_operator(item, 'OP1')
		self._rbar_b = self._get_rbar_by_operator(item, 'OP2')
		self._rbar_c = self._get_rbar_by_operator(item, 'OP3')

		self._cal_x_doublebar(item)
		self._cal_r_doublebar(item)
		self._cal_rp(item)
		self._cal_ro(item)
		#         print "-------------------"
		#         print item
		#         print "-------------------"

		self.LCL_x = self.x_double_bar - (self.r_double_bar * self.a2)
		self.UCL_x = self.x_double_bar + (self.r_double_bar * self.a2)
		self.LCL_r = 0  # LCL is zero with < 8 trials
		self.UCL_r = self.r_double_bar * self.d4

		# Repeatability, Equipment Variation
		#         self.EV = self.r_double_bar / self.d2_star_EV
		#         # Reproducibility, Appraiser(Operator) Variation
		#         tmp = (self.ro / self.d2_star_AV)**2 - ((self.EV**2) / (self._trials_num * self._part_num))
		#         self.AV = 0 if tmp < 0 else np.sqrt(tmp)
		#         # Repeatability & Reproducibility
		#         self.GRR = np.sqrt(self.EV**2 + self.AV**2)
		#         # Product variation
		#         self.PV = self.rp / self.d2_star_PV
		#         # Toatl variation
		#         self.TV = np.sqrt(self.EV**2 + self.AV**2 + self.PV**2)
		#         self.NDC = self.GRR and (self.PV / self.GRR) * 1.41

		self.EV, self.AV, self.GRR, self.PV, self.TV, self.NDC, self.precision_tolerance_ratio = GRR(df, lsl, uls)
		self.lsl = lsl
		self.uls = uls

		# Component Variance Method (% of Total Variation)
		self.EV_percent = self.TV and 100 * (self.EV ** 2 / self.TV ** 2)
		self.AV_percent = self.TV and 100 * (self.AV ** 2 / self.TV ** 2)
		self.GRR_percent = self.TV and 100 * (self.GRR ** 2 / self.TV ** 2)
		self.PV_percent = self.TV and 100 * (self.PV ** 2 / self.TV ** 2)

	def test(self):
		item = 'SFR_110lp_60IH_TL_H'
		self.calculate_grr(item)


if __name__ == '__main__':
	# filename = r'E:\GRR\data\Downloads\C1_test\clifford_phase\GRR_C1_Combo1_01_phase_01_out.csv'
	filename = r'/media/xsliao/0001A3DF0001D948/GRR/data/Downloads/C1_test\clifford_phase\GRR_C1_C\ombo1_01_phase_01_out.csv'
	try:
		raw_df = pd.read_csv(filename)
	except Exception:
		print 'exceptions occured when read csv file to DataFrame'

	grr_calculator = GrrCalculator(raw_df)
	grr_calculator.test()
	print 'hi'
