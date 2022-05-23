# Aishwarya Sivakumar - as6418
# Sairam Haribabu - sh4188

from googleapiclient.discovery import build
import sys
from content import Content
import rocchio

# Method to procees the search result returned by google.
# Traverses through the list of search results and takes relevancy information from user.
# Creates docs, a list of dictionaries of title and snippet.
# Returns docs and no of relevant docs.
def process_search(res):
    docs = []
    relevant_count = 0
    counter = 1
    for item in res['items']:
        dict = {}
        dict["title"] = item['title']
        dict["snippet"] = item['snippet']
        print("Result: ", counter)
        print("TITLE: ", item['title'])
        print("URL: ", item['displayLink'])
        print("SUMMARY: ", item['snippet'])
        print("\n")
        yes = input("Relevant(Y/N)?")
        print("\n")
        if yes.lower() == 'y':
            dict["relevancy"] = 1
            relevant_count += 1
        else:
            dict["relevancy"] = 0
        docs.append(dict)
        counter += 1
    return docs, relevant_count


# Prints the summary block
# Prints current query, current precision, required precision and new query.
def print_summary(old_query, new_query, current_precision, required_precision):
    print("FEEDBACK SUMMARY")
    print("Query: ", old_query)
    print("Current Precision: ", current_precision / 10)
    print("Required precision: ", required_precision)
    if new_query:
        print("Augmented query is: ", new_query)
    else:
        print("Precision achieved!")
    print("\n")


# Iteratively queries google service with query.
# Every iteration does:
#  Calls method to process search results.
#  Calls Content constructor with processed data.
#  Calls rocchio to get updated query.
def main():
    api_key = 'AIzaSyAo07nnsj2_blbE3Yh_N0d1eL8vSth73Pg'
    engine_id = 'acc8d36446995d94c'
    required_precision = float(sys.argv[1])
    query = sys.argv[2]
    service = build("customsearch", "v1", developerKey=api_key)
    iteration_counter = 1
    original_query = query
    while (1):
        print("Iteration Number : ", iteration_counter)
        result = service.cse().list(q=query, cx=engine_id, ).execute()
        if len(result['items']) < 10:
            print("Not enough documents to proceed!")
            return
        docs, no_of_relevant_docs = process_search(result)
        if no_of_relevant_docs == 0:
            print("Not enough relevant documents for next iteration!")
            return
        if no_of_relevant_docs >= 10 * required_precision:
            print_summary(query, None, no_of_relevant_docs, required_precision)
            return
        content = Content(docs, query, original_query, no_of_relevant_docs)
        new_query = rocchio.augment_query(content)
        print_summary(query, new_query, no_of_relevant_docs, required_precision)
        query = new_query
        iteration_counter += 1


if __name__ == '__main__':
    main()
