#Graficos do processamento da axys

from pylab import *
from datetime import *

def graf(data_hora2,mat_onda,eta_mat,dspx_mat,dspy_mat):

	#			 0    1     2    3      4     5      6     7    8    9
	#mat_onda: ([Hs, H10, Hmax, Tmed, Tmax, THmax, HTmax, hm0, tp, dirtp])

	#plotagem das alturas de onda

	# figure()

	# plot(mat_onda[:,0])
	# plot(mat_onda[:,7])
	# plot(mat_onda[:,1])
	# plot(mat_onda[:,2])

	# legend(('Hs','hm0','H10','Hmax'))

	# #plotagem dos periodos

	# figure()

	# plot(mat_onda[:,8])
	# plot(mat_onda[:,3])
	# plot(mat_onda[:,4])

	# legend(('tp','Tmed','Tmax'))

	#plotagem de todas as series de elevacao 
	# * a ideia eh verificar de forma rapido se existe algum valores espurio em algumas serie (no periodo selecionado)
	
	# figure ()
	# plot(eta_mat)
	# title('series de elevacao')

	# figure ()
	# plot(dspx_mat)
	# title('series de dspx')

	# figure ()
	# plot(dspy_mat)
	# title('series de dspy')

	#plotagem dos histogramas das series temporais de onda
	
	#cria variaveis em linha para a plotagem do histograma

	eta_mat1 = reshape(eta_mat,eta_mat.shape[0]*eta_mat.shape[1])
	dspx_mat1 = reshape(dspx_mat,dspx_mat.shape[0]*dspx_mat.shape[1])
	dspy_mat1 = reshape(dspy_mat,dspy_mat.shape[0]*dspy_mat.shape[1])

	# figure ()
	# hist(eta_mat1,100)
	# title('series de elevacao')

	# figure ()
	# hist(dspx_mat1,100)
	# title('series de dspx')

	# figure ()
	# hist(dspy_mat1,100)
	# title('series de dspy')

	figure ()
	subplot(2,1,1), title('elevacao')
	plot(eta_mat)
	subplot(2,1,2)
	hist(eta_mat1,100)
	savefig('hist_eta_RS')

	figure()
	subplot(2,1,1), title('dspx')
	plot(dspx_mat)
	subplot(2,1,2)
	hist(dspx_mat1,100)
	savefig('hist_dspx_RS')

	figure()
	subplot(2,1,1), title('dspy')
	plot(dspy_mat)
	subplot(2,1,2)
	hist(dspy_mat1,100)
	savefig('hist_dspy_RS')

	#plot das series de Hs, Hmax, hm0, tp

	figure ()
	subplot(2,1,1), title('Hs')
	plot(mat_onda[:,0])
	subplot(2,1,2)
	hist(mat_onda[:,0],100)
	savefig('hist_Hs_RS')

	figure()
	subplot(2,1,1), title('Hmax')
	plot(mat_onda[:,2])
	subplot(2,1,2)
	hist(mat_onda[:,2],100)
	savefig('hist_Hmax_RS')

	figure()
	subplot(2,1,1), title('hm0')
	plot(mat_onda[:,7])
	subplot(2,1,2)
	hist(mat_onda[:,7],100)
	savefig('hist_hm0_RS')

	figure()
	subplot(2,1,1), title('tp')
	plot(mat_onda[:,8])
	subplot(2,1,2)
	hist(mat_onda[:,8],100)
	savefig('hist_tp_RS')

	figure()
	subplot(2,1,1), title('dirtp')
	plot(mat_onda[:,9])
	subplot(2,1,2)
	hist(mat_onda[:,9],100)
	savefig('hist_dirtp_RS')

	
	##plotagem com 2 eixos y

	fig = figure()
	ax1 = fig.add_subplot(111) #subplot, da para mudar
	t = range(len(mat_onda)) #cria vetor de tempo
	ax1.plot(t,mat_onda[:,9],'b-') #direcao de onda
	ax1.set_xlabel('tempo (horas)')
	ax1.set_ylabel('direcao de onda (graus)',color='b')
	ax2 = ax1.twinx()
	ax2.plot(t,mat_onda[:,8],'r-') #periodo de pico
	ax2.set_ylabel('periodo de pico (s)',color='r')
	axis('tight')


	##plotagem com data no eixo x (ainda nao esta funcionando)

	## exemplo

	# dates_in_string = ['2010-01-01', '2010-01-02', '2010-02-03', '2010-04-05', '2010-07-19']
	# dates_datetime = []
	# for d in dates_in_string:

	#     dates_datetime.append(datetime.datetime.strptime(d, '%Y-%m-%d'))

	# dates_float = date2num(dates_datetime)
	# list1 = [1,2,3,4,5]
	# list2 = [1,2,4,8,16]
	# plot_date(dates_float, list1, linestyle='-', xdate=True, ydate=False)
	# plot_date(dates_float, list2, linestyle='-', xdate=True, ydate=False)




	# dates_in_string = data_hora2
	# dates_datetime = []

	# for d in dates_in_string:

	# 	dates_datetime.append(datetime.datetime.strptime(d, '%d/%m/%Y-%h'))

	# dates_float = date2num(dates_datetime)

	# list1 = mat_onda[:,0]

	# plot_date(dates_float, list1, linestyle='-', xdate=True, ydate=False)

	##grafico polar

	# N = 150
	# r = 2*rand(N)
	# theta = 2*pi*rand(N)
	# area = 200*r**2*rand(N)
	# colors = theta
	# ax = subplot(111, polar=True)
	# c = scatter(theta, r, c=colors, s=area, cmap=cm.hsv)
	# c.set_alpha(0.75)
	
	  # fig, ax = subplots(subplot_kw=dict(projection='polar'))
	  # ax.set_theta_zero_location("N")
	  # ax.set_theta_direction(-1)





	show()






