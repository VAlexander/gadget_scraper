#!-*- encoding: utf-8 -*-

import csv

input_items = []
mapping_items = []
zero_ids = []


class MappingItem(object):
    """Represents object for mapping from CIYG site"""

    def __init__(self, input_list):
        self.id = input_list[0]
        self.product_name = input_list[1]
        self.manufacturer_name = input_list[2]

    id = 0
    manufacturer_name = ''
    product_name = ''


class CIYGItem(object):
    def __init__(self, input_list):
        self.manufacturer_name = input_list[0].strip()
        self.product_name = input_list[1].strip()

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

        self.base_value = "{:.2f}".format(self.base_value)
        self.non_working = "{:0.2f}".format(self.non_working)
        self.working_poor_modifier = "{:0.2f}".format(self.working_poor_modifier)

    manufacturer_name = ''
    product_name = ''
    base_value = 0
    non_working = 0
    working_poor_modifier = 0
    id = 1


def read_input_csv(filename):
    """Reads csv from input filename and returns list of CIYGItems"""
    result = []

    try:
        open(filename, 'rb')
    except IOError:
        open(filename, 'wb')
    finally:
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            compare_my_mobile_phones = list(reader)[1:]

            for row in compare_my_mobile_phones:
                result.append(CIYGItem(row))

    return result


def read_mapping_csv(filename):
    """Reads csv from input filename and returns list of MappingItems"""
    result = []

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        mapping_values = list(reader)[1:]

        for row in mapping_values:
            result.append(MappingItem(row))

    return result


def read_zeroes_csv(filename):
    """Reads csv from input filename and returns list of IDs"""
    result = []

    try:
        open(filename, 'rb')
    except IOError:
        open(filename, 'wb')
    finally:
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            mapping_values = list(reader)[1:]

            for row in mapping_values:
                result.append(row[0])

    return result


def map_items():
    """Iterates through input and mapping items. If found exact match on manufacturer and product name,
    then set input item's ID to mapping ID for future export"""
    for input_item in input_items:
        for mapping_item in mapping_items:
            if input_item.manufacturer_name == mapping_item.manufacturer_name and \
                            input_item.product_name == mapping_item.product_name:
                if input_item.id not in zero_ids:
                    input_item.id = mapping_item.id


def write_mapped_items_to_csv(filename):
    """Writes all items that are mapped to csv with input filename"""
    with open(filename, 'wb') as csvfile:
        fieldnames = ['product_id', 'product_name', 'manufacturer_name', 'base_value', 'non_working',
                      'working_poor_modifier', 'working_good_modifier', 'EE', 'O2', 'ORANGE', 'OTHER', 'TESCO', 'THREE',
                      'TMOBILE', 'UNKNOWN', 'UNLOCKED', 'VODAFONE']

        writer = csv.writer(csvfile)

        writer.writerow(fieldnames)
        for input_item in input_items:
            if input_item.id != -1 and input_item.id not in zero_ids:
                if input_item.base_value == '0.00':
                    zero_ids.append(input_item.id)

                writer.writerow(
                    (input_item.id, input_item.product_name, input_item.manufacturer_name, input_item.base_value,
                     input_item.non_working, input_item.working_poor_modifier, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))


def write_new_items_to_csv(filename):
    """Writes any new items to csv with input filename"""
    with open(filename, 'wb') as csvfile:
        fieldnames = ['product_id', 'product_name', 'manufacturer_name', 'base_value', 'non_working',
                      'working_poor_modifier', 'working_good_modifier', 'EE', 'O2', 'ORANGE', 'OTHER', 'TESCO', 'THREE',
                      'TMOBILE', 'UNKNOWN', 'UNLOCKED', 'VODAFONE']

        writer = csv.writer(csvfile)

        writer.writerow(fieldnames)
        for input_item in input_items:
            if input_item.id == -1:
                writer.writerow(
                    (input_item.id, input_item.product_name, input_item.manufacturer_name, input_item.base_value,
                     input_item.non_working, input_item.working_poor_modifier, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))


def write_zeroes_to_csv(filename):
    with open(filename, 'wb') as csvfile:
        fieldnames = ['product_id', ]

        writer = csv.writer(csvfile)

        writer.writerow(fieldnames)

        for zero_id in zero_ids:
            writer.writerow((zero_id,))


def start_mapping(input_filename, mapping_filename, zeroes_filename, output_filename, new_items_filename):
    global input_items
    global mapping_items
    global zero_ids

    input_items = read_input_csv(input_filename)
    mapping_items = read_mapping_csv(mapping_filename)
    zero_ids = read_zeroes_csv(zeroes_filename)

    map_items()

    write_mapped_items_to_csv(output_filename)
    write_new_items_to_csv(new_items_filename)
    write_zeroes_to_csv(zeroes_filename)