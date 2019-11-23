def reformat():

    recs = open('recs.txt', "r")
    recs_db_load = open('recs_db_load.txt', "w+")

    for line in recs:
        line.replace("\\", "")
        temp = line.split(":<mail>")
        print(temp)
        recs_db_load.write(temp[0] + "\n" + "<mail>" + temp[1])

    recs.close()
    recs_db_load.close()


reformat()