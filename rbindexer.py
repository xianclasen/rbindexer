import csv
from pypdf import PdfReader

# Replace with the name of the realbook file
reader = PdfReader("vgleadsheets-all-C.pdf")

# Replace with the page range that contains the table of contents
toc_pages = reader.pages[4:25]

# Replace with the output file name
csv_file = 'vgm.csv'

# Parse the table of contents page
def parseTocPage(toc_page):
    output = []
    toc_text = toc_page.extract_text()
    toc_split = toc_text.split('\n')
    new_title = True
    for i in toc_split:
        if new_title:
            title = ''
        try:
            int(i)
            title = title + ',' + i
            output.append(title)
            new_title = True
        except:
            new_title = False

            # Get rid of problematic character in the titles
            title = title.replace('"', '')
            title = title.replace(",", "")
            title = title + i.replace(",", "")
    
    return output

# Function to extract title and page number from each item
def extract_info(item):
    parts = item.split(',')
    title = parts[0]
    page_number = int(parts[1])
    return title, page_number

# Get the initial list with the titles and start page numbers
index = []
for page in toc_pages:
    index = index + parseTocPage(page)

# Reconstructing the list so that it has the end page number
reconstructed_list = []
for i in range(len(index) - 1):
    title, page_number = extract_info(index[i])
    _, next_page_number = extract_info(index[i + 1])
    reconstructed_list.append((title, page_number, next_page_number - 1))
title, page_number = extract_info(index[-1])
reconstructed_list.append((title, page_number, None))

# Writing to CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Page Start', 'Page End'])
    for item in reconstructed_list:
        writer.writerow(item)