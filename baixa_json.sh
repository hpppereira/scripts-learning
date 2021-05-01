#!/bin/bash
#########################################################
#
#		Scrit para baixar dados ALES do link
#			ftp://podaac.jpl.nasa.gov/allData/coastal_alt/L2/ALES/jason-2/
#
#		Utilizacao:
#			Dentro da pasta onde se encontra esse script rode o comando
#			$bash baixa_jason.sh
#
#			Certifique-se que a variavel DIROUT esteja com o caminho correto 
#				para armazenamento dos arquivos baixados
#
#

link='ftp://podaac.jpl.nasa.gov/allData/coastal_alt/L2/ALES/jason-2/'

# DIROUT='/media/nina/Seagate Expansion Drive/Documents/Mestrado projeto/Jason2_data/Jason2_pontual'

DIROUT='/home/lioc/Documentos/Julia_Kaiser/Track_Jason/Santos'

cd $DIROUT

for i in {165..203}; do
	cycle=`printf "%03d\n" $i`
	echo "c${cycle}"

	wget -O index.html ${link}/c${cycle}/

	link_down=`cat index.html | grep JA2_GPS_2PdP${cycle}_050 | sed -n '1p' | awk -F "href=\"" '{print $2}' | awk -F "\"" '{print $1}'`

  file_out=`echo $link_down | awk -F "/" '{print $NF}'`

	# wget -O ${DIROUT}/$file_out $link_down
	wget -O $file_out $link_down

done
