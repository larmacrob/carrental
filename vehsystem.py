#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      marisa.llorens
#
# Created:     26/11/2015
# Copyright:   (c) marisa.llorens 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import vehicles as vh
from _datetime import datetime
from datetime import date


class Welcome(tk.Tk):
    global root
    def __init__(self,master):
        self.master = master
        self.master.geometry('400x200+100+200')
        #self.master.tk.Tk.title ('WELCOME')
        self.master = master
        #self.master.geometry('400x200+100+200')
        self.master.title ('Car Rental Project')
        self.label1=tk.Label(self.master,text='Welcome to the Car Rental Project GUI').grid(columnspan=3,row=0,column=0,sticky="nsew")
        self.label1 = tk.Label(self.master, text='Please Select an Option Below' ).grid(columnspan=3,row=1, column=0,sticky="nsew")
        self.button1 = tk.Button(self.master,text="Customer User",fg='blue',command=self.gotoCustomer).grid(row=3,column=1, padx=5, pady=5)
        self.button2=tk.Button(self.master,text="Administrator",fg='blue',command=self.gotoAdmin).grid(row=3,column=2, padx=5, pady=5)
        self.button3 = tk.Button(self.master, text="Quit", fg='blue', command=self.finish).grid(row=3,column=3, padx=5, pady=5)

    def gotoCustomer(self):
        root2=tk.Toplevel(self.master)
        myGUI=Customer(root2)
        return

    def gotoAdmin(self):
        self.root3=tk.Toplevel(self.master)
        myGUI=Admin(self.root3)

        return

    def finish(self):
        self.master.destroy()

