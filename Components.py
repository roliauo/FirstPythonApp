# 林宥如 507170055
# -*- coding: utf-8 -*-

import tkinter # 介面化套件
import pandas # 資料處理套件
import matplotlib.pyplot as plt # 圖表套件
from pandastable import Table # 表格套件
import AppConstants

### plot - font setting
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'sans-serif'] 
plt.rcParams['axes.unicode_minus'] = False


class ControlPanel(tkinter.Frame):   
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, bg='violet', width=AppConstants.WINDOW_WIDTH, height=AppConstants.WINDOW_HEIGHT/3) # 建立框架
        self.pack(fill='x') # 自動填滿左右(x方向)
        # self.grid(row=0, column=0, sticky="n")
        self.createWidgets(parent, controller) # 布置組件內容

    # def createOptionMenu(self, controller, columnName: str):
    #     list_school = controller.prop_dataFrame['學校名稱'].unique().tolist() # pandas找出欄位:<學校名稱>所有不重複的值 (為numpy.ndarray，再轉為串列)  
    #     list_school.insert(0, '所有學校') # 加入'全部'之選項

    #     controller.prop_school.set(list_school[0]) # 預設選項一        
    #     controller.prop_school.trace('w', onUpdateData) # 監聽選項改變時，觸發function。 'w'為監聽模式

    #     optionMenu_school = tkinter.OptionMenu(self, controller.prop_school, *list_school)
    #     optionMenu_school.pack()

    def createWidgets(self, parent, controller):
        
        ### option list # or search?

        def createOptionMenu(columnName: str, selection: tkinter.StringVar):
            optionLabel = tkinter.Label(self, text=columnName)
            # optionLabel.pack(side=tkinter.LEFT)

            optionsList = controller.prop_dataFrame[columnName].unique().tolist() # pandas找出欄位:<學校名稱>所有不重複的值 (為numpy.ndarray，再轉為串列)  
            optionsList.insert(0, '所有') # 加入'全部'之選項

            selection.set(optionsList[0]) # 預設選項一        
            selection.trace('w', onUpdateData) # 監聽選項改變時，觸發function。 'w'為監聽模式

            optionMenu = tkinter.OptionMenu(self, selection, *optionsList)
            # optionMenu.pack(side=tkinter.LEFT)
            optionMenu.pack(side=tkinter.LEFT)

        def onUpdateData(*args): # *args 為不限定長度之參數 print(args) -> output: ('PY_VAR0', '', 'w')
            controller.updateFrame(ReportPanel) # 更新ReportPanel的資料

        ### school menu
        createOptionMenu('學校名稱', controller.prop_school)

        ### department menu
        createOptionMenu('科系名稱', controller.prop_department)

        ### degree menu
        createOptionMenu('等級別', controller.prop_degree)

        ### chart button
        def showChart(dataFrame, chartType: str, columnX: str, columnY: str):
            dataArrX = columnX #dataFrame[columnX] #need to be modified
            dataArrY = columnY #dataFrame[columnY]
            if chartType == AppConstants.CHART_BAR:
                plt.bar(dataArrX, dataArrY)
            elif chartType == AppConstants.CHART_PIE:
                plt.pie(dataArrY, labels = dataArrX)
            elif chartType == AppConstants.CHART_LINE:
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
        btn_showChart.pack()


class ReportPanel(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent) 
        self.pack(fill='both', expand=True) # 填滿全部
        self.createWidgets(parent, controller) # 布置組件內容

    def createWidgets(self, parent, controller):  
        print('ReportPanel:', controller.prop_school.get())
        report = Table(self, dataframe=controller.filterData(), showstatusbar=True) 
        report.show()

