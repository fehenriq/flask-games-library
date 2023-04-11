import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='87654321'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no name de usuário ou password')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

TABLES = {}
TABLES['Games'] = ('''
    CREATE TABLE `games` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `category` varchar(40) NOT NULL,
    `platform` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
    CREATE TABLE `users` (
    `name` varchar(20) NOT NULL,
    `nickname` varchar(8) NOT NULL,
    `password` varchar(100) NOT NULL,
    PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
    table_sql = TABLES[table_name]
    try:
        print('Criando tabela {}:'.format(table_name), end=' ')
        cursor.execute(table_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Já existe')
        else:
                print(err.msg)
    else:
        print('OK')

# inserindo usuarios
user_sql = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
users = [
    ("Felipe Rodrigues", "FeHenriq", generate_password_hash("fran").decode("utf-8")),
    ("Fran Oliveira", "FranOliv", generate_password_hash("fe").decode("utf-8")),
    ("Dri Rodrigues", "DriCake", generate_password_hash("mae").decode("utf-8"))
]
cursor.executemany(user_sql, users)

cursor.execute('select * from jogoteca.users')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
games_sql = 'INSERT INTO games (name, category, platform) VALUES (%s, %s, %s)'
games = [
    ('God of War', 'Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Fight', 'Xbox'),
    ('League of Legends', 'MOBA', 'PC'),
    ('Clash Royale', 'MOBA', 'Mobile'),
    ('Grand Theft Auto', 'RPG', 'PS4'),
    ('Albion Online', 'MMORPG', 'PC')
      
]
cursor.executemany(games_sql, games)

cursor.execute('select * from jogoteca.games')
print(' -------------  Jogos:  -------------')
for game in cursor.fetchall():
    print(game[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
