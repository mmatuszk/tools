import csv

input_fname = 'in_products.csv'

out_fname_base = "out_products"

# initializing the titles and rows list
fields = []
rows = []

# initialize row count
out_row_ct = 1000

def writeCSVFile(filename, fields, rows):
    # writing to csv file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        #csvfile.write('\ufeff')

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)

with open(input_fname, 'r', encoding='utf-8') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    # get total number of rows
    print("Total no. of rows: %d" % (csvreader.line_num))

in_num_rows = len(rows)

print(in_num_rows // out_row_ct)
print(in_num_rows % out_row_ct)
for i in range(in_num_rows // out_row_ct):
    out_fname = out_fname_base+'_%03d'%(i+1)+'.csv'
    start   = i*out_row_ct
    end     = i*out_row_ct+out_row_ct
    print(start, end)
    writeCSVFile(out_fname, fields, rows[start:end])

if (in_num_rows % out_row_ct > 0):
    i += 1
    out_fname = out_fname_base+'_%03d'%(i+1)+'.csv'
    start   = i*out_row_ct
    writeCSVFile(out_fname, fields, rows[start:])
