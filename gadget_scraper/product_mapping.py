#!-*- encoding: utf-8 -*-

import csv


class MappingItem(object):
    """Represents object for mapping from CIYG site"""

    def __init__(self, input_list):
        # Get first 3 columns
        self.id, self.product_name, self.manufacturer_name = input_list[:3]

        # And last 10 for network modifiers if they're present
        try:
            self.EE, self.O2, self.ORANGE, self.OTHER, self.TESCO, \
            self.THREE, self.TMOBILE, self.UNKNOWN, self.UNLOCKED, \
            self.VODAFONE = input_list[3:]
        except ValueError:
            pass

    def get_net_mods(self):
        result = list()

        result.append("{:.2f}".format(float(self.EE)))
        result.append("{:.2f}".format(float(self.O2)))
        result.append("{:.2f}".format(float(self.ORANGE)))
        result.append("{:.2f}".format(float(self.OTHER)))
        result.append("{:.2f}".format(float(self.TESCO)))
        result.append("{:.2f}".format(float(self.THREE)))
        result.append("{:.2f}".format(float(self.TMOBILE)))
        result.append("{:.2f}".format(float(self.UNKNOWN)))
        result.append("{:.2f}".format(float(self.UNLOCKED)))
        result.append("{:.2f}".format(float(self.VODAFONE)))

        return result

    id = 0
    manufacturer_name = ''
    product_name = ''
    EE = 0
    O2 = 0
    ORANGE = 0
    OTHER = 0
    TESCO = 0
    THREE = 0
    TMOBILE = 0
    UNKNOWN = 0
    UNLOCKED = 0
    VODAFONE = 0


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
            self.working_poor_modifier = -1 * self.base_value
        # Average scraped products base value up to £15.00 match reduction to that of the non working modifier.
        elif self.base_value < 15:
            self.working_poor_modifier = -1 * self.non_working
        # Average scraped products base value above £15.00 = 20% reduction of the base value (-20%)
        elif self.base_value >= 15:
            self.working_poor_modifier = -1 * (self.base_value * 0.2)

        self.base_value = "{:.2f}".format(self.base_value)
        self.non_working = "{:0.2f}".format(self.non_working)
        self.working_poor_modifier = "{:0.2f}".format(self.working_poor_modifier)

    def set_net_mods(self, net_mods):
        self.EE, self.O2, self.ORANGE, self.OTHER, self.TESCO, \
        self.THREE, self.TMOBILE, self.UNKNOWN, self.UNLOCKED, \
        self.VODAFONE = net_mods

    manufacturer_name = ''
    product_name = ''
    base_value = 0
    non_working = 0
    working_poor_modifier = 0
    id = 1
    EE = 0
    O2 = 0
    ORANGE = 0
    OTHER = 0
    TESCO = 0
    THREE = 0
    TMOBILE = 0
    UNKNOWN = 0
    UNLOCKED = 0
    VODAFONE = 0


