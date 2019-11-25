from bsddb3 import db
from query_creation import query_creation

'''******************************************************************************************************
*                                  Next Lexicographic Order (sorta?)                                    *
******************************************************************************************************'''


def next_lex(mystring):
    for x in range(len(mystring) - 1, -1, -1):
        if mystring[x] == "z":
            mystring = mystring[:-1]
            return next_lex(mystring)
        else:
            last = mystring[-1]
            mystring = mystring[:-1] + chr(ord(last) + 1)
            return mystring


'''******************************************************************************************************
*                                            Terms Search                                               *
******************************************************************************************************'''


def terms_search(curs, term):
    result = curs.set(bytes(term, 'utf-8'))
    query_set = set()

    while True:
        if result is not None:
            query_set.add(result[1])
            result = curs.next_dup()
        else:
            break

    return query_set


'''******************************************************************************************************
*                                            Terms Search Wild                                          *
******************************************************************************************************'''


def terms_search_wild(curs, term):
    result = curs.set_range(bytes(term, 'utf-8'))
    end_condition = next_lex(term)
    query_set = set()

    while result is not None:
        if str(result[0].decode("utf-8")) >= end_condition:
            break
        else:
            query_set.add(result[1])
            result = curs.next()

    return query_set


'''******************************************************************************************************
*                                            Dates Search                                               *
******************************************************************************************************'''


def dates_search(curs, term):
    symbol = ''
    length = len(term)
    query_set = set()
    i = 0
    for i in range(3):
        if term[i].isdigit() == False:
            symbol += term[i]

        else:
            j = i
            break
    term = term[j:]
    print(term)
    print(symbol)

    result = curs.set(bytes(term, 'utf-8'))

    if symbol == ':':
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.next_dup()
            else:
                break

    elif symbol == '>':
        result = curs.next_nodup()
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.next()
            else:
                break

    elif symbol == '<':
        result = curs.prev()
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.prev()

            else:
                break

    elif symbol == '>=':
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.next()
            else:
                break

    elif symbol == '<=':
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.next_dup()
            else:
                break

        result = curs.prev_nodup()
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.prev()
            else:
                break

    return query_set


'''******************************************************************************************************
*                                            Emails Search                                              *
******************************************************************************************************'''


def emails_search(curs, term):
    result = curs.set(bytes(term, 'utf-8'))
    query_set = set()

    while True:
        if result is not None:
            query_set.add(result[1])
            result = curs.next_dup()
        else:
            break

    return query_set


'''******************************************************************************************************
*                                             Body Search                                               *
******************************************************************************************************'''


def body_search(curs, term):
    term_1 = 'b-' + term
    term_2 = 's-' + term

    result = curs.set(bytes(term_1, 'utf-8'))
    query_set = set()

    while True:
        if result is not None:
            query_set.add(result[1])
            result = curs.next_dup()
        else:
            break

    result = curs.set(bytes(term_2, 'utf-8'))

    while True:
        if result is not None:
            query_set.add(result[1])
            result = curs.next_dup()
        else:
            break

    return query_set


'''******************************************************************************************************
*                                          Body Search Wild                                             *
******************************************************************************************************'''


def body_search_wild(curs, term):
    term_1 = 'b-' + term
    term_2 = 's-' + term
    end_condition1 = next_lex(term_1)
    end_condition2 = next_lex(term_2)

    result = curs.set_range(bytes(term_1, 'utf-8'))
    query_set = set()

    while result is not None:
        if str(result[0].decode("utf-8")) >= end_condition1:
            break
        else:
            query_set.add(result[1])
            result = curs.next()

    result = curs.set(bytes(term_2, 'utf-8'))

    while result is not None:
        if str(result[0].decode("utf-8")) >= end_condition2:
            break
        else:
            query_set.add(result[1])
            result = curs.next()
    
    return query_set


'''******************************************************************************************************
*                                                 MAIN                                                  *
******************************************************************************************************'''


