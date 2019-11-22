import xml.etree.ElementTree as ET

def main():

    file = input("Please print the name of the XML file")
    tree = ET.parse(file)
    root = tree.getroot()
    count = len(tree.findall('mail'))

    date_file = open("dates.txt","w+")
                
    for x in root.findall('mail'):
        date = x.find('date').text
        row_id = x.find('row').text
        body = x.find('body').text
        date_file.write("%s: %s\n" %(date,row_id))
                           
    date_file.close()

if __name__ == "__main__":
    main()
