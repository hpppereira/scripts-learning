#criando funcoes e passando como parametro

class Teste:
	def __call__(self, *a): #cria a funcao executavel
		print a

def logged(f):

	def logger(f, *a): #funcao f e qualquer parametro a
		
		print 'Chamando', f.__name__,'com',a
		return f(*a)
	return logger

@logged
def soma(a, b):
	return a+b

print logger(soma, 2, 3)
print loggedsoma(2, 3)