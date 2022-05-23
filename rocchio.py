# Aishwarya Sivakumar - as6418
# Sairam Haribabu - sh4188

from collections import defaultdict

# Method implements rocchio's technique with beta as 0.8 and gamma as 0.2
# Bigrams precaculated is used to increase the weights of special words
def implement_rocchio(content):
    beta = 0.8
    gamma = 0.2
    relevant = content.relevant
    irrelevant = content.irrelevant
    bigrams = content.bigrams
    query_words = content.query
    len_r = len(relevant)
    len_irr = len(irrelevant)
    weights = defaultdict(float)
    for vector in relevant:
        for term in vector:
            weights[term] = weights.get(term, 0) + beta * vector[term] / len_r
    for vector in irrelevant:
        for term in vector:
            weights[term] = weights.get(term, 0) - gamma * vector[term] / len_irr
    for bigram in bigrams:
        word1 = bigram[0][0]
        word2 = bigram[0][1]
        weights[word1] *= max(2, bigram[1])
        weights[word2] *= max(2, bigram[1])
        if word1 in query_words:
            weights[word2] *= 1.5
        if word2 in query_words:
            weights[word1] *= 1.5
    return weights


# Method to get final weights of words in vocab and choose 2 candidate words
# The word with highest weight is chosen as first and a word with unique second
# highest weight is chosen as second.
# This handles cases where multiple words have same weight where we only augment query with
# 1 additional word.
# The initial query words are kept as is and new words are appended behind
def augment_query(content):
    query_words = content.query
    original_query_words = content.original_query
    weights = implement_rocchio(content)
    first_word = None
    second_word = None
    weights = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True))
    for term in weights.keys():
        if term not in query_words:
            if first_word is None:
                first_word = term
            elif second_word is None:
                second_word = term
                break

    query_words = list(set(query_words) - set(original_query_words))
    query_words.append(first_word)
    query_words.append(second_word)

    query_words = dict.fromkeys(query_words, 0)
    for word in query_words.keys():
        query_words[word] = weights.get(word, 0)
    query_words = dict(sorted(query_words.items(), key=lambda item: item[1], reverse=True))
    query = ' '.join(original_query_words) + " " + ' '.join(query_words)
    return query
