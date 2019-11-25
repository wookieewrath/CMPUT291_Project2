






recs = open('backslash.txt', "r")

for line in recs:

    line = line.replace("\\", "")
    print(line)

recs.close()

