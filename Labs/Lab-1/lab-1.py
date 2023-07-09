L1 = ['university', 'blue', 29, (4, 99, 186), [(6,'w'), 19, (5,'z')], 'DATA', 'N9E', 21, 'Delta']
L2 = ['openai', 'law', 98, 8.00, 'lion', 'extranet']

#1.1 Work with list indexing and slicing

#a.
#print(L1[2][1])
# output will be error as index 2 contains an int

#b.
#print(L1[3][0])
# output: 4 as index 3 contains (4, 99, 186) and first index of this set is 4

#c.
#print(L1[4][2][1])
# output: z as index 4 contains [(6,'w'),19,(5,'z')] and index 2 of this list contains (5,'z') and index 1 of this set contains 'z'

#d.
#print(len(L1))
# output: 9

#e.
#print(L1[14])
# output: Index out of range

#f.
#print(L1[-4:-1])
# output: ['DATA'. 'N9E', 21] because traversing from last index till the fourth last index gives us these values.

#g.
#print(L1[2:14])
# output: [29, (4, 99, 186), [(6, 'w'), 19, (5, 'z')], 'DATA', 'N9E', 21, 'Delta'] as it prints all values after 2nd index

#h.
#print(L2+L1)
# output: ['openai', 'law', 98, 8.0, 'lion', 'extranet', 'university', 'blue', 29, (4, 99, 186), [(6, 'w'), 19, (5, 'z')], 'DATA', 'N9E', 21, 'Delta'] as L2 gets appended with L1

#i.
#print(L2*2)
# output: ['openai', 'law', 98, 8.0, 'lion', 'extranet', 'openai', 'law', 98, 8.0, 'lion', 'extranet'] as it duplicates the values of list

#j.
#L1[4][1]=4
#print(L1[4][1])
# output: as it updates list [(6, 'w'), 19, (5, 'z')] at index 4 to [(6, 'w'), 4, (5, 'z')] by replacing value at index 1 of this list

#k.
#del L2[-3]
#print(L2)
# output: It will delete the third last element in the list which is 8.00, updated list is ['openai', 'law', 98, 'lion', 'extranet']

#1.2- Work with list methods and data types:

#a.
#L1.append('ublike')
#print(L1)
# output: It appends ublike at the end of the list

#b.
#L2.pop()
#print(L2)
# output: extranet gets removed from L2 and the new values of list L2 are ['openai', 'law', 98, 8.0, 'lion']

#c.
#L2.insert(3, 4.8)
#print(L2)
# output: 4.8 gets inserted into the list L2 at index 3, updated list is ['openai', 'law', 98, 4.8, 8.0, 'lion']

#d.
#L2.append([44,50])
#print(L2)
# output: [44,50] gets appended at the end of the list L2, updated list is ['openai', 'law', 98, 4.8, 8.0, 'lion', [44, 50]]

#Part 2-Strings in Python
s1 = "One should note that IEEE Transactions are extremely selected"
s2 = "There are two areas in cloud computing: performance and security"

#work with string indexing, slicing, striding, assignment, concatenation

#a.
#print(s1[:9])
# output: One shoul as it prints values of string from first index till the 9th

#b.
#print(s2[-1:-4])
# output: It prints nothing. 

#c.
#print(s2[-2:])
# output: ty as it prints all values from second last till the last

#d.
#print(s2[0:15:2])
# output: Teeaetoa as it prints all the values from index 0 till 15 with a step(indetentions) value of 2

#e.
#print(s1+" "+s2)
#output: "One should note that IEEE Transactions are extremely selected There are two areas in cloud computing: performance and security", as it concatenates both the strings

#Work with string methods

#a.
#print(s2.endswith('security'))
# output: True

#b.
#print(s2.split())
# output: ['There', 'are', 'two', 'areas', 'in', 'cloud', 'computing:', 'performance', 'and', 'security']

#c.
s1=s1.upper()
s2=s2.upper()
#print(s1)
#print(s2)
# output: ONE SHOULD NOTE THAT IEEE TRANSACTIONS ARE EXTREMELY SELECTETHERE ARE TWO AREAS IN CLOUD COMPUTING: PERFORMANCE AND SECURITY

#d.
#print(s2.replace('data',''))
# output: There are two areas in cloud computing: performance and security, as the string does not contain data so nothing gets replaced.

#e.
#print(s1.count('E'))
# output: 3

# 1) Part 3- Dictionary in Python: Define the following dicts:

#dictionary literals
d1={"name": "Alex", "age": 35, (4, 'f'):['x', 'y', 'z'], 6: "Canada", 44: 99, 19:555}
#dictionary using sequences
d2 = dict([("name","Nancy"), ('age', 44), ((3,4), ['a', 'b', 'c']), (0, 'black'), (33, 67)])
#dictionary using keywords
d3 = dict(id=777, name='Michel', siblings=['Fung', 'Martin', 'Richard']) 

#work with dict methods:

#a.
#print(d1.keys())
# output: dict_keys(['name', 'age', (4, 'f'), 6, 44, 19]), returns all the keys

#b.
#print(d2.values())
# output:dict_values(['Nancy', 44, ['a', 'b', 'c'], 'black', 67]), returns all the values

#c.
#print(d3.get('id'))
# output: 777

#d.
#print(d2.get('age'))
# output: 44

#e.
#print(d3.get('age'))
# output: None

#f.
#print(d3.get('name', 'Tim'))
# output: Michel

#g.
#print(d2.items())
# output: dict_items([('name', 'Nancy'), ('age', 44), ((3, 4), ['a', 'b', 'c']), (0, 'black'), (33, 67)])

#h.
#print(d3['siblings'])
# output: ['Fung', 'Martin', 'Richard']

#i.
#print(d2['siblings'])
# output: KeyError: 'siblings'

#j.
print(d2.update(d3))
#print(d2)
# output: updates d2 with d3 {'name': 'Michel', 'age': 44, (3, 4): ['a', 'b', 'c'], 0: 'black', 33: 67, 'id': 777, 'siblings': ['Fung', 'Martin', 'Richard']}

#k.
print(d2['siblings'])
# output: ['Fung', 'Martin', 'Richard']

#l.
print(d2['name'])
# output: Michel

#m.
print(d1==d2)
# output: False

#n.
print(len(d2))
# output: 7

#o.
for key in d1.keys():
 print(key)
# output: name
#age
#(4, 'f')
#6
#44
#19

#p.
for key in d2.keys():
 print(d2[key]) 
# output: Michel
#44
#['a', 'b', 'c']
#black
#67
#777
#['Fung', 'Martin', 'Richard']


#End