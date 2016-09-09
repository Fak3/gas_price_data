#!/usr/bin/env python

import csv

from os.path import dirname, join

import requests
import xlrd


def parse(url, filename, monthly=False):
    # Download xls data
    response = requests.get(url)
    response.raise_for_status()
    open('data.xls', 'wb+').write(response.content)

    book = xlrd.open_workbook('data.xls')
    sheet = book.sheet_by_name('Data 1')

    with open(filename, 'wb+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Price'])  # Write csv header as first row

        for row in list(sheet.get_rows())[3:]:
            # Convert xls date to python datetime
            date = xlrd.xldate.xldate_as_datetime(row[0].value, book.datemode).date()
            if monthly:
                date = date.replace(day=1)
            writer.writerow([date.isoformat(), row[1].value])


def rpath(*args):
    return join(dirname(__file__), *args)

parse('http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls', rpath('../data/gas_price_daily.csv'))
parse('http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls', rpath('../data/gas_price_monthly.csv'), monthly=True)
