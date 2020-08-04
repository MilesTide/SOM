# -*- coding: utf-8 -*-
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import csv
import heapq

# 向量归一化，转化为对应单位向量，这样计算欧几里得距离就
# 可以转化为计算向量的点积（二维平面中，单位向量点积就是
# cos theta），点积越大距离越近
def normalize(vector):
    if np.linalg.norm(vector)==0:
        return vector
    else:
        return vector / np.linalg.norm(vector)

class Som:
    def initialize(self, model, dimension):
        self.nodes = []
        # 初始化节点，这里是方格的大小，由两层for循环控制
        for i in range(model[0]):
            temp = []#控制每一层的权值向量
            for j in range(model[1]): #randn函数返回一个或一组样本，具有标准正态分布。
                vector = np.random.randn(dimension)  # 每个节点都包含一个维度和输入向量维度相同的向量
                vector = normalize(vector)  # 归一化,将变量变为[0,1]之间的数
                temp.append(vector)
            self.nodes.append(temp) #两次append变为[[,],[,]]的形式
        self.model = model  # 便于遍历节点

    def best_matching_unit(self, vector):#批次最佳匹配单元
        result = [0, 0]  # 返回优胜节点坐标
        max = -10000
        for i in range(self.model[0]):#还是用方格网络来控制循环，遍历整个方格网络
            for j in range(self.model[1]):
                temp = self.nodes[i][j].dot(vector)#.dot,得到内积即欧式距离,即权值和真实值之间的距离，内积越大，说明两者之间越相似
                if temp > max:
                    max = temp
                    result[0], result[1] = i, j#优胜结点的坐标
        return result #返回优胜结点

    def get_r_p(self, N):  # 根据距离优胜节点的距离变化的值
        return 1.0 / math.exp(N)

    def neighbor(self, pos, table):#pos指优胜结点的位置坐标，table是需要调整的布尔表
        result = []
        x = pos[0]#优胜结点的行列坐标分别为x,y
        y = pos[1]
        #调整根据距离依次向外扩散，一个优胜结点返回上下左右四个邻居
        if x - 1 >= 0: #向左调整
            if not table[x - 1][y]: #table[][]中的值为true或false，如果为false说明需要调整，true说明不用调整
                result.append([x - 1, y])#如果没有调整过，那么将坐标添加到result列表中
                table[x - 1][y] = True#将此坐标的改为调整过，即true
        if x + 1 < self.model[0]: #向右调整
            if not table[x + 1][y]:
                result.append([x + 1, y])
                table[x + 1][y] = True
        if y - 1 >= 0: #向上调整
            if not table[x][y - 1]:
                result.append([x, y - 1])
                table[x][y - 1] = True
        if y + 1 < self.model[1]:  #向下调整
            if not table[x][y + 1]:
                result.append([x, y + 1])
                table[x][y + 1] = True
        return result  #返回需要调整的坐标值

    def get_neighbor(self, BMU, r):  # 获取邻居节点，返回值为[[距离为1坐标集合..], [距离为2坐标集合..], [...], ...]
        result = []
        if r > 0: #如果调整的半径大于0
            table = []  # 记录已经存入的结点
            for i in range(self.model[0]):#model[0],代表的是维度的大小
                table.append([False] * self.model[1])#将table赋model[0]*model[1]个大小的False值,和网络网格大小相同
            table[BMU[0]][BMU[1]] = True #优胜结点的坐标记为true
            # print("table=", table)
            neighbors = self.neighbor(BMU, table);  # 距离为1的节点，周围的四个邻居
            result.append(neighbors)#result内为[[,],[,],[,]]的结构
            for i in range(r - 1):#因为r=3，所以这里是返回邻居距离为2的点
                temp = []
                for x in neighbors:#根据距离为1的邻居，向外扩充一圈，找到距离为2的邻居，由于内圈的值都是true，可以用这避免重复
                    temp += self.neighbor(x, table)
                neighbors = temp  # 距离为2+i的结点
                result.append(neighbors)
        return result

    def update_nodes(self, BMU, example, r, eta):  # 参数：优胜节点坐标，输入向量，优胜领域半径，学习率
        # print("r, eta=", r, eta)
        # print("before update=", self.nodes)
        w = self.nodes[BMU[0]][BMU[1]]#找到获胜的权值向量
        w += eta * self.get_r_p(0) * (example - w)  # 更新优胜节点，向真实向量靠近
        self.nodes[BMU[0]][BMU[1]] = normalize(w)#更新结点，归一化后
        neighbors = self.get_neighbor(BMU, r);#取得获胜结点的邻居，即周围应该调整的结点
        # print("neighbors=", neighbors)
        for i in range(len(neighbors)): #neighbors中有距离为1和2的邻居,i取值总长度
            for pos in neighbors[i]:  # 依次更新节点
                w = self.nodes[pos[0]][pos[1]]
                w += eta * self.get_r_p(i + 1) * (example - w)
                self.nodes[pos[0]][pos[1]] = normalize(w)

        # print("after update=", self.nodes)

    def eta(self, t):  # 参数：当前迭代次数，隐含参数：最大迭代次数，学习率初始值
        if t <= self.MAX_ITERATION / 10:  # 前1/10次迭代学习率线性下降到1/20
            return self.init_eta - t * self.k1
        else:  # 后9/10次迭代学习率线性下降到0
            return self.init_eta / 20 - (t - self.MAX_ITERATION / 10) * self.k2

    def get_r(self, t):  # 优胜邻域随着迭代次数变小
        return int(self.init_r * (1 - t / self.MAX_ITERATION))  # 向下取整

    def train(self, get_batch, MAX_ITERATION, init_eta, MIN_ETA,
              init_r):  # 参数：获取每次迭代所需样本的函数，最大迭代次数，学习率初始值，最小学习率，优胜领域初始值
        self.MAX_ITERATION = MAX_ITERATION
        self.init_eta = init_eta  # 学习率初始值
        #学习率的下降斜率分为两个阶段，前期调整比较大，到后期调整越来越小
        self.k1 = (19 / 20 * self.init_eta) / (1 / 10 * self.MAX_ITERATION)  # 学习率线性下降斜率1，大1/1000
        self.k2 = (1 / 20 * self.init_eta) / (9 / 10 * self.MAX_ITERATION)  # 学习率线性下降斜率2，小1/10000
        self.init_r = init_r
        count = 0
        while count < MAX_ITERATION and self.eta(count) > MIN_ETA:
            batch = get_batch()
            # print(">>>>>>>>>>>>>>>>>count=", count)
            # print("batch=", batch)
            for example in batch:
                # print("example=", example)
                BMU = self.best_matching_unit(example)#找到和每个真实向量相近的权值向量（可能多个真实向量对应同一个权值向量）
                # print("BMU=",BMU)
                self.update_nodes(BMU, example, self.get_r(count), self.eta(count))
            count = count + 1
        print("迭代次数：", count)
        print("最终学习率：", self.eta(count))

    def mapping(self, vector):
        vector = normalize(vector)
        return self.best_matching_unit(vector)  # 返回优胜节点坐标

