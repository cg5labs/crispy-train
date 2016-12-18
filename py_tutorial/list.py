#!/usr/bin/python

my1stlist = [ 'Joe', 'Bob', 'Alice' ]

my2ndlist = [ 1, 2 ,3 ]

print my1stlist[0]
print my1stlist[2]

print "List/Array length: " + str(len(my1stlist))

my1stlist.append("Jimbo")

print "List/Array length: " + str(len(my1stlist))

mysortedlist = sorted(my1stlist)

for item in mysortedlist:
  print item,
print


