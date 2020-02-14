#!/usr/bin/python2
#
# Copyright 2017 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
'get_attachments' is a tool to find Testlog attachment files from
BigQuery / GCS across a given date range, and to save them to disk.
"""
from __future__ import print_function

import argparse
import hashlib
import json
import os
import shutil
import string
import subprocess

DATE_FORMAT = '%Y%m%d%H%M%S'
HASH_FILE_READ_BLOCK_SIZE = 1024 * 64  # 64kb
GSUTIL_TEST_PERMISSION_PATH = 'gs://chromeos-localmirror-private/testing/'
DEFAULT_START_TIME = '1970-01-01'
DEFAULT_END_TIME = '2100-12-31'
DEFAULT_TARGET_DIR = './factory_attachments'
DEFAULT_BQ_PATH = 'bq'
DEFAULT_GSUTIL_PATH = 'gsutil'
DEFAULT_SERIAL_NUMBER_KEY = 'serial_number'


def CheckVersion(args):
	subprocess.check_call([args.gsutil_path, '--version'])
	print('Checking your gsutil permission....')
	subprocess.check_call([args.gsutil_path, 'ls',
	                       GSUTIL_TEST_PERMISSION_PATH])
	subprocess.check_call([args.bq_path, 'version'])
	print('Checking your BigQuery permission and BigQuery dataset ID....')
	subprocess.check_call([args.bq_path, 'show',
	                       '--project_id', 'chromeos-factory',
	                       '--dataset_id', args.dataset_id])
	print()


def RunQuery(args):
	query_statement_words = [
		'SELECT',
		'    attachment.path AS remote,',
		'    FORMAT_TIMESTAMP("%s", startTime) AS start_time,',
		'    attachment.key AS attachment_key,',
		'    (',
		'        SELECT serialNumber.value',
		'        FROM UNNEST(data.serialNumbers) AS serialNumber',
		'        WHERE serialNumber.key="%s"',
		'    ) AS serial_number',
		'FROM',
		'    `chromeos-factory.%s.testlog_events` AS data,',
		'    UNNEST(data.attachments) AS attachment',
		'WHERE',
		'    attachment.key LIKE "%%%s%%" AND',
		'    history[OFFSET(2)].time > TIMESTAMP("%s") AND',
		'    history[OFFSET(2)].time < TIMESTAMP("%s")']
	query_statement = string.join(query_statement_words, '\n')
	query = query_statement % (DATE_FORMAT, args.serial_number_key,
	                           args.dataset_id, args.attachment_key,
	                           args.start_date, args.end_date)
	print('Execute the query, you can also copy-paste the follwing query to\n'
	      'https://bigquery.cloud.google.com')
	print('-' * 37 + 'QUERY' + '-' * 38 + '\n' + query + '\n' + '-' * 80 + '\n')
	result_json = subprocess.check_output([args.bq_path, 'query',
	                                       '--max_rows', '1000000',
	                                       '--nouse_legacy_sql',
	                                       '--format', 'json', query])
	print()
	return result_json


def Download(args, results):
	commands = [args.gsutil_path, '-m', 'cp', '-n']
	for row in results:
		row['tmp'] = os.path.join('tmp', row['remote'].split('/')[-1])
		commands.append(row['remote'])
	commands.append('tmp')
	subprocess.check_call(commands)


def FileHash(path):
	file_hash = hashlib.md5()
	with open(path, 'rb') as f:
		for chunk in iter(lambda: f.read(HASH_FILE_READ_BLOCK_SIZE), ''):
			file_hash.update(chunk)
	return file_hash.hexdigest()


def CopyAndDelete(results):
	for row in results:
		local = '%s_%s_%s_%s' % (row['start_time'], row['attachment_key'],
		                         row['serial_number'] or 'NoSerialNumber',
		                         FileHash(row['tmp']))
		print(row['remote'] + ' --> ' + local)
		shutil.copyfile(row['tmp'], local)
	shutil.rmtree('tmp')


def main():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description='Attachment downloader script',
		epilog='Common errors are permission and installation.\n'
		       'Please check https://cloud.google.com/sdk/docs/ to\n'
		       '  (1) update your gsutil to 4.26 and BigQuery CLI to 2.0.24\n'
		       '  (2) authorize gcloud by "gcloud init" or "gcloud auth login"')
	parser.add_argument(
		'dataset_id',
		help='The BigQuery dataset ID.')
	parser.add_argument(
		'attachment_key',
		help='The attachment key.')
	parser.add_argument(
		'--start_date', '-s', default=DEFAULT_START_TIME,
		help='The start of date. Default: %s' % DEFAULT_START_TIME)
	parser.add_argument(
		'--end_date', '-e', default=DEFAULT_END_TIME,
		help='The end of date. Default: %s' % DEFAULT_END_TIME)
	parser.add_argument(
		'--target_dir', '-t', default=DEFAULT_TARGET_DIR,
		help='The target directory. Default: %s' % DEFAULT_TARGET_DIR)
	parser.add_argument(
		'--bq_path', '-b', default=DEFAULT_BQ_PATH,
		help='The bq path. Default: %s' % DEFAULT_BQ_PATH)
	parser.add_argument(
		'--gsutil_path', '-g', default=DEFAULT_GSUTIL_PATH,
		help='The gsutil path. Default: %s' % DEFAULT_GSUTIL_PATH)
	parser.add_argument(
		'--serial_number_key', '-sn', default=DEFAULT_SERIAL_NUMBER_KEY,
		help='The key of the serial number to put in the file name. '
		     'Default: %s' % DEFAULT_SERIAL_NUMBER_KEY)
	args = parser.parse_args()
	CheckVersion(args)
	result_json = RunQuery(args).strip()
	if not result_json:
		print('Query returned zero records.\n'
		      'Done!')
		return
	results = json.loads(result_json)
	print('Found %d files!\n' % len(results))
	if not os.path.isdir(os.path.join(args.target_dir, 'tmp')):
		os.makedirs(os.path.join(args.target_dir, 'tmp'))
	os.chdir(args.target_dir)
	Download(args, results)
	CopyAndDelete(results)
	print('Done!')


if __name__ == '__main__':
	main()
