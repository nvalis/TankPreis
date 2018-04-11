#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tankpreis


def main():
	soup = tankpreis.get_details_page('1337')
	print(tankpreis.get_station_info(soup))
	print(tankpreis.get_prices(soup))


if __name__ == '__main__':
	main()
