#orientacao a objeto

class Pessoa:
	
	def __init__(self, nome, email):

		self.nome = nome
		self.email = email

	def digaOi(self):

		print 'Oi, eu sou %s' %self.nome

	def ler(self, arquivo):

		print arquivo.read()

	def __add__(self, other):
		
		return Grupo(self, other)

	def __repr__(self):

		return '<Pessoa %s>' %self.nome



class Grupo:

	def __init__(self, *pessoas):

		self.pessoas = list(pessoas)

	def apresentacao(self):

		for p in self.pessoas:

			p.digaOi()

	def __add__(self, other):

		if type(other) == Grupo:

			return Grupo(*(self.pessoas+other.pessoas))

		return Grupo(*(self.pessoas+[other]))

class Programador(Pessoa):

	pass

if __name__ == '__main__':

	p = Programador('Joaquim', 'joaquim@fbi.gov')
	p.digaOi()
	print 'e-mail:', p.email 
