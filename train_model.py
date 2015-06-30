# writes in format:
# WORD P(pos|word) P(neg|word)
# for each WORD that appears n or more times

input_file = 'C:/Users/Patrick/Downloads/spider_google_play/tokenized.txt'
output_file = 'C:/Users/Patrick/Downloads/spider_google_play/out_probabilities.txt'
test_output = 'C:/Users/Patrick/Downloads/spider_google_play/test_output.txt'
SEPARATOR = '\001'

n = 8

if __name__ == '__main__':
    reviews = open(input_file)
    probs = open(output_file, 'w')
    test = open(test_output, 'w')
    phrases = {} # [word, (num pos, num neg)}
    total_words = 0.0
    pos_words = 0.0
    neg_words = 0.0
    pos_rev = 0.0
    neg_rev = 0.0
    review_list = reviews.readlines()
    num_reviews = len(review_list)
    pos = 0

    test_cases = []
    total = 0
    for review in review_list:
        if pos == int(0.7 * num_reviews):
            test_cases.append(review)
            continue
        pos += 1

        words = review.lower().split(SEPARATOR)
        tag = 0
        if words[0] == '3':
            test_cases.append(review)
            continue
        elif words[0] == '1' or words[0] == '2':
            tag = -1
            neg_rev += 1
        elif words[0] == '4' or words[0] == '5':
            tag = 1
            pos_rev += 1
        total += 1
        words.pop(0)
        #words = list(set(words))
        for word in words:
            word = word.strip()
            if word == '\n' or word == '':
                continue

            total_words += 1
            if not phrases.get(word):
                if tag == 1:
                    phrases[word] = [1.0, 0.0]
                    pos_words += 1
                else:
                    phrases[word] = [0.0, 1.0]
                    neg_words += 1
            else:
                if tag == 1:
                    phrases[word][0] += 1
                    pos_words += 1
                else:
                    phrases[word][1] += 1
                    neg_words += 1
    print total
    print "total words: ", total_words
    print "pos_words: ", pos_words
    print "neg_words: ", neg_words
    print "pos_rev: ", pos_rev
    print "neg_rev: ", neg_rev

    p_pos_rev = pos_rev / (pos_rev + neg_rev)
    p_neg_rev = neg_rev / (pos_rev + neg_rev)

    test.write(str(pos_rev) + ' ' + str(neg_rev) + '\n')
    for review in test_cases:
        test.write(review)

    for phrase in phrases:
        if phrases[phrase][0] + phrases[phrase][1] < n:
            continue

        # if phrases[phrase][1] > 180:
        #     print phrase
        #     continue

        pos_occ = phrases[phrase][0]
        neg_occ = phrases[phrase][1]

        pos_prob = (pos_occ / pos_words)  # * p_pos_rev / \
                   #((pos_occ + neg_occ) / (pos_rev + neg_rev))
        neg_prob = (neg_occ / neg_words) # * p_neg_rev / \
                   #((pos_occ + neg_occ) / (pos_rev + neg_rev))
        if pos_prob == 0 or neg_prob == 0:
            continue
        if pos_prob > neg_prob:
            if pos_prob / neg_prob <= 1.15:
                continue
            # elif pos_prob / neg_prob >= 15.0:
            #     continue
        else:
            if neg_prob / pos_prob <= 1.15:
                continue
            # elif neg_prob / pos_prob >= 15.0:
            #     continue
        probs.write(phrase + SEPARATOR + str(pos_prob) + SEPARATOR + str(neg_prob) + '\n' )

    probs.close()
    reviews.close()
    test.close()

# 1.10: 0.839055793991
# 1.15: 0.839239730227

# 15.0: 0.839239730227