import itertools
import camelot
import file_manager_v101 as fm
import pandas as pd
from tkinter import mainloop
import datetime
import numpy as np

now = datetime.datetime.now().strftime("%d-%m-%Y")


def onclick(event):
    """ Appending the x,y coordinates to a list when clicked """
    ix, iy = str(event.xdata), str(event.ydata)

    global coordinates
    coordinates.extend((ix, iy))


def grouper(iterable, n, fillvalue=0):
    """ iterates and gives results with n times"""
    it = [iter(iterable)] * n
    return itertools.zip_longest(*it, fillvalue=fillvalue)


# Increasing the width of table displayed
pd.set_option("display.width", 1000)
pd.set_option('display.max_columns', 11)

file_name = fm.get_file_name(file_extension=".pdf")
page_count = int(input("please enter the number of pages: "))
coordinates = []
for number in range(1, page_count + 1):
    # reading through pages of the pdf, showing the user the table to specify table area
    table = camelot.read_pdf(f"{file_name}",
                             pages=f"{number}",
                             flavor="stream"
                             )
    fig = camelot.plot(table[0], kind="text")
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    fig.show()
    mainloop()


# iterating over 4 values at a time since there are multiple pages and distinct page layouts of tables
grouped = grouper(coordinates, 4)

# joins 4 coordinates into one string wit "," in between the strings
joined_coordinates = []
for coor in grouped:
    joined_coordinates.append(",".join(coor))


# Creating Dataframe from the data read.
tables = []
pages = 1
for coordinates in joined_coordinates:
    table = camelot.read_pdf(f"{file_name}",
                              flavor='stream',
                              table_areas=[coordinates],
                              pages=str(pages),
                              strip_text="\n")
    tables.append(table)
    pages += 1
no_of_rows = 0
for pages in tables:
    page_df = pages[0].df
    page_df = page_df.replace(r'^\s*$', np.nan, regex=True)

    # TODO EMPTY THE ORIGIN COLUMN AND MOVE THE REST ONE COLUMN TO THE RIGHT
    try:
        striped_file_name = file_name.split(".")[0]
        with pd.ExcelWriter(f"{striped_file_name} {now}.xlsx",
                            mode="a",
                            engine="openpyxl",
                            if_sheet_exists="overlay") as writer:
            page_df.to_excel(writer, startrow=no_of_rows, index=False, header=False)
            no_of_rows += page_df[page_df.columns[1]].count()
    except FileNotFoundError:
        striped_file_name = file_name.split(".")[0]
        with pd.ExcelWriter(f"{striped_file_name} {now}.xlsx",
                            mode="w",
                            engine="openpyxl",) as writer:
            page_df.to_excel(writer, index=False)
        no_of_rows = page_df[page_df.columns[1]].count() + 1

