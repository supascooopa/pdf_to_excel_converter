# bismillahirrahmanirrahim
# BELOW WORKS PERFECTLY TESTED WITH TWO DIFFERENT INVOICES
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

file_name = fm.get_file_name()

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
question = input("EMO??")
for pages in tables:
    page_df = pages.df

    page_df = page_df.replace(r'^\s*$', np.nan, regex=True)
    page_df = page_df.dropna(subset=[0])
    # if page_df["Line"] == " ":
    #     print(page_df["Line"].index)
    # print(page_df)
    if question == "yes":
        product_lst = ["iron", "straightener", "brush", "styler", "dryer", "clipper", 'waver', "citrus press", "toaster",
                       "juicer", "kettle", "dehumidifier", "grill", "blender", "chopper", "food processor", "mixer",
                       "grinder", "coffee", "fryer", "cooker", 'garment streamer', "steamer", 'massager',
                       'espresso', 'bread', "crimper", "curl", "roller", "fan", "hand blender", "smoothie maker",
                       "hand mixer", "soup maker", "induction", "oven"]
        turkish_product_list = ["??t??", "Sa?? d??zle??tirici", 'tarak', 'Sa?? ??ekil verici', 'sa?? kurutucu', 'Sa?? kesme aleti',
                                'sa?? dalgaland??r??c??','narenciye s??kaca????', 'Ekmek k??zart??c??', 'meyve suyu s??k??c??',
                                'Su ??s??t??c??s??', 'Nem giderici', 'Elektrik mangal', 'Blender', 'Do??ray??c??', 'Mutfak robotu',
                                'Mikser', 'kahve ve baharat ??????t??c??', 'Kahve makinas??', 'K??zart??c??', 'Pi??irici','dikey ??t??',
                                'buharl?? pi??irici', 'masaj aleti', 'espresso makinesi', 'ekmek yapar', "sa?? tost makinesi",
                                "sa?? k??v??rt??c??","sa?? k??v??rt??c?? rulo", "vantilat??r", "el blenderi", "smoothie makinesi",
                                "el mikseri", "??orba makinesi", "end??ksyon oca????", "f??r??n"]
        pattern = "|".join(product_lst)
        page_df = page_df.loc[page_df[5].str.contains(pattern, case=False, na=False)]

        for product in range(len(product_lst)):
            searched_pat = page_df[5].str.contains(product_lst[product], case=False, na=False)
            turkish_product_name = turkish_product_list[product]
            page_df[5].mask(searched_pat, turkish_product_name, inplace=True)

        product_brands_codes = ["BA", "BRN", "DE", "GE", "HO", "HON", "KE", "KR", "MO", "MOR", "PH", "RE", "REV", "RU",
                                "SAL", "TEF", "TO",
                                "TRE", "WA"]

        product_brands = ["babyliss", "Braun", "Delonghi", "George Foreman", "Homedics", "Honeywell", "Kenwood", "Krups",
                          "moulinex", "morphy richards",
                          "Philips", "remington", "Revlon", "Russel Hobbs", "Salter",
                          "Tefal", "Toni and guy", "Tresemme", "Wahl"]

        page_df["brand_names"] = page_df[1]
        for brand in range(len(product_brands_codes)):
            searched_pat = page_df[1].str.contains(product_brands_codes[brand], case=False, na=False)
            brand_name = product_brands[brand]
            page_df["brand_names"].mask(searched_pat, brand_name, inplace=True)

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

