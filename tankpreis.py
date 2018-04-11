# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_details_page(tankstellen_id):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
		'Host': 'www.clever-tanken.de'
	}
	r = requests.get(f'http://www.clever-tanken.de/tankstelle_details/{tankstellen_id}', headers=headers)
	return BeautifulSoup(r.text, 'html.parser')


def get_prices(soup):
	price_list = soup.find(id='main-content-fuel-price-list')
	prices = {}
	for category in price_list.find_all('div', {'class': 'fuel-price-entry'}):
		typ = category.find('div', {'class': 'fuel-price-type'}).find_all('span')[0].text
		base_price = category.find('span', {'ng-bind': 'display_preis'}).text.replace(' ', '')
		suffix = category.find('sup', {'ng-bind': 'suffix'}).text
		prices[typ] = float(base_price + suffix)
	return prices


def get_station_info(soup):
	name = soup.find('span', {'id': 'main-content-fuel-station-header-name'}).text
	adress_block = soup.find('div', {'id': 'gas_station_address'})
	adress = adress_block.find('span', {'itemprop': 'streetAddress'}).text
	plz = adress_block.find('span', {'itemprop': 'http://schema.org/postalCode'}).text
	ort = adress_block.find('span', {'itemprop': 'http://schema.org/addressCountry'}).text
	return adress, plz, ort
