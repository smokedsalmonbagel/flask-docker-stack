from baseObject import baseObject
import hashlib
from user_tags import user_tags    
import datetime
import re

class Users(baseObject):
    def __init__(self):
        self.setup('users')
        self.roles = ['student','admin']

    def toList(self):
        l = []
        for row in self.data:
            s = f"{row['Name']} {row['Username']} {row['Semester']} {row['FirstLogin']}{row['LastLogin']} {row['LastPasswordSet']}{row['Role']} "  
            l.append(s)
        return l
    def deleteByuid(self, uid):
        sql = f"DELETE FROM `{self.tn}` WHERE uid=%s"
        self.cur.execute(sql,(uid,))
    def getByUsername(self,name): #field,value
        sql = f"Select *,uid as uid from `{self.tn}` where `Username` = %s" 
        #print(sql)
        self.cur.execute(sql,(name,))
        for row in self.cur:
            self.data.append(self.r2d(row))
        #print(self.data)
    def getById(self,id): #field,value
        sql = f"Select *,uid as uid from `{self.tn}` where `uid` = %s" 
        self.cur.execute(sql,(id,))
        for row in self.cur:
            self.data.append(self.r2d(row))

    def tryLogin(self, Username):
        sql = f"SELECT *,uid as uid FROM `{self.tn}` WHERE `Username` = %s"
        self.cur.execute(sql,(Username,))
        rows=self.cur.fetchall()
        self.data = []
        for row in rows:
            self.data.append(self.r2d(row))
        if len(self.data) == 1:
            return True
        else:
            return False
    def update_time(self,name,value):
        sql = f"UPDATE `{self.tn}` SET {name}=%s WHERE uid = %s"
        self.cur.execute(sql,(value,self.data[0]['uid']))
    def verify_new(self,n=0):
        if len(self.data[n]['Name']) <= 1:
            self.errors.append('Name must be longer.')
        if re.match(r'[a-zA-Z\s]+$',self.data[n]['Name']) is None: 
            self.errors.append('Name contains invalid characters.')
        if self.data[n]['Username'] == '':
            self.errors.append('Username cannot be blank.')
        u = Users()
        u.getByUsername(self.data[n]['Username'])
        if len(u.data) > 0:
            self.errors.append('Username already in use.')
        if self.data[0]['password'] != self.data[0]['confirm_password']:
            self.errors.append('retyped password must match!')
        if len(self.data[0]['password']) < 5:
            self.errors.append('password must be more than 4 chars.')
        
        if len(self.errors) == 0:
            return True
        else:
            return False
    def verify_update(self,n=0):
        if len(self.data[n]['Name']) <= 1:
            self.errors.append('Name must be longer.')
        if re.match(r'[a-zA-Z\s]+$',self.data[n]['Name']) is None: 
            self.errors.append('Name contains invalid characters.')
        if self.data[n]['Username'] == '':
            self.errors.append('Username cannot be blank.')
        u = Users()
        u.getByUsername(self.data[n]['Username'])
        if len(u.data) > 1:
            self.errors.append('Username already in use.')
        if self.data[0]['password'] == '' and self.data[0]['confirm_password'] == '':
            del self.data[0]['password']
            del self.data[0]['confirm_password']
        else:
        
        
            if self.data[0]['password'] != self.data[0]['confirm_password']:
                self.errors.append('retyped password must match!')
            if len(self.data[0]['password']) < 5:
                self.errors.append('password must be more than 4 chars.')
        
        if len(self.errors) == 0:
            return True
        else:
            return False
    def verify_update_myaccount(self,n=0):
        if len(self.data[n]['Name']) <= 1:
            self.errors.append('Name must be longer.')
        if re.match(r'[a-zA-Z\s]+$',self.data[n]['Name']) is None: 
            self.errors.append('Name contains invalid characters.')
        
        if len(self.errors) == 0:
            return True
        else:
            return False
        
    def verify_password(self):
        if self.data[0]['password'] != self.data[0]['confirm_password']:
            self.errors.append('retyped password must match!')
        if len(self.data[0]['password']) < 5:
            self.errors.append('password must be more than 4 chars.')
        
        if len(self.errors) == 0:
            return True
        else:
            return False

    def get_active_tags(self):
                                                                           
        n=0
        self.active_tids = []
        for row in self.data:
            ut = user_tags()
            ut.get_by_uid(row['uid'])
            self.data[n]['active_tids'] = []
            for user_tag in ut.data:
                self.data[n]['active_tids'].append(str(user_tag['tid']))
            n+=1
    def add_tags(self,tids):
        from tags import tags
        ut= user_tags()
        dts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for tid in tids:
            t = tags()
            t.getById(tid)
            if len(t.data )== 0:
                print("Tag missing")
            if t.data[0]['vis'] == 'public':
                print('ADDING TID: ',tid)
                ut.tag_uids(tid,[self.data[0]['uid']],dts)
    def add_tags_admin(self,tids):
        ut= user_tags()
        print("tids:",tids)
        ut.tag_uids(tids,[self.data[0]['uid']],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
    def getAll(self,sort=''):

        sql = f"SELECT *,uid as uid FROM `{self.tn}`;"
 
        self.cur.execute(sql)
        self.data = []
        for row in self.cur.fetchall():
            self.data.append(self.r2d(row))

    def performSearch(self,query,sort=''):
        sql = f"SELECT *,uid as uid FROM `{self.tn}` WHERE `Name` LIKE '%{query}%' or `Username` LIKE '%{query}%'"
        self.cur.execute(sql)
        for row in self.cur:
            self.data.append(self.r2d(row))

   