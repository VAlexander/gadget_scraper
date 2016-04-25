import csv

fieldnames = ['product_id', 'product_name', 'manufacturer_name', 'EE', 'O2', 'ORANGE', 'OTHER', 'TESCO',
                              'THREE', 'TMOBILE', 'UNKNOWN', 'UNLOCKED', 'VODAFONE']

with open('mapping_details\mapping_details_mobile.csv', 'rb') as fi:
    with open('mapping_details\mapping_details_mobile_.csv', 'wb') as fo:

        reader = csv.reader(fi)
        writer = csv.writer(fo)

        input_list = list(reader)[1:]
        print len(input_list)
        writer.writerow(fieldnames)
        for row in input_list:
            x = list()
            x[:] = row[:]
            for a in range(10):
                x.append(0)

            writer.writerow(x)
