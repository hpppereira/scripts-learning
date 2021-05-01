#curso python

#map reduce
'''
achar os valores impares e calcular o quadrado'''

numbers = range(101)

ret = []

for n in numbers:
	if n % 2: #se tem resto
		ret.append(n ** 2)

print ret

def impar(n):
	return n % 2

def quadrado(n):
	return n ** 2

print map(quadrado, filter(impar, numbers))


#listen comprehension

ret1 = [ n ** 2 for n in numbers if n % 2 ]

print ret1