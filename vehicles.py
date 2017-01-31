#-------------------------------------------------------------------------------
# Name:        car rental classes and setup
# Purpose:
#
# Author:      Larry McEvoy
#
# Created:     3/1/2017
#
#-------------------------------------------------------------------------------

from datetime import datetime
from datetime import timedelta
from math import ceil
from math import floor
import sqlite3

#inserts a new booking into the bookings table
def insertbooking(plate,startd,endd,cid):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute('''insert into bookings (CID,PLATE,STDT,ENDDT)
               VALUES(?,?,?,?)''',(cid,plate,startd,endd,))

    conn.commit()
    conn.close()

def delbooking(bid):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute('''select cid from bookings where ID =? and stdt <= date('now')''',(bid,))
    rows = c.fetchall()
    if len(rows)>0:
        print ("Can't Delete")
        conn.close()
        return False
    else:
        c.execute('''delete from bookings where ID =?''',(bid,))
        conn.commit()
        conn.close()
        return True

#function to insert a new customer into the customer details returns a customer id
def insertcustomer(cname,cadd,cemail):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute('''insert into customers (NAME,ADDRESS,EMAIL)
                   VALUES(?,?,?)''', (cname, cadd, cemail))
    conn.commit()
    parquery = "SELECT CID FROM customers where email='{}'".format(cemail)

    print(parquery)
    try:
        c.execute(parquery)
        rows = c.fetchone()
        if len(rows) > 0:
            return rows[0]
    except:
        return 0.0
    conn.close()

#return all future and current bookings by customer id
def showbookings(cid):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    print(cid)
    c.execute("select bk.id,bk.plate,vh.make,vh.model,bk.stdt,bk.enddt from bookings as bk inner join vehicles as vh on bk.plate=vh.plate where cid=? and (bk.stdt >= date('now') or bk.enddt >= date('now'))",(cid,))
    rows = c.fetchall()
    cusboklist = []
    for row in rows:
        bid = row[0]
        plate=row[1]
        make=row[2]
        model=row[3]
        startd=row[4]
        endd=row[5]
        cusboklist.append([bid,plate,make,model,startd,endd])
    conn.close()
    return cusboklist

#vehicle class
class Vehicle:

    def __init__(self,plate):
        self.__plate=plate
        self.__dayc=float
        self.__wkc=float
        self.__wkndc=float
        self.__cons=float
        self.__make = str
        self.__model = str
        self.__fuelc=float
        self.__booked=[]
        self.__extras={}
        self.__type=str

    def setplate(self,plate):
        self.__plate=plate

    def getplate(self):
        return self.__plate

    def setdaycost(self,dayc):
        self.__dayc=dayc

    def getdaycost(self):
        return self.__dayc

    def setweekcost(self, wkc):
        self.__wkc=wkc

    def getweekcost(self):
        return self.__wkc

    def setweekendcost(self, wkndc):
        self.__wkndc = wkndc

    def getweekendcost(self):
        return self.__wkndc

    def setmake(self,make):
        self.__make=make

    def getmake(self):
        return self.__make

    def setmodel(self,model):
        self.__model=model

    def getmodel(self):
        return self.__model

    def setfuelcon(self, fuelc):
        self.__fuelc = fuelc

    def getfuelcon(self):
        return self.__fuelc

    def setbooked(self,cid,sd,ed):
        self.__booked.append([cid,sd,ed])

    def getbooked(self):
        return self.__booked

    def setextra(self,extype,extcost):
        self.__extras.update({extype:extcost})

    def getextra(self,type):
        return self.__extras.get(type)


    def settype(self,type):
        self.__type = type

    def gettype(self):
        return self.__type

#method to check if a booking exists between two dates
    def chckbk(self,date1,date2):
        status=''
        date_format1 = "%Y-%m-%d"
        startd = date1
        endd = date2
        x=getbook(self.getplate())
        print (x)
        if x=='no bookings':
            return 'available'
        elif len(x)>0:
             for dets in x:
                 books=datetime.strptime(dets[2], date_format1).date()
                 booke=datetime.strptime(dets[3], date_format1).date()
                 if (startd<=booke) and (endd>=books):
                     status= 'Booked'
        if status=='Booked':
            return status
        else:
            return 'available'
        # else:
        #     return False
