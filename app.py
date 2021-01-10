# 林宥如 507170055
# -*- coding: utf-8 -*-

import tkinter # 介面化套件
import pandas # 資料處理套件
import re # 字串處理
import csv
import constants # 自定義常數
from components import GroupbyPanel
from components import FilterPanel
from components import ReportPanel

class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self) # 建立視窗

        ### window setting
        self.title('Python 期末專題 - 507170055 林宥如')
        self.geometry(str(constants.WINDOW_WIDTH) + 'x' + str(constants.WINDOW_HEIGHT)) # 設定視窗大小(參數為字串)
        self.minsize(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        # self.configure(background='white') # background
        # tkinter.Grid.rowconfigure(self, 0, weight=1) # y方向拓展
        # tkinter.Grid.columnconfigure(self, 0, weight=1) # x方向拓展

        ### properties setting
        self.prop_originalData = None # 原始資料表
        self.prop_currentData = None # 目前顯示之資料
        self.prop_currentData_columns = tkinter.StringVar() # 追蹤目前資料欄位
        self.prop_school = tkinter.StringVar() # tkinter.StringVar()為tkinter的追蹤變數，預設為空字串:''，取值用get()
        self.prop_degree = tkinter.StringVar() # 學位
        self.prop_department = tkinter.StringVar() # 科系
        self.prop_grouby = [tkinter.StringVar() for i in range(3)] # 建立一個長度為3 的 StringVar串列 (因會放入學校/科系/學位，這三個項目)
        self.frames = {} # 存取框架

        self.loadData()
        self.display() # 布置組件內容      

        ### 監聽目前資料欄位，監聽選項改變時，觸發function。 'w'為監聽模式
        def updateFilterPanel(*args):
            self.updateFrame(FilterPanel)
        self.prop_currentData_columns.trace('w', updateFilterPanel)
        self.prop_school.trace('w', self.onUpdateData) 
        self.prop_degree.trace('w', self.onUpdateData) 
        self.prop_department.trace('w', self.onUpdateData) 


    def onUpdateData(self, *args): # *args 為不限定長度之參數 print(args) -> output: ('PY_VAR0', '', 'w')
        self.updateFrame(GroupbyPanel) # 因為布局關係所以更新 (原本不加的話用pack佈局會錯位)
        self.updateFrame(FilterPanel)
        self.updateData()
        self.updateFrame(ReportPanel) # 更新ReportPanel的資料
    
    def updateFrame(self, frameClass): 
        frame = frameClass(self) # 建立框架
        if self.frames[frameClass] is not None: # 若框架存在的話即銷毀
            self.frames[frameClass].destroy() 
        self.frames[frameClass] = frame
    
    def loadData(self):
        dataUrl = 'http://stats.moe.gov.tw/files/detail/108/108_students.csv'
        self.prop_originalData = pandas.read_csv(dataUrl) # pandas獲取資料輸出為dataFrame
        # merge: pandas.concat([df1, df2], axis=)

        ### parse data
        self.prop_originalData = self.prop_originalData.rename({'等級別': '學位'}, axis='columns') # 更改欄位名稱
        columns = self.prop_originalData.columns.values.tolist() # 得到資料表的欄位串列
      
        # 將計數欄位轉成數字
        data = self.prop_originalData.copy()
        for col in columns:
            if len(re.findall("計|男|女", col)) > 0:
                data[col] = [int(re.sub(',|-', '', x)) if len(re.sub(',|-', '', x)) > 0 else 0 for x in data[col].tolist()] # 欄位值字串轉數字 (方法一) : re.sub取代記號後轉數字
                # data[col] = data[col].apply(pandas.to_numeric, errors='coerce') # 欄位值字串轉數字 (方法二: 套件函式)，errors='coerce'為非數字用NaN取代 
                
        data['學校代碼'] = data['學校代碼'].astype(str) # 數字轉為字串 (因groupby 算總和時會相加失真)

        self.prop_originalData = data
        self.prop_currentData = data
        self.prop_currentData_columns.set(self.prop_originalData.columns.values)

    def dataAnalysis(self):
        # print(self.prop_originalData.groupby('學校名稱').get_group('國立政治大學'))
        data = self.prop_originalData.copy()
        columns = data.columns.values.tolist() # 得到資料表的欄位串列

        ##### calculate
        # allStudentsNum = data['總計'].sum().astype(int) # 總就學人數

        ##### new data       
        # data.groupby(['學校代碼', '學校名稱']).sum().astype(int) # 校別總人數  # sum有小數點，用astype轉換為int
        # data = data.groupby(['學校代碼', '學校名稱', '科系名稱'], as_index=False).sum() # 校+系別            
        # data = data.groupby(['學校代碼', '學校名稱', '科系名稱'], as_index=False).sum()  #, as_index=False
        # data = data.groupby(['學校代碼', '學校名稱', '科系名稱', '學位'], as_index=False).sum() 

        ### as_index=False 設定非索引需指定欄位轉成數字，不可一同轉換
        # data.groupby(['學校代碼', '學校名稱'], as_index=False).sum()
        # data['總計'] = data['總計'].astype(int)
        ###

        data = data.groupby(['學校名稱', '科系名稱']).sum().astype(int) # sum有小數點，用astype轉換為int #系總人數
        # data['全校人數'] = 
        # data = data[['學校名稱', '總計']]
        # data = pandas.DataFrame({

        # })

    def updateData(self):
        data = self.prop_originalData.copy() # use original data
        data = self.groupbyData(data)
        data = self.filterData(data)
        self.prop_currentData = data # set current data
        self.prop_currentData_columns.set(self.prop_currentData.columns.values)

    def groupbyData(self, varData):
        data = varData.copy() # default data
        groupbyList = [x.get() for x in self.prop_grouby if len(x.get()) > 0] # 產生prop_grouby的字串串列
        # groupbyList = [column for column in groupbyList if column in self.prop_currentData_columns.get()] # 目前資料欄位出現的才做groupby

        if '學校名稱' in groupbyList:
            groupbyList.insert(0, '學校代碼')

        if len(groupbyList) > 0:
            data = data.groupby(groupbyList, as_index=False).sum() 
        
        return data
    
    def hasFilter(self, condition: tkinter.StringVar): # 判斷是否有此條件 (若選擇'全部'視為無條件)
        if condition is None or len(condition.get()) < 1 or condition.get().find(constants.SELECTION_ALL) > -1 :
            return False
        else:
            return True
           
    def filterData(self, varData):
        data = varData.copy() # default data

        hasColumn: bool = lambda columnName:  columnName in data.columns.values.tolist() # 判斷欄位是否在目前資料中        
        # pandas: []可過濾資料，當存在條件時過濾資料，因為會有多重條件且不一定同時存在，所以不能同時過濾      
        if hasColumn('學校名稱') and self.hasFilter(self.prop_school):
            data = data[data['學校名稱'] == self.prop_school.get()] 
        
        if hasColumn('科系名稱') and self.hasFilter(self.prop_department):
            data = data[data['科系名稱'] == self.prop_department.get()]
        
        if hasColumn('學位') and self.hasFilter(self.prop_degree):
            data = data[data['學位'] == self.prop_degree.get()]
        
        return data
        
    def display(self):  
        groupbyPanel = GroupbyPanel(self)    
        filterPanel = FilterPanel(self)
        reportPanel = ReportPanel(self)

        self.frames[GroupbyPanel] = groupbyPanel # set frames
        self.frames[FilterPanel] = filterPanel 
        self.frames[ReportPanel] = reportPanel 
    

if __name__ == "__main__":
    app = App()
    app.mainloop() # 視窗持續存在

#133-66=67