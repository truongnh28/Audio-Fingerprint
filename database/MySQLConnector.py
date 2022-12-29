import pymysql
from utils.hparam import hp
from database.IConnector.IConnector import IConnector


class MySQLConnector(IConnector):

    def __init__(self):
        # Call the constructor of the parent class
        super().__init__()

        # Obtained database connection
        self.conn = None

        # Initialize the cursor
        self.cursor = None

        # Connect to the database, assign cursors and database connections
        self._connection()

        pass

    # How to connect
    def _connection(self):

        # Get the connection to mysql
        self.conn = pymysql.connect(
            # CPU name
            host=hp.fingerprint.database.host,
            # The port number
            port=hp.fingerprint.database.port,
            # username
            user=hp.fingerprint.database.user,
            # user password
            password=hp.fingerprint.database.password,
            # Name database
            database=hp.fingerprint.database.database,
            # character set
            charset=hp.fingerprint.database.charset
        )

        # cursor
        self.cursor = self.conn.cursor()
        pass

    # Method to save a fingerprint
    def _add_finger_print(self, item, music_id_fk):
        # SQL
        sql = "insert into %s(%s, %s, %s) values(%s, '%s', '%s')" % (
            hp.fingerprint.database.tables.finger_prints.name,
            hp.fingerprint.database.tables.finger_prints.column.music_id_fk,
            hp.fingerprint.database.tables.finger_prints.column.hash,
            hp.fingerprint.database.tables.finger_prints.column.offset,
            music_id_fk,
            item[0],
            item[1]
        )

        # Execute the SQL statement
        self.cursor.execute(sql)
        self.conn.commit()
        pass

    # store fingerprint
    def store_finger_prints(self, hashes, music_id_fk):
        # Traverse the fingerprints and save them to the database one by one (hash, offset)
        for item in hashes:
            self._add_finger_print(item=item, music_id_fk=music_id_fk)
        pass

    # Find music according to the path of the music
    def find_music_by_music_path(self, music_path):
        # SQL
        sql = "select %s from %s where %s = '%s'" % (
            # column names
            hp.fingerprint.database.tables.music.column.music_id,
            # Table Name
            hp.fingerprint.database.tables.music.name,
            # column names
            hp.fingerprint.database.tables.music.column.music_path,
            # incoming parameters
            music_path
        )

        # Execute SQL
        self.cursor.execute(sql)
        # get the return value
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    # Find out how many Hash numbers this song has according to the music id
    def calculation_hash_num_by_music_id(self, music_id):
        # SQL
        sql = "select count('%s') from %s where %s = %s" % (
            hp.fingerprint.database.tables.finger_prints.column.id_fp,
            hp.fingerprint.database.tables.finger_prints.name,
            hp.fingerprint.database.tables.finger_prints.column.music_id_fk,
            music_id
        )

        # Execute SQL
        self.cursor.execute(sql)

        # get the return value
        result = self.cursor.fetchone()
        if result is None:
            return 0
        else:
            return result[0]

    # add songs
    def add_music(self, music_path):

        # SQL
        sql = "insert into %s(%s, %s) values ('%s', '%s')" % (
            hp.fingerprint.database.tables.music.name,
            hp.fingerprint.database.tables.music.column.music_name,
            hp.fingerprint.database.tables.music.column.music_path,
            music_path.split(hp.fingerprint.path.split)[-1],
            music_path
        )

        self.cursor.execute(sql)
        self.conn.commit()

        # Find the song id according to music_path
        music_id = self.find_music_by_music_path(music_path=music_path)
        return music_id

    # Find a fingerprint
    def _find_finger_print(self, hash):
        sql = "select %s, %s from %s where %s = '%s'" % (
            hp.fingerprint.database.tables.finger_prints.column.music_id_fk,
            hp.fingerprint.database.tables.finger_prints.column.offset,
            hp.fingerprint.database.tables.finger_prints.name,
            hp.fingerprint.database.tables.finger_prints.column.hash,
            hash
        )
        self.cursor.execute(sql)
        # get the return value
        result = self.cursor.fetchone()
        if result == None:
            return [0, 0]
        return result

    # Find fingerprints
    def find_math_hash(self, hashes):
        # Find fingerprints one by one, [hash, offset]
        for item in hashes:
            music_id_fk, offset_database = self._find_finger_print(item[0])

            # The fingerprint to be checked corresponds to the song id in the database, the offset of the fingerprint
            # to be checked in the database, and the offset of the fingerprint to be checked in the music
            # segment to be checked
            yield music_id_fk, offset_database, item[1]

            pass
        pass

    pass
