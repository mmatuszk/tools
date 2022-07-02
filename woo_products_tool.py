import csv
from bs4 import BeautifulSoup

input_fname = 'in_products.csv'

out_fname_base = "out_products"

def readCSVFile(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        #initialize variables
        fields  = []
        rows    = []
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

        # get total number of rows
        print("Total no. of rows: %d" % (len(rows)))
        return (fields, rows)

def processImages(rows):
    id_img_err = []
    for row in rows:
        id = row[0]
        description = row[1]
        images = row[2]
        blackdot_image = 'blackdot.io'

        soup = BeautifulSoup(description, "html.parser")
        description_images = []
        image_link_error = 0
        image_link_ok = 0
        for img in soup.findAll('img'):
            if img.get('src') is None:
                # something is wrong with the html
                image_link_error += 1
                print("errors: %d" % image_link_error)
                print("Product id: "+id)
                print(img)
            elif blackdot_image in img.get('src'):
                image_link_ok = +1
                #description_images.append(img.get('src'))

        print("errors: %d" % image_link_error)
        print("ok: %d" % image_link_ok)


fields, rows = readCSVFile(input_fname)

processImages(rows)