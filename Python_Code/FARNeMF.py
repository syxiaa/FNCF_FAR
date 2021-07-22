# 2020-07-17 22:11:04
# CXX
# 《Fast symbolic and numerical attribute reduction algorithm based on neighborhood rough set》
import time

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def FARNeMF():   # Fast forward attribute reduction algorithm based on classical rough set
    # Step 1:  normalize red=∅
    # start1=time.process_time()
    red = [-1, -2]  # The last column is the line number; Second to last column, label
    smp_chk = U  # The boundary domain is initially the domain of argument
    C_red = list(C)
    # Step 2:
    while smp_chk.shape[0]:  # Loop until the boundary domain is empty
        temp_POS = []
        temp_ROW = []
        temp_k = 0
        for k in C_red:
            attribute = list(red)
            attribute.append(k)
            DT = U[:, attribute]
            POS = []
            ROW = []
            for x in smp_chk[:, -1]:
                if get_neighborhood(int(x), DT):  # If the current point is a positive field
                    POS.append(int(x))
                    ROW.append(np.where(smp_chk[:, -1] == x)[0])
            if len(temp_POS) < len(POS):
                temp_POS = list(POS)
                temp_ROW = list(ROW)
                temp_k = k
        if temp_POS:  # If the largest positive field is not empty, the corresponding attribute K is added to the reduction
            red.append(temp_k)
            C_red.remove(temp_k)
            smp_chk = np.delete(smp_chk, temp_ROW, axis=0)

        else:
            del red[0]
            del red[0]
            return red
    del red[0]
    del red[0]
    return red


def get_neighborhood(x, DT):  # If the calculation field is a positive field, return true; otherwise, return false. The judgment of positive field is different
    Mul_Array = DT[list(np.where(DT[:, 1] != DT[x, 1])[0]), :]
    rlen = len(DT[0])
    loxj = DT[x][2:rlen]
    min1=np.sqrt(np.sum(np.square(Mul_Array[0][2:rlen]-loxj)))
    for k in range(1,len(Mul_Array)):
        tlen=np.sqrt(np.sum(np.square(Mul_Array[k][2:rlen]-loxj)))
        if tlen<min1:
            min1=tlen
    if min1<sigema:
        return False
    else:
        return True
if __name__ == '__main__':

    dataa = ["german"]
    for k in range(len(dataa)):
        start = time.process_time()
        df = pd.read_csv("D:\py\\UCI\\" + dataa[k] + ".csv", header=None)
        data = df.values
        data=data[:50,:]
        numberSample, numberAttribute = data.shape
        print("datasetname：",dataa[k])
        print("shape",data.shape)
        minMax = MinMaxScaler()  # Normalize the data
        U = np.hstack((minMax.fit_transform(data[:, 1:]), data[:, 0].reshape(numberSample, 1)))
        C = list(np.arange(0, numberAttribute - 1))
        D = list(set(U[:, -1]))
        index = np.array(range(0, numberSample)).reshape(numberSample, 1)
        U = np.hstack((U, index))
        for i in range(1, 2):
            sigema = 0.16*i
            start1=time.process_time()
            red= FARNeMF()
            print("red:",red)
            end1=time.process_time()
            print("sigama:",sigema, " ", red,"time：",end1-start1)
        end = time.process_time()
        print("total_time:", end - start)
        print("\n")


