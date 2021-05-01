# Acesso ao ftp do python - teste para 
# aprender como acessar dados via ftp

from ftplib import FTP

#conecta ao ftp
ftp = FTP('ftp.debian.org') # connect to host, default port

#funcao para indicar que foi conectado
print ftp.getwelcome()

#faz o login
ftp.login() #user anonymous, passwd anonymous@

#entra na pasta debian (funcao para ir para a pasta desejada)
ftp.cwd('debian')               # change into "debian" directory

#lista os diretorios da pasta que estamos (no caso a debian)
ftp.retrlines('LIST')           # list directory contents

#baixa o arquivo para a pasta que esta o programa
ftp.retrbinary('RETR README', open('README', 'wb').write)

#fecha a conexao?
ftp.quit()




## lista os diretorios e arquivos do servidor ftp
## files  = ftp.dir()
## print files
## ftp.cwd('/pub/unix') #muda para o diretorio /pub/unix
## 