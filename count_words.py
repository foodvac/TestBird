input_file = 'C:/Users/Patrick/Downloads/spider_google_play/clean_output.txt'
output = 'C:/Users/Patrick/Downloads/spider_google_play/wordfreq.txt'

if __name__ == '__main__':
    wordfreq = {}

    file = open(input_file)
    out = open(output, 'w')

    for line in file.readlines():
        old_line = line.lower().split('\001')
        for word in old_line:
            word = word.strip()
            if word == '\n' or word == '':
                continue
            if not wordfreq.get(word):
                wordfreq[word] = 1
            else:
                wordfreq[word] += 1

    freqlist = []

    for item in wordfreq:
        freqlist.append((item, wordfreq[item]))

    freqlist = sorted(freqlist, key=lambda pair: pair[1] * -1)

    for item in freqlist:
        out.write(item[0] + ' ' + str(item[1]))
        out.write('\n')

    file.close()
    out.close()