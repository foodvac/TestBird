import nltk

grammar = "NP: {<DT>?<JJ>*<NN>}" # pattern
cp = nltk.RegexpParser(grammar)
SEPARATOR = '\001'
input_file = 'C:/Users/Patrick/Downloads/spider_google_play/out_probabilities.txt'
test_file = 'C:/Users/Patrick/Downloads/spider_google_play/test_output.txt'
test_results = 'C:/Users/Patrick/Downloads/spider_google_play/test_results.txt'
wrong_results = 'C:/Users/Patrick/Downloads/spider_google_play/wrong_results.txt'

plaintext = False

def chunk_review(review):
    try:
        sentences = nltk.sent_tokenize(review.decode('utf8'))
        final = []
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            tmp = []
            for token in tokens:
                tmp.append(token.decode('utf8'))
            tokens = tmp
            tagged = nltk.pos_tag(tokens)
            result = cp.parse(tagged)
            for i in range(len(result)):
                subtree = result[i]
                try:
                    phrase = ''
                    for leaf in subtree.leaves():
                        phrase = phrase + leaf[0] + ' '
                    final.append(phrase)
                except AttributeError:
                    final.append(subtree[0])
        return final
    except:
        return None

if __name__ == '__main__':
    probs = open(input_file)
    word_probs = {}
    for line in probs.readlines():
        word_line = line.split(SEPARATOR)
        for word in word_line:
            word.strip()
        word_probs[word_line[0]] = (float(word_line[1]), float(word_line[2]))
    probs.close()

    test = open(test_file)
    info = test.readline().split()
    p_pos = float(info[0])/(float(info[0]) + float(info[1]))
    p_neg = float(info[1])/(float(info[0]) + float(info[1]))
    print 'Done processing'

    # if plaintext:
    #     review = raw_input('Enter review: ')
    #     chunked = chunk_review(review)
    #     for phrase in chunked:
    #         cur = phrase.strip().lower()
    #         try:
    #             p_pos = p_pos * word_probs[cur][0]
    #             p_neg = p_neg * word_probs[cur][1]
    #         except:
    #             continue
    #     print chunked
    #     print "Probability it is positive: ", p_pos
    #     print "Probability it is negative: ", p_neg
    #     if p_pos >= p_neg:
    #         print "Positive review"
    #     else:
    #         print "Negative review"
    # else:
    results = open(test_results, 'w')
    wrong = open(wrong_results, 'w')
    correct = 0.0
    total = 0.0
    false_pos = 0
    false_neg = 0
    for review in test.readlines():
        p_pos = float(info[0])/(float(info[0]) + float(info[1]))
        p_neg = float(info[1])/(float(info[0]) + float(info[1]))
        if total % 100 == 1:
            print total
        line = review.split('\001')
        score = line.pop(0)
        chunked = list(set(line))
        #print chunked
        len(chunked)
        for phrase in chunked:
            cur = phrase.strip().lower()
            try:
                p_pos = p_pos * word_probs[cur][0]
                p_neg = p_neg * word_probs[cur][1]
            except KeyError:
                continue
        if p_pos >= p_neg:
            if score == '1' or score == '2':
                wrong.write(review)
                for phrase in chunked:
                    cur = phrase.strip().lower()
                    try:
                        wrong.write(cur + ': ' + str(word_probs[cur][0]) + '\t' + str(word_probs[cur][1]) + '\n')
                    except KeyError:
                        print cur
                        continue
                wrong.write(str(p_pos) + '\t' + str(p_neg) + '\n')
                false_pos += 1
                total += 1
            elif score == '3':
                results.write('POSITIVE ' + review)
            else:
                correct += 1
                total += 1
        else:
            if score == '1' or score == '2':
                correct += 1
                total += 1
            elif score == '3':
                results.write('NEGATIVE ' + review)
            else:
                wrong.write(review)
                for phrase in chunked:
                    cur = phrase.strip().lower()
                    try:
                        wrong.write(cur + ': ' + str(word_probs[cur][0]) + '\t' + str(word_probs[cur][1]) + '\n')
                    except KeyError:
                        print cur
                        continue
                wrong.write(str(p_pos) + '\t' + str(p_neg) + '\n')
                false_neg += 1
                total += 1

    print 'False positive: ', false_pos
    print 'False negative: ', false_neg
    print correct
    print total
    print correct / total
    wrong.close()
    results.close()


# False positive:  552
# False negative:  3379
