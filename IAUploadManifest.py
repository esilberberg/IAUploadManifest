# Prepares BCC student newspaper "The Communicator" metadata for upload to Internet Archive

import glob
import os
import csv


def Get_Identifier(doc):
    month_dict = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12",
        "Fall": "09",
        "Spring": "03",
        "December-January": "12",
        "January-February": "01",
        "March-April": "03",
        "September-October": "09",
        "May-June": "05"
    }

    split_doc = os.path.splitext(doc)
    # remove pdf extension of doc, tokenize doc pdf basename
    char_list = split_doc[0].split()
    month = month_dict.get(char_list[2])
    identifier = f"ERROR: {split_doc[0]}"

    # identifier formulation depending on doc file name
    try:
        if char_list[4] == "(2)":
            identifier = f"{char_list[1]}_{char_list[3]}{month}01"
        elif char_list[4] == "(1)":
            identifier = f"{char_list[1]}_{char_list[3]}{month}00"
        elif int(char_list[3]) < 10:
            identifier = f"{char_list[1]}_{char_list[4]}{month}0{char_list[3]}"
        else:
            identifier = f"{char_list[1]}_{char_list[4]}{month}{char_list[3]}"

    except IndexError:
        identifier = f"{char_list[1]}_{char_list[3]}{month}00"

    return identifier


# Create a list of dicts
upload_manifest = []

for pdf in glob.glob("*.pdf"):

    split_pdf = os.path.splitext(pdf)
    pdf_basename = split_pdf[0]

    upload_dict = {
        "identifier": Get_Identifier(pdf),
        "file": pdf,
        "description": "The student newspaper of Bronx Community College. Issues from this collection date from 1959 to 2012 and were published in the Bronx, New York.",
        "subject[0]": "Student activism",
        "subject[1]": "Newspaper",
        "subject[2]": "Bronx",
        "title": pdf_basename,
        "creator": "Bronx Community College",
        "coverage": "Bronx, New York",
        "mediatype": "texts",
        "date": Get_Identifier(pdf)[13:17],
        "language": "eng",
        "betterpdf": "true",
        "licenseurl": "https://creativecommons.org/licenses/by-nc-sa/4.0/"
    }
    upload_manifest.append(upload_dict)

f = open("IAUploadManifest.csv", "w", newline='')
writer = csv.DictWriter(
    f, fieldnames=["identifier", "file", "description",
                   "subject[0]", "subject[1]", "subject[2]",
                   "title", "creator", "coverage", "mediatype", "date",
                   "language", "betterpdf", "licenseurl"]
)
writer.writeheader()
writer.writerows(upload_manifest)
f.close()
