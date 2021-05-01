#Graficos do processamento da axys

from pylab import *
from datetime import *

def graf(mat_onda,eta_mat_cons,dspx_mat_cons,dspy_mat_cons,reg_fw,Hmax_fw,Hs_fw,THmax_fw,rel_fw,ind_fw):
    
    close('all')

    eta_mat_cons = eta_mat_cons[0:1024,:]
    dspx_mat_cons = dspx_mat_cons[0:1024,:]
    dspy_mat_cons = dspy_mat_cons[0:1024,:]

	# 			 0    1     2    3      4     5      6     7    8    9
	# mat_onda: ([Hs, H10, Hmax, Tmed, Tmax, THmax, HTmax, hm0, tp, dirtp])

	# plotagem das alturas de onda

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

	# plotagem de todas as series de elevacao 
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

	# plotagem dos histogramas das series temporais de onda
	
	# cria variaveis em linha para a plotagem do histograma


#	eta_mat1 = reshape(eta_mat_cons,eta_mat_cons.shape[0]*eta_mat_cons.shape[1])
#	dspx_mat1 = reshape(dspx_mat_cons,dspx_mat_cons.shape[0]*dspx_mat_cons.shape[1])
#	dspy_mat1 = reshape(dspy_mat_cons,dspy_mat_cons.shape[0]*dspy_mat_cons.shape[1])

	# figure ()
	# hist(eta_mat1,100)
	# title('series de elevacao')

	# figure ()
	# hist(dspx_mat1,100)
	# title('series de dspx')

	# figure ()
	# hist(dspy_mat1,100)
	# title('series de dspy')

#	figure ()
#	subplot(2,1,1), title('Elevacao')
#	plot(eta_mat_cons)
#	subplot(2,1,2)
#	hist(eta_mat1,100)
#	savefig('hist_eta_RS')
#
#	figure()
#	subplot(2,1,1), title('Deslocamento em x')
#	plot(dspx_mat_cons)
#	subplot(2,1,2)
#	hist(dspx_mat1,100)
#	savefig('hist_dspx_RS')
#
#	figure()
#	subplot(2,1,1), title('Deslocamento em y')
#	plot(dspy_mat_cons)
#	subplot(2,1,2)
#	hist(dspy_mat1,100)
#	savefig('hist_dspy_RS')

	# plot das series de Hs, Hmax, hm0, tp

#	figure ()
#	subplot(2,1,1), title('Altura significativa (Hs)')
#	plot(mat_onda[:,0])
#	subplot(2,1,2)
#	hist(mat_onda[:,0],100)
#	savefig('hist_Hs_RS')
#
#	figure()
#	subplot(2,1,1), title('Altura maxima (Hmax)')
#	plot(mat_onda[:,2])
#	subplot(2,1,2)
#	hist(mat_onda[:,2],100)
#	savefig('hist_Hmax_RS')
#
#	figure()
#	subplot(2,1,1), title('Altura significativa (Hm0)')
#	plot(mat_onda[:,7])
#	subplot(2,1,2)
#	hist(mat_onda[:,7],100)
#	savefig('hist_hm0_RS')
#
#	figure()
#	subplot(2,1,1), title('Periodo de pico (Tp)')
#	plot(mat_onda[:,8])
#	subplot(2,1,2)
#	hist(mat_onda[:,8],100)
#	savefig('hist_tp_RS')
#
#	figure()
#	subplot(2,1,1), title('Direcao associada ao periodo de pico (DirTp)')
#	plot(mat_onda[:,9])
#	subplot(2,1,2)
#	hist(mat_onda[:,9],100)
#	savefig('hist_dirtp_RS')

	
	# #plotagem com 2 eixos y

#	 fig = figure()
#	 ax1 = fig.add_subplot(111) #subplot, da para mudar
#	 t = range(len(mat_onda)) #cria vetor de tempo
#	 ax1.plot(t,mat_onda[:,9],'b-') #direcao de onda
#	 ax1.set_xlabel('tempo (horas)')
#	 ax1.set_ylabel('direcao de onda (graus)',color='b')
#	 ax2 = ax1.twinx()
#	 ax2.plot(t,mat_onda[:,8],'r-') #periodo de pico
#	 ax2.set_ylabel('periodo de pico (s)',color='r')
#	 axis('tight')

	# #plotagem de histograma com 2 eixos y

