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

def processImages(rows):
    id_img_err  = []
    out_rows = []

    for row in rows:
        id = row[0]
        description = row[1]
        images = row[2]
        blackdot_image = 'blackdot.io'

        soup = BeautifulSoup(description, "html.parser")

        # find images in the description, save them in a list and remove them from description
        description_image_list = []
        for img in soup.findAll('img'):
            if img.get('src') is None:
                # something is wrong with the html
                if id not in id_img_err:
                    id_img_err.append(id)
                print(id, img)
            elif blackdot_image in img.get('src'):
                description_image_list.append(img.get('src'))
                # remove the img tab
                img.decompose()

        out_description = str(soup)
        out_images = images
        # if images found in the description, we need to add them to images
        if len(description_image_list) > 0:
            # convert existing images to a list
            tmp_image_list = images.split()
            # add images found in the description
            tmp_image_list += description_image_list
            out_images = ",".join(tmp_image_list)
            out_rows.append([id, out_description, out_images])

    return out_rows

# remove extra tags from description
def deleteExtraElements(rows):
    out_rows = []
    link_ct = 0
    script_ct = 0

    for row in rows:
        id = row[0]
        description = row[1]
        images = row[2]

        soup = BeautifulSoup(description, "html.parser")

        update = False
        # find class: ProductDescriptionImg and remove from description
        for p in soup.findAll('p', {'class': 'ProductDescriptionImg'}):
            # remove the <p> from description
            p.decompose()
            update = True

        # remove all links from description
        for a in soup.findAll('a'):
            # print("link found (",id,"): ",a.get('href'))
            a.decompose()
            link_ct += 1
            update = True

        # remove any scripts
        for s in soup.findAll('script'):
            print("script found (",id,")")
            s.decompose()
            script_ct += 1
            update = True


        if update:
            out_description = str(soup)
            out_rows.append([id, out_description])


    print(link_ct, " links found")
    print(script_ct, " scripts found")
    return out_rows

fields, rows = readCSVFile(input_fname)

out_rows = processImages(rows)
#out_rows = deleteExtraElements(rows)

print("Updated items: ", len(out_rows))


writeCSVFile('out_products.csv', fields, out_rows)