#method to calculate the cost between two dates
    def calculatecost(self,date1,date2,insxt,satxt,csxt):

        date_format = "%d/%m/%Y"

        startd = date1
        endd = date2
        boklen=(endd-startd).days+1

        if insxt==1:
            insc=getextcost(self.getplate(), 'Ins')
        else:
            insc=0
        if satxt==1:
            satc=getextcost(self.getplate(), 'Sat')
        else:
            satc=0
        if csxt == 1:
            csc = getextcost(self.getplate(), 'Cseat')
            # Cap child seat hire at 10 days
            if boklen <=10:
                csl=boklen
            else:
                csl=10

        else:
            csc = 0
            csl=0
        #function to count weekend days and ordinary days
        def getwknd(date, rem, wks):
            od = 0
            wkndd = 0
            if wks >0:
                adddays=wks*7
                date=date+timedelta(days=adddays)
            else:
                pass
            for i in range(rem):
                if date.weekday() < 5:
                    od += 1
                    date = date + timedelta(days=1)
                else:
                    wkndd += 1
            return (od, wkndd / 2)

        #function to get the cost
        def getcost(startd,boklen):
            if boklen%7==0:
                cost =self.getweekcost()*(boklen/7)
                extcost = round(((boklen * satc) + (boklen * insc) + (csl * csc)), 2)
                return cost,extcost

            else :
                wks=floor(boklen/7)
                rem=boklen%7
                days=getwknd(startd,rem,wks)
                #print (days)
                # cost calculated as number of weeks + number or extra days + any weekend days if vehicle is hired for
                # any part of the weekend the full weekend rate is charged
                cost =(self.getweekcost()*wks)+(self.getdaycost()*days[0])+(self.getweekendcost()*ceil(days[1]))
                extcost=round(((boklen*satc)+(boklen*insc)+(csl*csc)),2)
                # cost reduced to weekly rate if the calculated hire exceeds the weekly rate
                # and car has been hired for more than 1 week
                if cost/self.getweekcost()>wks and wks>1:
                    cost=(self.getweekcost()*(wks+1))
                return cost,extcost
        return getcost(startd, boklen)

class Passveh(Vehicle):
    def __init__(self,plate):
        Vehicle.__init__(self,plate)
        self.__nopass=int

    def setpassangers(self,psngr):
        self.__nopass=psngr

    def getpassangers(self):
        return self.__nopass


class Cars(Passveh):
    def __init__(self,plate):
        Vehicle.__init__(self,plate)
        self.__doors=int

    def setdoors(self,doors):
        self.__doors=doors

    def getdoors(self):
        return self.__doors


class Vans(Passveh):
    def __init__(self,plate):
        Vehicle.__init__(self,plate)
        self.__cap = float

    def setcapacity(self, cap):
        self.__cap = cap

    def getcapacity(self):
        return self.__cap


class Camper(Vehicle):
    def __init__(self,plate):
        Vehicle.__init__(self,plate)
        self.__beds=int

    def setbeds(self,beds):
        self.__beds=beds

    def getbeds(self):
        return self.__beds

def makeclass(rows):
    list=[]
    for row in rows:
        x=row[0]
        if row[7]=='Cars':
            x=Cars (row[0])
            x.setmake(row[1])
            x.setmodel(row[2])
            x.setfuelcon(row[3])
            x.setdaycost(row[4])
            x.setweekcost(row[5])
            x.setweekendcost(row[6])
            x.settype(row[7])
            x.setdoors(row[8])
            x.setpassangers(row[9])
            x.setextra('Sat', getextra(row[0], 'Sat'))
            x.setextra('Ins', getextra(row[0], 'Ins'))
            x.setextra('Cseat', getextra(row[0], 'Cseat'))
            list.append(x)
        elif row[7]=='Vans':
            x=Vans (row[0])
            x.setmake(row[1])
            x.setmodel(row[2])
            x.setfuelcon(row[3])
            x.setdaycost(row[4])
            x.setweekcost(row[5])
            x.setweekendcost(row[6])
            x.settype(row[7])
            x.setpassangers(row[9])
            x.setcapacity(row[11])
            x.setextra('Sat', getextra(row[0], 'Sat'))
            x.setextra('Ins', getextra(row[0], 'Ins'))
            list.append(x)
        elif row[7]=='Camper':
            x=Camper(row[0])
            x.setmake(row[1])
            x.setmodel(row[2])
            x.setfuelcon(row[3])
            x.setdaycost(row[4])
            x.setweekcost(row[5])
            x.setweekendcost(row[6])
            x.settype(row[7])
            x.setbeds(row[10])
            x.setextra('Sat',getextra(row[0],'Sat'))
            x.setextra('Ins', getextra(row[0], 'Ins'))

            list.append(x)
    return(list)
#return all types to populate the types list
def vehtypes():
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute("SELECT distinct(Type) FROM vehicles")
    rows = c.fetchall()
    list = []
    for row in rows:
        x=row[0]
        list.append(x)
    conn.close()
    return list

def getvehbyplate(query):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    parquery="SELECT * FROM vehicles where PLATE='{}'".format(query)
    print (parquery)
    c.execute(parquery)
    rows = c.fetchall()
    conn.close()
    return makeclass(rows)

