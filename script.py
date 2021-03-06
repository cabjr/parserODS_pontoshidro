import sys
import os
import numpy as np
import json
from pandas_ods_reader import read_ods
import numpy as np
from pyexcel_ods import save_data
from collections import OrderedDict


def iterate_over_matrix(listM):
    #each item is a matrix / group of data
    resultM = []
    for item in listM:
        newM = []
        for i in range(len(item)):
            if i == 1 or i ==0:
                aux = [item[i][0], item[i][1], np.nan, np.nan]
                newM.append(aux) 
            elif i >= 2 and i+1 < len(item) and (item[i+1][1] != None and item[i+1][1] != np.nan) and (item[i][0] != None and item[i][1] != np.nan):
                aux = [(item[i][0]), (item[i][1]), (((item[i+1][1] - item[i-1][1])/2)*item[i][0]), (item[0][1] * (((item[i+1][1] - item[i-1][1])/2)*item[i][0]))]
                newM.append(aux)
        media = np.mean([item[i][0] for i in range (len(newM)) if i != 0 and item[i][0] != None])
        maxLarg = max([item[i][1] for i in range (len(newM)) if i != 0])
        area = (maxLarg*media*item[0][1])
        newM.append([media,maxLarg,area,np.nan])
        resultM.append(newM)
    return resultM
        
def generate_odsFile(matrix):
    data = OrderedDict()
    for item in range(len(matrix)):
        lastAux = np.array(matrix[item])
        newList = lastAux.tolist()
        nl = []
        for i in range(len(newList)):
            el= []
            for j in range(len(newList[i])):
                if type(newList[i][j]) is str:
                    el.append(newList[i][j].replace('.',',').replace('nan',''))
            nl.append(el)
        data.update({matrix[item][0][0]: nl })
    save_data("resultado.ods", data)        

## profundidade, largura, área, vazão (veloc * area) 
## somas
## média profundida, máximo largura


def generate_csv(matrix):
    csvText = ''
    for item in range(len(matrix)):
        lastAux = np.array(matrix[item])
        newList = lastAux.tolist()
        for i in range(len(newList)):
            for j in range(len(newList[i])):
                if i == len(newList):
                    csvText += newList[i][j].replace('.',',').replace('nan','')
                else:
                    csvText += newList[i][j].replace('.',',').replace('nan','') + ';'
            csvText+= '\n'
        csvText+= ';;;\n'
    file1 = open("resultados.csv","w") 
    file1.write(csvText)
    file1.close() 
    print(csvText)

if (len(sys.argv)==0 or len(sys.argv)==1):
    print('Favor Inserir o nome do arquivo a ser processado')
elif (len(sys.argv)==2):
    pedido = read_ods(sys.argv[1], 1, columns=["profundidade", "largura", "area"], headers=False)
    matrixes = []
    aux = []
    for i in range(len(pedido['profundidade'])):
        if 'PY-' in str(pedido['profundidade'][i]) or '-' in str(pedido['profundidade'][i]):
            if (len(aux)>0):
                matrixes.append(aux)
                aux = []
        aux.append([pedido['profundidade'][i], pedido['largura'][i], pedido['area'][i]])
    matrixes.append(aux)
    print(matrixes)
    #generate_odsFile(iterate_over_matrix(matrixes))
    generate_csv(iterate_over_matrix(matrixes))
    print('Arquivo resultado.ods gerado com sucesso.')