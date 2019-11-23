import xml.etree.ElementTree as ET
import re
import os
import test


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
    print("Created terms.txt")
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
    print("Created dates.txt")
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
    print("Created emails.txt")
    emails_file = open("emails.txt", "w+")
    for x in root.findall('mail'):
        from_address = x.find('from').text
        to_address = x.find('to').text
        row_id = x.find('row').text
        emails_file.write("from-%s:%s\n" % (from_address, row_id))
        emails_file.write("to-%s:%s\n" % (to_address, row_id))
    emails_file.close()
    print("Created ✓")

    '''******************************************************************************************************
    *                                          Create recs.txt                                            *
    ******************************************************************************************************'''

    print("Created recs.txt")
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

    '''******************************************************************************************************
    *                                        Sort the created files                                         *
    ******************************************************************************************************'''

    print("\nSorting terms.txt files:")
    os.system('sort -n -o terms.txt terms.txt | uniq')
    print("Sorted ✓")

    print("\nSorting dates.txt files:")
    os.system('sort -n -o dates.txt dates.txt | uniq')
    print("Sorted ✓")

    print("\nSorting emails.txt files:")
    os.system('sort -n -o emails.txt emails.txt | uniq')
    print("Sorted ✓")

    print("\nSorting recs.txt files:")
    os.system('sort -n -o recs.txt recs.txt | uniq')
    print("Sorted ✓")

    '''******************************************************************************************************
    *                                  Reformat (again smh) for db_load                                     *
    ******************************************************************************************************'''

    print("Reformatting terms.txt for db_load")
    terms = open('terms.txt', "r")
    terms_db_load = open('terms_db_load.txt', "w+")
    for line in terms:
        line.replace("\\", "")
        temp = line.split(":")
        terms_db_load.write(temp[1] + temp[0] + "\n")
    terms.close()
    terms_db_load.close()
    print("Reformatted ✓")

    print("Reformatting dates.txt for db_load")
    dates = open('dates.txt', "r")
    dates_db_load = open('dates_db_load.txt', "w+")
    for line in dates:
        line.replace("\\", "")
        temp = line.split(":")
        dates_db_load.write(temp[1] + temp[0] + "\n")
    dates.close()
    dates_db_load.close()
    print("Reformatted ✓")

    print("Reformatting emails.txt for db_load")
    emails = open('emails.txt', "r")
    emails_db_load = open('emails_db_load.txt', "w+")
    for line in emails:
        line.replace("\\", "")
        temp = line.split(":")
        emails_db_load.write(temp[1] + temp[0] + "\n")
    emails.close()
    emails_db_load.close()
    print("Reformatted ✓")

    print("Reformatting recs.txt for db_load")
    recs = open('recs.txt', "r")
    recs_db_load = open('recs_db_load.txt', "w+")
    for line in recs:
        line.replace("\\", "")
        temp = line.split(":<mail>")
        recs_db_load.write(temp[0] + "\n" + "<mail>" + temp[1])
    recs.close()
    recs_db_load.close()
    print("Reformatted ✓")
    print("\n")

    '''******************************************************************************************************
    *                                          Create index files                                           *
    ******************************************************************************************************'''

    os.system('echo "Creating te.idx"')
    os.system('db_load -f terms_db_load.txt -T -t btree te.idx')
    os.system('db_dump -p -f terms_index te.idx')
    os.system('echo "Completed"')

    os.system('echo "Creating em.idx"')
    os.system('db_load -f emails_db_load.txt -T -t btree em.idx')
    os.system('echo "Completed"')

    os.system('echo "Creating da.idx"')
    os.system('db_load -f dates_db_load.txt -T -t btree da.idx')
    os.system('echo "Completed"')

    os.system('echo "Creating re.idx"')
    os.system('db_load -f recs_db_load.txt -T -t hash re.idx')
    os.system('echo "Completed"')

    test.print_happiness()


if __name__ == "__main__":
    main()
