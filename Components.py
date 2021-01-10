# 林宥如 507170055
# -*- coding: utf-8 -*-

import tkinter # 介面化套件
import pandas # 資料處理套件
import matplotlib.pyplot as plt # 圖表套件
from pandastable import Table # 表格套件
import constants

### plot - font setting (顯示中文)
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
        
        ### title
        title = tkinter.Label(self, text='===== Groupby =====') # 建立label
        title.grid(row=0, column=0, padx=20, pady=5) # 佈件

        ### checkbox (for groupby)
        createCheckButton(1, '學校名稱', parent.prop_grouby[0])
        createCheckButton(2, '科系名稱', parent.prop_grouby[1])
        createCheckButton(3, '學位', parent.prop_grouby[2])

        
class FilterPanel(tkinter.Frame):   
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent) # 建立框架
        self.pack(fill='x') # 自動填滿左右(x方向)
        # self.grid(row=1, sticky='n')
        self.display(parent)

    def display(self, parent):   
        def createOptionMenu(rowId: int, columnName: str, selection: tkinter.StringVar): # rowId為佈件需求
            noColumn = columnName not in parent.prop_currentData_columns_str.get() # 判斷欄位是否在目前資料中
            optionsList = ['-'] if noColumn else parent.prop_currentData[columnName].unique().tolist() # pandas找出特定欄位中所有不重複的值 (為numpy.ndarray，再轉為串列)  
            optionsList.insert(0, constants.SELECTION_ALL) # 加入'全部'之選項
            
            if len(selection.get()) == 0:
                selection.set(optionsList[0]) # 預設選項一  

            optionMenu = tkinter.OptionMenu(self, selection, *optionsList)

            if noColumn: # 若目前資料沒有此欄位的話禁止點選              
                optionMenu.configure(state='disabled')

            optionLabel = tkinter.Label(self, text=columnName) # 建立label
            optionLabel.grid(row=rowId, column=0, padx=0, pady=5) # 佈件
            optionMenu.grid(row=rowId, column=1, padx=0, pady=5) 

        ### title
        title = tkinter.Label(self, text='===== Filter =====') # 建立label
        title.grid(row=0, column=0, padx=20, pady=10) # 佈件

        ### option menu
        createOptionMenu(1, '學校名稱', parent.prop_school)
        createOptionMenu(2, '科系名稱', parent.prop_department)
        createOptionMenu(3, '學位', parent.prop_degree)

        ### chart button
        def showChart(chartType: str = constants.CHART_BAR):
            data = parent.prop_currentData.copy()
            dataColumns = parent.prop_currentData.columns.values.tolist()
            hasGroupby = len(parent.getGroupbyList()) > 0
            filterDict = {
                '學校名稱': parent.prop_school.get(),
                '科系名稱': parent.prop_department.get(),
                '學位': parent.prop_degree.get()
            }
            filterList = list(filterDict.values())

            def plotChart(dataArrX, columnY_list, labels):
                for i, y in enumerate(columnY_list):
                    if chartType == constants.CHART_BAR:
                        plt.bar(dataArrX, y, label=labels[i])
                    elif chartType == constants.CHART_LINE:
                        plt.plot(dataArrX, y, label=labels[i])
                    # elif chartType == constants.CHART_PIE:
                    #     plt.pie(dataArrY, labels = dataArrX)

            ## 判斷圖表之x,y欄位
            if hasGroupby == False and filterList.count(constants.SELECTION_ALL) == len(filterList): # 無任何篩選 --> # 總就學人數
                columnX = '全學年'
                plotChart(['全學年'], [data['總計'].sum(), data['男生計'].sum(), data['女生計'].sum()], ['總計', '男生計', '女生計'])
            else:
                if hasGroupby and filterList.count(constants.SELECTION_ALL) == len(filterList): # 只有groupby --> 選擇第一欄  

                    if dataColumns[0] == '學校代碼':
                        columnX = '學校名稱'
                    else:
                        columnX = dataColumns[0]  

                elif hasGroupby == False: # 只有filter --> 找出其他選擇'全部'的欄位 作為 x軸資料，三個filter都下的話就選總計前一個

                    if constants.SELECTION_ALL not in filterList:
                        columnX = dataColumns[dataColumns.index('總計') - 1]
                    else:
                        index = filterList.index(constants.SELECTION_ALL)
                        columnX = list(filterDict.keys())[index]

                else: 
                    columnX = dataColumns[dataColumns.index('總計') - 1]

                plotChart(data[columnX], [data['總計'], data['男生計'], data['女生計']], ['總計', '男生計', '女生計'])          
           

                # if chartType == constants.CHART_BAR:
                #     plt.bar(dataArrX, data['總計'], label='總計')
                #     plt.bar(dataArrX, data['男生計'], label='男生計')
                #     plt.bar(dataArrX, data['女生計'], label='女生計')
                # elif chartType == constants.CHART_LINE:
                #     plt.plot(dataArrX, data['總計'], label='總計')
                #     plt.plot(dataArrX, data['男生計'], label='男生計')
                #     plt.plot(dataArrX, data['女生計'], label='女生計')
                # elif chartType == constants.CHART_PIE:
                #     plt.pie(dataArrY, labels = dataArrX)

            
            
            plt.ylabel("人數")
            plt.xlabel(columnX)
            plt.title("Chart")
            plt.legend(loc = 'best')
            plt.show()

        btn_showChart = tkinter.Button(self, text='Bar Chart', command=lambda: showChart(constants.CHART_BAR)) # lambda: showChart(constants.CHART_BAR)
        btn_showChart.grid(row=6, column=0, padx=20, pady=20)
        btn_showChart = tkinter.Button(self, text='Line Chart', command=lambda: showChart(constants.CHART_LINE))
        btn_showChart.grid(row=6, column=1, padx=20, pady=20)


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
