import sqlite3            
import pymysql, mysecrets
import settings
import os

class baseObject:
    def setup(self,tn):
        global app_log
        self.app_log = settings.app_log
        self.e = None
        self.tn = tn
        self.conn = None
        self.cur = None
        self.fields = []
        self.errors = []
        self.pk = None
        self.onefield=None
        self.data = [] #data is a list of dictionaries representing rows in our table
        self.establishConnection()
        self.getFields()


    def establishConnection(self):
        self.conn = pymysql.connect(host=mysecrets.host, port=mysecrets.port, user=mysecrets.user,
                       passwd=mysecrets.passwd, db=mysecrets.db, autocommit=True)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
    def set(self,d):
        self.data.append(d)
    def r2d(self,row):
        d={}
        for k in row.keys():
            d[k]=str(row[k])
        return d
    def getFields(self):
        sql = f'''DESCRIBE `{self.tn}`;'''
        self.cur.execute(sql)
        for row in self.cur:
            if 'auto_increment' in row['Extra'].lower():
                self.pk = row['Field']
            else:
                self.fields.append(row['Field'])
    def insert(self,n=0):
        #print("================",self.fields)
        count = 0
        vals = []
        sql = f"INSERT INTO `{self.tn}` (" 
        for field in self.fields:
            sql += f"`{field}`,"
            vals.append(self.data[n][field])
            count +=1
        sql = sql[0:-1] + ') VALUES ('
        tokens = ("%s," * count)[0:-1]
        sql += tokens + ');'
        #print(sql,vals)
        self.cur.execute(sql,vals)
        self.data[n][self.pk] = self.cur.lastrowid

    def getById(self,id):
        sql = f"Select * from `{self.tn}` where `{self.pk}` = %s" 
        #print(sql,id)
        self.cur.execute(sql,(id))
        self.data = []
        for row in self.cur:
            self.data.append(row)
    def getByIds(self,ids): 
        sql = f"Select * from `{self.tn}` where " + (f' `{self.pk}` = %s OR' * len(ids))
        sql = sql[:-2]
        print(sql,ids)
        self.cur.execute(sql,(ids))
        self.data = []
        for row in self.cur:
            self.data.append(row)
    def getByField(self,field,val):
        sql = f"Select * from `{self.tn}` where `{field}` = %s" 
        print(sql,val)
        self.cur.execute(sql,(val))
        self.data = []
        for row in self.cur:
            self.data.append(row)
    def createBlank(self):
        d = {}
        for field in self.fields:
            d[field] = ''
        self.set(d)
       
    def getAll(self):
        sql = f"Select * from `{self.tn}`" 
        self.cur.execute(sql)
        self.data = []
        for row in self.cur:
            self.data.append(self.r2d(row))
    # UPDATE [tablename] SET [col] = [val] , .... WHERE [pk] = [our objects pk] 
    def update(self,n=0):
        vals=[]
        fvs=''
        for field in self.fields:
            if field in self.data[n].keys():
                fvs += f"`{field}`=%s,"
                vals.append(self.data[n][field])
        fvs=fvs[:-1]
        sql=f"UPDATE `{self.tn}` SET {fvs} WHERE `{self.pk}` = %s"
        vals.append(self.data[n][self.pk])
        #print(sql,vals)
        self.cur.execute(sql,vals)
    def deleteById(self,id):
        sql = f"Delete from `{self.tn}` where `{self.pk}` = %s" 
        self.cur.execute(sql,(id))
    def add_db(self,username, password):
        #print(f"Add MySQL {servername} {dbname}")

        sql = [
            f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'",
            f"CREATE DATABASE IF NOT EXISTS `{username}`",
            f"GRANT ALL PRIVILEGES ON `{username}%`.* TO '{username}'@'localhost' WITH GRANT OPTION",
            f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'",
            f"GRANT ALL PRIVILEGES ON `{username}%`.* TO '{username}'@'%' WITH GRANT OPTION"
        ]

    #    GRANT ALL PRIVILEGES ON `username}`.* TO 'yash6'@'localhost'; ALTER USER 'yash6'@'localhost' ;

        try:
            conn = pymysql.connect(
                host=mysecrets.servername,
                user=mysecrets.username,  # Assuming you are using the root user to execute these queries
                password=mysecrets.password,
                port=3306, # Replace with the root user's password
                database=""
            )

            cursor = conn.cursor()

            for sqlq in sql:
                print(sqlq)
                cursor.execute(sqlq)

            conn.commit()

            cursor.close()
            conn.close()
            return True
        except pymysql.Error as e:
            self.app_log.error(f"SQL Error:{e}")
            print("Error: ", e)
            self.e = e
            return False
            
    def update_db_pass(self, un, pw):
        sql = [
            f"SET PASSWORD FOR '{un}'@'localhost' = '{pw}';",
            f"SET PASSWORD FOR '{un}'@'%' = '{pw}';"
            ]

        try:
            conn = pymysql.connect(
                host=mysecrets.servername,
                user=mysecrets.username,  # Assuming you are using the root user to execute these queries
                password=mysecrets.password,
                port=3306, # Replace with the root user's password
                database=""
            )


            cursor = conn.cursor()

            for sqlq in sql:
                    cursor.execute(sqlq)

            conn.commit()

            cursor.close()
            conn.close()
        except pymysql.connect.Error as e:
                print("Error: ", e)
    def createBlank(self):
        d = {}
        for field in self.fields:
            d[field] = ''
        self.set(d)

        
