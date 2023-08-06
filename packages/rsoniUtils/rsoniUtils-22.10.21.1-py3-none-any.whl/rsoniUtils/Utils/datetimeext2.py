import time
from datetime import timezone, timedelta
import datetime
import os
import pandas as pd
import calendar
from dateutil.relativedelta import relativedelta


DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


class clsDateTime2Ext:
    def __init__(self):
        self.Name = "dateTime_EXT"

    def GetCurrentDateTimeSTR(self):
        dt = datetime.datetime.now()
        # tz=ZoneInfo('Asia/Kolkata')
        ##utc_time = dt.replace(tzinfo=timezone.utc)
        filstrUTCdt = dt.strftime(DATE_TIME_FORMAT)
        #print("dir utc_time -> ",filstrUTCdt)
        return filstrUTCdt

    def GetCurrentDateTimeDTM(self):
        filstrUTCdt = self.GetCurrentDateTimeSTR()
        str2DTM = datetime.datetime.strptime(filstrUTCdt, DATE_TIME_FORMAT)
        return str2DTM

    def GetCurrentDateTimeDTMpd(self):
        dtm = self.GetCurrentDateTimeDTM()
        return pd.Timestamp(
            dtm.year, dtm.month, dtm.day, dtm.hour, dtm.minute, dtm.second)

    def GetDateinformatSTR(self, yy, mm, dd, hh=0, mins=0, ss=0):
        mmm = str(mm)
        if (len(mmm) == 1):
            mmm = "0"+str(mm)
        ddd = str(dd)
        if (len(ddd) == 1):
            ddd = "0"+str(dd)
        hhh = str(hh)
        if (len(hhh) == 1):
            hhh = "0"+str(hh)
        minss = str(mins)
        if (len(minss) == 1):
            minss = "0"+str(minss)
        sss = str(ss)
        if (len(sss) == 1):
            sss = "0"+str(sss)

        return str(yy)+"-"+mmm+"-"+ddd+"T"+hhh+":"+minss+":"+sss+".000Z"

    def GetDateTimeFromDTM2STR(self, dtDTM):
        return self.GetDateinformatSTR(dtDTM.year, dtDTM.month, dtDTM.day, dtDTM.hour, dtDTM.minute, dtDTM.second)

    def GetDateTimeFromSTR2DTM(self, dtSTR):
        return datetime.datetime.strptime(dtSTR, DATE_TIME_FORMAT)

    def GetDateinformatDTM(self, yy, mm, dd, hh=0, mins=0, ss=0):
        filstrUTCdt = self.GetDateinformatSTR(yy, mm, dd, hh, mins, ss)
        str2DTM = datetime.datetime.strptime(filstrUTCdt, DATE_TIME_FORMAT)
        return str2DTM

    def GetDateinformatDTMpd(self, yy, mm, dd):
        dtm = self.GetDateinformatDTM(yy, mm, dd)
        return pd.Timestamp(
            dtm.year, dtm.month, dtm.day, dtm.hour, dtm.minute, dtm.second)

    def LastDateofMonth(self, yy, mm):
        return calendar.monthrange(yy, mm)[1]

    def Total6MonthsDates(self, Startyyyy, Endyyyy):
        returnLst = [[]]
        Nextyy = Startyyyy
        returnLst.append([self.GetDateinformatSTR(Nextyy, 1, 1),
                          self.GetDateinformatSTR(Nextyy, 6, 30)])
        returnLst.append([self.GetDateinformatSTR(Nextyy, 7, 1),
                          self.GetDateinformatSTR(Nextyy, 12, 31)])
        while (Nextyy < Endyyyy):
            Nextyy = Nextyy+1
            returnLst.append([self.GetDateinformatSTR(Nextyy, 1, 1),
                              self.GetDateinformatSTR(Nextyy, 6, 30)])
            returnLst.append([self.GetDateinformatSTR(Nextyy, 7, 1),
                              self.GetDateinformatSTR(Nextyy, 12, 31)])
        finaldf = pd.DataFrame(returnLst, columns=['StartDT', 'EndDT'])
        finaldf = finaldf[(finaldf.StartDT.notnull())]
        return finaldf

    def Total3MonthsDates(self, Startyyyy, Endyyyy):
        returnLst = [[]]
        Nextyy = Startyyyy
        returnLst.append([self.GetDateinformatSTR(Nextyy, 1, 1),
                          self.GetDateinformatSTR(Nextyy, 3, 31)])
        returnLst.append([self.GetDateinformatSTR(Nextyy, 4, 1),
                          self.GetDateinformatSTR(Nextyy, 6, 30)])
        returnLst.append([self.GetDateinformatSTR(Nextyy, 7, 1),
                          self.GetDateinformatSTR(Nextyy, 9, 30)])
        returnLst.append([self.GetDateinformatSTR(Nextyy, 10, 1),
                          self.GetDateinformatSTR(Nextyy, 12, 31)])
        while (Nextyy < Endyyyy):
            Nextyy = Nextyy+1
            returnLst.append([self.GetDateinformatSTR(Nextyy, 1, 1),
                              self.GetDateinformatSTR(Nextyy, 3, 31)])
            returnLst.append([self.GetDateinformatSTR(Nextyy, 4, 1),
                              self.GetDateinformatSTR(Nextyy, 6, 30)])
            returnLst.append([self.GetDateinformatSTR(Nextyy, 7, 1),
                              self.GetDateinformatSTR(Nextyy, 9, 30)])
            returnLst.append([self.GetDateinformatSTR(Nextyy, 10, 1),
                              self.GetDateinformatSTR(Nextyy, 12, 31)])
        finaldf = pd.DataFrame(returnLst, columns=['StartDT', 'EndDT'])
        finaldf = finaldf[(finaldf.StartDT.notnull())]
        return finaldf

    def Total3MonthsCount(self, frmDT1, ToDt1):
        totalCount = 0
        NextDT = frmDT1
        print(NextDT)
        while (NextDT < ToDt1):
            NextDT = self.AddinDateDTM(NextDT, returnType="STR", mths=3)
            totalCount += 1
            print(NextDT)
            # print("totalCount",totalCount)
        return totalCount

    def GetYear(self, dtVal):
        if (type(dtVal) is str):
            str2DTM = datetime.datetime.strptime(dtVal, DATE_TIME_FORMAT)
            return str2DTM.year
        if (type(dtVal) is datetime.datetime):
            str2DTM = dtVal
            return str2DTM.year

    def AddinDateDTM(self, startDateSTR, returnType="STR", ddays=0, mths=0, yyears=0, hours=0, mins=0, secs=0):
        if (type(startDateSTR) is str):
            str2DTM = datetime.datetime.strptime(
                startDateSTR, DATE_TIME_FORMAT)
        if (type(startDateSTR) is datetime.datetime):
            str2DTM = startDateSTR
        if (type(startDateSTR) is pd.Timestamp):
            str2DTM = startDateSTR
        returnValue = str2DTM + datetime.timedelta(days=ddays)
        returnValue = returnValue + relativedelta(months=+mths)
        returnValue = returnValue + relativedelta(years=+yyears)
        returnValue = returnValue + relativedelta(hours=+hours)
        returnValue = returnValue + relativedelta(minutes=+mins)
        returnValue = returnValue + relativedelta(seconds=+secs)
        if (returnType == "STR"):
            return self.GetDateTimeFromDTM2STR(returnValue)
        return returnValue

######################################################
# print(GetCurrentDateTimeSTR())
#print(GetDateinformatSTR(2022, 1, 1))

# print(GetCurrentDateTimeDTM())
#print(GetDateinformatDTM(2022, 1, 1))

# print(GetCurrentDateTimeDTMpd())
#print(GetDateinformatDTMpd(2022, 1, 1))


#print(AddinDateDTM(GetCurrentDateTimeDTM(), 0,-1, 0))

# print(GetDateinformatSTRFromDTM(GetCurrentDateTimeDTM()))
# print(AddinDateDTM(GetCurrentDateTimeDTM(),yyears=-5))

#ToDt = GetCurrentDateTimeSTR()
# GetCurrentDateTimeDTMFromSTR(ToDt)

# (AddinDateDTM(GetCurrentDateTimeDTMFromSTR(ToDt),returnType="STR",yyears=-5))

##Total3MonthsCount(GetDateinformatSTR(2022, 1, 1),GetCurrentDateTimeSTR())
# print(Total3MonthsDates(2020,2022))
