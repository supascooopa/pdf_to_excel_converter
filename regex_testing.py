# import re
#
# string = "$273.55  pcs "
# # match = re.match("\d+", string).span()
# # match2 = re.search(r"\d+", string)
# match3 = re.search("\W\d+\.\d+",string)
# # print(match2.span(), string[match2.span()[1]:])
# # print(string[match[0]:match[1]])
# print(match3)
# print(match3.span()[1])
# print(string[match3.span()[1]:])
import ctypes

from ctypes.util import find_library

find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))
