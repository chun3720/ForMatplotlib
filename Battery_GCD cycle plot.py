# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:06:16 2021
last update : Feb 15 2022
@author: jycheon
"""
from loadexp import *
import pandas as pd
import os
import string
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
# plt.style.use(['science', 'grid'])
plt.style.use(['science', 'no-latex'])
year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022\\"

class LIB_tot(Dataloads):  
    # df_list = []
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        # (self.name, self.ext) = self.file.split('.')
        self.data = pd.read_excel(self.file_path, sheet_name = '데이터_1_1', index_col = 0) 
        self.data.columns = ["cycle number", "Capacity (Ah/g)"]
        # self.X, self.Y = self.data.columns[0]
        self.x, self.y  = self.data.columns
        self.X = self.data[self.x]
        self.Y = self.data[self.y]

    def __str__(self):
        self.label = self.name.replace("_", "-")
        return self.label
    
    def cycle_plot(self, k = 3):
        # columns = list(self.data.columns)
        # self.X, self.Y = self.data[columns[0]], self.data[columns[1]]
        plt.plot(self.X , self.Y, 'o', label = LIB_tot.__str__(self))
        # plt.title(self.name + " with cycle", fontsize = 9)
        plt.xlabel("Cycle nunmber")
        plt.xticks(np.arange(0, max(x)+1, k))
        # plt.yticks(np.arange(0, max(y)*1.1))
        plt.ylabel("Specific Capacity ($Ah/g$)")
        
        # plt.show()
        
        
def get_export(exp, path, check = 'n', convertor = 'n'):
    output_path = f'{path}output\\'
    
    if not os.path.exists(output_path):
        os.mkdir(output_path) 

    if check == 'y':
        
        with pd.ExcelWriter(f'{output_path}Cycle_tot.xlsx') as writer:

            for i, cy in enumerate(exp):
                
                df = cy.data[:]
                df["Capacity (Ah/g)"] *= 1000
                # df["Capacity (Ah/g)"] = df["Capacity (Ah/g)"].apply(lambda x: x*1000)
                df.columns = ["mAh/g", cy.name]
                plt.plot(df[df.columns[0]], df[df.columns[1]],'o', label = cy.name)
                df.to_excel(writer, startcol = 2*i, index = False)
            leg = plt.legend(fontsize = 'xx-small')
            for line, text in zip(leg.get_lines(), leg.get_texts()):
                text.set_color(line.get_color())
            plt.xlabel("Cycle nunmber")
            plt.ylabel("Specific Capacity ($mAh/g$)")
            plt.show()
        
        if convertor != 'n':
            
            with pd.ExcelWriter(f'{output_path}Cycle_recalculation.xlsx') as writer:

                for i, cy in enumerate(exp):
                    
                    quest = input(f"type conversion factor for '{cy.file}' (make sure it means denominator): ")
                    basis = float(quest)
                    df1 = cy.data[:]
                    # df1["Capacity (Ah/g)"] *= 1000
                    df1["Capacity (Ah/g)"] /= basis
                    df1.columns = ["mAh/g(active)", cy.name]
                    plt.plot(df1[df1.columns[0]], df1[df1.columns[1]], 'o', label = cy.name)
                    df1.to_excel(writer, startcol = 2*i, index = False)
                leg = plt.legend(fontsize = 'xx-small')
                for line, text in zip(leg.get_lines(), leg.get_texts()):
                    text.set_color(line.get_color())
                plt.title("recalculation")
                plt.xlabel("Cycle nunmber")
                plt.ylabel("Specific Capacity ($mAh/g$)")
                plt.show()
        
    else:
        with pd.ExcelWriter(f'{output_path}Cycle_tot.xlsx') as writer:
    
            for i, cy in enumerate(exp):
                cy.data.rename(columns = {"cycle number": "Ah/g", "Capacity (Ah/g)": cy.name}).to_excel(writer, startcol = 2*i, index = False)
                
                # df = cy.data[:]
                # df.columns = ["Ah/g", cy.name]
                # df.to_excel(writer, startcol = 2*i, index = False)
                
                
        if convertor != 'n':
            # basis = float(convertor)/100
            with pd.ExcelWriter(f'{output_path}Cycle_recalculation.xlsx') as writer:

                for i, cy in enumerate(exp):
                    quest = input(f"type conversion factor for '{cy.file}' (make sure it means denominator): ")
                    basis = float(quest)
                    df = cy.data[:]
                    df["Capacity (Ah/g)"] /= basis
                    df.columns = ["Ah/g", cy.name]
                    plt.plot(df[df.columns[0]], df[df.columns[1]], 'o', label = cy.name)
                    df.to_excel(writer, startcol = 2*i, index = False)
                    
                leg = plt.legend(fontsize = 'xx-small')
                for line, text in zip(leg.get_lines(), leg.get_texts()):
                    text.set_color(line.get_color())
                plt.title("recalculation")
                plt.xlabel("Cycle nunmber")
                plt.ylabel("Specific Capacity ($Ah/g$)")
                plt.show()
                    
    return output_path
    

def cycle_sns(exp_obj):
    
    plt.figure(figsize = (3, 2.5))
    for exp in exp_obj:
        x = exp.data.columns[0]
        y = exp.data.columns[1]
        sns.scatterplot(x = x, y = y, data = exp.data)
        

def cycle_plt(exp):
    
    # for i in range(len(exp)):
    for ex in exp:
        name = ex.name.replace("_", "-")
        plt.plot(ex.X, ex.Y, 'o', label = name)
        # exp[i].cycle_plot(k)
    
    leg = plt.legend(fontsize = 'xx-small')
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    
    plt.xlabel("Cycle nunmber")
    plt.ylabel("Specific Capacity ($Ah/g$)")
    plt.show()


raw, path, _, _ = fileloads(year_path, ".xlsx")
exp_data = build_data(path, raw, LIB_tot)

cycle_plt(exp_data)
# cycle_sns(exp_data)
check = input("convert to mAh/g? yes (y) or no(n) :")
convertor  = input("want to recalculate ? yes (y) or no(n) :")

out_path = get_export(exp_data, path, check, convertor)


