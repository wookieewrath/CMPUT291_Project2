#The following function will take a string to search from the user and map all search words to their search values.
#Each entry in the dictionary will have the following format:
#'SEARCH_KEY' : 'OPERATOR''SEARCH_VALUE'
#Where the operator before the search value can be: ":", "<", or ">" since we need these fields to appropriately query the database.
search_string = input("Enter a string to search by: ")
decomposed_string = list(search_string) #Will decompose the original search_string into a list of its individual characters.
query = {} #Initialize the query dictionary

symbols = ["<",">",":"]
keywords = ["row", "date", "from", "to", "subject", "subj", "cc", "bcc", "body"]

#While we are not at the end of the list, continue to loop through the decomposed_string until you reach a symbol.
#Insert white space before and after the symbol.
#Break the loop when you have reached the end of the decomposed_string.
item = 0
while True:
        if item >= len(decomposed_string):
                break
        elif decomposed_string[item] in symbols:
                decomposed_string.insert(item, " ")
                decomposed_string.insert(item+2, " ")
                item = item+2
        
        else:
                item = item+1

#Rejoin the decomposed_string into a string with white spaces.
#The purpose of this was to ensure that every symbol in the query has white space around itself to isolate it when we call .split()
string = "".join(decomposed_string)

#string.split() will remove all white spaces and create an array of search fields, symbols, and search values.
search_terms = string.split()

#Search this array for symbols.
#If the search_term before the symbol is a keyword, create a dictionary entry.
for i in range(len(search_terms)):
        if search_terms[i] in symbols:
                if search_terms[i-1] in keywords:
                        query[search_terms[i-1]] = search_terms[i] + search_terms[i+1]
                        
print(query)



