import numpy as np
import pandas as pd

__all__ = ["getNumMat", "sacleMat", "wightMat", "getIdeals", "getDistance", "getIndex", "topsis"]

# 获取指标体系，构建评价矩阵
def getNumMat(data):
    '''
    【参数详解】\n
    data：需要评价的原始数据，pandas.dataframe对象\n
    【返回值详解】\n
    A：评价矩阵，numpy.array对象\n
    '''
    A = np.array(data)
    return A

# 无量纲化评价矩阵
def scaleMat(A):
    '''
    【参数详解】\n
    A：评价矩阵\n
    【返回值详解】\n
    B：无量纲化评价矩阵\n
    '''
    B = np.zeros(A.shape)
    for i in range(0, A.shape[1]):
        B[:,i] = A[:,i]/np.linalg.norm(A[:,i])
    return B

# 构造加权评价矩阵
def wightMat(B, w):
    '''
    【参数详解】\n
    B：无量纲化评价矩阵\n
    w：权重向量\n
    【返回值详解】\n
    C：加权评价矩阵\n
    '''
    w = np.array(w)
    C = B * w.T
    return C

# 确定正理想解和负理想解
def getIdeals(C, targets):
    '''
    【参数详情：】\n
    C：加权评价矩阵\n
    targets：目标约束向量，对应长度为评价矩阵的列数，如第一列为效益型指标，则目标约束向量第一个值为1，
    若为成本型指标，则为0，例如targets=[1,1,0]代表前两个指标为效益型指标，第三个指标为成本型指标\n
    【返回值详情：】\n
    best_solution：正理想解\n
    worsst_solution：负理想解\n
    '''
    def getBest(data, target):
        if target == 0:
            return data.min()
        elif target == 1:
            return data.max()
        else:
            return "参数异常"

    def getWorst(data, target):
        if target == 0:
            return data.max()
        elif target == 1:
            return data.min()
        else:
            return "参数异常"

    if C.shape[1] == len(targets):
        bs = np.zeros(len(targets))
        ws = np.zeros(len(targets))
        for i in range(0, len(targets)):
            bs[i] = getBest(C[:,i], target=targets[i])
            ws[i] = getWorst(C[:,i], target=targets[i])
        return bs,ws
    else:
        return "数据异常"

# 计算每个评价对象到正负理想解的距离
def getDistance(C, best_solution, worst_solution):
    '''
    【参数详情：】\n
    C：加权评价矩阵\n
    best_solution：正理想解\n
    worst_solution：负理想解\n
    【返回值详情：】\n
    dmax：各评价对象到正理想解的距离\n
    dmin：各评价对象到负理想解的距离\n
    '''
    dmax = np.zeros(C.shape[0])
    dmin = np.zeros(C.shape[0])
    for i in range(0, C.shape[0]):
        dmax[i] = np.sqrt(np.sum((C[i,:]-best_solution)**2))
        dmin[i] = np.sqrt(np.sum((C[i,:]-worst_solution)**2))
    return dmax, dmin

# 计算综合评价指数
def getIndex(dmax, dmin):
    '''
    【参数详解】\n
    dmax：各评价对象到正理想解的距离\n
    dmin：各评价对象到负理想解的距离\n
    【返回值详解】\n
    index：各评价对象的综合评价指数\n
    '''
    return dmin/(dmin + dmax)

# 主函数
def topsis(data, targets, w=None):
    '''
    【参数详解】
    data：需要评价的原始数据，pandas.dataframe对象\n
    targets：目标约束向量，对应长度为评价矩阵的列数，如第一列为效益型指标，则目标约束向量第一个值为1，
    若为成本型指标，则为0，例如targets=[1,1,0]代表前两个指标为效益型指标，第三个指标为成本型指标\n
    w：权重向量\n
    【返回值详解】
    result：返回结果，即每个评价对象的综合评价指数
    '''
    if w==None:
        w = np.ones(np.array(data).shape[1])
    else:
        A = getNumMat(data)
        B = scaleMat(A)
        C = wightMat(B, w)
        bs, ws = getIdeals(C, targets)
        dmax, dmin = getDistance(C, best_solution=bs, worst_solution=ws)
        index = getIndex(dmax, dmin)
    result = pd.DataFrame(index.T,index=data.index)
    return result