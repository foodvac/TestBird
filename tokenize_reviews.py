# tokenizes reviews in database by word, writes result to output

output = 'C:/Users/Patrick/Downloads/spider_google_play/tokenized.txt'

import nltk

from lib.dbconnect import ConnectDB

SEPARATOR = '\001'

def get_reviews():
    conn = ConnectDB(conn_cfg='cfg/db.cfg', db='appdb', dbtype='postgresql')
    conn.cursor.execute("SELECT score, review_content FROM review_table;")
    reviews = conn.cursor.fetchall()
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    a = open(output, 'w')
    cnt = 0
    pos = 0
    for item in reviews:
        if pos % 100 == 1:
            print pos
        pos += 1
        #print item
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
            else:
                continue
            new_line = str(score) + SEPARATOR
            for sentence in sentences:
                tokens = nltk.word_tokenize(sentence)
                new_line += SEPARATOR.join(tokens) + SEPARATOR
            a.write(new_line)
            a.write('\n')
        except:
            cnt += 1
            continue
    print cnt
    a.close()

if __name__ == '__main__':
    get_reviews()