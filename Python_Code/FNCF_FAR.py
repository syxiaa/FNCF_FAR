# 2021-07-22 22:11:04
# CXX
# 《A Fast Neighborhood Calculation Framework》
import time
import copy
import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import MinMaxScaler


def FNCF_FAR():
    """
     The algorithm program is based on the idea of sorting to accelerate farnemf,
    the specific content of reference paper.
    :return:Row：Attribute reduction results, pos_num:Number of positive fields
    """

    label = U[:, -1]#labels list
    pos = []
    T_len = 0
    R_Dic = []
    R_pos = []
    arr = [i for i in range(0, numberAttribute - 1)]
    Row = []
    re_arr = 0#Currently, the attributes with the most positive fields
    pos_num = 0#Number of positive fields

    for i in range(0, numberAttribute - 1):
        #Loop through attribute columns
        cmk_chk = U[:, i]
        chk_Sort = sort_U[:, i]
        l = r = 0
        rest = []
        dist=[]
        temp_len = 0
        temp_pos = []
        for xj in chk_Sort:
            loaXj = cmk_chk[xj]
            while l < r and cmk_chk[chk_Sort[l]] - loaXj < -sigema:
                l += 1
                rest.pop(0)
            while r < numberSample and cmk_chk[chk_Sort[r]] - loaXj <= sigema:
                rest.append(chk_Sort[r])
                r += 1
            tag1 = label[xj]
            tag2 = True
            for j in range(r - l):
                if label[rest[j]] != tag1:
                    tag2 = False
                    break
            if tag2:
                temp_pos.append(xj)
                temp_len += 1
        if temp_len > T_len:
            re_arr = i
            T_len = temp_len
            pos = temp_pos

    R_pos = list(sort_U[:, re_arr])
    if T_len:
        #when T_len>0, and we add the first attribute to the Row.
        arr.remove(re_arr)
        Row.append(re_arr)
        chk_Sort2 = R_pos.copy()
        cl = 0
        pos_num += len(pos)
        for t in range(numberSample):
            if chk_Sort2[t] in pos:
                pos.remove(R_pos[t - cl])
                R_pos.pop(t - cl)
                cl += 1
        l = r = 0
        cmk_chk = U[:, re_arr]
        rest = []
        re_len = len(R_pos)
        for xj in R_pos:
            loaXj = cmk_chk[xj]
            while l < r and cmk_chk[R_pos[l]] - loaXj < -sigema:
                l += 1
                rest.pop(0)
            for w in range(r, re_len):
                d = cmk_chk[R_pos[r]] - loaXj
                if d <= sigema:
                    r += 1
                    rest.append(R_pos[w])
                else:
                    break
            rest1 = copy.deepcopy(rest)
            R_Dic.append(rest1)

    else:
        return Row, pos_num
    while len(R_Dic) > 0:
        #when the positive more than 0
        pos = []
        Tr_len = 0
        re_arr = -1
        for i in arr:
            T_len = 0
            T_pos = []
            new_arr = U[:, [i, -1]]
            for j in range(len(R_pos)):
                loaXj = new_arr[R_pos[j], 0]
                lolab = label[R_pos[j]]
                flag = True
                for k in R_Dic[j]:
                    if new_arr[k][1] != lolab and np.abs(new_arr[k][0] - loaXj) <= sigema:
                        flag = False
                        break
                if flag:
                    T_pos.append(R_pos[j])
                    T_len += 1
            if T_len > Tr_len:
                Tr_len = T_len
                pos = copy.deepcopy(T_pos)
                re_arr = i
        if Tr_len > 0:
            #remove the positive sample points
            li = 0
            pos_num += len(pos)
            arr.remove(re_arr)
            Row.append(re_arr)
            for i in range(len(R_pos)):
                if R_pos[i - li] in pos:
                    R_Dic.pop(i - li)
                    R_pos.pop(i - li)
                    li += 1
            UDate = U[:, re_arr]
            tr = 0
            for r in R_Dic:
                lr = 0
                lo = UDate[R_pos[tr]]
                tr += 1
                for j in range(len(r)):
                    if r[j - lr] in pos or np.abs(UDate[r[j - lr]] - lo) > sigema:
                        r.pop(j - lr)
                        lr += 1
        else:
            return Row, pos_num
    return Row, pos_num


if __name__ == '__main__':
    dataa = ['LEUKEMIA'] # the dataset
    with open(r"F:\py\Python\result.csv", "w", newline='', encoding="utf-8") as jg:
        writ = csv.writer(jg)
        for k in range(len(dataa)):
            # start = time.process_time()
            df = pd.read_csv("F:\\py\\UCI\\" + dataa[k] + ".csv", header=None)
            data = df.values
            writ.writerow([dataa[k], str(data.shape)])
            numberSample, numberAttribute = data.shape
            writ.writerow(["δ", "S_Reduct", "SFARNEMF", "FARNEMF", "SFARNEMF"])
            minMax = MinMaxScaler()  # Normalize the data
            U = np.hstack((minMax.fit_transform(data[:, 1:]), data[:, 0].reshape(numberSample, 1)))
            C = list(np.arange(0, numberAttribute - 1))  # condition attribute
            D = list(set(U[:, -1]))  # decision attribute
            index = np.array(range(0, numberSample)).reshape(numberSample, 1)  # index
            sort_U = np.argsort(U[:, 0:-1], axis=0)
            U1 = np.hstack((U, index))  # add index to the dataset
            time1 = time2 = 0
            for i in range(1, 51):
                sigema = 0.01 * i
                print("sigima", sigema)
                F_posnum = R_posnum = 0
                start2 = time.process_time()
                Row, R_posnum = FNCF_FAR()
                end2 = time.process_time()
                R_time = end2 - start2
                print("ROW", Row)
                writ.writerow([sigema, Row,  R_time, R_posnum, F_posnum])
            writ.writerow([" "])


