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
#Create a copy of the search_terms array called subject_body_searches, which we will shortlist for words without an keyword/operator prefix.
search_terms = string.split()
subject_body_searches= []
for i in range(len(search_terms)):
        subject_body_searches.append(search_terms[i])

#Traverse the search_terms array looking for a symbol.
#If the word before the symbol is not an existing key in the query, create a new dictionary entry.
#Otherwise, append the new value to the existing keyword in the query.
#Remove the keyword, the operator, and the value from the subject_body_searches array which will have only appropriate values after the for-loop.
for i in range(len(search_terms)):
        if search_terms[i] in symbols:
                if search_terms[i-1] in keywords and search_terms[i-1] not in query:
                        query[search_terms[i-1]] = ["".join(search_terms[i] + search_terms[i+1])]
                        subject_body_searches.remove(search_terms[i-1])
                        subject_body_searches.remove(search_terms[i])
                        subject_body_searches.remove(search_terms[i+1])
                        
                elif search_terms[i-1] in keywords and search_terms[i-1] in query:
                        query[search_terms[i-1]].append("".join(search_terms[i] + search_terms[i+1]))
                        subject_body_searches.remove(str(search_terms[i-1]))
                        subject_body_searches.remove(str(search_terms[i]))
                        subject_body_searches.remove(str(search_terms[i+1]))     

#If subject is an existing keyword add all the elements of subject_body_searches to their list value
#If not, create the keyword, and add the value
#If body is not an existing keyword add all the elements of subject_body_searches to their list value
#If not, create the keyword, and add the value
print("SEARCH TERMS IN EITHER THE SUBJECT OR BODY:", subject_body_searches) 
print("QUERY DICTIONARY", query)

email_searches = []
terms_searches = []
dates_searches = []

for search_term in query:
        if search_term == "to" or search_term == "from" or search_term == "cc" or search_term == "bcc":
                for value in range(len(query[search_term])):
                        search = search_term + '-' + query[search_term][value][1:]
                        email_searches.append(search)
        
        if search_term == "subj" or search_term == "subject" or search_term == "body":
                for value in range(len(query[search_term])):
                        search = search_term[0] + '-' + query[search_term][value][1:]
                        terms_searches.append(search)
        
        if search_term == "date":
                for value in range(len(query[search_term])):
                        search = query[search_term][value]
                        dates_searches.append(search)


print("EMAIL SEARCHES:", email_searches)
print("TERMS SEARCHES:", terms_searches)
print("DATES SEARCHES:", dates_searches)