print("1")
s = "string"          
print(s[0:2])        # st
print(s[:3])         # str
print(s[3:])         # ing
s2 = "one"          
 
print("Write " + 2*s2 + " " + s)                # Write oneone string
print("hello %s, lab %d  !" % ("students",1))   # hello students, lab 1  !             
 
import string
print("hello {}, lab {}".format("world",1))     # hello world, lab 1
print("hello {1}, lab {0}".format("world",1))   # incepand cu python 2.6

####################################################################

print("")
print("2")
print("Un string:", "4" + "2")                 # Un string: 42
print("Un numar:", 4 % 3 + int("41"))          # Un numar: 42
print("Un string:", "4" + str(2))              # Un string: 42
print('persoana %s are %d ani' % ("X", 42))    # persoana X are 42 ani
print((2.0 + 3.0j) * (2.1  -6.0j))             # (22.2-5.7j)
print(2 ** 3 ** 2)                             # 512

####################################################################

print("")
print("3")
alta_lista = [1,2,3,4]
print(alta_lista)
lista = []
print(lista)
lista.append(5)             # lista va fi [5]
print(lista)
lista.extend(alta_lista)    # lista va fi [5, 1 ,2, 3, 4]
print(lista)
del lista[0]                # lista va fi [1, 2, 3, 4]
print(lista)
del lista[0:2]              # lista va fi [3, 4]
print(lista)
print([1,2,3][2:2])         # afiseaza []
print([1,2,3][0:2])         # afiseaza [1, 2]
print([1,2,3][2:5])         # afiseaza [3]

######################################################################

print("")
print("4")
dict={}
dict[0] = "primul"
dict["unu"] = 2     
print(dict)          # {0: 'primul', 'unu': 2}
dict2 = dict
dict2[3] = "ceva" 
 
del dict2["unu"]  
print(dict)                 # {0: 'primul', 3: 'ceva'}
print(len(dict))            # 2
print(5 in dict)    # False
if 0 in dict:
    dict["3"] = 2  
print(dict)                 # {0: 'primul', '3': 2, 3: 'ceva'}
print(list(dict.keys()))          # [0, '3', 3]

#######################################################################

print("")
print("5")
def fractie(x, y=1):   # y are valoare implicita
    if (y==0):
        return         # va întoarce None
    else:
        return float(x)/float( y)
def fractie2():
    #TODO
    pass
 
print(fractie(6, 4))
print(fractie(6))       # y va fi 1

#######################################################################

print("")
print("6")
from random import random
print(random())

######################################################################

print("")
print("7")
import io
f = open('input.txt','w')
f.write("hello")
f.close()

with open('input.txt', 'r') as f:
    for line in f:   #citire linie cu linie din fisier
        print(line)

#######################################################################

print("")
print("8")
def f1():
   print("hello1")
   print(__name__)
 
#f1()

def f2(f):
	f()

f2(f1)