#    figure()
#    hist(rand(10),color='b')
#    twinx()
#    hist(rand(10),alpha=0.3,color='r')
#    axis([0,1,0,1.5])
    


	# #plotagem com data no eixo x (ainda nao esta funcionando)

	# # exemplo

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

	# #grafico polar
	# import matplotlib as mpl

	# polar_trans = mpl.transforms.Polar.PolarTransform(theta_offset=np.pi/2)
	# ax = plt.axes(projection=polar_trans)
	# ax.plot(np.arange(100)*0.15, np.arange(100)) 

	# import matplotlib.pylab as plt

	# fig = plt.figure()
	# ax = fig.add_axes( [0.1, 0.1, 0.8, 0.8] ,polar = True)
	# ax.set_theta_offset(pi/2)
	# ax.set_theta_direction(-1)
	# ax.set_xticklabels( [ 'N', 'NE', 'L', 'SE', 'S', 'SO', 'O', 'NO', 'N' ] )

	# plt.show()

	# ## aqui voce seta os valores de theta e r
	# #bars = ax.bar( theta (anglo em rad), r (intensidade do vento)  )
	# bars = ax.bar( pi , 1 )
	# #executa de um em um e vai vendo..

	# fig, ax = subplots(subplot_kw=dict(projection='polar'))
 # 	   ax.set_theta_zero_location("N")
 # 	   ax.set_theta_direction(-1)
 # 	   autumn()
 # 	   cax = ax.contourf(pi, 2, values, 30)
 # 	   autumn()
 # 	   cb = fig.colorbar(cax)
 # 	   cb.set_label("Pixel reflectance")


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

	# plotagem das series de ondas que contem freakwaves

	#   for i in range(len(reg_fw)):
	  	
	#   	figure()

	#   	plot(eta_mat_cons[:,ind_fw[i]])

	#   	title(str(reg_fw[i]) + ', ' + 'Hmax = ' + str(round(Hmax_fw[i],2)) + ', ' + 'Hs = ' + str(round(Hs_fw[i],2)) + ', ' + 'THmax = ' + str(round(THmax_fw[i],2)) + ', ' + 'Rel_fw = ' + str(round(rel_fw[i],2)) )

	#   	savefig('freak'+str(i))

	# figure()

	# plot(Hmax_fw), title('Altua das freakwaves (Alturas maximas das series)')

	# figure()

	# plot(Hs_fw), title('Alturas significativas das series')

	# figure()

	# plot(rel_fw), title('Relacao entre Hmax/Hs')

    #tentar plotar histograma com dois eixos

    #arruma a matriz para fazer o grafico

    eta1 = resize(eta_mat_cons,(size(eta_mat_cons),1))
    dspx1 = resize(dspx_mat_cons,(size(dspx_mat_cons),1))
#
#
#    
    figure()
    hist(eta1,50,color='b')
    ylabel('Num Ocorrencias',color='b')
    xlabel('Elevacao')
    title('Rio Grande do Sul')
    #twinx()
    #hist(eta1,50,color='r',alpha=0.3)
    #axis([-4,4,0,50])    
    #ylabel('n ocorrencias',color='r')


	# dados = loadtxt('/home/hppp/Dropbox/Tese/CQ_Python/Boia_MB_RS/freakwaves/Saida_Param_Axys_RS.txt',skiprows=1)

	# dadosm = loadtxt('/home/hppp/Dropbox/Tese/CQ_Python/Boia_MB_RS/freakwaves/Saida_Param_Axys_Maio_RS.txt',skiprows=1)

	# #          0     1   2    3      4     5    6    7      8     9      10   11   12   13 
	# # dados = ano, mes, dia, hora, minuto, Hs, H10, Hmax, Tmed, THmax, HTmax, Hm0, Tp, DirTp

	# datam = []

	# for i in range(len(dadosm)):

	# datam.append(datetime(int(dadosm[i,0]),int(dadosm[i,1]),int(dadosm[i,2]),int(dadosm[i,3]),int(dadosm[i,4])))

	# plot(mat_onda[:,2]/mat_onda[:,0],mat_onda[:,0],'o')
	# title('Relacao entre a razao Hmax/Hs')
	# xlabel('Razao entre Hmax e Hs')
	# ylabel('Altura significativa (m)')

    show()
