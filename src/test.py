import tempfile

# with tempfile.TemporaryDirectory() as d:
#     with open(d+"/temp.txt", "w") as temp:
#         temp.write("booba")

tempdir = tempfile.TemporaryDirectory()
tempdir_location = tempdir.name + "/"
print(tempdir_location)