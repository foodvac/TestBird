import nltk

from lib.dbconnect import ConnectDB

SEPARATOR = '\001'

def get_reviews():
    conn = ConnectDB(conn_cfg='cfg/db.cfg', db='appdb', dbtype='postgresql')
    conn.cursor.execute("SELECT review_content FROM review_table;")
    reviews = conn.cursor.fetchall()
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    a = open('C:/Users/Patrick/Downloads/spider_google_play/output.txt', 'w')
    cnt = 0
    pos = 0
    for item in reviews:
        if pos % 100 == 1:
            print pos
        pos += 1
        #print item
        try:
            sentences = nltk.sent_tokenize(item[0].decode('utf8'))
            for sentence in sentences:
                tokens = nltk.word_tokenize(sentence)
                tmp = []
                for item in tokens:
                    tmp.append(item.decode('utf8'))
                tokens = tmp
                tagged = nltk.pos_tag(tokens)
                result = cp.parse(tagged)
                # first = True
                for i in range(len(result)):
                    subtree = result[i]
                    try:
                        phrase = ''
                        for item in subtree.leaves():
                            phrase = phrase + item[0] + ' '
                        phrase += SEPARATOR
                        #phrase.encode('utf8')
                        a.write(phrase)
                    except AttributeError:
                        phrase = subtree[0] + SEPARATOR
                        #phrase.encode('ASCII')
                        a.write(phrase.encode('utf8'))
            a.write('\n')
        except:
            cnt += 1
            continue
    print cnt
    a.close()

if __name__ == '__main__':
    get_reviews()