def main():
    terms_file = "te.idx"
    dates_file = "da.idx"
    emails_file = "em.idx"
    recs_file = "re.idx"

    terms_database = db.DB()
    dates_database = db.DB()
    emails_database = db.DB()
    recs_database = db.DB()

    terms_database.open(terms_file)
    dates_database.open(dates_file)
    emails_database.open(emails_file)
    recs_database.open(recs_file)

    terms_curs = terms_database.cursor()
    dates_curs = dates_database.cursor()
    emails_curs = emails_database.cursor()
    recs_curs = recs_database.cursor()

    print("\nWelcome to the database!")
    print(">Entering 'output=full' will output full records")
    print(">Entering 'output=brief' will output Row ID and Subject")
    print(">Enter 'EXIT' to exit the database\n")

    mode = "brief"

    while True:
        foo = input("Please enter a search query: ")

        if foo == 'EXIT':
            break

        if foo == "output=full":
            mode = "full"
            print("Now in full output mode.")
            continue

        if foo == "output=brief":
            mode = "brief"
            print("Now in brief output mode.")
            continue

        search_dict = query_creation(foo)
        print("This is the search dictionary")
        print(search_dict)

        sets = []

        for database in search_dict:

            if database == "terms_curs":
                i = 0
                for term in search_dict[database]:
                    if i == 0:
                        if '%' in term:
                            term = term[:-1]
                            term_set = terms_search_wild(terms_curs, term)
                        else:
                            term_set = terms_search(terms_curs, term)
                        i += 1
                    else:
                        if '%' in term:
                            term = term[:-1]
                            term_set = term_set.intersection(terms_search(terms_curs, term))
                        else:
                            term_set = term_set.intersection(terms_search(terms_curs, term))

                sets.append(term_set)

            if database == "dates_curs":
                i = 0
                for term in search_dict[database]:
                    if i == 0:
                        dates_set = dates_search(dates_curs, term)
                        i += 1
                    else:
                        dates_set = dates_set.intersection(dates_search(dates_curs, term))

                sets.append(dates_set)

            if database == "emails_curs":
                i = 0
                for term in search_dict[database]:
                    if i == 0:
                        emails_set = emails_search(emails_curs, term)
                        i += 1
                    else:
                        emails_set = emails_set.intersection(emails_search(emails_curs, term))

                sets.append(emails_set)

            if database == "subj_or_body":
                i = 0
                for term in search_dict[database]:
                    if i == 0:
                        if '%' in term:
                            term = term[:-1]
                            body_set = body_search_wild(terms_curs,term)
                        else:
                            body_set = body_search(terms_curs, term)
                        i += 1
                    else:
                        if '%' in term:
                            term = term[:-1]
                            body_set = body_set.intersection(body_search_wild(terms_curs,term))
                        else:
                            body_set = body_set.intersection(body_search(terms_curs, term))

                sets.append(body_set)

            j = 0
            for i in sets:
                if j == 0:
                    final_set = i
                    j += 1

                else:
                    final_set = final_set.intersection(i)

            some_list = list(final_set)
            some_list.sort()

            if mode == "full":
                print("\n")
                for row in some_list:
                    result = recs_curs.set(row)
                    print(result[1].decode("utf-8"))

            elif mode == "brief":
                print("\n")
                for row in some_list:
                    result = recs_curs.set(row)

                    subject = result[1].decode("utf-8")

                    subject = subject[subject.find("<subj>") + 6: subject.find("</subj>")]
                    print(result[0].decode("utf-8"), end='')
                    print(" " + subject)

    arnie = r'''

        Hasta la vista, baby.
                               ______
                             <((((((\\\
                             /      . }\
                             ;--..--._|}
          (\                 '--/\--'  )
           \\                | '-'  :'|
            \\               . -==- .-|
             \\               \.__.'   \--._
             [\\          __.--|       //  _/'--.
             \ \\       .'-._ ('-----'/ __/      \
              \ \\     /   __>|      | '--.       |
               \ \\   |   \   |     /    /       /
                \ '\ /     \  |     |  _/       /
                 \  \       \ |     | /        /
                  \  \      \        /

    '''
    print(arnie)


if __name__ == "__main__":
    main()
