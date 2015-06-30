test_output = 'C:/Users/Patrick/Downloads/spider_google_play/test_output.txt'
new_test = 'C:/Users/Patrick/Downloads/spider_google_play/new_test.txt'

import random

if __name__ == '__main__':
    test = open(test_output)
    ntest = open(new_test, 'w')

    pos = []
    neg = []
    reviews = []
    for line in test.readlines():
        if line[0] == '1' or line[0] == '2':
            neg.append(line)
        elif line[0] != '3':
            pos.append(line)
    n = 0
    if len(pos) > len(neg):
        n = len(neg)
    else:
        n = len(pos)

    for i in range(n):
        reviews.append(pos[i])
        reviews.append(neg[i])

    random.shuffle(reviews)

    ntest.write(str(float(n)) + ' ' + str(float(n)) + '\n')

    for review in reviews:
        ntest.write(review)

    test.close()
    ntest.close()