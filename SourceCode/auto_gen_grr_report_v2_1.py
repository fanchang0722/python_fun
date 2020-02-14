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
@file: auto_gen_grr_report_v2_0.py
@time: 2018/5/7 9:09
"""

import argparse
import gc
import json

import matplotlib
import numpy as np
import pandas as pd

from grr_calculator import GrrCalculator

# gc.set_debug(gc.DEBUG_STATS|gc.DEBUG_LEAK)
matplotlib.use('PDF')
import matplotlib.pyplot as plt
import cStringIO
from pdf_image import PdfImage

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.graphics.shapes import *
from reportlab.platypus import PageBreak

styles = getSampleStyleSheet()

from Tkinter import *

# Constant values
K1 = 3.05  # r=3 replicates(Trials)
K2 = 2.70  # 3 appraisers
K3 = 1.62  # 10 parts
D4 = 2.575  # D4 table value for 3 operators
D3 = 0  # D3 table value for 3 operators
A2 = 1.023  # A2 table value for 3 operators
"""
Range:
    UCL = D4*Range_mean
    LCL = D3*Range_mean
Xbar:
    UCL = Xbar_mean + A2*Range_mean 
    LCL = Xbar_mean - A2*Range_mean

"""

Title = "Hello world"
pageinfo = u"Gage Capability R&R Study "
PAGE_HEIGHT = 400
ois_option = ['shift1', 'shift2']


class AutoGenGrrReport(object):

	def __init__(self, grr_root_dir):
		self._grr_root_dir = grr_root_dir
		self._story = [Spacer(1, 0.01 * inch)]
		path = os.path.split(grr_root_dir)
		self._pdf_doc_dir = os.path.join(path[0], 'GrrReport.pdf')
		self.current_location = path[0]
		self._doc = SimpleDocTemplate(self._pdf_doc_dir,
		                              pagesize=A4,
		                              pageCompression=0,
		                              topMargin=2.54 * cm,
		                              bottomMargin=2.54 * cm,
		                              leftMargin=1.91 * cm,
		                              rightMargin=1.91 * cm)

		print os.path.split(grr_root_dir)
		self._grr_calculator = None
		self._grr_cal_records = [['Num',
		                          'Item',
		                          'Repeatability',
		                          'Reproducibility',
		                          'NDC',
		                          'RR',
		                          'Result'
		                          ]]

		self._current_df = None

		self.fig = plt.figure()
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)

	def _get_spec(self, spec):
		value_list = spec.split("'")
		if "==" not in spec:
			lsl = float(value_list[1].split("<=")[0].strip())
			uls = float(value_list[1].split("<=")[-1].strip())
			return lsl, uls
		else:
			print spec
			lsl = float(value_list[1].split("==")[1].strip())
			uls = float(value_list[1].split("==")[1].strip())
			return lsl, uls

	def _get_station(self, station_id):
		file_name = os.path.join(self.current_location, station_id + ".csv")
		try:
			print file_name
			df = pd.read_csv(file_name)
			print df
			print np.array(df['item'])
			return np.array(df['item'])
		except Exception:
			print 'exceptions occured when read csv file to DataFrame'
			return None

	def analyze_grr(self, station=None):
		# self._add_heading_1('2 Details')
		item_counter = 0
		for index in range(self.total_index):
			item_test = 0

			# if item_counter > 5:
			#     break
			path = os.path.split(self._grr_root_dir)
			filename = os.path.join("%s_phase_%02d_out.csv" % (path[1], index))
			item_list = []
			item_list = self._get_station(station)

			print "++++++++=", item_list
			print len(item_list)
			if filename.endswith('csv'):
				cur_filename_absolute = os.path.join(self._phase_csv_dir, filename)
				print 'Current file name: %s' % cur_filename_absolute

				if not self._import_data(cur_filename_absolute):
					continue

				if not self._import_limits_data(os.path.join(self._spec_dir, "spec_%02d.csv" % index)):
					continue

				self._grr_calculator = GrrCalculator(self._current_df)  # Implementation GRR Calculator
				columns = self._current_df.columns
				columns = list(columns.drop('Station', 1))

				for item_ind, item in enumerate(columns):
					unanmed_str = 'Unnamed: %s' % (item_ind + 1)
					if item in ['SN', 'Operator', 'Station', 'Unnamed', ':', unanmed_str]:
						continue

					item_test += 1
					if (item in item_list):
						item_counter += 1

						print 'item counter: %s' % item_counter

						try:
							lsl, uls = self._get_spec(str(self._current_limits_df[item][0]))
							print lsl, uls
						except Exception:
							continue
						newdf = self._current_df[self._current_df.columns[[1, 2, item_test + 2]]]
						self._grr_calculator.calculate_grr(item, newdf, lsl, uls)  # GRR Calculation
						tag = "item_tag_%s" % item_counter
						self._add_item_link('2.%s %s' % (item_counter, item,), tag)
						self._add_all_plot(item)
						self._add_grr_result_table()  # Add result table
						self._update_grr_records(item_counter, item)  # Update global grr calculation records
				else:
					print "missing ", item
		self._add_total_result_table()
		self._doc.build(self._story, onLaterPages=self._myLaterPages)
		# self._doc.multiBuild()

	def _import_data(self, filename):
		"""Import data and calculate the X bar and range bar, store to xf_df for return"""
		try:
			self._current_df = pd.read_csv(filename)
			return True
		except Exception:
			print 'exceptions occured when read csv file to DataFrame'
			return False

	def _import_limits_data(self, filename):
		"""Import limits data from spec file"""
		try:
			self._current_limits_df = pd.read_csv(filename)
			return True
		except Exception:
			print 'exceptions occured when read csv file to DataFrame'
			return False

	def _update_grr_records(self, item_counter, item):
		if self._grr_calculator.precision_tolerance_ratio < 10:
			result = 'Excellent'
		elif self._grr_calculator.precision_tolerance_ratio > 10 and self._grr_calculator.precision_tolerance_ratio <= 20:
			result = 'Adequate'
		elif self._grr_calculator.precision_tolerance_ratio > 20 and self._grr_calculator.precision_tolerance_ratio <= 30:
			result = 'Marginally Acceptable'
		else:
			result = 'Unacceptable'

		tag = "item_tag_%s" % item_counter
		itemstr = '<a href="%s" color="blue">%s</a>' % (tag, item,)
		style = styles['Normal']
		p = Paragraph(itemstr, style)
		self._grr_cal_records.append([item_counter, p,
		                              self._format_data(self._grr_calculator.EV_percent, 4),
		                              self._format_data(self._grr_calculator.AV_percent, 4),
		                              self._format_data(self._grr_calculator.NDC, 1),
		                              self._format_data(self._grr_calculator.precision_tolerance_ratio, 4),
		                              result])

	def _parse_clifford_json_to_csv(self):
		path = os.path.split(self._grr_root_dir)
		station = path[1]
		self._csv_dir = os.path.join(path[0], 'clifford_csvs')
		if not os.path.exists(self._csv_dir):
			os.mkdir(self._csv_dir, 0755)

		self._spec_dir = os.path.join(path[0], 'spec_csv')
		if not os.path.exists(self._spec_dir):
			os.mkdir(self._spec_dir, 0755)

		for sub_folder in os.listdir(self._grr_root_dir):
			if sub_folder == 'clifford_csvs' or sub_folder.startswith('.'):
				continue
			op = sub_folder
			count = 0
			meas = 0

			current_op_folder = os.path.join(self._grr_root_dir, sub_folder)
			for filename in os.listdir(current_op_folder):
				# TODO(xsliao): should cleaning the filename to delete the Error file
				if filename.endswith('json'):
					meas += 1
					count += 1

					current_filename_absolute = os.path.join(current_op_folder, filename)
					sn = filename.split('_')[1]
					with open(current_filename_absolute, 'r') as fp:
						result = fp.read()

					parsed_json = json.loads(result)
					key = 'phases'
					subkey = 'measurements'
					index = 1
					self.total_index = len(parsed_json[key])
					for idx in range(len(parsed_json[key])):
						self.out_spec_file = os.path.join(self._spec_dir, "spec_%02d.csv" % idx)
						out_filename = os.path.join(self._csv_dir,
						                            sn + ("_%s_measurement%d_%02d.csv" % (op, meas, idx)))
						file_spec = open(self.out_spec_file, "w")
						#                         spec_temp = ""
						#                         spec_temp2 = ""
						fp = open(out_filename, 'w')
						if parsed_json[key][idx]['measurements']:
							temp = 'Station,SN,Operator,'
							temp2 = station + ',' + filename.split('_')[1] + ',' + op + ','
							spec_temp = 'Station,SN,Operator,'
							spec_temp2 = station + ',' + filename.split('_')[1] + ',' + op + ','
							for subkey in parsed_json[key][idx]['measurements'].keys():
								#                                 print parsed_json[key][idx]['measurements'][subkey].values()
								temp += str(parsed_json[key][idx]['measurements'][subkey].values()[2]) + ','
								spec_temp += str(parsed_json[key][idx]['measurements'][subkey].values()[2]) + ','
								temp2 += str(parsed_json[key][idx]['measurements'][subkey].values()[1]) + ','
								spec_temp2 += str(parsed_json[key][idx]['measurements'][subkey].values()[3]) + ','

							index += 1
							fp.writelines(temp + '\r\n')
							fp.writelines(temp2 + '\r\n')
							file_spec.writelines(spec_temp + '\r\n')
							file_spec.writelines(spec_temp2 + '\r\n')
						#                             print spec_temp
						#                             print spec_temp2
						fp.close()
						file_spec.close()

	def _combine_clifford_csvs_to_phase(self):
		for idx in range(self.total_index):
			count = 0
			if idx > 9:
				endstring = str(idx)
			else:
				endstring = '0' + str(idx)

			path = os.path.split(self._grr_root_dir)
			self._phase_csv_dir = os.path.join(path[0], 'clifford_phase')
			if not os.path.exists(self._phase_csv_dir):
				os.mkdir(self._phase_csv_dir)

			footnote = '%s_phase_%s_out.csv' % (path[1], endstring,)
			outfilename = os.path.join(self._phase_csv_dir, footnote)
			fout = open(outfilename, 'w')
			for filename in os.listdir(self._csv_dir):
				if filename.endswith(endstring + '.csv'):
					current_filename_absolute = os.path.join(self._csv_dir, filename)
					if os.path.exists(current_filename_absolute):
						fp = open(current_filename_absolute, 'r')
						header = fp.readline().rstrip('\r\n')
						result = fp.readline().rstrip('\r\n')
						fp.close()
						if count == 0:
							fout.writelines(header + '\r\n')
							fout.writelines(result + '\r\n')
						else:
							fout.writelines(result + '\r\n')
						count += 1
			fout.close()

	def pares_clifford_grr_data(self):
		self._parse_clifford_json_to_csv()
		self._combine_clifford_csvs_to_phase()

	def _format_data(self, f, n):
		if f is None:
			return None
		elif f == 0:
			return 0.0
		elif np.isnan(f):
			return -1

		return f

	#         if round(f) == f:
	#             m = len(str(f)) - 1 - n
	#             if f / (10 ** m) == 0.0:
	#                 return f
	#             else:
	#                 return float(int(f) / (10 ** m) * (10 ** m))
	#         return round(f, n - len(str(int(f)))) if len(str(f)) > n + 1 else f

	def _add_title(self, content, debug=False):
		style = styles['Title']
		p = Paragraph(content, style)
		if debug:
			p._showBoundary = True
		self._story.append(p)

	def _add_heading_1(self, content, debug=False):
		heading1_style = styles['Heading1']
		p = Paragraph(content, heading1_style)
		if debug:
			p._showBoundary = True
		self._story.append(p)

	def _add_heading_2(self, content, debug=False):
		heading2_style = styles['Heading2']
		p = Paragraph(content, heading2_style)
		if debug:
			p._showBoundary = True
		self._story.append(p)

	def _add_heading_3(self, content, debug=False):
		heading3_style = styles['Heading3']
		p = Paragraph(content, heading3_style)
		if debug:
			p._showBoundary = True
		self._story.append(p)

	def _add_normal_content(self, content, debug=False):
		style = styles['Normal']
		style.spaceAfter = 10
		style.spaceBefore = 10
		p = Paragraph(content, style)
		if debug:
			p._showBoundary = True
		self._story.append(p)

	def _add_item_link(self, content, tag, debug=False):
		content_link = '<a name="%s"/>%s' % (tag, content)
		self._add_heading_3(content_link, debug)

	def _plot_xbar(self):

		# Plot 1: xbar chart
		averages = [self._grr_calculator._app_a_ave,
		            self._grr_calculator._app_b_ave,
		            self._grr_calculator._app_c_ave]

		print averages
		self.ax_1 = plt.subplot(321)
		ind_point = 1
		x_ticks_pos = []
		for avg_ind, avg in enumerate(averages):
			y = avg
			length = len(avg)
			x = np.linspace(ind_point, ind_point + length - 1, length)
			x_ticks_pos.append(ind_point + length / 2)
			ind_point += length
			plt.plot(x, y, 'o-', linewidth=1, markersize=3)

		plt.xticks(x_ticks_pos, ['OP1', 'OP2', 'OP3'], fontsize=8)
		plt.title('Xbar chart', fontsize=8)
		plt.ylabel('Sample Range', fontsize=8)
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)

		ymin, ymax = plt.ylim()
		plt.vlines(x=[10, 20], ymin=ymin, ymax=ymax, color='black', linewidth=0.5)

		xmin, xmax = plt.xlim()
		plt.hlines(xmin=xmin, xmax=xmax,
		           y=[self._grr_calculator.LCL_x, self._grr_calculator.UCL_x],
		           color='red', linewidth=1)
		plt.hlines(xmin=xmin, xmax=xmax,
		           y=self._grr_calculator.x_double_bar,
		           color='green', linewidth=1)

	def _plot_rbar(self):
		# Plot 2: rbar chart
		ranges = [self._grr_calculator._app_a_range,
		          self._grr_calculator._app_b_range,
		          self._grr_calculator._app_c_range]

		self.ax_2 = plt.subplot(322)
		ind_point = 1
		x_ticks_pos = []
		for range_ind, range in enumerate(ranges):
			y = range
			length = len(range)
			x = np.linspace(ind_point, ind_point + length - 1, length)
			x_ticks_pos.append(ind_point + length / 2)
			ind_point += length
			plt.plot(x, y, 'o-', linewidth=1, markersize=3)
		plt.title('Rbar chart', fontsize=8)
		plt.ylabel('Sample Range', fontsize=8)
		plt.xticks(x_ticks_pos, ['OP1', 'OP2', 'OP3'], fontsize=8)
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)

		ymin, ymax = plt.ylim()
		plt.vlines(x=[10, 20], ymin=ymin, ymax=ymax, color='black', linewidth=0.5)

		xmin, xmax = plt.xlim()
		plt.hlines(xmin=xmin, xmax=xmax,
		           y=[self._grr_calculator.LCL_r, self._grr_calculator.UCL_r],
		           color='red', linewidth=1)
		plt.hlines(xmin=xmin, xmax=xmax,
		           y=self._grr_calculator.r_double_bar,
		           color='green', linewidth=1)

	def _plot_measurement_by_parts(self, item):
		# plot 3: Measurement by Parts'
		# raw_df = self._current_df
		sns = set(self._current_df['SN'])

		self.ax_3 = plt.subplot(323)
		meanvals = []
		for sn_ind, sn in enumerate(sns):
			curdata = self._current_df[item][self._current_df['SN'] == sn]
			curdata = curdata.values
			meanvals.append(np.mean(curdata))
			length = len(curdata)
			# plt.plot(np.repeat((sn_ind + 1), length), curdata, 'o', markerfacecolor='none', markersize=5)
			plt.plot(np.repeat((sn_ind + 1), length), curdata, 'o', markersize=2)
		plt.plot(xrange(1, len(meanvals) + 1), meanvals, 'r-', linewidth=0.6, markerfacecolor='none', markersize=3)
		plt.title('Measurement by Parts', fontsize=8)
		plt.ylabel('Sample Mean', fontsize=8)
		# plt.grid(True)
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)

	def _plot_measurement_by_operatoros(self, item):
		# plot 4: Measurement by Operators
		self.ax_4 = plt.subplot(324)
		# raw_df = self._current_df
		ops = set(self._current_df['Operator'])
		meanvals = []
		for op_ind, op in enumerate(ops):
			curdata = self._current_df[item][self._current_df['Operator'] == op]
			curdata = curdata.values
			meanvals.append(np.mean(curdata))
			length = len(curdata)
			# plt.plot(np.repeat((op_ind + 1), length), curdata, 'o', markerfacecolor='none', markersize=5)
			plt.plot(np.repeat((op_ind + 1), length), curdata, 'o', markersize=2)
		plt.plot(xrange(1, len(meanvals) + 1), meanvals, 'r-', linewidth=0.6, markerfacecolor='none', markersize=3)
		plt.title('Measurement by Operators', fontsize=8)
		plt.xticks([1, 2, 3], ['OP1', 'OP2', 'OP3'], fontsize=8)
		plt.yticks(fontsize=8)
		plt.xticks(fontsize=8)

	def _plot_operators_parts_interaction(self, item):
		# plot 5: Operaotrs * Parts Interaction
		averages = [self._grr_calculator._app_a_ave,
		            self._grr_calculator._app_b_ave,
		            self._grr_calculator._app_c_ave]

		self.ax_5 = plt.subplot(325)
		linestyles = ['o-', 's-', '*-', '+-', 'x-']
		hs = []
		for avg_ind, avg in enumerate(averages):
			x = np.linspace(1, len(avg), len(avg))
			y = avg
			length = len(avg)
			h = plt.plot(x, y, linestyles[avg_ind], linewidth=1, markersize=4, markerfacecolor='none')
			hs.append(h)

		plt.title('Operators*parts Interaction', fontsize=8)
		plt.ylabel('Average', fontsize=8)
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)
		plt.legend(['OP1', 'OP2', 'Op3'], loc='best', fontsize=5)

	def _plot_result_bar_chart(self):
		x_pos = [self._grr_calculator.EV_percent,
		         self._grr_calculator.AV_percent,
		         self._grr_calculator.GRR_percent,
		         self._grr_calculator.PV_percent]
		y_pos = np.arange(4)
		y_ticks = ['Repeat', 'Reprod', 'GR&R', 'Part2Part']

		self.ax_6 = plt.subplot(326)
		plt.barh(y_pos, x_pos, align='center', ecolor='black')
		plt.yticks(np.arange(4), y_ticks, fontsize=8)
		plt.xticks(np.arange(0, 101, 20), ['0', '20', '40', '60', '80', '100'], fontsize=8)
		# plt.yticks(y_ticks)
		plt.xlabel('Percent', fontsize=8)
		plt.title('Contribution', fontsize=8)
		plt.gca().xaxis.grid(True, linewidth=1, color='black', linestyle='--')

	def _add_all_plot(self, item):
		fig = plt.figure()
		# plt.xticks(fontsize=8)
		# plt.yticks(fontsize=8)

		self._plot_xbar()
		self._plot_rbar()
		self._plot_measurement_by_parts(item)
		self._plot_measurement_by_operatoros(item)
		self._plot_operators_parts_interaction(item)
		self._plot_result_bar_chart()

		plt.tight_layout()
		imgdata = cStringIO.StringIO()
		fig.savefig(imgdata, format='PDF')
		pi = PdfImage(imgdata, width=500, height=315)
		pi._showBoundary = 1
		self._story.append(pi)

		print('pi: %s' % sys.getrefcount(pi))
		print('story: %s' % sys.getsizeof(self._story))

		fig.clear()
		plt.clf()
		plt.close('all')
		del [pi, self.ax_1, self.ax_2, self.ax_3, self.ax_4, self.ax_5, self.ax_6]
		gc.collect()
		print 'debug'
		# objgraph.show_growth()

	def _add_grr_result_table(self):
		self._add_heading_3('Conclusion')

		rstval = [
			#             ['D2*(EV)', self._grr_calculator.d2_star_EV,
			#              'XbarDiff', self._format_data(self._grr_calculator.xbar_diff, 4)],
			#             ['D2*(AV)', self._grr_calculator.d2_star_AV,
			#              'Rp', self._format_data(self._grr_calculator.rp, 4)],
			#             ['D2*(PV)', self._grr_calculator.d2_star_PV,
			#              'UCL(Rbar)', self._format_data(self._grr_calculator.UCL_r, 4)],
			#             ['A2', self._grr_calculator.a2,
			#              'LCL(Rbar)', self._format_data(self._grr_calculator.LCL_r, 4)],
			#             ['D4', self._grr_calculator.d4,
			#              'UCL(Xbar)', self._format_data(self._grr_calculator.UCL_x, 4)],
			#             ['Rbar', self._format_data(self._grr_calculator.r_double_bar, 4),
			#              'LCL(Xbar)', self._format_data(self._grr_calculator.LCL_x, 4)],
			['Measurement Source', 'StdDev (SD)', 'Description'],
			['Upper limit(ULS)', self._format_data(self._grr_calculator.uls, 8)],
			['lower limit(LSL)', self._format_data(self._grr_calculator.lsl, 8)],
			['Equipment Variation(EV, Repeatability)', self._format_data(self._grr_calculator.EV, 8)],
			['Appraiser Variation(AV, Reproducibility)', self._format_data(self._grr_calculator.AV, 8)],
			['GRR', self._format_data(self._grr_calculator.GRR, 8)],
			['Part Variation(PV)', self._format_data(self._grr_calculator.PV, 8)],
			['Total Variation(TV)', self._format_data(self._grr_calculator.TV, 8)],
			['Precision/Tolerance Ratio', self._format_data(self._grr_calculator.precision_tolerance_ratio, 8)]]

		t = Table(rstval, style=[('LINEABOVE', (0, 0), (3, 0), 2, colors.black),
		                         ('LINEABOVE', (0, 1), (3, 1), 1, colors.black),
		                         ('LINEBELOW', (0, 9), (3, 9), 1, colors.black),
		                         ('LINEBELOW', (0, -1), (3, -1), 1, colors.black),
		                         ('LEADING', (0, 0), (-1, -1), 10),
		                         ('FONTSIZE', (0, 0), (-1, -1), 10)])
		t.hAlign = 'CENTER'
		self._story.append(t)
		self._story.append(PageBreak())

	def _add_total_result_table(self):
		heading1_style = styles['Heading1']
		p = Paragraph('1 Summary', heading1_style)
		sstyles = [('LINEABOVE', (0, 0), (6, 0), 2, colors.black),
		           ('LINEBELOW', (0, 0), (6, 0), 1, colors.black),
		           ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
		           ('FONTSIZE', (0, 0), (5, 0), 12),
		           ('GRID', (0, 0), (-1, -1), 1, colors.gray),
		           ('LEADING', (0, 0), (-1, -1), 10),
		           ('FONTSIZE', (0, 0), (-1, -1), 10)]
		for r_ind, r in enumerate(self._grr_cal_records):
			if r_ind == 0:
				continue
			curdata = r[5]
			if curdata <= 10 and curdata > 0:
				style = ('BACKGROUND', (6, r_ind), (6, r_ind), colors.green)
			elif curdata > 10 and curdata <= 20:
				style = ('BACKGROUND', (6, r_ind), (6, r_ind), colors.yellow)
			elif curdata > 20 and curdata <= 30:
				style = ('BACKGROUND', (6, r_ind), (6, r_ind), colors.orange)
			else:
				style = ('BACKGROUND', (6, r_ind), (6, r_ind), colors.red)
			sstyles.append(style)
		t = Table(self._grr_cal_records, style=sstyles)
		t.hAlign = 'CENTER'

		self._story.insert(0, PageBreak())
		self._story.insert(0, t)
		self._story.insert(0, p)

	def _myLaterPages(self, canvas, doc):
		# canvas.drawImage("snkanim.gif", 36, 36)
		canvas.saveState()
		# canvas.setStrokeColorRGB(1,0,0)
		# canvas.setLineWidth(5)
		# canvas.line(66,72,66,PAGE_HEIGHT-72)
		canvas.setFont('Times-Roman', 9)
		canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
		canvas.restoreState()


if __name__ == '__main__':
	# Select the GRR data root directory
	# tk_root = Tk()
	# tk_root.withdraw()
	# grr_root_dir = tkFileDialog.askdirectory(title='Select GRR data folder...')
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', action="store", dest="folder_name", help="The destination folder name")
	parser.add_argument('-s', action="store", dest="station", help="Please use combo1,ois,nfov,combo2")
	args = parser.parse_args()
	if args.folder_name is None:
		print "The folder is None and exit"
		sys.exit()
	if args.station is None:
		print "The station is None and exit"
		sys.exit()
	#     current_path = os.path.abspath(".")
	#     grr_root_dir = os.path.join(current_path, "calibration")
	# grr_root_dir = r'/media/xsliao/0001A3DF0001D948/GRR/data/Downloads/C1_test/GRR_C1_Combo1_01'

	auto = AutoGenGrrReport(grr_root_dir=args.folder_name)
	auto.pares_clifford_grr_data()
	auto.analyze_grr(args.station)
