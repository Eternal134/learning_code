# @author: 吴振龙
# @student id：E51814014
# @date：2020-09-24

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# 用于计算c=1到9聚类过程的平均迭代次数
iteration_count = 0

class Iris_Cluster():
    """iris数据集的聚类分析类，创建对象时指定类别数C，调用iterator方法完成聚类"""
    def __init__(self, my_c):
        
        self.c = my_c
        self.iris_file_name = "iris.txt"
        self.original_datas = []
        self.clustered_datas = []
        self.centers = []
        self.clusters_distances = []
        self.J_value = 0
        
    def read_iris_datas(self):
        """从文件中读取iris数据集，保存到self.original_datas列表"""
        with open(self.iris_file_name) as file_object:
            file_text = file_object.read().split('\n')
            
        for data in file_text:
            t_data = tuple([float(i) for i in data.split(',')[:4]])
            self.original_datas.append(t_data)
        
    def simply_init(self):
        """确定初始类心，简单取前c个样本"""
        self.read_iris_datas()
        
        for cluster in self.original_datas[:self.c]:
            self.centers.append(cluster)
            
    def furthest_distance_init(self):
        """最远距离法确定初始类心"""
        self.read_iris_datas()
        self.centers.append(self.original_datas[0])
        for i in range(self.c - 1):
            # 第一重循环：选出c - 1个类心，因为类心0已经确定
            max_center_distance = 0
            for j in range(len(self.original_datas)):
                # 第二重循环：找出与当前所有类心距离之和最大的数据，作为第i个类心
                if self.original_datas[j] in self.centers:
                    continue
                total_d_between_other_centers = 0
                for centeri in self.centers:
                    total_d_between_other_centers += iris_Euclidean_distance(self.original_datas[j], centeri)
                if max_center_distance < total_d_between_other_centers:
                    index = j
                    max_center_distance = total_d_between_other_centers    
            self.centers.append(self.original_datas[index])        
            
    def update_center(self):
        """重新计算类心"""
        new_centers = [tuple(np.mean(np.array(i), axis = 0)) for i in self.clustered_datas]
        if sum([iris_Euclidean_distance(new_centers[i], self.centers[i]) for i in range(self.c)]) < 0.5:
            return False
        else:
            self.centers = new_centers
            return True
    
    def clustering(self):
        """聚类"""
        if self.c == 1:
            self.clustered_datas = [self.original_datas]
            return
        self.clustered_datas = [[] for i in range(self.c)]
        for data in self.original_datas:
            min_distance = -1
            min_center = 0
            for i in range(self.c):
                d = iris_Euclidean_distance(data, self.centers[i])
                if min_distance < 0 or d < min_distance:
                    min_distance = d
                    min_center = i
            self.clustered_datas[min_center].append(data)
            
    def calculate_J_value(self):
        """计算J值"""
        self.clusters_distances.clear()
        for cluster, center in zip(self.clustered_datas, self.centers):
            d = 0
            for data in cluster:
                d += pow(iris_Euclidean_distance(data, center), 2)
            self.clusters_distances.append(d)
        self.J_value = sum(self.clusters_distances)
            
    def iterator(self):
        """迭代聚类"""
        self.furthest_distance_init()                # 最远距离法初始化类心
        # self.simply_init()                           # 简单法初始化类心
        self.clustering()                            # 初始聚类
        self.J_value = 0
        for i in range(10):
            # 重复迭代，重新计算类心、聚类
            if not self.update_center():
                break
            self.clustering()
            if self.c == 1:
                break
        self.calculate_J_value()
        global iteration_count
        iteration_count += i
        
    def wirte_to_flie(self):
        with open("iris_{}_cluster.txt".format(self.c), 'w') as f:
            for i in range(self.c):
                for data in self.clustered_datas[i]:
                    f.write(str(data) + "class" + str(i + 1) + '\n')
                    
    def draw_clustered_result(self):
        """聚类结果可视化，对于四维特征数据集iris，绘制四个三维图形，每个图形包括iris的三个特征"""
        fig = plt.figure(1)
        # ax = plt.axes(projection = '3d')
        # 准备绘制四个子图
        ax1 = fig.add_subplot(221, projection = '3d')
        ax2 = fig.add_subplot(222, projection = '3d')
        ax3 = fig.add_subplot(223, projection = '3d')
        ax4 = fig.add_subplot(224, projection = '3d')
        colors = ['r', 'b', 'g', 'pink', 'm', 'c', 'k', 'aqua', 'gold']             # 不同类使用不同颜色绘制散点图
        for cluster, color in zip(self.clustered_datas, colors):
            feature1, feature2, feature3, feature4 = list(zip(*cluster))            # 解包出同类中所有模式的每个特征
            ax1.scatter(feature1, feature2, feature3, s = 3, color = color)
            ax1.set_title('feature123', size = 10)
            ax2.scatter(feature1, feature2, feature4, s = 3, color = color)
            ax2.set_title('feature124', size = 10)
            ax3.scatter(feature1, feature3, feature4, s = 3, color = color)
            ax3.set_title('feature134', size = 10)
            ax4.scatter(feature2, feature3, feature4, s = 3, color = color)
            ax4.set_title('feature234', size = 10)
            for axi in [ax1, ax2, ax3, ax4]:
                axi.set_xticks([])
                axi.set_yticks([])
                axi.set_zticks([])
        
        plt.savefig('iris_{}_cluster.jpg'.format(self.c), dpi = 500)
        # plt.show()
        

def iris_Euclidean_distance(iris1, iris2):
    # 计算欧式距离
    iris = [iris1[i] - iris2[i] for i in range(len(iris1))]
    d = 0
    for i in range(len(iris1)):
        d = d + pow(iris[i], 2)
    return pow(d, 0.5)

def main():

    j_values = []
    for c in range(1, 10):
        # 聚类数从1到9，分别计算观察聚类结果
        iris_cluster = Iris_Cluster(c)              # 创建Iris_Cluster类
        iris_cluster.iterator()                     # 迭代聚类
        j_values.append(iris_cluster.J_value)       # 保存该c值下的J值
        if c == 2 or c == 3 or c == 6:                               
            # 根据得到的J_c曲线图观察到，c为2或3时聚类效果较好，保存c为2或3时的聚类结果文本和可视化图形
            # 再保存c为6时的聚类结果，以作对比分析
            iris_cluster.wirte_to_flie()
            iris_cluster.draw_clustered_result()
    print("average number of interation:\t{}".format(iteration_count / 9), end = '')
    # 绘制J-C散点图
    plt.figure()
    plt.scatter(range(1, 10), j_values, s = 3, color = 'black')
    plt.xlabel('c')
    plt.ylabel('J')
    plt.savefig("J_c.jpg", dpi = 200)
    
if __name__ == "__main__":
    main()