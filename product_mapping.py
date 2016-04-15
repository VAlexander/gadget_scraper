#!-*- encoding: utf-8 -*-

import csv


class CIYGItem(object):
    def __init__(self, input_list):
        self.manufacturer_name = input_list[0]
        self.product_name = input_list[1]

        working_prices = [float(x) for x in input_list[2:8] if x]
        try:
            average_base_value = sum(working_prices) / len(working_prices)
        except ZeroDivisionError:
            average_base_value = 0

        # Average scraped products value falling below £2.50 do not offer on (0 base price on CIYG)
        if average_base_value < 2.5:
            self.base_value = 0
        # Average scraped products value £2.50 to £20.00 set 50% of the average price
        elif 2.5 <= average_base_value < 20:
            self.base_value = 0.5 * average_base_value
        # Average scraped products value £20.00 upwards set at average price minus 5%
        elif average_base_value >= 20:
            self.base_value = average_base_value - (average_base_value * 0.05)

        non_working_prices = [float(x) for x in input_list[8:] if x]
        try:
            average_non_working = sum(non_working_prices) / len(non_working_prices)
        except ZeroDivisionError:
            average_non_working = 0

        # Average scraped products value falling below £5.00 do not offer on (0 non working modifier price)
        if average_non_working < 5:
            self.non_working = 0
        # Average scraped products value £2.50 to £20.00 set 50% of the average price
        elif average_non_working >= 5:
            self.non_working = average_non_working

        # Average scraped products non working price is up to £5.00 do not offer on (maximum reduction resulting in 0 offer)
        if self.non_working < 5:
            self.working_poor_modifier = 0
        # Average scraped products base value up to £15.00 match reduction to that of the non working modifier.
        elif self.base_value < 15:
            self.working_poor_modifier = -1 * self.non_working
        # Average scraped products base value above £15.00 = 20% reduction of the base value (-20%)
        elif self.base_value >= 15:
            self.working_poor_modifier = -1 * (self.base_value * 0.2)

        # print (self.manufacturer_name,
        #        self.product_name,
        #        average_base_value,
        #        self.base_value,
        #        average_non_working,
        #        self.non_working,
        #        self.working_poor_modifier)

    manufacturer_name = ''
    product_name = ''
    base_value = 0
    non_working = 0
    working_poor_modifier = 0


with open('compare_my_mobile_phones.csv', 'rb') as f:
    reader = csv.reader(f)
    compare_my_mobile_phones = list(reader)[1:]

items = []

for phone in compare_my_mobile_phones:
    items.append(CIYGItem(phone))

