import nltk

from lib.dbconnect import ConnectDB

SEPARATOR = '\001'

def get_reviews():
    conn = ConnectDB(conn_cfg='cfg/db.cfg', db='appdb', dbtype='postgresql')
    conn.cursor.execute("SELECT review_content FROM review_table;")
    reviews = conn.cursor.fetchall()
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    a = open('C:/Users/Patrick/Downloads/spider_google_play/tokenized.txt', 'w')
    cnt = 0
    pos = 0
    for item in reviews:
        if pos % 100 == 1:
            print pos
        pos += 1
        #print item
        try:
            sentences = nltk.sent_tokenize(item[0].decode('utf8'))
            new_line = ''
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