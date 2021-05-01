

#importa modulo ftp
from ftplib import FTP

#concecta ao host
ftp = FTP('eftp.ifremer.fr')

#retorna uma mensagem dizendo que foi concectado
#wlc = ftp.getwelcome()
#print wlc

#login (user,password)
ftp.login('w1f612','tempo2')

#lista os diretorios
#ftp.retrlines('LIST')
#files = ftp.dir()

#mudar o diretorio
ftp.cwd('waveuser/globwave/data/l2p/altimeter/gdr/cryosat2/2012/001')

#para voltar ao diretorio
ftp.cwd('..')


#listar o nome dos arquivos presentes no diretorio corrente
filelist = ftp.nlst()

filename = filelist[0]
# filename = 'GW_L2P_ALT_JAS1_NRT_20130620_003742_20130620_023429_537_173.nc'


#comando para recuperar dados no modo binario
ftp.retrbinary('RETR %s' %filename, open(filename, 'w').write)

#remove a arquivo do servidos
#ftp.delete()

#cria um novo diretorio no server
#ftp.mkd(pathname)

#retorna o pathname do diretorio corrente
#ftp.pwd()

#fechar uma comunicacao via ftp
#ftp.quit()



## ============================================================================ ##