def getextcost(plate,extra):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    parquery = "SELECT extcst FROM extras where PLATE='{}'and extra ='{}'".format(plate,extra)
    print(parquery)
    try:
        c.execute(parquery)
        rows = c.fetchone()
        conn.close()
        if len(rows)>0:
            return rows[0]
        else:
            return 0.0
    except:
        return 0.0



def getbook(plate):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    parquery = "SELECT * FROM bookings where PLATE='{}'".format(plate)
    #print(parquery)

    c.execute(parquery)
    x=c.fetchall()
    conn.close()
    blist = []
    if len(x)>0:
        for ent in x:
            cid=ent[1]
            stdat=ent[3]
            enddat=ent[4]
            blist.append([cid,plate,stdat,enddat])
        return (blist)
    else:
        return 'no bookings'

def chkfuturebookbyplate(plate):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute('''select cid from bookings where plate =? and (stdt >= date('now') or enddt >= date('now'))''',(plate,))
    rows = c.fetchall()
    if len(rows)>0:
        return True
    else:
        return False



class Cust:
    def __init__(self,cemail):
        self.__cemail = cemail
        self.__cid = int
        self.__cname = str
        self.__caddress = str

    def setcid(self,cid):
        self.__cid=cid

    def getcid(self):
        return self.__cid

    def setcname(self,cname):
        self.__cname=cname

    def getcname(self):
        return self.__cname

    def setcadd(self,cadd):
        self.__caddress=cadd

    def getcadd(self):
        return self.__caddress

    def setcemail(self,cemail):
        self.__cemail=cemail

    def getcemail(self):
        return self.__cemail

#method to check if customer email exists in customer table
def custcheck(email):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    parquery = "SELECT * FROM customers where email='{}'".format(email)
    print(parquery)
    c.execute(parquery)
    rows = c.fetchone()
    conn.close()
    if rows is None:
        return False, 'Not Customer'
    else:
        return True, makeclasscus(rows)



def makeclasscus(rows):
    list=[]
    x=Cust(rows[3])
    x.setcid(rows[0])
    x.setcadd(rows[2])
    x.setcname(rows[1])
    list.append(x)
    return list

def vehlist():
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c=conn.cursor()
    c.execute("SELECT * FROM vehicles")
    rows = c.fetchall()
    conn.close()
    return makeclass(rows)

def insertveh(type,evhvars,extvars):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles WHERE PLATE=?",(evhvars[7],))
    rows = c.fetchall()
    if type=='Camper':
        if len(rows) <=0:
            c.execute('''
            insert into vehicles (make, model,fcon,dcst,wkcst,wkndcst,beds,plate,type)
                       VALUES(?,?,?,?,?,?,?,?,?)''', (evhvars[0],evhvars[1],evhvars[2],evhvars[3],evhvars[4],evhvars[5],evhvars[6],evhvars[7],type,))
            for row in extvars:
                if row[0] == 'Ins':
                    c.execute('''
                            insert into extras(extra,extcst,plate)
                            values (?,?,?)''',(row[0],row[1],row[2],))

                if row[0] == 'Sat':
                    c.execute('''
                    insert into extras(extra,extcst,plate)
                    values (?,?,?)''', (row[0], row[1], row[2],))
            conn.commit()
            conn.close()
            return 'Vehicle Inserted'
        else:
            print ('Vehicle Already Exists')
            return 'Vehicle Already Exists'


    elif type=='Cars':
        if len(rows) <=0:
            c.execute('''
            insert into vehicles (make, model,fcon,dcst,wkcst,wkndcst,doors,passangers,plate,type)
                       VALUES(?,?,?,?,?,?,?,?,?,?)''', (evhvars[0],evhvars[1],evhvars[2],evhvars[3],evhvars[4],evhvars[5],evhvars[6],evhvars[7],evhvars[8],type,))
            for row in extvars:
                if row[0] == 'Ins':
                    c.execute('''
                            insert into extras(extra,extcst,plate)
                            values (?,?,?)''',(row[0],row[1],row[2],))

                if row[0] == 'Sat':
                    c.execute('''
                    insert into extras(extra,extcst,plate)
                    values (?,?,?)''', (row[0], row[1], row[2],))

                if row[0] == 'Cseat':
                    c.execute('''
                    insert into extras(extra,extcst,plate)
                    values (?,?,?)''', (row[0], row[1], row[2],))
            conn.commit()
            conn.close()
            return 'Vehicle Inserted'
        else:
            print ('Vehicle Already Exists')
            return 'Vehicle Already Exists'
    else:
        if len(rows) <=0:
            c.execute('''
            insert into vehicles (make, model,fcon,dcst,wkcst,wkndcst,passangers,capacity,plate,type)
                       VALUES(?,?,?,?,?,?,?,?,?,?)''', (evhvars[0],evhvars[1],evhvars[2],evhvars[3],evhvars[4],evhvars[5],evhvars[6],evhvars[7],evhvars[8],type,))
            for row in extvars:
                if row[0] == 'Ins':
                    c.execute('''
                            insert into extras(extra,extcst,plate)
                            values (?,?,?)''',(row[0],row[1],row[2],))

                if row[0] == 'Sat':
                    c.execute('''
                    insert into extras(extra,extcst,plate)
                    values (?,?,?)''', (row[0], row[1], row[2],))


            conn.commit()
            conn.close()
            return 'Vehicle Inserted'
        else:
            print ('Vehicle Already Exists')
            return 'Vehicle Already Exists'