class Customer(tk.Frame):
    def __init__(self, master,):
        super(Customer, self).__init__()
        typeopts = vh.vehtypes()
        self.csx = tk.IntVar()
        self.master = master
        self.master.geometry('800x600+100+200')
        self.inxt=tk.IntVar()
        self.satxt=tk.IntVar()
        self.srchtypevar=tk.StringVar()
        self.srchtypevar.set(typeopts[0])
        self.srctypom=tk.OptionMenu(self.master,self.srchtypevar,*typeopts,command=self.gotoSearch).grid(row=2,column=0)
        #self.srchbuttype = tk.Button(self.master, text="Show Vehicles", fg='blue', command=self.gotoSearch).grid(row=2,column=1,sticky="ew")
        self.strdate=tk.Entry(master)
        self.strdate.grid(row=1,column=0)
        self.enddate=tk.Entry(master)
        self.enddate.grid(row=1,column=1)
        self.insext=tk.Checkbutton(master,text='Add Supplementary\nInsurance',variable=self.inxt)
        self.insext.grid(row=2,column=2)
        self.satnxt = tk.Checkbutton(master, text='Add Sat\nNav', variable=self.satxt)
        self.satnxt.grid(row=2, column=3)
        self.csxt = tk.Checkbutton(master, text='Add Child\nSeat', variable=self.csx)
        self.csxt.grid(row=2, column=4)
        self.csxt.grid_remove()
        self.btframe=tk.Frame(self.master,width=800)
        self.btframe.grid(row=3,column=0,columnspan=4)
        self.quit = tk.Button(self.master, text="back", fg='blue',command=self.back).grid(row=0, column=3, padx=5,
                                                                                               pady=5)
        self.bookings=tk.Button(self.master, text="Show Bookings",command=self.booklst).grid(row=0,column=2)

        stdat = tk.Label(master, text='Start Date').grid(row=0, column=0)
        endat = tk.Label(master, text='End Date').grid(row=0, column=1)
        self.gotoSearch()
    def back(self):
        self.master.destroy()



    def booklst(self):
        def delbook(bid):
            x=vh.delbooking(bid)
            if x is False:
                tk.messagebox.showinfo("Erro", 'Sorry that booking has \nstarted and cannot be cancelled', parent=self.bkframe)
                self.bklst.destroy()
            else:
                tk.messagebox.showinfo("Cancelled", 'Your booking has been cancelled', parent=self.bkframe)
                self.bklst.destroy()


        def getbooklst():

            email=(self.emadd.get().lower())
            print(email)
            a=vh.custcheck(email)
            if a[0] is False:
                self.txtnot.grid(row=2,column=1)
                self.txtnot['text']='Sorry we have no record\n of that email address'
            else:
                self.makelab.grid(row=1,column=2)
                self.modlab.grid(row=1, column=3)
                self.bkstlab.grid(row=1, column=4)
                self.bkenlab.grid(row=1, column=5)
                cid=a[1][0].getcid()
                print(cid)
                cbook=vh.showbookings(cid)
                print(cbook[0])
                z=2

                for row in cbook:
                    self.button = tk.Button(self.bkframe, text='cancel',command=lambda x=(row[0]): delbook(x)).grid(row=z, column=1)
                    self.make = tk.Label(self.bkframe, text=row[2]).grid(row=z, column=2)
                    self.model = tk.Label(self.bkframe, text=row[3]).grid(row=z, column=3)
                    self.start = tk.Label(self.bkframe, text=row[4]).grid(row=z, column=4)
                    self.end = tk.Label(self.bkframe, text=row[5]).grid(row=z, column=5)
                    z+=1
            self.searchbt.grid_forget()

        self.bklst=tk.Toplevel(self.master)
        self.quitbk = tk.Button(self.bklst, text="back", fg='blue', command=self.backbk)
        self.quitbk.grid(row=0, column=4)
        self.emadd = tk.Entry(self.bklst)
        self.emadd.grid(row=0, column=1)
        self.emlabel=tk.Label(self.bklst,text='Enter Your Email Address').grid(row=0, column=0)
        self.searchbt = tk.Button(self.bklst, text='Search Bookings', command=getbooklst)
        self.searchbt.grid(row=0, column=3)
        self.bkframe = tk.Frame(self.bklst)
        self.bkframe.grid(row=10, column=1)
        self.txtnot=tk.Label(self.bkframe,text='')
        self.txtnot.grid(row=2,column=1)
        self.txtnot.grid_forget()
        self.makelab = tk.Label(self.bkframe, text='Make')
        self.modlab = tk.Label(self.bkframe, text='Model')
        self.bkstlab = tk.Label(self.bkframe, text='Booking\nStarts')
        self.bkenlab = tk.Label(self.bkframe, text='Booking\nEnds')


    def backbk(self):
        self.bklst.withdraw()

    def gotoSearch(self,*args,**kwargs):
        self.csxt.deselect()
        self.csxt.grid_remove()
        z=3
        root = self.btframe
        typ=self.srchtypevar.get()
        list=vh.vehlist()

        def valdates():
            date_format = "%d/%m/%Y"
            try:
                startd = datetime.strptime(self.strdate.get(), date_format).date()
            except ValueError:
                startd = ''
            try:
                endd = datetime.strptime(self.enddate.get(), date_format).date()
            except ValueError:
                endd = ''
            if startd == '' or endd == '':
                return (False,'Please enter a valid start and\nend date in the format DD/MM/YYYY')
            elif startd < date.today():
                return (False,'Date entered must be in the future')
            elif endd < startd:
                return (False,'Sorry the end date must be after or equal the start date')
            else:
                return(True,startd,endd)

        def availability(plate):
            x = vh.getvehbyplate(plate)
            vdate = valdates()
            if vdate[0]is True:
                startd=vdate[1]
                endd=vdate[2]
                for veh in x:
                    if veh.getplate()==plate:
                        x=veh.chckbk(startd, endd)
                        print (x)
                        if x =='Booked':
                            y='Sorry Not Available'
                        else:
                            y='The vehicle you selected is available\nfor the selected dates'
            else:
                y=vdate[1]
            tk.messagebox.showinfo("Availability", y, parent=self.btframe)

        def quote(name):
            pllst=vh.getvehbyplate(name)
            vdate = valdates()
            if vdate[0] is True:
                for veh in pllst:
                    if veh.getplate()==name:
                        x=veh.calculatecost(vdate[1],vdate[2],self.inxt.get(),self.satxt.get(),self.csx.get())
                        y='Rental Cost = €{}\nSelected Extras Cost = €{}\nTotal Cost=€{}'.format(round(x[0],2),round(x[1],2),round(x[0]+x[1],2))
                    print (y)
            else:
                y=vdate[1]
            tk.messagebox.showinfo("Cost", y, parent=self.btframe)

        for widget in self.btframe.winfo_children():
            widget.destroy()
        self.head=tk.Label(root, text='Daily\nCost').grid(row=0, column=4)
        self.head1= tk.Label(root, text='Weekly\nCost').grid(row=0, column=5)
        self.head2 = tk.Label(root, text='Weekend\nCost').grid(row=0, column=6)
        self.head3 = tk.Label(root, text='')
        self.head3.grid(row=0, column=7)
        self.head3.grid_remove()
        self.head4 = tk.Label(root, text='')
        self.head4.grid(row=0, column=8)
        self.head4.grid_remove()

        def insbook():
            print(booking)
            vh.insertbooking(booking[1],booking[2],booking[3],booking[4])
            self.custdet.destroy()
            tk.messagebox.showinfo("Thank You", 'Thank you your booking is complete', parent=self.btframe)


            pass
        def chkcust():
            #print (booking)
            global booking
            bkstr=booking[0]
            print(bkstr)
            x = self.email.get()
            print(x)
            y = vh.custcheck(x)
            if y[0] is True:
                t = y[1]
                print(t)
                z = t[0].getcadd()
                self.cname.delete(0, tk.END)
                self.cname.insert(0, t[0].getcname())
                self.cadd.delete(0, tk.END)
                self.cadd.insert(0, t[0].getcadd())
                self.book['text']=bkstr
                booking.append(t[0].getcid())
                self.okbtn.grid_forget()
                self.bookbt.grid(row=10,column=2)
            else:
                self.cname.delete(0,tk.END)
                self.cadd.delete(0, tk.END)
                self.book['text'] = 'You are not a returning customer\nPlease enter your Name and Address \nand press the Register Key to continue'
                self.okbtn.grid_forget()
                self.regbt.grid(row=10,column=2)

        def regbook():
            global booking
            self.regbt.grid_forget()
            bkstr = booking[0]
            cname=self.cname.get()
            cadd=self.cadd.get()
            cemail=self.email.get().lower()
            x=vh.insertcustomer(cname, cadd, cemail)
            print(x)
            booking.append(x)
            self.book['text'] = bkstr
            self.bookbt.grid(row=10, column=2)

        def makebook(plate):
            try:
                vdate=valdates()
                if vdate[0] is False:
                    raise ValueError(vdate[1])
                else:
                    veh=vh.getvehbyplate(plate)
                    startd=vdate[1]
                    endd=vdate[2]
                    ins=self.inxt.get()
                    sat=self.satxt.get()
                    cseat=self.csx.get()
                    x=veh[0].chckbk(startd, endd)
                    if x =='Booked':
                        raise ValueError('Sorry Not Available')
                    else:
                        cost=veh[0].calculatecost(startd,endd,ins,sat,cseat)
                        print (cost)
                        y='You are booking a {} {} \nfrom {} to {} at a \nTotal Cost of €{} \nincluding Extras costing €{} \npress Book to confirm'.format(veh[0].getmake(),veh[0].getmodel(),startd,endd,cost[0]+cost[1],cost[1])
                        global booking
                        booking=[y,plate,startd,endd]

                self.custdet=tk.Toplevel()

                self.button = tk.Button(self.custdet, text="Back", command=self.custdet.destroy).grid(row=10,column=1)
                self.emlabel=tk.Label(self.custdet,text="Please Enter your Email Address\nand press ok to continue").grid(row=1,column=1)
                self.email=tk.Entry(self.custdet,width =50)
                self.email.grid(row=1,column=2)
                self.cnamelab=tk.Label(self.custdet,text="Name")
                self.cnamelab.grid(row=2,column=1)
                self.cname=tk.Entry(self.custdet,width=50)
                self.cname.grid(row=2,column=2)
                self.cadd=tk.Entry(self.custdet,width=50)
                self.cadd.grid(row=3,column=2)
                self.caddlab=tk.Label(self.custdet,text="Address")
                self.caddlab.grid(row=3,column=1)
                self.book=tk.Label(self.custdet,text='')
                self.book.grid(row=4,column=2)
                self.okbtn = tk.Button(self.custdet, text='OK', command=chkcust)
                self.okbtn.grid(row=9,column=1)
                self.bookbt = tk.Button(self.custdet, text='Book', command=insbook)
                self.bookbt.grid(row=10, column=2)
                self.bookbt.grid_forget()
                self.regbt=tk.Button(self.custdet, text='Register', command=regbook)

            except ValueError as err:
                tk.messagebox.showinfo("Error", err, parent=self.btframe)

            return

        for veh in list:
            if veh.__class__.__name__==typ:
                if typ=='Cars':
                    self.csxt.grid()
                    button=tk.Button(root,text='Check\n Availability',command=lambda x=veh.getplate():availability(x)).grid(row=z,column=1)
                    button1=tk.Button(root,text='Get\n Quote',command=lambda x=veh.getplate():quote(x)).grid(row=z,column=2)
                    button3 = tk.Button(root, text='book', command=lambda x=veh.getplate(): makebook(x)).grid(row=z,column=10)
                    x = veh.getmake(), veh.getmodel()
                    y = ' '.join(map(str, x))
                    label=tk.Label(root,text=y).grid(row=z,column=3)
                    dayc = tk.Label(root, text=veh.getdaycost(), bd=2).grid(row=z, column=4)
                    wkc = tk.Label(root, text=veh.getweekcost(), bd=2).grid(row=z, column=5)
                    wkndc = tk.Label(root, text=veh.getweekendcost(), bd=2).grid(row=z, column=6)
                    doors=tk.Label(root,text=veh.getdoors(),bd=2).grid(row=z, column=7)
                    psngrs=tk.Label(root,text=veh.getpassangers(),bd=2).grid(row=z, column=8)
                    z=z+1
                    print(y)
                    self.head3['text']='Doors'
                    self.head4['text'] = 'Passengers'
                    self.head3.grid()
                    self.head4.grid()
                elif typ=='Vans':
                    button=tk.Button(root,text='Check\n Availability',command=lambda x=veh.getplate():availability(x)).grid(row=z,column=1)
                    button1=tk.Button(root,text='Get\n Quote',command=lambda x=veh.getplate():quote(x)).grid(row=z,column=2)
                    button3 = tk.Button(root, text='book', command=lambda x=veh.getplate(): makebook(x)).grid(row=z,
                                                                                                              column=10)
                    x = veh.getmake(), veh.getmodel()
                    y = ' '.join(map(str, x))
                    label = tk.Label(root, text=y).grid(row=z, column=3)
                    dayc = tk.Label(root, text=veh.getdaycost(),bd=2).grid(row=z, column=4)
                    wkc = tk.Label(root, text=veh.getweekcost(),bd=2).grid(row=z, column=5)
                    wkndc = tk.Label(root, text=veh.getweekendcost(),bd=2).grid(row=z, column=6)
                    psngrs = tk.Label(root, text=veh.getpassangers(), bd=2).grid(row=z, column=7)
                    cap = tk.Label(root, text=veh.getcapacity(), bd=2).grid(row=z, column=8)
                    z += 1
                    print(y)
                    self.head3['text'] = 'Passengers'
                    self.head4['text'] = 'Capacity'
                    self.head3.grid()
                    self.head4.grid()
                else:
                    button = tk.Button(root, text='Check\n Availability',
                                       command=lambda x=veh.getplate(): availability(x)).grid(row=z, column=1)
                    button1 = tk.Button(root, text='Get\n Quote', command=lambda x=veh.getplate(): quote(x)).grid(row=z,
                                                                                                                  column=2)
                    button3 = tk.Button(root, text='book', command=lambda x=veh.getplate(): makebook(x)).grid(row=z,
                                                                                                              column=10)
                    x = veh.getmake(), veh.getmodel()
                    y = ' '.join(map(str, x))
                    label = tk.Label(root, text=y).grid(row=z, column=3)
                    dayc = tk.Label(root,text=veh.getdaycost()).grid(row=z, column=4)
                    wkc = tk.Label(root, text=veh.getweekcost()).grid(row=z, column=5)
                    wkndc=tk.Label(root, text=veh.getweekendcost()).grid(row=z, column=6)
                    beds=tk.Label(root, text=veh.getbeds()).grid(row=z,column=7)
                    z +=1
                    print(y)
                    self.head3['text'] = 'Beds'
                    self.head3.grid()
            #y=veh.chckbk('18/12/2016','23/12/2016')

            #x=veh.calculatecost('18/12/2016','23/12/2016')
            #print (x,y)
            #if type=='Camper'
            #print (veh.getbeds(),veh.getfuelcon(),veh.getplate())

    def myquit(self):
        self.master.withdraw()

