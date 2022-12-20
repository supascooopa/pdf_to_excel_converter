# bismillahirrahmanirrahim
import camelot
import numpy as np
import file_manager_v101 as fm
import pandas as pd
from tkinter import mainloop
import datetime
from tools import new_file_path

def onclick(event):
    """ Appending the x,y coordinates to a list when clicked """
    global coordinates
    ix, iy = str(event.xdata), str(event.ydata)
    coordinates.extend((ix, iy))

# Increasing the width of table displayed
pd.set_option("display.width", 1000)
pd.set_option('display.max_columns', 11)

file_name = fm.get_file_name(file_extension=".pdf")

pages_question = input("please enter the page number")
# reading through pages of the pdf, showing the user the table to specify table area
table = camelot.read_pdf(f"{file_name}",
                         flavor='stream',
                         pages=pages_question)
fig = camelot.plot(table[0], kind='text')
coordinates = []
cid = fig.canvas.mpl_connect('button_press_event', onclick)
fig.show()
mainloop()
coordinates_of_table = ",".join(coordinates)
# Creating Dataframe from the data read.
no_of_rows = 0
tables = camelot.read_pdf(f"{file_name}",
                          flavor='stream',
                          table_areas=[coordinates_of_table],
                          pages=pages_question,
                          strip_text="\n",
                          row_tol=15)

page_df = tables[0].df
new_file_name = new_file_path(".xlsx", file_name)
try:
    with pd.ExcelWriter(new_file_name,
                        mode="a",
                        engine="openpyxl",
                        if_sheet_exists="overlay") as writer:
        page_df.to_excel(writer, startrow=no_of_rows, index=False, header=False)
        no_of_rows += page_df[page_df.columns[1]].count()
except FileNotFoundError:
    with pd.ExcelWriter(new_file_name,
                        mode="w",
                        engine="openpyxl", ) as writer:
        page_df.to_excel(writer, index=False)
    no_of_rows = page_df[page_df.columns[1]].count() + 1
