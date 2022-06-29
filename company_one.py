# bismillahirrahmanirrahim
import camelot
import numpy as np
import file_manager_v101 as fm
import pandas as pd
from tkinter import mainloop
import datetime

now = datetime.datetime.now().strftime("%d-%m-%Y")

def onclick(event):
    """ Appending the x,y coordinates to a list when clicked """
    ix, iy = str(event.xdata), str(event.ydata)

    global coordinates
    coordinates.extend((ix, iy))


# Increasing the width of table displayed
pd.set_option("display.width", 1000)
pd.set_option('display.max_columns', 11)

for file in fm.current_directory_files():
    file = file.lower()
    if file.endswith(".pdf"):
        print(file)
file_name = input("please enter the name of the pdf: ")
pages_question = input("please enter the page number")
# reading through pages of the pdf, showing the user the table to specify table area
table = camelot.read_pdf(f"{file_name}.pdf",
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
tables = camelot.read_pdf(f"{file_name}.pdf",
                          flavor='stream',
                          table_areas=[coordinates_of_table],
                          pages=pages_question,
                          strip_text="\n",
                          row_tol=15)

page_df = tables[0].df

try:
    with pd.ExcelWriter(f"{file_name} {now}.xlsx",
                        mode="a",
                        engine="openpyxl",
                        if_sheet_exists="overlay") as writer:
        page_df.to_excel(writer, startrow=no_of_rows, index=False, header=False)
        no_of_rows += page_df[page_df.columns[1]].count()
except FileNotFoundError:
    with pd.ExcelWriter(f"{file_name} {now}.xlsx",
                        mode="w",
                        engine="openpyxl", ) as writer:
        page_df.to_excel(writer, index=False)
    no_of_rows = page_df[page_df.columns[1]].count() + 1