#这里是数据的位置
way = 'F:\DayCandles2017-201807\ExtractData.csv'
data1 = pd.DataFrame(pd.read_csv(way,header=None))
temp = np.array(data1)
data2 =[]
for i in range(len(data1)):
    data2.extend([[temp[i][3], temp[i][4], temp[i][5]]])
data = data2
#print(data2)
#data=[[1,0,1,1,0,1],[1,0,0,1,1,1],[1,1,1,1,1,1],[0,0,0,0,1,1],[0,1,1,0,1,1],[1,0,1,0,1,0],[1,0,1,1,0,1]]
features = np.array(list(map(normalize, data)))  # 归一化，这里相当于将data中的每一条数据依次放到normalize函数中

def full_batch():#batch，分批处理，返回分批处理的结果
    return features

som = Som()
som.initialize([1, 3], 3)#需要调整，这里代表方格网络大小，以及特征个数，网格大小代表需要分的类别数，比如1000条数据分成6类，网格大小就是[3,2]

def entrance():
    csvFile = "F:\DayCandles2017-201807\FirstCluster.csv"
    result = list(map(som.mapping, features))#标准化后的数据对应的权值向量的坐标，权值向量坐标最多100个,result长度为总数据的长度
    count_pos = {}
    for pos in result:
        if result.count(pos) >= 1:
            #print(result.count(pos))
            count_pos[str(pos[0]) + ',' + str(pos[1])] = result.count(pos) #count_pos记录每个坐标出现的次数
    # lambda匿名函数,只执行一次，x是一个数组
    x = np.array(list(map(lambda x: x[0], result))) #取出result的横坐标，即每个result[0],括号里的x就代表result
    y = np.array(list(map(lambda x: x[1], result))) #取出result的纵坐标,即每个result[1]
    size = np.array(list(map(lambda x: count_pos[str(x[0]) + ',' + str(x[1])], result)))
    dif = list(set(size))
    dif =heapq.nlargest(5,dif)
    #print(dif)
    color = np.arctan2(y, x)
    plt.scatter(x, y, s=size, c=color, alpha=0.6, marker=',')
    #print(len(x))
    for i in range(len(x)):  # 打上标签
        plt.annotate(str(count_pos[str(x[i]) + ',' + str(y[i])]), xy=(x[i], y[i]), xytext=(x[i] + 0.1, y[i] + 0.1))
        #plt.annotate(str(size[i]), xy=(x[i], y[i]), xytext=(x[i] + 0.1, y[i] + 0.1))
        #print(data[i])
        #for j in range(len(dif)):
        #if dif[j]-size[i]==0:
        with open(csvFile, 'a', newline='') as f:  # 条件满足，记录数据
            text = [temp[i][0],temp[i][1], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8],temp[i][2],size[i],[x[i],y[i]]]
            csv.writer(f).writerow(text)
        f.close()

    plt.show()


#print("数据",features)
som.train(full_batch, 10000, 0.8, 0.05, 10)# 参数：获取每次迭代所需样本的函数，最大迭代次数，学习率初始值，最小学习率，优胜领域初始值
entrance()