import psycopg2


class PostGreExecutor:
    def __init__(self, database_name, user_name, password, host, port):
        self.database_name = database_name
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port

        self._conn = self.GetConnect()
        if self._conn:
            self._cur = self._conn.cursor()

    def GetConnect(self):
        """
        connect to the db
        :return:
        """
        conn = False
        try:
            conn = psycopg2.connect(
                database=self.database_name,
                user=self.user_name,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except Exception as err:
            print("connect to db fialed, %s" % err)
        return conn

    def ExceQuery(self, sql):
        res = ""
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as err:
            print("query {} failed, err={}".format(sql, err))
        else:
            return res

    def ExecNonQuery(self, sql):
        flag = False
        # id = None
        try:
            self._cur.execute(sql)
            # id = self._cur.fetchone()[0]
            self._conn.commit()
            flag = True
        except Exception as err:
            self._conn.rollback()
            print("execute {} fail,err={}".format(sql, err))
            return False
        else:
            return flag

    def GetConnectionInfo(self):
        print("connection info")
        print("postgresql host:{}:{}, username:{}, db{}".format(self.host, self.port, self.user_name,
                                                                self.database_name))
