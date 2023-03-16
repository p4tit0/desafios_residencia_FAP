


def parse(filepath):
    file = open(filepath, "r")
    for line in file:
        print(line)
    file.close()



if __name__ == '__main__':
    parse('games.log')
