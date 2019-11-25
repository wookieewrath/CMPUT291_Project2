import xml.etree.ElementTree as ET
import re
import os


def main():
    # Load the input XML file into Python3 as an Element Tree.
    # Create a tree and root object to navigate the file, and a count object to dictate the summation of elements.
    file = input("Please print the name of the XML file: ")
    tree = ET.parse(file)
    root = tree.getroot()

    '''******************************************************************************************************
    *                                           Create terms.txt                                            *
    ******************************************************************************************************'''
    # Format:
    # s-"subject_term":"row_id"
    # b-"body_term":"row_id"
    print("Creating terms.txt")
    length = len(tree.findall("mail"))
    alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789')
    terms = open("terms.txt", "w+")
    for x in range(length):
        if root[x][4].text is not None:
            string = re.split(r"[^0-9a-zA-Z_\-]", root[x][4].text)
            for y in string:
                if len(''.join(filter(alphabet.__contains__, y)).lower()) > 2:
                    terms.write("s-" + ''.join(filter(alphabet.__contains__, y)).lower() + ":" + root[x][0].text + "\n")
        if root[x][7].text is not None:
            string = re.split(r"[^0-9a-zA-Z_\-]", root[x][7].text)
            for y in string:
                if len(''.join(filter(alphabet.__contains__, y)).lower()) > 2:
                    terms.write("b-" + ''.join(filter(alphabet.__contains__, y)).lower() + ":" + root[x][0].text + "\n")
    terms.close()
    print("Created ✓")

    '''******************************************************************************************************
    *                                           Create dates.txt                                            *
    ******************************************************************************************************'''
    # Format: "date":"row_id"
    print("Creating dates.txt")
    date_file = open("dates.txt", "w+")
    for x in root.findall('mail'):
        date = x.find('date').text
        row_id = x.find('row').text
        body = x.find('body').text
        date_file.write("%s:%s\n" % (date, row_id))
    date_file.close()
    print("Created ✓")

    '''******************************************************************************************************
    *                                          Create emails.txt                                            *
    ******************************************************************************************************'''
    # Format:
    # from-"from_address":"row_id"
    # to-"to_address":"row_id"
    print("Creating emails.txt")
    emails_file = open("emails.txt", "w+")
    for x in root.findall('mail'):
        from_address = x.find('from').text
        to_address = x.find('to').text
        cc_address = x.find('cc').text
        bcc_address = x.find('bcc').text
        row_id = x.find('row').text
        
        if to_address != None:
            to_emails = to_address.split(",") 
            for email in to_emails:
                emails_file.write("to-%s:%s\n" % (email, row_id))
        
        if from_address != None:
            from_emails = from_address.split(",")
            for email in from_emails:
                emails_file.write("to-%s:%s\n" % (email, row_id))
                
        if cc_address != None:
            cc_emails = cc_address.split(",")
            for email in cc_emails:
                emails_file.write("to-%s:%s\n" % (email, row_id))
        
        if bcc_address != None:
            bcc_emails = bcc_address.split(",")
            for email in bcc_emails:
                emails_file.write("to-%s:%s\n" % (email, row_id))        
                
    emails_file.close()
    print("Created ✓")
    
    '''******************************************************************************************************
    *                                           Create recs.txt                                             *
    ******************************************************************************************************'''

    print("Creating recs.txt")
    recs_file = open("recs.txt", "w+")
    xml_file = open(file, "r")

    i = 0

    for line in xml_file:
        i += 1
        if i > 2 and line[0:9] != '</emails>':
            if line[0:6] == '<mail>':
                j = 11
                row = line[j]
                while j < 19:
                    j += 1
                    if line[j].isdigit():
                        row += line[j]
                recs_file.write("%s:%s" % (row, line))
            else:
                recs_file.write("%s" % (line))

    recs_file.close()
    xml_file.close()
    print("Created ✓")
    print("")

    '''******************************************************************************************************
    *                                        Sort the created files                                         *
    ******************************************************************************************************'''
    
    print("Sorting terms.txt files:")
    os.system('sort -o terms.txt terms.txt -u')
    print("Sorted ✓")

    print("Sorting dates.txt files:")
    os.system('sort -o dates.txt dates.txt -u')
    print("Sorted ✓")

    print("Sorting emails.txt files:")
    os.system('sort -o emails.txt emails.txt -u')
    print("Sorted ✓")

    print("Sorting recs.txt files:")
    os.system('sort -o recs.txt recs.txt -u')
    print("Sorted ✓")
    print("")

    '''******************************************************************************************************
    *                                  Reformat (again smh) for db_load                                     *
    ******************************************************************************************************'''

    print("Reformatting terms.txt for db_load")
    terms = open('terms.txt', "r")
    terms_db_load = open('terms_db_load.txt', "w+")
    for line in terms:
        line = line.replace("\\", "")
        temp = line.split(":")
        terms_db_load.write(temp[0] + "\n" +  temp[1])
    terms.close()
    terms_db_load.close()
    print("Reformatted ✓")

    print("Reformatting dates.txt for db_load")
    dates = open('dates.txt', "r")
    dates_db_load = open('dates_db_load.txt', "w+")
    for line in dates:
        line = line.replace("\\", "")
        temp = line.split(":")
        dates_db_load.write(temp[0] + "\n" +  temp[1])
    dates.close()
    dates_db_load.close()
    print("Reformatted ✓")

    print("Reformatting emails.txt for db_load")
    emails = open('emails.txt', "r")
    emails_db_load = open('emails_db_load.txt', "w+")
    for line in emails:
        line = line.replace("\\", "")
        temp = line.split(":")
        emails_db_load.write(temp[0] + "\n" +  temp[1])
    emails.close()
    emails_db_load.close()
    print("Reformatted ✓")

    print("Reformatting recs.txt for db_load")
    recs = open('recs.txt', "r")
    recs_db_load = open('recs_db_load.txt', "w+")
    for line in recs:
        line = line.replace("\\", "")
        temp = line.split(":<mail>")
        recs_db_load.write(temp[0] + "\n" + "<mail>" + temp[1])
    recs.close()
    recs_db_load.close()
    print("Reformatted ✓")
    print("")

    '''******************************************************************************************************
    *                                          Create index files                                           *
    ******************************************************************************************************'''

    os.system('echo "Creating te.idx"')
    os.system('db_load -f terms_db_load.txt -c duplicates=1 -T -t btree te.idx')
    os.system('db_dump -p -f terms_index te.idx')
    os.system('echo "Completed ✓"')

    os.system('echo "Creating em.idx"')
    os.system('db_load -f emails_db_load.txt -c duplicates=1 -T -t btree em.idx')
    os.system('db_dump -p -f emails_index em.idx')
    os.system('echo "Completed ✓"')

    os.system('echo "Creating da.idx"')
    os.system('db_load -f dates_db_load.txt -c duplicates=1 -T -t btree da.idx')
    os.system('db_dump -p -f dates_index da.idx')
    os.system('echo "Completed ✓"')

    os.system('echo "Creating re.idx"')
    os.system('db_load -f recs_db_load.txt -c duplicates=1 -T -t hash re.idx')
    os.system('db_dump -p -f recs_index re.idx')
    os.system('echo "Completed ✓"')

    turtle = (r'''
                Yee we done bois!!!
                
                "Brevity is the soul of wit"
                    -- William Shakespeare, Hamlet
                        -- K. N. King, C Programming: a Modern Approach
                        
                                         ___-------___
                                     _-~~             ~~-_
                                 _-~                    /~-_
              /^\__/^\          /~  \                   /    \
             /|  O|| O|       /     \_______________/          \
            | |___||__|      /       /                \          \
            |          \    /      /                    \          \
            |   (_______) /______/                        \_________ \
            |         / /         \                      /             \
             \         \^\\         \                  /                 \     /
              \         ||           \______________/      _-_          //\__//
               \       ||------_-~~-_ ------------- \ --/~   ~\        || __/)
                ~-----||====/~      |==================|       |/~~~~~
                 (_(__/  ./       /                   \_\      \.
                           (_(___/                       \_____)_)

                           ''')
    print(turtle)


if __name__ == "__main__":
    main()
