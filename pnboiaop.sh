#!/bin/bash

#operacional para baixar os dados do pnboia
#do site da marinha, goos e siodoc, faz a 
#consistencia dos dados e salva figura

#baixa o dado e gera as figuras

#henriquep
/usr/local/python/anaconda/bin/python /home/hp/Dropbox/pnboia/rot/mbpnboia.py
#lioc
/usr/local/python/anaconda/bin/python /home/lioc/Dropbox/pnboia/rot/mbpnboia.py

#gera as figuras para a avaliacao operacional da previsao
#henriquep
/usr/local/python/anaconda/bin/python /home/hp/Dropbox/pnboia/rot/plotaprevisao.py
#lioc
/usr/local/python/anaconda/bin/python /home/lioc/Dropbox/pnboia/rot/plotaprevisao.py

