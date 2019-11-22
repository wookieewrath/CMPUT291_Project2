import xml.etree.ElementTree as ET

def main():

#Load the input XML file into Python3 as an Element Tree.
#Create a tree and root object to navigate the file, and a count object to dictate the summation of elements.
    file = input("Please print the name of the XML file")
    tree = ET.parse(file)
    root = tree.getroot()
    count = len(tree.findall('mail'))

#Creates the "dates.txt" file from the XML input using the following format:
#"date":"row_id"
    date_file = open("dates.txt","w+")      
    for x in root.findall('mail'):
        date = x.find('date').text
        row_id = x.find('row').text
        body = x.find('body').text
        date_file.write("%s: %s\n" %(date,row_id))          
    date_file.close()
    
#Creates the "emails.txt" file from the XML input using the following format:
#from-"from_address":"row_id"
#to-"to_address":"row_id"    
emails_file = open("emails.txt", "w+")
for x in root.findall('mail'):
    from_address = x.find('from').text
    to_address = x.find('to').text
    row_id = x.find('row').text
    emails_file.write("from-%s:%s\n" % (from_address, row_id))
    emails_file.write("to-%s:%s\n" % (to_address, row_id))
emails_file.close()

if __name__ == "__main__":
    main()
