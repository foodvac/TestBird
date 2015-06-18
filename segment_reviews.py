# chunks reviews by pattern defined in grammar

import nltk
import random
from lib.dbconnect import ConnectDB

SEPARATOR = '\001'

def get_reviews():
    conn = ConnectDB(conn_cfg='cfg/db.cfg', db='appdb', dbtype='postgresql')
    conn.cursor.execute("SELECT score, review_content FROM review_table;")
    reviews = conn.cursor.fetchall()
    random.shuffle(reviews)
    grammar = "NP: {<DT>?<JJ>*<NN>}" # pattern
    cp = nltk.RegexpParser(grammar)
    a = open('C:/Users/Patrick/Downloads/spider_google_play/out.txt', 'w')
    cnt = 0
    pos = 0
    for item in reviews:
        if pos % 100 == 1:
            print pos
        pos += 1
        score = -1
        try:
            sentences = nltk.sent_tokenize(item[1].decode('utf8'))
            if item[0] == ' Rated 1 stars out of five stars ':
                score = 1
            elif item[0] == ' Rated 2 stars out of five stars ':
                score = 2
            elif item[0] == ' Rated 3 stars out of five stars ':
                score = 3
            elif item[0] == ' Rated 4 stars out of five stars ':
                score = 4
            elif item[0] == ' Rated 5 stars out of five stars ':
                score = 5
            if score == -1:
                continue
            else:
                a.write(str(score) + SEPARATOR)
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
                        phrase += SEPARATOR
                        a.write(phrase.encode('utf8'))
                    except AttributeError:
                        phrase = subtree[0] + SEPARATOR
                        a.write(phrase.encode('utf8'))
            a.write('\n')
        except:
            cnt += 1
            continue
    print cnt
    a.close()

if __name__ == '__main__':
    get_reviews()