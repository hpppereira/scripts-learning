#!/bin/bash

#operacional para baixar os dados do pnboia
#do site da marinha, goos e siodoc, faz a 
#consistencia dos dados e salva figura

#baixa o dado

#henriquep
/usr/local/python/anaconda/bin/python /home/hp/Dropbox/pnboia/rot/getpnboia.py

#lioc
/usr/local/python/anaconda/bin/python /home/lioc/Dropbox/pnboia/rot/getpnboia.py


#gera as figuras

#henriquep
/usr/local/python/anaconda/bin/python /home/hp/Dropbox/pnboia/rot/pnboiamb.py

#lioc
/usr/local/python/anaconda/bin/python /home/lioc/Dropbox/pnboia/rot/pnboiamb.py

