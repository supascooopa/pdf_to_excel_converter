import pikepdf
import os


passwords = input("please enter the password: ")
list_of_files = filter(os.path.isfile, os.listdir(os.curdir))
print("Here is your current files contained in current directory: ")
count = 1
for files in list(list_of_files):
    print(f'{count}. {files}')
    count += 1
file_name = input("Please write the file name? ")
with pikepdf.open(f"{file_name}", password=passwords) as pdf:
    pdf.save(f"unlocked {file_name}")
