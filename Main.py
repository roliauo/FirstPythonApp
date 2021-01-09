# 林宥如 507170055
# -*- coding: utf-8 -*-

import tkinter # 介面化套件
import pandas # 資料處理套件
import csv
import AppConstants
from Components import ControlPanel
from Components import ReportPanel

class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self) # 建立視窗

        ### window setting
        self.title('Python 期末專題 - 507170055 林宥如')
        self.geometry(str(AppConstants.WINDOW_WIDTH) + 'x' + str(AppConstants.WINDOW_HEIGHT)) # 設定視窗大小(參數為字串)
        self.configure(background='white') # background

        ### properties setting
        self.prop_dataFrame = None
        self.prop_school = tkinter.StringVar() # tkinter.StringVar()為tkinter的追蹤變數，取值用get()
        self.prop_degree = tkinter.StringVar() # 學位
        self.prop_department = tkinter.StringVar() # 科系
        self.frames = {} # 存取框架

        ### display
        self.loadData()
        self.createWidgets() # 布置組件內容

    def showFrame(self, frameClass):
        frame = self.frames[frameClass]
        frame.tkraise()
    
    def updateFrame(self, frameClass):
        frame = frameClass(self, self)
        if self.frames[frameClass] is not None:
            self.frames[frameClass].destroy()
        self.frames[frameClass] = frame
        # self.frames[frameClass].pack()
    
    def loadData(self):
        dataUrl = 'http://stats.moe.gov.tw/files/detail/108/108_students.csv'
        self.prop_dataFrame = pandas.read_csv(dataUrl) # dataFrame
    
    def filterData(self):
        # 判斷是否有此條件
        hasFilter: bool = lambda condition: False if condition is None or len(condition.get()) < 1 or condition.get().find('所有') > -1 else True 
        
        data = self.prop_dataFrame # default data
        
        # pandas: .loc 可過濾條件，當存在條件時過濾資料，因為會有多重條件
        if hasFilter(self.prop_school):
            data = data.loc[data['學校名稱'] == self.prop_school.get()] 
        
        if hasFilter(self.prop_department):
            data = data.loc[data['科系名稱'] == self.prop_department.get()]
        
        if hasFilter(self.prop_degree):
            data = data.loc[data['等級別'] == self.prop_degree.get()]
        
        return data
        
        # if self.prop_school is None or self.prop_school.get().find('所有') > -1:
        #     return self.prop_dataFrame
        # else:
        #     # return self.prop_dataFrame.loc[self.prop_dataFrame['學校名稱'] == self.prop_school.get()]
        #     return self.prop_dataFrame.loc[
        #         (self.prop_dataFrame['學校名稱'] == self.prop_school.get()) & 
        #         (self.prop_dataFrame['科系名稱'] == self.prop_department.get()) &
        #         (self.prop_dataFrame['等級別'] == self.prop_degree.get())
        #         ]

    def createWidgets(self):
        # container = tkinter.Frame(self)
        # container.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
       
        controlPanel = ControlPanel(self, self)
        reportPanel = ReportPanel(self, self)
        self.frames[ReportPanel] = reportPanel
        # self.showFrame(ReportPanel)
    

#data.groupby('學校名稱').size()
#print(data.groupby('學校名稱').get_group('國立政治大學'))

if __name__ == "__main__":
    app = App()
    app.mainloop()