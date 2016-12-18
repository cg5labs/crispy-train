#!/usr/bin/python

# Python dictionaries are similar to associative arrays or hash structures in other languages.
people = { 'sam': 38, 'joe': 42, 'susan': 31, 'zed': 28 }

# get the dictionary keys
print people.keys()

# get the dictionary values
print people.values()

# get a specific dictionary element
print "Sam's age: " + str(people['sam'])

# iterate over the dictionary (default iteration: same as people.keys() )
for i in people:
  print i

for i in people:
  print "key:" + i

for i in people.values():
  print "value:" + str(i)

# iterate over keys and values
for i in people:
  print "Person: " + i + " " + "Age: " + str(people[i])



