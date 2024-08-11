import csv
from _csv import writer

from Config.config import CSV_FILE, LIST_SUBJECTS


async def write_to_csv(list_data):
    # with open(CSV_FILE, mode='w', encoding='utf-8') as file:
    #     writer_object = writer(file)
    #     writer_object.writerow(LIST_SUBJECTS)

    with open(CSV_FILE, mode='a', encoding='utf-8', newline='') as file:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(file)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(list_data)
        # Close the file object
        file.close()


