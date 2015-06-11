output = 'C:/Users/Patrick/Downloads/spider_google_play/output.txt'
new_output = 'C:/Users/Patrick/Downloads/spider_google_play/clean_output.txt'
words_to_remove = 'C:/Users/Patrick/Downloads/spider_google_play/to_remove.txt'

def remove(to_remove):
    old_file = open(output)
    new_file = open(new_output, 'w')
    pos = 0
    for line in old_file.readlines():
        if pos % 500 == 0:
            print pos
        pos += 1
        old_line = line.lower().split('\001')
        for i in range(len(old_line)):
            old_line[i] = old_line[i].strip()
        for word in to_remove:
            try:
                for i in range(len(old_line)):
                    old_line.remove(word)
            except:
                continue
        clean_string = '\001'.join(old_line)
        if clean_string != '':
            new_file.write(clean_string + '\n')
    new_file.close()
    old_file.close()


if __name__ == '__main__':
    to_remove = []
    word_file = open(words_to_remove)
    for line in word_file.readlines():
        to_remove.append(line.lower().strip())
    remove(to_remove)
    word_file.close()