class Admin():
    def __init__(self,master):
        self.master=master

        self.adbtframe = tk.Frame(master,height=300, width=800)
        self.detframe=tk.Frame(master)
        self.adbtframe.config(height=800,width=800)
        self.detframe.grid(row=2,column=1)
        self.adbtframe.grid(row=1,column=1)
        self.showveh=tk.Button(self.adbtframe,text='Back',command=self.quitadmin)
        self.showveh.grid(row=1,column=4)
        self.addveh=tk.Button(self.adbtframe,text='Add Vehicles',command=self.insertnewveh)
        self.addveh.grid(row=1,column=2)
        self.platelab=tk.Label(self.detframe,text='Reg').grid(row=1,column=2)
        self.dayclab = tk.Label(self.detframe, text='Day\nCost').grid(row=1, column=3)
        self.wkcstlab = tk.Label(self.detframe, text='Week\nCost').grid(row=1, column=4)
        self.wkendcstlab = tk.Label(self.detframe, text='Weekend\nCost').grid(row=1, column=5)
        self.hasbooklab = tk.Label(self.detframe, text='Has\nBookings').grid(row=1, column=6)

        self.gotoaminveh()
    def delveh(self,plate):
        vh.delveh(plate)
        self.quitadmin()





    def quitadmin(self):

        self.master.destroy()



    def insertnewveh(self):

        def quitins():
            self.vehin.destroy()
            pass

        def insert():

            try:
                float(self.daycst.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for day cost', parent=self.vehin)
            try:
                float(self.wekcst.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for week cost', parent=self.vehin)

            try:
                float(self.wkndcst.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for week end cost', parent=self.vehin)
            try:
                float(self.satext.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for Sat Nav Cost', parent=self.vehin)

            try:
                float(self.insext.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for Additional Insurance Cost',
                                       parent=self.vehin)


            if self.intypevar.get() == 'Camper':

                print(self.make.get(),self.model.get())
                #print (int(self.edbeds.get()))

                try:
                    int(self.edbeds.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for beds', parent=self.vehin)

            elif  self.intypevar.get() == 'Cars':
                try:
                    int(self.psngr.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for Passengers', parent=self.vehin)

                try:
                    int(self.doors.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for Doors', parent=self.vehin)
                try:
                    float(self.cseatext.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for Child Seat Cost', parent=self.vehin)

            else:
                try:
                    int(self.psngr.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use whole number values for Passengers', parent=self.vehin)

                try:
                    float(self.cap.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for Capacity', parent=self.vehin)
            plate=self.plate.get()
            type=self.intypevar.get()
            if self.intypevar.get() == 'Camper':
                vehvars = (self.make.get(), self.model.get(), float(self.fuelcon.get()), float(self.daycst.get()),
                           float(self.wekcst.get()), float(self.wkndcst.get()), int(self.edbeds.get()), plate)
                extvars = []
                ext1 = ('Sat', float(self.satext.get()), plate)
                extvars.append(ext1)
                ext2 = ('Ins', float(self.insext.get()), plate)
                extvars.append(ext2)
            elif self.intypevar.get() == 'Cars':
                vehvars = (self.make.get(), self.model.get(), float(self.fuelcon.get()), float(self.daycst.get()),
                           float(self.wekcst.get()), float(self.wkndcst.get()), int(self.doors.get()),int(self.psngr.get()), plate)
                extvars = []
                ext1 = ('Sat', float(self.satext.get()), plate)
                extvars.append(ext1)
                ext2 = ('Ins', float(self.insext.get()), plate)
                extvars.append(ext2)
                ext3 = ('Cseat',float(self.cseatext.get()),plate)
                extvars.append(ext3)
            else:
                vehvars = (self.make.get(), self.model.get(), float(self.fuelcon.get()), float(self.daycst.get()),
                           float(self.wekcst.get()), float(self.wkndcst.get()), float(self.cap.get()),int(self.psngr.get()), plate)
                extvars = []
                ext1 = ('Sat', float(self.satext.get()), plate)
                extvars.append(ext1)
                ext2 = ('Ins', float(self.insext.get()), plate)
                extvars.append(ext2)

            vh.insertveh(type,vehvars, extvars)
            self.vehin.destroy()
            self.quitadmin()

        def adddets(*args):
            for widget in self.typspec.winfo_children():
                widget.destroy()
            print (self.intypevar.get())
            if self.intypevar.get() == 'Camper':
                self.edbeds = tk.Entry(self.typspec)
                self.edbeds.grid(row=9, column=2)
                tk.Label(self.typspec, text='Beds').grid(row=9, column=1)
                self.satext = tk.Entry(self.typspec)
                self.satext.grid(row=10, column=2)
                tk.Label(self.typspec, text='Sat Nav Cost').grid(row=10, column=1)
                self.insext = tk.Entry(self.typspec)
                self.insext.grid(row=11, column=2)
                tk.Label(self.typspec, text='Additional Insurance Cost').grid(row=11, column=1)
            elif self.intypevar.get() == 'Cars':
                self.doors = tk.Entry(self.typspec)
                self.doors.grid(row=9, column=2)
                tk.Label(self.typspec, text='Doors').grid(row=9, column=1)
                self.psngr = tk.Entry(self.typspec)
                self.psngr.grid(row=10, column=2)
                tk.Label(self.typspec, text='Passengers').grid(row=10, column=1)
                self.satext = tk.Entry(self.typspec)
                self.satext.grid(row=11, column=2)
                tk.Label(self.typspec, text='Sat Nav Cost').grid(row=11, column=1)
                self.insext = tk.Entry(self.typspec)
                self.insext.grid(row=12, column=2)
                tk.Label(self.typspec, text='Additional Insurance Cost').grid(row=12, column=1)
                self.cseatext = tk.Entry(self.typspec)
                tk.Label(self.typspec, text='Child Seat Cost').grid(row=13, column=1)
                self.cseatext.grid(row=13, column=2)
            else:
                self.psngr = tk.Entry(self.typspec)
                self.psngr.grid(row=9, column=2)
                tk.Label(self.typspec, text='Passengers').grid(row=9, column=1)
                self.cap = tk.Entry(self.typspec)
                self.cap.grid(row=10, column=2)
                tk.Label(self.typspec, text='Carrying Capacity').grid(row=10, column=1)
                self.satext = tk.Entry(self.typspec)
                self.satext.grid(row=11, column=2)
                tk.Label(self.typspec, text='Sat Nav Cost').grid(row=11, column=1)
                self.insext = tk.Entry(self.typspec)
                self.insext.grid(row=12, column=2)
                tk.Label(self.typspec, text='Additional Insurance Cost').grid(row=12, column=1)
            print('More Details here')
        # insert from here
        self.vehin = tk.Toplevel(self.master)
        typeopts = vh.vehtypes()
        self.incsx = tk.IntVar()
        self.platelab = tk.Label(self.vehin, text='Registration').grid(row=1, column=1)
        self.plate = tk.Entry(self.vehin)
        self.plate.grid(row=1, column=2)
        self.make = tk.Entry(self.vehin)
        self.make.grid(row=2, column=2)
        tk.Label(self.vehin, text='Make').grid(row=2, column=1)
        self.model = tk.Entry(self.vehin)
        self.model.grid(row=3, column=2)
        tk.Label(self.vehin, text='Model').grid(row=3, column=1)
        self.daycst = tk.Entry(self.vehin)
        self.daycst.grid(row=4, column=2)
        self.daycst.focus()
        tk.Label(self.vehin, text='Day Cost').grid(row=4, column=1)
        self.wekcst = tk.Entry(self.vehin)
        self.wekcst.grid(row=5, column=2)
        tk.Label(self.vehin, text='Week Cost').grid(row=5, column=1)
        self.wkndcst = tk.Entry(self.vehin)
        self.wkndcst.grid(row=6, column=2)
        tk.Label(self.vehin, text='Weekend Cost').grid(row=6, column=1)
        self.fuelcon = tk.Entry(self.vehin)
        self.fuelcon.grid(row=7, column=2)
        tk.Label(self.vehin, text='Fuel Consumption l/100km').grid(row=7, column=1)
        tk.Label(self.vehin, text='Type').grid(row=8, column=1)
        self.quitupd = tk.Button(self.vehin, text='Back', command=quitins)
        self.quitupd.grid(row=20, column=1)
        self.svchngs = tk.Button(self.vehin, text='Insert', command=insert)
        self.svchngs.grid(row=20, column=2)
        self.intypevar = tk.StringVar()
        self.intypevar.set(typeopts[0])
        self.intype=tk.OptionMenu(self.vehin, self.intypevar, *typeopts,command=adddets).grid(row=8, column=2)
        self.typspec = tk.Frame(self.vehin)
        self.typspec.grid(row=12, column=1,columnspan=2)
        adddets()






        # end of insert



    def editveh(self,plate):
        def quitupd():
            self.vehed.destroy()

        def update():

            try:
                float(self.daycst.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for day cost', parent=self.vehed)
            try:
                float(self.wekcst.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for week cost', parent=self.vehed)

            try:
                float(self.wkndcst.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for week end cost', parent=self.vehed)
            try:
                float(self.satext.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for Sat Nav Cost', parent=self.vehed)

            try:
                float(self.insext.get())
            except ValueError:
                tk.messagebox.showinfo("Erro", 'Please use numeric values for Additional Insurance Cost',
                                       parent=self.vehed)


            if x[0].gettype() == 'Camper':

                print(self.make.get(),self.model.get())
                print (int(self.edbeds.get()))

                try:
                    int(self.edbeds.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for beds', parent=self.vehed)

            elif  x[0].gettype() == 'Cars':
                try:
                    int(self.psngr.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for Passengers', parent=self.vehed)

                try:
                    int(self.doors.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for Doors', parent=self.vehed)
                try:
                    float(self.cseatext.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for Child Seat Cost', parent=self.vehed)

            else:
                try:
                    int(self.psngr.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use whole number values for Passengers', parent=self.vehed)

                try:
                    float(self.cap.get())

                except ValueError:
                    tk.messagebox.showinfo("Erro", 'Please use numeric values for Capacity', parent=self.vehed)
            if x[0].gettype() == 'Camper':
                vehvars = (self.make.get(), self.model.get(), float(self.fuelcon.get()), float(self.daycst.get()),
                           float(self.wekcst.get()), float(self.wkndcst.get()), int(self.edbeds.get()), plate)
                extvars = []
                ext1 = ('Sat', float(self.satext.get()), plate)
                extvars.append(ext1)
                ext2 = ('Ins', float(self.insext.get()), plate)
                extvars.append(ext2)
            elif x[0].gettype() == 'Cars':
                vehvars = (self.make.get(), self.model.get(), float(self.fuelcon.get()), float(self.daycst.get()),
                           float(self.wekcst.get()), float(self.wkndcst.get()), int(self.doors.get()),int(self.psngr.get()), plate)
                extvars = []
                ext1 = ('Sat', float(self.satext.get()), plate)
                extvars.append(ext1)
                ext2 = ('Ins', float(self.insext.get()), plate)
                extvars.append(ext2)
                ext3 = ('Cseat',float(self.cseatext.get()),plate)
                extvars.append(ext3)
            else:
                vehvars = (self.make.get(), self.model.get(), float(self.fuelcon.get()), float(self.daycst.get()),
                           float(self.wekcst.get()), float(self.wkndcst.get()), float(self.cap.get()),int(self.psngr.get()), plate)
                extvars = []
                ext1 = ('Sat', float(self.satext.get()), plate)
                extvars.append(ext1)
                ext2 = ('Ins', float(self.insext.get()), plate)
                extvars.append(ext2)

            vh.updateveh(x[0].gettype(), vehvars, extvars)
            self.vehed.destroy()
            self.quitadmin()




        x=vh.getvehbyplate(plate)
        typeopts=vh.vehtypes()
        #editwindow
        self.vehed = tk.Toplevel(self.master)
        self.platelab = tk.Label(self.vehed, text='Registration').grid(row=1, column=1)
        self.plate=tk.Label(self.vehed, text=x[0].getplate()).grid(row=1,column=2)
        self.make=tk.Entry(self.vehed)
        self.make.insert(0, x[0].getmake())
        self.make.grid(row=2,column=2)
        tk.Label(self.vehed,text='Make').grid(row=2,column=1)
        self.model = tk.Entry(self.vehed)
        self.model.insert(0, x[0].getmodel())
        self.model.grid(row=3, column=2)
        tk.Label(self.vehed, text='Model').grid(row=3, column=1)
        self.daycst = tk.Entry(self.vehed)
        self.daycst.insert(0, x[0].getdaycost())
        self.daycst.grid(row=4, column=2)
        self.daycst.focus()
        tk.Label(self.vehed, text='Day Cost').grid(row=4, column=1)
        self.wekcst = tk.Entry(self.vehed)
        self.wekcst.insert(0, x[0].getweekcost())
        self.wekcst.grid(row=5, column=2)
        tk.Label(self.vehed, text='Week Cost').grid(row=5, column=1)
        self.wkndcst = tk.Entry(self.vehed)
        self.wkndcst.insert(0, x[0].getweekendcost())
        self.wkndcst.grid(row=6, column=2)
        tk.Label(self.vehed, text='Weekend Cost').grid(row=6, column=1)
        self.fuelcon=tk.Entry(self.vehed)
        self.fuelcon.insert(0, x[0].getfuelcon())
        self.fuelcon.grid(row=7, column=2)
        tk.Label(self.vehed, text='Fuel Consumption l/100km').grid(row=7, column=1)
        tk.Label(self.vehed, text='Type').grid(row=8, column=1)
        self.quitupd = tk.Button(self.vehed, text='Back',command=quitupd)
        self.quitupd.grid(row=20, column=1)
        self.svchngs = tk.Button(self.vehed, text='Save Changes', command=update)
        self.svchngs.grid(row=20, column=2)
        if x[0].gettype()=='Camper':
            tk.Label(self.vehed, text='Camper').grid(row=8, column=2)

            self.edbeds=tk.Entry(self.vehed)
            self.edbeds.insert(0,x[0].getbeds())
            self.edbeds.grid(row=9, column=2)
            tk.Label(self.vehed, text='Beds').grid(row=9, column=1)
            self.satext=tk.Entry(self.vehed)
            self.satext.insert(0,vh.getextcost(plate,'Sat'))
            self.satext.grid(row=10,column=2)
            tk.Label(self.vehed, text='Sat Nav Cost').grid(row=10, column=1)
            self.insext=tk.Entry(self.vehed)
            self.insext.insert(0,vh.getextcost(plate,'Ins'))
            self.insext.grid(row=11,column=2)
            tk.Label(self.vehed, text='Additional Insurance Cost').grid(row=11, column=1)
        elif x[0].gettype()=='Cars':
            tk.Label(self.vehed, text='Cars').grid(row=8, column=2)

            self.doors=tk.Entry(self.vehed)
            self.doors.insert(0,x[0].getdoors())
            self.doors.grid(row=9, column=2)
            tk.Label(self.vehed, text='Doors').grid(row=9, column=1)
            self.psngr=tk.Entry(self.vehed)
            self.psngr.insert(0,x[0].getpassangers())
            self.psngr.grid(row=10, column=2)
            tk.Label(self.vehed, text='Passengers').grid(row=10, column=1)
            self.satext = tk.Entry(self.vehed)
            self.satext.insert(0,vh.getextcost(plate,'Sat'))
            self.satext.grid(row=11, column=2)
            tk.Label(self.vehed, text='Sat Nav Cost').grid(row=11, column=1)
            self.insext=tk.Entry(self.vehed)
            self.insext.insert(0,vh.getextcost(plate,'Ins'))
            self.insext.grid(row=12, column=2)
            tk.Label(self.vehed, text='Additional Insurance Cost').grid(row=12, column=1)
            self.cseatext=tk.Entry(self.vehed)
            self.cseatext.insert(0,vh.getextcost(plate,'Cseat'))
            tk.Label(self.vehed, text='Child Seat Cost').grid(row=13, column=1)
            self.cseatext.grid(row=13, column=2)
        else:
            tk.Label(self.vehed, text='Vans').grid(row=8, column=2)
            self.psngr = tk.Entry(self.vehed)
            self.psngr.insert(0, x[0].getpassangers())
            self.psngr.grid(row=9, column=2)
            tk.Label(self.vehed, text='Passengers').grid(row=9, column=1)
            self.cap = tk.Entry(self.vehed)
            self.cap.insert(0, x[0].getcapacity())
            self.cap.grid(row=10, column=2)
            tk.Label(self.vehed, text='Carrying Capacity').grid(row=10, column=1)
            self.satext = tk.Entry(self.vehed)
            self.satext.insert(0, vh.getextcost(plate, 'Sat'))
            self.satext.grid(row=11, column=2)
            tk.Label(self.vehed, text='Sat Nav Cost').grid(row=11, column=1)
            self.insext = tk.Entry(self.vehed)
            self.insext.insert(0, vh.getextcost(plate, 'Ins'))
            self.insext.grid(row=12, column=2)
            tk.Label(self.vehed, text='Additional Insurance Cost').grid(row=12, column=1)

            pass







    def gotoaminveh(self):
        z=2
        amlist=vh.vehlist()
        for veh in amlist:
            self.edtbutton = tk.Button(self.detframe, text='edit',command=lambda x=veh.getplate(): self.editveh(x)).grid(row=z, column=1)
            self.plate = tk.Label(self.detframe, text=veh.getplate(), bd=2).grid(row=z, column=2)
            self.dayc=tk.Label(self.detframe, text=veh.getdaycost(), bd=2).grid(row=z, column=3)
            self.wekcost=tk.Label(self.detframe, text=veh.getweekcost(), bd=2).grid(row=z, column=4)
            self.wekcost = tk.Label(self.detframe, text=veh.getweekendcost(), bd=2).grid(row=z, column=5)
            if vh.chkfuturebookbyplate(veh.getplate())is True:
                x='Yes'
            else:
                x='No'
            self.bked=tk.Label(self.detframe,text=x).grid(row=z,column=6)
            if x=='No':
                self.delbutton = tk.Button(self.detframe, text='Delete\nVehicle',command=lambda x=veh.getplate(): self.delveh(x)).grid(row=z, column=7)
            z+=1




def main():
    root=tk.Tk()
    Welcom=Welcome(root)
    root.mainloop()

if __name__ == '__main__':
    main()
