import xml.etree.ElementTree as ET
import re

tree = ET.parse('eClass Data/1k_records.xml')
root = tree.getroot()

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
            if(len(''.join(filter(alphabet.__contains__, y)).lower())>2):
                terms.write("b-" + ''.join(filter(alphabet.__contains__, y)).lower() + ":" + root[x][0].text + "\n")

