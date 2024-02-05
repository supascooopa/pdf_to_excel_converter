import camelot
import file_manager_v101 as fm
import pandas as pd
from tkinter import mainloop
import re
from tools import new_file_path

def onclick(event):
    """ Appending the x,y coordinates to a list when clicked """
    global coordinates
    ix, iy = str(event.xdata), str(event.ydata)
    coordinates.extend((ix, iy))

# Increasing the width of table displayed
pd.set_option("display.width", 1000)
pd.set_option('display.max_columns', 7)

file_name = fm.get_file_name(file_extension=".pdf")

# reading through pages of the pdf, showing the user the table to specify table area
table = camelot.read_pdf(f"{file_name}",
                         flavor='stream')
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
                          pages="all",
                          strip_text="\n")
for pages in tables:
    page_df = pages.df
    # combining the columns
    page_df.columns = page_df.iloc[0] + " " + page_df.iloc[1]
    page_df.columns = page_df.columns.str.strip()
    page_df = page_df.iloc[2:].reset_index(drop=True)

    # TODO: separate Sl no. from Description goods column
    # combining what is actually should be one cell but appears as multiple cells in the dataframe
    for index, row in page_df.iterrows():
        # dividing index and description
        try:
            search_result_num = re.search("\d+", row["Sl No."])
            search_result_str = re.search(r"\D+", row["Sl No."])
            if search_result_num and search_result_str:
                row["Description of Goods"] = row["Sl No."][search_result_num.span()[1]:]
                row["Sl No."] = search_result_num.group()
        except KeyError:
            search_result_num = re.search("\d+", row[0])
            search_result_str = re.search(r"\D+", row[0])
            if search_result_num and search_result_str:
                row["Description of Goods"] = row[0][search_result_num.span()[1]:]
                row[0] = search_result_num.group()
        # dividing price and 'pcs'
        if "Due on" not in page_df:
            search_result = re.search("\W\d+\.\d+",row["Amount"])
            if search_result:
                row["per"] = search_result.group()
                row["Amount"] = row["Amount"][search_result.span()[1]:]

    dislocated = []
    missing = []
    # iterates over rows
    for index, row in page_df.iterrows():
        # finds the "Sl No." empty ones
        try:
            if row["Sl No."] == "":
                # adds them to a list
                missing.append(index)
                # if it's the last index and has no "SL no." add to the last
                if index == page_df.index[-1]:
                    dislocated.append(missing)
            else:

                # if iteration runs into a filled "Sl No."
                if len(missing) > 0:
                    # appends into dislocated list
                    dislocated.append(missing)
                    missing = []
        except KeyError:
            if row[0] == "":
                # adds them to a list
                missing.append(index)
                # if its the last index and has no "SL no." add to the last
                if index == page_df.index[-1]:
                    dislocated.append(missing)
            else:
                # if iteration runs into a filled "Sl No."
                if len(missing) > 0:
                    # appends into dislocated list
                    dislocated.append(missing)
                    missing = []
    # iterates over dislocated rows list
    for cells in dislocated:
        # takes the first item and subtracts 1 to find the dislocated cells origin
        # as they all have one originating above them
        origin_cell = cells[0] - 1
        # iterates over the cells
        for cell in cells:
            page_df.iloc[origin_cell] = page_df.iloc[origin_cell] + " " + page_df.iloc[cell]
    for cells in dislocated:
        page_df = page_df.drop(cells)
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
                            engine="openpyxl",) as writer:
            page_df.to_excel(writer, index=False)
        no_of_rows = page_df[page_df.columns[1]].count() + 1

# enables me to see the areas of text
# camelot.plot(tables[1], kind='text').show()
# mainloop()
