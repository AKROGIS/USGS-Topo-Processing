
list1 = 'pdf_urls_for_uget.txt'
list2 = 'pdf_urls_for_uget2.txt'
list3 = 'pdf_urls_for_uget3.txt'

set1 = set()
with open(list1) as fh:
    for line in fh:
        set1.add(line)

set2 = set()
with open(list2) as fh:
    for line in fh:
        set2.add(line)

set3 = set2 - set1
with open(list3, 'w') as fh:
    for line in set3:
        fh.write(line)
