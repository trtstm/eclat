import sys


movies = {}

movie_fh = open('movies.csv')
movie_fh.readline()
for line in movie_fh:
    csv = line.split(',')

    id = int(csv[0])
    title = csv[1]
    movies[id] = title
movie_fh.close()

def convertItemsets(line):
    support = float(fh.readline().strip())
    items = line.split(' ')

    print('Support: {}'.format(support))

    for i in range(0, len(items)):
        ids = items[i].split('>')
        ids = map(lambda id: movies[int(id)], ids)

        ids = ' > '.join(ids)
        items[i] = ids

    print('\n'.join(items))

    print('\n')

def convertRules(line):
    items = line.split(' ')

    line2 = fh.readline().strip()
    line3 = fh.readline().strip()

    print('Confidence: {}'.format(line3))

    for i in range(0, len(items)):
        ids = items[i].split('>')
        ids = map(lambda id: movies[int(id)], ids)

        ids = ' > '.join(ids)
        items[i] = ids

    print('\n'.join(items))
    print('=>')

    items = line2.split(' ')

    for i in range(0, len(items)):
        ids = items[i].split('>')
        ids = map(lambda id: movies[int(id)], ids)

        ids = ' > '.join(ids)
        items[i] = ids

    print('\n'.join(items))

    print('\n')



fh = open(sys.argv[1], 'r')
state = 'itemsets'
for line in fh:
    line = line.strip()
    if line == 'itemsets' or line == 'rules':
        state = line
        continue

    if state == 'itemsets':
        convertItemsets(line)
    else:
        convertRules(line)
fh.close()
