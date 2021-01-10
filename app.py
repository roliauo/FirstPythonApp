# 林宥如 507170055
# -*- coding: utf-8 -*-

import tkinter # 介面化套件
import pandas # 資料處理套件
import re # 字串處理
import csv
import constants # 自定義常數
from components import ControlPanel
from components import ReportPanel

class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self) # 建立視窗

        ### window setting
        self.title('Python 期末專題 - 507170055 林宥如')
        self.geometry(str(constants.WINDOW_WIDTH) + 'x' + str(constants.WINDOW_HEIGHT)) # 設定視窗大小(參數為字串)
        self.configure(background='white') # background

        ### properties setting
        self.prop_dataFrame = None # 原始資料表
        self.prop_columnsDict = {} # 資料欄位字典
        self.prop_school = tkinter.StringVar() # tkinter.StringVar()為tkinter的追蹤變數，取值用get()
        self.prop_degree = tkinter.StringVar() # 學位
        self.prop_department = tkinter.StringVar() # 科系
        self.prop_grouby = []
        self.frames = {} # 存取框架

        ### display
        self.loadData()
        self.createWidgets() # 布置組件內容
    
    def updateFrame(self, frameClass): 
        frame = frameClass(self) # 建立
        if self.frames[frameClass] is not None:
            self.frames[frameClass].destroy() # 若框架存在的話即銷毀
        self.frames[frameClass] = frame
    
    def loadData(self):
        dataUrl = 'http://stats.moe.gov.tw/files/detail/108/108_students.csv'
        self.prop_dataFrame = pandas.read_csv(dataUrl) # pandas獲取資料輸出為dataFrame

        columns = self.prop_dataFrame.columns.values.tolist() # 得到資料表的欄位串列
        zipColumns = zip(columns, columns)
        self.prop_columnsDict = dict(zipColumns) # 將欄位轉成字典表
        # print(self.prop_columnsDict)

        ### parse data
        # 將計數欄位轉成數字
        data = self.prop_dataFrame.copy()
        for col in columns:
            if len(re.findall("計|男|女", col)) > 0:
                data[col] = [int(re.sub(',|-', '', x)) if len(re.sub(',|-', '', x)) > 0 else 0 for x in data[col].tolist()] # 欄位值字串轉數字 (方法一) : re.sub取代記號後轉數字
                # data[col] = data[col].apply(pandas.to_numeric, errors='coerce') # 欄位值字串轉數字 (方法二: 套件函式)，errors='coerce'為非數字用NaN取代 
        self.prop_dataFrame = data
        # merge: pandas.concat([df1, df2], axis=)

    def dataAnalysis(self):
        # print(self.prop_dataFrame.groupby('學校名稱').get_group('國立政治大學'))
        data = self.prop_dataFrame.copy()
        columns = data.columns.values.tolist() # 得到資料表的欄位串列

        # ironman_df = pandas.DataFrame({
        #     'team':['A','B','C','C','B','B'],
        #     'number':[int(x) for x in list(['7', '8', '7', '0', '8', '1'])] # 將字串轉成數字串列
        #     }, #np.random.randint(10, size=6) #['7', '8', '7', '0', '8', '1']
        #     columns=['team','number'])
        # print(ironman_df)
        # print(ironman_df.groupby('team').sum()) #

        ##### calculate
        # allStudentsNum = data['總計'].sum().astype(int) # 總就學人數

        ##### new data       
        # data.groupby(['學校代碼', '學校名稱']).sum().astype(int) # 校別總人數  # sum有小數點，用astype轉換為int
        # data = data.groupby(['學校代碼', '學校名稱', '科系名稱'], as_index=False).sum() # 校+系別

        ### as_index=False 設定非索引需指定欄位轉成數字，不可一同轉換
        # data.groupby(['學校代碼', '學校名稱'], as_index=False).sum()
        # data['總計'] = data['總計'].astype(int)
        ###

        data = data.groupby(['學校名稱', '科系名稱']).sum().astype(int) # sum有小數點，用astype轉換為int #系總人數
        # data['全校人數'] = 
        # data = data[['學校名稱', '總計']]
        # data = pandas.DataFrame({

        # })

    def groupbyData(self):
        data = self.prop_dataFrame.copy() # default data

        if len(self.prop_grouby) > 0:
            data = data.groupby(self.prop_grouby, as_index=False).sum() 
        
        return data
        
    
    def filterData(self):
        data = self.prop_dataFrame.copy() # default data

        # 判斷是否有此條件
        hasFilter: bool = lambda condition: False if condition is None or len(condition.get()) < 1 or condition.get().find(constants.SELECTION_ALL) > -1 else True 
        
        # data = data.groupby(['學校代碼', '學校名稱', '科系名稱'], as_index=False).sum()  #, as_index=False
        # data = data.groupby(['學校代碼', '學校名稱', '科系名稱', '等級別'], as_index=False).sum() 
        
        # pandas: []可過濾資料，當存在條件時過濾資料，因為會有多重條件且不一定同時存在，所以不能同時過濾      
        if hasFilter(self.prop_school):
            data = data[data['學校名稱'] == self.prop_school.get()] 
        
        if hasFilter(self.prop_department):
            data = data[data['科系名稱'] == self.prop_department.get()]
        
        if hasFilter(self.prop_degree):
            data = data[data['等級別'] == self.prop_degree.get()]
        
        return data
        
    def createWidgets(self):      
        controlPanel = ControlPanel(self)
        reportPanel = ReportPanel(self)

        self.frames[ControlPanel] = controlPanel # set frames
        self.frames[ReportPanel] = reportPanel 
    

if __name__ == "__main__":
    app = App()
    app.mainloop()