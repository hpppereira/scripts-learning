# import csv
# import MySQLdb
import pandas as pd
import os
import csv
import pymysql

pathname = os.environ['HOME'] + '/Dropbox/AtmosMarine/MySQL/database/'
filename = 'INMET_EMA_ABROLHOS_2016.csv'

mydb = pymysql.connect(host='127.0.0.1', port=3306, user='root',passwd='admin',db='DADOS_MET')
cursor = mydb.cursor()

csv_data = pd.read_csv(pathname + filename)
csv_data = csv_data.dropna()

# caso nao tenha uma tabela com algum stId criada,
# necessario criar uma linha com o nome da estacoes.stId

# cursor.execute('INSERT INTO estacoes \
# 			  (stId,nomeEstacao,uf,cidade,latitude,longitude,codigoOMM,registro) \
# 			   VALUES ("RJ001","rio","RJ","Rio de Janeiro",10.0,20.0,"XX","XX")');
# mydb.commit()

for row in csv_data.values:

	row = list(row.astype(str))

	print row

	cursor.execute('INSERT INTO dadosMeteorologicos \
	(estacoes_id,dataHora,temperatura,umidade,po,press,rad,pre,vdd,vvel) \
	VALUES( ( SELECT id FROM estacoes WHERE estacoes.stId = "RJ001"), \
	%s, %s, %s, %s, %s, %s, %s, %s, %s )', row );

mydb.commit()
cursor.close()


