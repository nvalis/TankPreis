#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tankpreis
from config import stations
# stations = {'1234': ['Diesel', 'Super E10', 'Super E5'], '2345': ['Diesel', 'Super E10', 'Super E5']}

import schedule
import datetime
import time
import sys
import os
import logging
logging.basicConfig(level=logging.INFO)


def get_prices(station_id):
	soup = tankpreis.get_details_page(station_id)
	prices = tankpreis.get_prices(soup)
	prices['datetime'] = datetime.datetime.now()
	return prices


def write_prices(station_prices, stations):
	for i, prices in station_prices.items():
		f_name = f'data/{i}.txt'
		with open(f_name, 'a') as out_file:
			data = '\t'.join([str(prices[c]) for c in stations[i]])
			out_file.write(f'{prices["datetime"]}\t{data}\n')


def update_prices(stations):
	prices = {i: get_prices(i) for i in stations.keys()}
	logging.info(f'Got prices: {prices}')
	write_prices(prices, stations)


def main():
	for i in stations.keys():
		f_name = f'data/{i}.txt'
		if not os.path.isfile(f_name):  # create and initialize file if it not exists
			with open(f_name, 'w') as out_file:
				column_headers = '\t'.join(stations[i])
				out_file.write(f'# datetime\t{column_headers}\n')
		else:
			logging.error(f'File {f_name} already exists, exiting...')
			sys.exit(1)

	# Run
	schedule.every(10).minutes.do(update_prices, stations)
	while True:
		schedule.run_pending()
		time.sleep(1)


if __name__ == '__main__':
	main()
