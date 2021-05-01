# -*- coding: utf-8 -*-

import MySQLdb

print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='admin', host='localhost', port=8080)

# Descomente se quiser desfazer o banco...
# conn.cursor().execute("DROP DATABASE `atmplay`;")
# conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE atmplay /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `atmplay`;
    CREATE TABLE `cidades` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `estado` varchar(40) COLLATE utf8_bin NOT NULL,
      `posicao` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `modelagem` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `wind_spd` varchar(20) COLLATE utf8_bin NOT NULL,
      `wind_dir` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

# stop

print ('Criando tabelas...')
conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO atmplay.cidades (nome, estado, posicao) VALUES (%s, %s,  %s)',
      [
            ('rio_de_janeiro', 'RJ', '-32.00, -44.00'),
            ('niteroi', 'RJ', '-32.00, -44.00'),
            ('sao_goncalo', 'RJ', '-32.00, -44.00'),
      ])

cursor.execute('select * from atmplay.cidades')
print(' -------------  Cidades:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO atmplay.modelagem (wind_spd, wind_dir) VALUES (%s, %s)',
      [
            ('Ação', 'PS4'),
            ('Esporte', 'Xbox One'),
            ('Indie', 'PS4'),
            ('RPG', 'SNES'),
            ('Corrida', 'SNES'),
            ('Estratégia', '3DS'),
      ])

cursor.execute('select * from jogoteca.jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()