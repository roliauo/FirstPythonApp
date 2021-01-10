# 林宥如 507170055
# -*- coding: utf-8 -*-

import tkinter # 介面化套件
import pandas # 資料處理套件
import matplotlib.pyplot as plt # 圖表套件
from pandastable import Table # 表格套件
import constants

### plot - font setting
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'sans-serif'] 
plt.rcParams['axes.unicode_minus'] = False

class GroupbyPanel(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent) # 建立框架
        self.pack(side=tkinter.TOP, fill='x') # 自動填滿左右(x方向)
        # self.grid(row=0, sticky='n') #sticky 可以使用 n, e, s, w 及組合來定位
        self.display(parent)

    def display(self, parent):
        def createCheckButton(rowId: int, itemName: str, checked: tkinter.StringVar):
            if len(checked.get()) == 0:
                checked.set('') # 預設 
            # checkboxState = 'active' #if enabled else 'disabled'
            checkbox = tkinter.Checkbutton(self, text=itemName, var=checked, onvalue=itemName, offvalue='', command=parent.onUpdateData) # onvalue/offvalue 設定 var 所得到的值  #, state=checkboxState
            checkbox.grid(row=rowId)
                       
        ### checkbox (for groupby)
        createCheckButton(3, '學校名稱', parent.prop_grouby[0])
        createCheckButton(4, '科系名稱', parent.prop_grouby[1])
        createCheckButton(5, '學位', parent.prop_grouby[2])

        
class FilterPanel(tkinter.Frame):   
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent) # 建立框架
        self.pack(fill='x') # 自動填滿左右(x方向)
        # self.grid(row=1, sticky='n')
        self.display(parent)

    def display(self, parent):   

        def createOptionMenu(rowId: int, columnName: str, selection: tkinter.StringVar):
            noColumn = columnName not in parent.prop_currentData_columns.get() # 判斷欄位是否在目前資料中
            optionsList = ['-'] if noColumn else parent.prop_currentData[columnName].unique().tolist() # pandas找出欄位:<學校名稱>所有不重複的值 (為numpy.ndarray，再轉為串列)  
            optionsList.insert(0, constants.SELECTION_ALL) # 加入'全部'之選項
            
            if len(selection.get()) == 0:
                selection.set(optionsList[0]) # 預設選項一  

            optionMenu = tkinter.OptionMenu(self, selection, *optionsList)
            
            if noColumn: # 若目前資料沒有此欄位的話禁止點選              
                optionMenu.configure(state='disabled')

            optionLabel = tkinter.Label(self, text=columnName) # 建立label
            optionLabel.grid(row=rowId, column=0, padx=20, pady=5) # 佈件
            optionMenu.grid(row=rowId, column=1, padx=20, pady=5) 

        ### option menu
        createOptionMenu(0, '學校名稱', parent.prop_school)
        createOptionMenu(1, '科系名稱', parent.prop_department)
        createOptionMenu(2, '學位', parent.prop_degree)

        ### chart button
        def showChart(dataFrame, chartType: str, columnX: str, columnY: str):
            dataArrX = columnX #dataFrame[columnX] #need to be modified
            dataArrY = columnY #dataFrame[columnY]
            if chartType == constants.CHART_BAR:
                plt.bar(dataArrX, dataArrY)
            elif chartType == constants.CHART_PIE:
                plt.pie(dataArrY, labels = dataArrX)
            elif chartType == constants.CHART_LINE:
                plt.plot(dataArrX, dataArrY)
                #plt.plot('x','y',data=data)
                #plt.plot(data['x'],data['y'])
            
            plt.show()
        def show():
            x = ["A", "B", "C", "D"]
            y = [3, 8, 1, 10]
            plt.bar(x,y)
            plt.show()

        btn_showChart = tkinter.Button(self, text='Chart', command=show)
        btn_showChart.grid(row=6, columnspan=3)


class ReportPanel(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent) 
        self.pack(side=tkinter.BOTTOM,fill='both', expand=True) # 填滿全部
        # self.grid(row=2, sticky='nesw')
        self.display(parent) # 布置組件內容

    def display(self, parent):  
        data = parent.prop_currentData #parent.getData()
        report = Table(self, dataframe=data, showstatusbar=True, editable=False) # 建立table               
        report.showIndex() # 加入此行才能顯示index
        report.show()
