from PyQt5 import QtWidgets, uic
from PyQt5 import QtWidgets, uic , QtGui #icon
import sys


##################### declare functions here ####################

def calOddDays(yearStart,yearEnd,day):        
            for i in range(yearStart+1,yearEnd,1):
                if (i % 4 == 0):
                    day += 2
                else:
                    day += 1
            day%=7
            return day
def checkLeap(year):
            if (year%4==0):
                return 29
            else:
                return 28 
def AddDays(yearStart,yearEnd,monthStart,monthEnd,months,dateStart,dateEnd,day,monthAddition):
        if (abs(yearEnd-yearStart)>1):
            for i in (yearStart+1,yearEnd):
                if (i % 4 == 0):
                    day += 2
                else:
                    day += 1
        months["2"]=checkLeap(yearStart)     
        for i in range(monthStart+1,13):
            monthAddition+=months[str(i)]
        months["2"]=checkLeap(yearEnd)
        for i in range(1,monthEnd):
            monthAddition+=months[str(i)]        
        day+=(monthAddition+abs(months[str(monthStart)]-dateStart)+dateEnd)%7            
        while( day>7):
            day%=7        
        return day

######################## UI starts here ################################

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()        
        uic.loadUi('calendar_gui.ui', self)  # pass your ui file name here
                
        ########## set custom icon ############
        self.setWindowIcon(QtGui.QIcon('resources/calendar.ico'))
        #######################################

        #lock window resize
        width=321
        height=249
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        ############################
        

        # find the button 'PressMeBtn' is the button name
        self.calculateBtn = self.findChild(
            QtWidgets.QPushButton, 'btnCalculate')
        # Remember to pass the definition/method, not the return value!
        self.calculateBtn.clicked.connect(self.printButtonPressed)

        self.dateInputStart = self.findChild(
            QtWidgets.QDateEdit, 'startMonthDate')
        self.dateInputEnd = self.findChild(QtWidgets.QDateEdit, 'endMonthDate')

        self.dayOftheWeek = self.findChild(
            QtWidgets.QComboBox, 'startDayOfTheWeek')
        self.EndDay = self.findChild(QtWidgets.QLabel, 'resultLabel')

        self.show()
    
    def printButtonPressed(self):
        # This is executed when the button is pressed
        # print(self.dateInput.date().month())
        dateStart = self.dateInputStart.date().day()
        monthStart = self.dateInputStart.date().month()
        yearStart = self.dateInputStart.date().year()

        dateEnd = self.dateInputEnd.date().day()
        monthEnd = self.dateInputEnd.date().month()
        yearEnd = self.dateInputEnd.date().year()        
        day = self.dayOftheWeek.currentIndex()+1
        originalDay=day
        monthAddition=0      
        answer = ''               
        months={"1":31,
                "2":28,
                "3":31,
                "4":30,
                "5":31,
                "6":30,
                "7":31,
                "8":31,
                "9":30,
                "10":31,
                "11":30,
                "12":31}
        
        ########################### Logic #####################
        """
        if (dateStart == dateEnd) and (monthStart == monthEnd) and (abs(yearEnd-yearStart) == 1):
            if (yearStart % 4 == 0):
                day += 2
            else:
                day += 1
        """
        #if both  date and month are different
        if ((dateStart != dateEnd) and (monthStart != monthEnd) and (yearEnd==yearStart)):
            if (yearStart%4==0) or (yearEnd%4==0):
                months["2"]=29         
            for i in range(monthStart+1,monthEnd):
                monthAddition+=months[str(i)]
            #print("added month:",monthAddition)
            day+=(monthAddition+abs(months[str(monthStart)]-dateStart)+dateEnd)%7
            while( day>7):
                day%=7
                
        #if only date is different
        elif ((dateStart != dateEnd) and (monthStart == monthEnd) and (yearEnd==yearStart)):
            months["2"]=checkLeap(yearStart)
            day=(abs(dateStart-dateEnd))%7
        
        #if only month is different
        elif ((dateStart == dateEnd) and (monthStart != monthEnd) and (yearEnd==yearStart)):
            months["2"]=checkLeap(yearStart)
            for i in range(monthStart+1,monthEnd):
                monthAddition+=months[str(i)]
            day+=(monthAddition+abs(months[str(monthStart)]-dateStart)+dateEnd)%7
        
        #if only year is different
        elif ((dateStart == dateEnd) and (monthStart == monthEnd) and (yearEnd!=yearStart)):
            if ((yearEnd%4==0) and (monthEnd>=2) and (dateEnd>=29)):
                day += 2
            else:
                day += 1
            day=calOddDays(yearStart,yearEnd,day)
        
        #if all are different
        elif ((dateStart != dateEnd) and (monthStart != monthEnd) and (yearEnd!=yearStart)):
            day=(AddDays(yearStart,yearEnd,monthStart,monthEnd,months,dateStart,dateEnd,day,monthAddition))
            
        
        if day==0:
            day=originalDay
            
        if day == 1:
            answer = 'Sunday'
        elif day == 2:
            answer = 'Monday'
        elif day == 3:
            answer = "Tuesday"
        elif day == 4:
            answer = "Wednesday"
        elif day == 5:
            answer = "Thursday"
        elif day == 6:
            answer = "Friday"
        elif day==7:
            answer = "Saturday"
        else:
            print("Error")


        print("day:", answer)
        self.EndDay.setText(str(answer))


app = QtWidgets.QApplication(sys.argv)

window = Ui()
app.exec_()
