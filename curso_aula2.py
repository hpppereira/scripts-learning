#abrir o ipython com as funcoes do pylab

#no terminal fazer:
#ipython --pylab

#equivalente ao size do matlab

a.shape

sendo 'a' a matriz

a. e aperta tab vai mostrar o que se pode fazer com a matriz 

np.ones(30 5 14) - cria matriz de 3 dimensoes

#size = tamanho total da matriz

#criar matriz 
x = np.array([[1,2,3],[1,2,3]])

#tirar media da linha ou coluna

x.mean() - faz  a media total
x.mean(axis=0) - media da coluna
x.mean(axis=1) - media da linha

a=np.arrange(10,190,10)

b=np.linspace(1,10,20)

#achar o indice

f = np.where(b > 0)

a=np.ones((10,5,3))

b=a[::,3]

#transformar um array em uma matriz de uma coluna

a.ravel()

f.readline #cada vez que roda, le uma linha

#salvar figura

no pyplot

savefig('figura.jpg')