def updateveh(type,vehvars,extvars):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    if type=='Camper':
        print (vehvars)
        c.execute('''
              update vehicles
              SET MAKE=?,
              MODEL=?,
              FCON=?,
              DCST=?,
              WKCST=?,
              WKNDCST=?,
              BEDS=?
              where plate=?
              ''',(vehvars[0],vehvars[1],vehvars[2],vehvars[3],vehvars[4],vehvars[5],vehvars[6],vehvars[7]))
        conn.commit()
        for row in extvars:
            if row[0]=='Ins':
                c.execute('''
                      update Extras
                      set extcst=?
                      where plate=?
                      and extra=?
                      ''', (row[1],row[2],row[0]))
                conn.commit()
            if row[0]=='Sat':
                c.execute('''
                      update Extras
                      set extcst=?
                      where plate=?
                      and extra=?
                      ''', (row[1],row[2],row[0]))
                conn.commit()
    elif type=='Cars':
        c.execute('''
                      update vehicles
                      SET MAKE=?,
                      MODEL=?,
                      FCON=?,
                      DCST=?,
                      WKCST=?,
                      WKNDCST=?,
                      DOORS=?,
                      PASSANGERS=?
                      where plate=?
                      ''',
                  (vehvars[0], vehvars[1], vehvars[2], vehvars[3], vehvars[4], vehvars[5], vehvars[6], vehvars[7],vehvars[8]))
        conn.commit()
        for row in extvars:
            if row[0] == 'Ins':
                c.execute('''
                              update Extras
                              set extcst=?
                              where plate=?
                              and extra=?
                              ''', (row[1], row[2], row[0]))
                conn.commit()
            elif row[0] == 'Sat':
                c.execute('''
                              update Extras
                              set extcst=?
                              where plate=?
                              and extra=?
                              ''', (row[1], row[2], row[0]))
                conn.commit()
            elif row[0] == 'Cseat':
                c.execute('''
                              update Extras
                              set extcst=?
                              where plate=?
                              and extra=?
                              ''', (row[1], row[2], row[0]))
                conn.commit()
    else:
        c.execute('''
                      update vehicles
                      SET MAKE=?,
                      MODEL=?,
                      FCON=?,
                      DCST=?,
                      WKCST=?,
                      WKNDCST=?,
                      capacity=?,
                      PASSANGERS=?
                      where plate=?
                      ''',
                  (vehvars[0], vehvars[1], vehvars[2], vehvars[3], vehvars[4], vehvars[5], vehvars[6], vehvars[7],vehvars[8]))
        conn.commit()
        for row in extvars:
            if row[0] == 'Ins':
                c.execute('''
                              update Extras
                              set extcst=?
                              where plate=?
                              and extra=?
                              ''', (row[1], row[2], row[0]))
                conn.commit()
            elif row[0] == 'Sat':
                c.execute('''
                              update Extras
                              set extcst=?
                              where plate=?
                              and extra=?
                              ''', (row[1], row[2], row[0]))
                conn.commit()
            elif row[0] == 'Cseat':
                c.execute('''
                              update Extras
                              set extcst=?
                              where plate=?
                              and extra=?
                              ''', (row[1], row[2], row[0]))
                conn.commit()


    conn.close()

def delveh(plate):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute('''Delete from vehicles where plate=?
                  ''', (plate,))
    conn.commit()

def getextra(plate,extra):
    conn = sqlite3.connect('rental.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute(''' select extcst from extras where plate=? and extra=?''',(plate,extra,))
    rows = c.fetchone()
    if rows is None:
        return 0.0
    else:
        return rows[0]


#populateveh()
# list=vehlist()
# for veh in list:
#
#     print (veh.getplate())
#     if type(veh)==Camper:
#         print ('Camper')
#     elif type(veh)==Cars:
#         print('Car')
#     else:
#         print ('Van')
#
#     y=veh.chckbk('18/12/2016','23/12/2016')
#
#     x=veh.calculatecost('18/12/2016','23/12/2016')
#     print (x,y)
#      #if type=='Camper'
#      #print (veh.getbeds(),veh.getfuelcon(),veh.getplate())

        

