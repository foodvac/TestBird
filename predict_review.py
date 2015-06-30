import nltk

grammar = "NP: {<DT>?<JJ>*<NN>}" # pattern
cp = nltk.RegexpParser(grammar)
SEPARATOR = '\001'
input_file = 'C:/Users/Patrick/Downloads/spider_google_play/out_probabilities.txt'
test_file = 'C:/Users/Patrick/Downloads/spider_google_play/test_output.txt'
test_results = 'C:/Users/Patrick/Downloads/spider_google_play/test_results.txt'
wrong_results = 'C:/Users/Patrick/Downloads/spider_google_play/wrong_results.txt'

plaintext = False

th = 0.3

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

def process_probs():
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
    test.close()
    print 'Done processing'
    return (word_probs, info)

def predict(threshold, word_probs, info):
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
    test = open(test_file)
    results = open(test_results, 'w')
    wrong = open(wrong_results, 'w')
    correct = 0.0
    total = 0.0
    true_pos = 0.0
    true_neg = 0.0
    false_pos = 0.0
    false_neg = 0.0
    for review in test.readlines():
        p_pos = float(info[0])/(float(info[0]) + float(info[1]))
        p_neg = float(info[1])/(float(info[0]) + float(info[1]))
        line = review.split('\001')
        score = line.pop(0)
        chunked = line
        if chunked == ["'ve", 'purchased', 'this software', 'a', 'few', 'years', 'ago', 'tried', 'various', 'versions', 'android', 'a', 'few', 'devices', 'experience', 'only', 'a', 'few', 'its', 'features', 'been', 'working', 'relatively', 'well', 'namely', 'backing', 'up', 'restoring', 'data', 'user', 'apps', '(', 'not', 'system', 'apps', ')', 'freezing', 'apps', 'try', 'anything', 'beyond', 'find', 'yourself', 'the twilight', 'zone', 'best', 'outcome', "'ll", 'simply', 'get', 'stuck', 'while', 'trying', 'do', 'what', 'wanted', 'do', '(', 'happened', 'me', 'e.g', 'when', 'tried', 'restore', 'a few user', 'apps', 'including', 'their', 'apk', ')', 'worst', 'outcome', "'ll", 'be', 'forced', 'factory-reset', 'your', 'phone', 'get', 'work', 'normally', 'again', '-', 'happened', 'me', 'way', 'too', 'often', 'e.g', 'after', 'trying', 'restore', 'some system', '(', '``', 'rom', "''", ')', 'apps', 'or', 'after', 'trying', 'integration', 'updates', 'system', '(', '``', 'rom', "''", ')', 'etc', 'bottom', 'line', ':', 'all', 'the software', 'can', 'reliably', 'back', 'up', 'restore', 'data', 'user', 'apps', '(', 'not', 'system', 'apps', ')', 'freeze', 'apps', 'do', 'your', 'phone', 'must', 'be', 'rooted', '(', 'what', 'happens', 'when', 'move', 'a', 'new', 'non-rooted phone', 'want', 'restore', '?', '?', '?', ')', 'so', 'feel', 'there', 'no real reason', 'buy', 'this app', 'instead', 'can', 'back', 'up', 'restore', 'user', 'apps', 'data', 'with', 'helium', 'which', 'free', 'more', 'importantly', '-', 'does', "n't", 'require', 'root', '\n']:
            ''.strip()
        #chunked = list(set(line))
        #print chunked
        for phrase in chunked:
            cur = phrase.strip().lower()
            try:
                p_pos = p_pos * word_probs[cur][0] * 10000
                p_neg = p_neg * word_probs[cur][1] * 10000
            except KeyError:
                continue

        p_prob = p_pos / (p_pos + p_neg)

        if p_prob > threshold:
            if score == '1' or score == '2':
                wrong.write(review)
                for phrase in chunked:
                    cur = phrase.strip().lower()
                    try:
                        wrong.write(cur + ': ' + str(word_probs[cur][0]) + '\t' + str(word_probs[cur][1]) + '\n')
                    except KeyError:
                        #print cur
                        continue
                wrong.write(str(p_pos) + '\t' + str(p_neg) + '\n')
                false_pos += 1
                total += 1
            elif score == '3':
                results.write('POSITIVE ' + review)
            else:
                true_pos += 1
                correct += 1
                total += 1
        else:
            if score == '1' or score == '2':
                true_neg += 1
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
                        #print cur
                        continue
                wrong.write(str(p_pos) + '\t' + str(p_neg) + '\n')
                false_neg += 1
                total += 1

    print 'True positive:\t', true_pos
    print 'True negative:\t', true_neg
    print 'False positive:\t', false_pos
    print 'False negative:\t', false_neg
    print correct
    print total
    print correct / total

    wrong.close()
    results.close()
    return (true_pos/(true_pos + false_neg), false_pos/(true_neg + false_pos))

if __name__ == '__main__':
    returned = process_probs()

    # ROC/AUC data gathering

    # values = []
    # for i in range(1001):
    #     if i % 10 == 0:
    #         print i
    #     values.append(predict(float(i) / 1000, returned[0], returned[1]))
    # val_file = open('C:/Users/Patrick/Downloads/spider_google_play/values.txt', 'w')
    # for value in values:
    #     val_file.write(str(value[0]) + '\t' + str(value[1]) + '\n')
    # val_file.close()

    # or just run once
    predict(th, returned[0], returned[1])

# 0.3:  0.842673206622
# 0.35: 0.84071122011
# 0.4:  0.841569589209