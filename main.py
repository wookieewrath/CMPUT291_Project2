import xml.etree.ElementTree as ET
import re
import os

def main():
    # Load the input XML file into Python3 as an Element Tree.
    # Create a tree and root object to navigate the file, and a count object to dictate the summation of elements.
    file = input("Please print the name of the XML file: ")
    tree = ET.parse(file)
    root = tree.getroot()
    count = len(tree.findall('mail'))

    # Creates terms.txt
    length = len(tree.findall("mail"))
    alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789')
    terms = open("terms.txt", "w+")
    for x in range(length):
        if root[x][4].text is not None:
            string = re.split(r"[^0-9a-zA-Z\_\-]", root[x][4].text)
            for y in string:
                if (len(''.join(filter(alphabet.__contains__, y)).lower()) > 2):
                    terms.write("s-" + ''.join(filter(alphabet.__contains__, y)).lower() + ":" + root[x][0].text + "\n")
        if root[x][7].text is not None:
            string = re.split(r"[^0-9a-zA-Z\_\-]", root[x][7].text)
            for y in string:
                if (len(''.join(filter(alphabet.__contains__, y)).lower()) > 2):
                    terms.write("b-" + ''.join(filter(alphabet.__contains__, y)).lower() + ":" + root[x][0].text + "\n")
    terms.close()

    # Creates the "dates.txt" file from the XML input using the following format:
    # "date":"row_id"
    date_file = open("dates.txt", "w+")
    for x in root.findall('mail'):
        date = x.find('date').text
        row_id = x.find('row').text
        body = x.find('body').text
        date_file.write("%s: %s\n" % (date, row_id))
    date_file.close()

    # Creates the "emails.txt" file from the XML input using the following format:
    # from-"from_address":"row_id"
    # to-"to_address":"row_id"
    emails_file = open("emails.txt", "w+")
    for x in root.findall('mail'):
        from_address = x.find('from').text
        to_address = x.find('to').text
        row_id = x.find('row').text
        emails_file.write("from-%s:%s\n" % (from_address, row_id))
        emails_file.write("to-%s:%s\n" % (to_address, row_id))
    emails_file.close()
    
    os.system('sort -o dates.txt dates.txt | uniq')
    os.system('sort -o emails.txt emails.txt | uniq')
    os.system('sort -o recs.txt recs.txt | uniq')
    os.system('sort -o terms.txt terms.txt | uniq')


if __name__ == "__main__":
    main()