class Mapper():
    input_items = []
    mapping_items = []
    zero_ids = []
    input_filename = ''
    mapping_filename = ''
    zeroes_filename = ''
    output_filename = ''
    new_items_filename = ''
    export_networks = False

    def __init__(self, input_filename, mapping_filename, zeroes_filename, output_filename, new_items_filename,
                 export_networks):
        self.input_filename = input_filename
        self.mapping_filename = mapping_filename
        self.zeroes_filename = zeroes_filename
        self.output_filename = output_filename
        self.new_items_filename = new_items_filename
        self.export_networks = export_networks

        self.read_input_csv()
        self.read_mapping_csv()
        self.read_zeroes_csv()

    def read_input_csv(self):
        """Reads csv from input filename and returns list of CIYGItems"""

        try:
            open(self.input_filename, 'rb')
        except IOError:
            open(self.input_filename, 'wb')
        finally:
            with open(self.input_filename, 'rb') as f:
                reader = csv.reader(f)
                compare_my_mobile_phones = list(reader)[1:]

                for row in compare_my_mobile_phones:
                    self.input_items.append(CIYGItem(row))

    def read_mapping_csv(self):
        """Reads csv from input filename and returns list of MappingItems"""

        with open(self.mapping_filename, 'rb') as f:
            reader = csv.reader(f)
            mapping_values = list(reader)[1:]

            for row in mapping_values:
                self.mapping_items.append(MappingItem(row))

    def read_zeroes_csv(self):
        """Reads csv from input filename and returns list of IDs"""

        try:
            open(self.zeroes_filename, 'rb')
        except IOError:
            open(self.zeroes_filename, 'wb')
        finally:
            with open(self.zeroes_filename, 'rb') as f:
                reader = csv.reader(f)
                mapping_values = list(reader)[1:]

                for row in mapping_values:
                    self.zero_ids.append(row[0])

    def map_ids(self):
        """Iterates through input and mapping items. If found exact match on manufacturer and product name,
        then set input item's ID to mapping ID for future export"""
        for input_item in self.input_items:
            for mapping_item in self.mapping_items:
                if input_item.manufacturer_name == mapping_item.manufacturer_name and \
                                input_item.product_name == mapping_item.product_name:
                    if input_item.id not in self.zero_ids:
                        input_item.id = mapping_item.id
                        input_item.set_net_mods(mapping_item.get_net_mods())

    def write_mapped_items_to_csv(self):
        """Writes all items that are mapped to csv with input filename"""
        with open(self.output_filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)

            if self.export_networks:
                fieldnames = ['product_id', 'product_name', 'manufacturer_name', 'base_value', 'non_working',
                              'working_poor_modifier', 'working_good_modifier', 'EE', 'O2', 'ORANGE', 'OTHER', 'TESCO',
                              'THREE', 'TMOBILE', 'UNKNOWN', 'UNLOCKED', 'VODAFONE']
            else:
                fieldnames = ['product_id', 'product_name', 'manufacturer_name', 'base_value', 'non_working',
                              'working_poor_modifier', 'working_good_modifier']

            writer.writerow(fieldnames)
            for input_item in self.input_items:
                if input_item.id != 1 and input_item.id not in self.zero_ids:
                    if input_item.base_value == '0.00':
                        self.zero_ids.append(input_item.id)

                    if self.export_networks:
                        writer.writerow(
                            (
                                input_item.id, input_item.product_name, input_item.manufacturer_name,
                                input_item.base_value,
                                input_item.non_working, input_item.working_poor_modifier, 0, input_item.EE,
                                input_item.O2, input_item.ORANGE, input_item.OTHER, input_item.TESCO, input_item.THREE,
                                input_item.TMOBILE, input_item.UNKNOWN, input_item.UNLOCKED, input_item.VODAFONE))
                    else:
                        writer.writerow(
                            (
                                input_item.id, input_item.product_name, input_item.manufacturer_name,
                                input_item.base_value,
                                input_item.non_working, input_item.working_poor_modifier, 0))

    def write_new_items_to_csv(self):
        """Writes any new items to csv with input filename"""
        with open(self.new_items_filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)

            if self.export_networks:
                fieldnames = ['product_id', 'product_name', 'manufacturer_name', 'base_value', 'non_working',
                              'working_poor_modifier', 'working_good_modifier', 'EE', 'O2', 'ORANGE', 'OTHER', 'TESCO',
                              'THREE', 'TMOBILE', 'UNKNOWN', 'UNLOCKED', 'VODAFONE']
            else:
                fieldnames = ['product_id', 'product_name', 'manufacturer_name', 'base_value', 'non_working',
                              'working_poor_modifier', 'working_good_modifier']

            writer.writerow(fieldnames)
            for input_item in self.input_items:
                if input_item.id == 1:
                    if self.export_networks:
                        writer.writerow(('', input_item.product_name, input_item.manufacturer_name, 0, 0, 0,
                                         0, input_item.EE, input_item.O2, input_item.ORANGE, input_item.OTHER,
                                         input_item.TESCO, input_item.THREE, input_item.TMOBILE, input_item.UNKNOWN,
                                         input_item.UNLOCKED, input_item.VODAFONE))
                    else:
                        writer.writerow(('', input_item.product_name, input_item.manufacturer_name, 0, 0, 0, 0))

    def write_zeroes_to_csv(self):
        with open(self.zeroes_filename, 'wb') as csvfile:
            fieldnames = ['product_id', ]

            writer = csv.writer(csvfile)

            writer.writerow(fieldnames)
            self.zero_ids = set(self.zero_ids)
            for zero_id in self.zero_ids:
                writer.writerow((zero_id,))

    def map_items(self):
        self.map_ids()
        self.write_mapped_items_to_csv()
        self.write_new_items_to_csv()
        self.write_zeroes_to_csv()
