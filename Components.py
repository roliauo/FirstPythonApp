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


class ControlPanel(tkinter.Frame):   
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent) # 建立框架
        self.pack(fill='x') # 自動填滿左右(x方向)
        self.createWidgets(parent, controller) # 布置組件內容

    def createWidgets(self, parent, controller):     
        ### option list # or search?
        def createOptionMenu(id: int, columnName: str, selection: tkinter.StringVar, label: str = ''):
            labelTxt = columnName
            if len(label) > 0:
                labelTxt = label
            optionLabel = tkinter.Label(self, text=labelTxt)
            # optionLabel.pack(side=tkinter.LEFT)
            optionLabel.grid(row=id, column=0, padx=20, pady=10)

            optionsList = controller.prop_dataFrame[columnName].unique().tolist() # pandas找出欄位:<學校名稱>所有不重複的值 (為numpy.ndarray，再轉為串列)  
            optionsList.insert(0, constants.SELECTION_ALL) # 加入'全部'之選項

            selection.set(optionsList[0]) # 預設選項一        
            selection.trace('w', onUpdateData) # 監聽選項改變時，觸發function。 'w'為監聽模式

            optionMenu = tkinter.OptionMenu(self, selection, *optionsList)
            # optionMenu.pack(side=tkinter.LEFT)
            optionMenu.grid(row=id, column=1)

        def onUpdateData(*args): # *args 為不限定長度之參數 print(args) -> output: ('PY_VAR0', '', 'w')
            controller.updateFrame(ReportPanel) # 更新ReportPanel的資料

        ### school menu
        createOptionMenu(0, '學校名稱', controller.prop_school)

        ### department menu
        createOptionMenu(1, '科系名稱', controller.prop_department)

        ### degree menu
        createOptionMenu(2, '等級別', controller.prop_degree, '學位')

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
        btn_showChart.grid(row=3)


class ReportPanel(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent) 
        self.pack(fill='both', expand=True) # 填滿全部
        self.createWidgets(parent, controller) # 布置組件內容

    def createWidgets(self, parent, controller):  
        print('ReportPanel:', controller.prop_school.get())
        report = Table(self, dataframe=controller.filterData(), showstatusbar=True,  editable=False) 
        report.show()

