import sys
import itertools
import math

tidlists = {1: {}};

min_sup = float(sys.argv[1])
min_conf = float(sys.argv[2])

print('Reading dataset.')
dataset = open(sys.argv[3])
tid = 0
for line in dataset:
    line = line.strip()
    if len(line) == 0:
        continue

    items = line.split(' ')

    for item in items:
        item = (item,)
        if item not in tidlists[1]:
            tidlists[1][item] = set()
        tidlists[1][item].add(tid)

    tid += 1
dataset.close()
print('Dataset reading done.')
transactions = tid
min_sup_count = min_sup * transactions

n_items = len(tidlists[1])
print('Number of items: {}.'.format(n_items))

tidlists[1] = {k:v for k,v in tidlists[1].items() if len(v) >= min_sup_count}

n_frequent_items = len(tidlists[1])
print('Number of requent items: {}. Removed {}.'.format(n_frequent_items, n_items - n_frequent_items))

def has_same_prefix(itemset1, itemset2, n):
    for i in range(0, min(len(itemset1), len(itemset2))):
        if n == 0:
            return True

        if itemset1[i] != itemset2[i]:
            return False
        n -= 1

    return n == 0

def eclat():
    k = 2
    while True:
        print('Searching for {}-itemsets.'.format(k))
        tidlists[k] = {}
        combination_counter = 0
        #n_combinations = math.factorial(len(tidlists[k-1]))/(2 * math.factorial(len(tidlists[k-1])-2))
        #print('Possible number of combinations: {}.'.format(n_combinations))
        for itemset1, itemset2 in itertools.combinations(tidlists[k-1].keys(), r=2):
            combination_counter += 1
            if not has_same_prefix(itemset1, itemset2, k-2):
                continue

            tidlist1, tidlist2 = tidlists[k-1][itemset1], tidlists[k-1][itemset2]
            intersection = tidlist1.intersection(tidlist2)
            if len(intersection) < min_sup_count:
                continue

            tidlists[k][tuple(list(itemset1) + [itemset2[len(itemset2)-1]])] = intersection


        if len(tidlists[k]) == 0:
            del tidlists[k]
            break


        print('Number of frequent {}-itemsets: {}.'.format(k, len(tidlists[k])))
        k += 1


    out = open(sys.argv[4], 'w')
    # Print results
    out.write('itemsets\n')
    for i in range(1, k):
        #print('Frequent {}-itemsets'.format(i))
        for (itemset, tidlist) in tidlists[i].items():
            out.write(' '.join(itemset1) + '\n')
            out.write(str(len(tidlist)/transactions) + '\n')

    out.write('rules\n')
    for i in range(1, k):
        #print('Frequent {}-itemsets'.format(i))
        for (itemset, tidlist) in tidlists[i].items():
            subsets = []
            for j in range(1, len(itemset)):
                subsets = subsets + list(itertools.combinations(itemset, j))

            for subset in subsets:
                difference = set(itemset).difference(subset)
                confidence = len(tidlist)/len(tidlists[len(subset)][tuple(subset)])
                if confidence < min_conf:
                    continue
                out.write(' '.join(subset) + '\n')
                out.write(' '.join(difference) + '\n')
                out.write(str(confidence) + '\n')

    out.close()

eclat()
