#!/bin/bash

## ---------------------------------------------------- #
## Baixa dados do GlobWave via ftp, no modo em tempo
## real (nrt). Dados a partir de 2009
##
## Satelites: CRYOSAT2, ENVISAT, JASON1, 
##            JASON1_geodetic, JASON2
##
## Obs: baixa dados em netcdf dos diretorios
## recursivamente (-r) atraves do comando 'wget -r'
## Modificar de diretorio de donwloadna linha de
## comando do wget
##
## exemplo:
## wget -r ftp://username:password@ftp.example.com/
##
## ---------------------------------------------------- #


#serivor (login e senha)
srv='ftp://w1f612:tempo2@eftp.ifremer.fr' 

#diretorio
dire='/waveuser/globwave/data/l2p/altimeter/nrt/'

#caminho do diretorio
ftpdir=$srv$dire

#baixa arquivos via wget -r
wget -r $ftpdir

#chamar programa em python
#python nc_gw.py



