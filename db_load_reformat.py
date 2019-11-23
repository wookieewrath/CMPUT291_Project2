def reformat():

    terms = open('terms.txt', "r")
    terms_out = open('terms_out.txt', "w+")
    dates = open('dates.txt', "r")
    dates_out = open('dates_out.txt', "w+")
    emails = open('emails.txt', "r")
    emails_out = open('emails_out.txt', "w+")

    for line in terms:
        line.replace("\\", "")
        temp = line.split(":")
        print(temp)
        terms_out.write(temp[1]+temp[0]+"\n")
    terms.close()
    terms_out.close()

    for line in dates:
        line.replace("\\", "")
        temp = line.split(":")
        print(temp)
        dates_out.write(temp[1]+temp[0]+"\n")
    dates.close()
    dates_out.close()

    for line in emails:
        line.replace("\\", "")
        temp = line.split(":")
        print(temp)
        emails_out.write(temp[1]+temp[0]+"\n")
    emails.close()
    emails_out.close()

reformat()