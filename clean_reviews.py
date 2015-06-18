output = 'C:/Users/Patrick/Downloads/spider_google_play/cleaned_out.txt'
new_output = 'C:/Users/Patrick/Downloads/spider_google_play/clean_out.txt'
words_to_remove = 'C:/Users/Patrick/Downloads/spider_google_play/to_remove.txt'

# removes words in words_to_remove from output and writes result to new_output

def remove(to_remove):
    old_file = open(output)
    new_file = open(new_output, 'w')
    pos = 0
    for line in old_file.readlines():
        if pos % 2000 == 0:
            print pos
        pos += 1
        old_line = line.lower().split('\001')
        for i in range(len(old_line)):
            old_line[i] = old_line[i].strip()
        score = old_line[0]
        old_line.pop(0)
        tmp = old_line
        j = 0
        for i in range(len(tmp)):
            try:
                n = float(tmp[i])
                old_line.pop(j)
            except:
                j += 1

        try:
            if old_line[0] == 'full' and old_line[1] == 'review':
                continue
        except:
            ''.strip

        old_line.insert(0, score)
        for word in to_remove:
            try:
                for i in range(len(old_line)):
                    old_line.remove(word)
            except:
                continue

        old_line = ['great' if 'great' in phrase else phrase for phrase in old_line]

        clean_string = '\001'.join(old_line)
        if clean_string not in ['1\001', '2\001', '3\001', '4\001', '5\001', '1', '2', '3', '4', '5']:
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