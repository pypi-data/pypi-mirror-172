import copy 
import random
import random as rand
import numpy as np
from numpy.lib.function_base import average
import pygame as pg
from pygame import pixelcopy
from pygame.transform import flip
from pygame.draw import line
from pygame.version import ver
import math as mh
import lddya.Ipygame as ipg
import pandas as pd

################################################## 1 蚁群算法路径规划 ###########################################


# Ant只管通过地图数据以及信息素数据，输出一条路径。其他的你不用管。
class Ant():
    def __init__(self,max_step,pher_imp,dis_imp) -> None:
        self.max_step = max_step    # 蚂蚁最大行动力
        self.pher_imp = pher_imp    # 信息素重要性系数
        self.dis_imp = dis_imp      # 距离重要性系数
        self.destination = [19,19]  # 默认的终点节点(在run方法中会重新定义该值)
        self.successful = True      #标志蚂蚁是否成功抵达终点
        self.record_way = [[0,0]]   #路径节点信息记录
        

    def run(self,map_data,pher_data,posi = None,dest = None):
        #Step 0:把蚂蚁放在起点处
        if posi == None:
            self.position = [0,0]       #蚂蚁初始位置[y,x] = [0,0],考虑到列表索引的特殊性，先定y，后定x
        if dest == None:
            self.destination = [len(map_data)-1,len(map_data)-1]
        #Step 1:不断找下一节点，直到走到终点或者力竭 
        for i in range(self.max_step):
            r = self.select_next_node(map_data,pher_data)
            if r == False:
                self.successful = False
                break
            else:
                if self.position == self.destination:
                    break
        else:
            self.successful = False
    
    def select_next_node(self,map_data,pher_data):
        '''
        Function:
        ---------
        选择下一节点，结果直接存入self.postion，仅返回一个状态码True/False标志选择的成功与否。
        '''
        y_1 = self.position[0]
        x_1 = self.position[1]
        #Step 1:计算理论上的周围节点
        node_be_selected = [[y_1-1,x_1-1],[y_1-1,x_1],[y_1-1,x_1+1],     #上一层
                            [y_1,x_1-1],              [y_1,x_1+1],       #同层
                            [y_1+1,x_1-1],[y_1+1,x_1],[y_1+1,x_1+1],     #下一层
                        ]
        #Step 2:排除非法以及障碍物节点    
        node_be_selected_1 = []
        for i in node_be_selected:
            if i[0]<0 or i[1]<0:
                continue
            if i[0]>=len(map_data) or i[1]>=len(map_data):
                continue
            if map_data[i[0]][i[1]] == 0:
                node_be_selected_1.append(i)
        if len(node_be_selected_1) == 0:    # 如果无合法节点，则直接终止节点的选择
            return False
        if self.destination in node_be_selected_1:   # 如果到达终点旁，则直接选中终点
            self.position = self.destination
            self.record_way.append(copy.deepcopy(self.position))
            map_data[self.position[0]][self.position[1]] = 1
            return True
        #Step 3:计算节点与终点之间的距离，构建距离启发因子
        dis_1 = []    # 距离启发因子
        for i in node_be_selected_1:
            dis_1.append(((self.destination[0]-i[0])**2+(self.destination[1]-i[1])**2)**0.5)
        #Step 3.1:使用偏差放大策略
        #dis_min = min(dis_1)
        #for j in range(len(dis_1)):
        #    dis_1[j] = dis_1[j]-0.80*dis_min
        #Step 3.2:倒数反转
        for j in range(len(dis_1)):
            dis_1[j] = 1/dis_1[j]

        #Step 4:计算节点被选中的概率
        prob = []
        for i in range(len(node_be_selected_1)):
            p = (dis_1[i]**self.dis_imp) * (pher_data[y_1*len(map_data)+x_1][node_be_selected_1[i][0]*len(map_data)+node_be_selected_1[i][1]]**self.pher_imp)
            prob.append(p)
        #Step 5:轮盘赌选择某节点
        prob_sum = sum(prob)
        for i in range(len(prob)):
            prob[i] = prob[i]/prob_sum
        rand_key = random.random()
        select_index = 0
        for k,i in enumerate(prob):
            if rand_key<=i:
                select_index = k
                break
            else:
                rand_key -= i
        #Step 6:更新当前位置，并记录新的位置，将之前的位置标记为不可通过
        self.position = copy.deepcopy(node_be_selected_1[k])
        self.record_way.append(copy.deepcopy(self.position))
        map_data[self.position[0]][self.position[1]] = 1
        return True



class ACO():
    def __init__(self,max_iter = 100,ant_num = 50,pher_imp = 1,dis_imp = 10,evaporate = 0.7,pher_init = 8) -> None:
        '''
            Params:
            --------
                pher_imp : 信息素重要性系数
                dis_imp  : 距离重要性系数
                evaporate: 信息素挥发系数(指保留的部分)
                pher_init: 初始信息素浓度
        '''
        #Step 0: 参数定义及赋值
        self.max_iter = max_iter       #最大迭代次数
        self.ant_num  = ant_num        #蚂蚁数量
        self.ant_gener_pher = 1    #每只蚂蚁携带的最大信息素总量
        self.pher_init = pher_init #初始信息素浓度
        self.ant_params = {        #生成蚂蚁时所需的参数
            'dis_imp':dis_imp,
            'pher_imp': pher_imp
        }
        self.map_data = []         #地图数据
        self.pher_data =[]         #信息素浓度数据
        self.evaporate = evaporate #信息素挥发系数
        self.map_lenght = 0        #地图尺寸,用来标定蚂蚁的最大体力，在loading_map()中给出
        self.generation_aver = []  #每代的平均路径(大小)，绘迭代图用
        self.generation_best = []  #每代的最短路径(大小)，绘迭代图用
        self.way_len_best = 999999 
        self.way_data_best = []     #最短路径对应的节点信息，画路线用 

        

    def load_map(self,filepath ='res\\map.dll',map_data = None,reverse = False):
        self.has_load_map = True
        if map_data == None:
            with open(filepath,'r') as f:
                a_1 = f.readlines()
            self.map_lenght = len(a_1)
            for i in range(self.map_lenght):
                a_1[i] = a_1[i].strip('\n')
            for i in a_1:
                l = []
                for j in i:
                    if j == '0':
                        l.append(0)
                    else:
                        l.append(1)
                self.map_data.append(l)
        else:
            self.map_data = copy.deepcopy(map_data)
            self.map_lenght = len(self.map_data)
        if reverse == True:
            self.map_data.reverse()
        self.init_pher(self.pher_init)  #初始化信息素浓度
    
    def init_pher(self,pher_init):
        self.pher_data = pher_init*np.ones(shape=[self.map_lenght*self.map_lenght,self.map_lenght*self.map_lenght])
        self.pher_data = self.pher_data.tolist()


        
    def run(self):
        #总迭代开始
        for i in range(self.max_iter):      
            success_way_list = []
            print('第',i,'代: ',end = '')
            #Step 1:当代若干蚂蚁依次行动
            for j in range(self.ant_num):   
                ant = Ant(max_step=self.map_lenght*3,pher_imp=self.ant_params['pher_imp'],dis_imp=self.ant_params['dis_imp'])
                ant.run(map_data=copy.deepcopy(self.map_data),pher_data=self.pher_data)
                if ant.successful == True:  #若成功，则记录路径信息
                    success_way_list.append(ant.record_way)
            print(' 成功率:',len(success_way_list),end= '')
            #Step 2:计算每条路径对应的长度，后用于信息素的生成量
            way_lenght_list = []
            for j in success_way_list:
                way_lenght_list.append(self.calc_total_lenght(j))
            #Step 3:更新信息素浓度
            #  step 3.1: 挥发
            self.pher_data = np.array(self.pher_data)
            self.pher_data = self.evaporate*self.pher_data
            self.pher_data = self.pher_data.tolist()
            #  step 3.2: 叠加新增信息素
            for k,j in enumerate(success_way_list):
                for t in range(len(j)-1):
                    self.pher_data[j[t][0]*self.map_lenght+j[t][1]][j[t+1][0]*self.map_lenght+j[t+1][1]] += self.ant_gener_pher/way_lenght_list[k]
            #Step 4: 当代的首尾总总结工作
            self.generation_aver.append(average(way_lenght_list))
            self.generation_best.append(min(way_lenght_list))
            if self.way_len_best>min(way_lenght_list):
                a_1 = way_lenght_list.index(min(way_lenght_list))
                self.way_len_best = way_lenght_list[a_1]
                self.way_data_best = copy.deepcopy(success_way_list[a_1])
            print('平均长度:',average(way_lenght_list),'最短:',min(way_lenght_list))
            

    
    def calc_total_lenght(self,way):
        lenght = 0
        for j1 in range(len(way)-1):
            a1 = abs(way[j1][0]-way[j1+1][0])+abs(way[j1][1]-way[j1+1][1])
            if a1 == 2:
                lenght += 1.41421
            else:
                lenght += 1
        return lenght

############################################2 基本遗传算法##############################################################
class GA():
    def __init__(self,population=50, max_iter = 100, cross_pro=0.95, mut_pro=0.15,chro_lenght = 10,chro_limit = [0,10], want_max = True):
        '''
            Function:
            ---------
                对GA的一些必要参数进行初始化，如种群大小、最大迭代、交叉概率、变异概率，染色体长度等进行初始化
            
            Params:
            -------
                eval_fun : fun
                    GA的染色体的评价函数，输入为染色体，输出为评价值,默认加载类自带的fun方法(函数最值求解模型)，
                    也可以通过类方法重写的形式替换fun方法
                chro_decode : fun
                    GA的染色体的解码函数，默认为自带的decode方法，即为二进制转十进制解码方法。
                population: int
                    种群大小
                max_iter :  int
                    最大迭代次数，默认为100
                cross_pro : float
                    交叉概率，区间(0,1)，默认为0.95
                mut_pro : float
                    变异概率，区间(0.1)，默认为0.15
                chro_lenght : int
                    染色体长度
                chro_limit  : list(size = 2)
                    控制十进制染色体的单个染色体片段的上下界限。默认为[0, 10]
                want_max : True or False
                    控制selection选择较大值还是较小值

            Return:
            ------
                None
        '''
        self.population = population
        self.max_iter = max_iter
        self.cross_pro = cross_pro
        self.mut_pro = mut_pro
        self.chro_lenght = chro_lenght
        self.chroms_list = []   # 染色体信息库
        self.child_list = []    #子代染色体信息库
        self.plot_ave = []
        self.plot_max = []
        self.plot_min = []
        self.best_x = []
        self.has_been_init_fun = False    # GA函数模块初始化标志变量，GA优化动作前必须先对相关函数模块初始化
        self.chro_limit = chro_limit
        self.want_max = want_max
        self.best_y = -999999 if want_max == True else 999999

    def init_fun(self,eval_fun=None,chro_decode = None,generate = None, cross = None,mutation = None):
        '''
            Function:
            ---------
                支持对GA中的一些功能函数模块进行二次开发更替。相关函数接口请查阅MD文档。
            
            Params:
            -------
                eval_fun :      评价函数，默认为内置fun函数
                chro_decode :   解码函数，默认为内置decode函数
                generate    :   个体生成函数，默认为内置generate_binary,另外提供十进制的生成函数generate_decimal
                cross       :   交叉函数，默认为内置cross_binary,另外提供十进制的交叉函数cross_decimal
                mutation    :   变异函数，默认为内置mutation_binary,另外提供十进制的变异函数mutation_decimal
        '''
        self.has_been_init_fun = True   
        self.eval_fun = eval_fun if eval_fun != None else self.fun
        self.decode = chro_decode if chro_decode != None else self.decode 
        self.generate_fun = generate if generate != None else self.generate_binary
        self.cross_fun = self.cross_decimal  if cross != None else self.cross_binary
        self.mutation_fun = self.mutation_decimal if mutation != None else self.mutation_binary
    
    def generate_binary(self,chro_lenght):
        '''
            Function:
            ---------
                按要求生成种群，即生成染色体，仅生成一个个体.

            Params:
            -------
                chro_lenght : int
                    染色体长度
                limit : list(lenght=2)
                    染色体每个元素的上下界，当为None时，即为二进制生成，否则若为[a,b]，则a为下限，b为上限。
            
            Return:
            -------
                chro_1 : list (lenght = chro_lenght)
                    一条染色体信息
        '''
        chro_1 = []
        for i in range(chro_lenght):
            chro_1.append(rand.randint(0,1))
        return chro_1

    def generate_decimal(self, chro_lenght,repeat = False):
        '''
            Function:
            --------
                生成规定的十进制的染色体。
            
            Params:
            -------
                chro_lenght : int
                    染色体长度
                
                repeat:
                    控制允许染色体的基因片段数字是否可以重复出现，默认为True
                
            Return:
            -------
                chro_1 : list(lenght = chro_lenght)
                    一条染色体信息
        '''
        chro_1 = []
        if repeat == True:
            for i in range(chro_lenght):
                chro_1.append(rand.randint(self.chro_limit[0],self.chro_limit[1]))
        else:
            chro_1 = np.argsort(np.random.rand(chro_lenght))
            chro_1 = chro_1.tolist()
        
        return chro_1
        
    def fun(self,x):
        '''
            Function:
            ---------
                该函数被设计仅作为资源模块供eval_fun初始化使用，不建议作为方法去调用！该函数的内容主要为
                f函数的极值搜索模型。
            
            Params:
            -------
                x : float/int
                decode解码后的染色体真实值
            
            Return:
            -------
                y : float/int
                对应函数的y值
                
            
        '''
        y =  x + 10*mh.sin(5*x) + 7*mh.cos(4*x)
        return y

    def decode(self,chro, limit = [0,10]):
        '''
            Function:
            ---------
                对一条染色体信息进行解码，默认模式为将二进制数据解码成十进制。
            
            Params:
            --------
                chro : list
                    染色体信息
                limit : list 
                    为十进制数据的范围
            
            Return:
            -------
                decode_value : int
                    十进制数据       
        '''
        chro_1 = copy.deepcopy(chro)
        chro_1.reverse()
        a_1 = 0
        for i in range(len(chro_1)):
            a_1 += chro_1[i]*(2**i)
        e = (a_1/(2**(len(chro_1))-1))*(limit[1]-limit[0]) + limit[0]
        return e

    def run(self):
        if self.has_been_init_fun == False:
            print('无法优化！GA函数模块未初始化，请执行init_fun()方法初始化！')
            return None
        else:
            print('GA优化开始...')
        # Step 1: 初始化生成若干个初代个体
        for i in range(self.population):
            self.chroms_list.append(self.generate_fun(chro_lenght=self.chro_lenght))
        for i in range(self.max_iter):
            # Step 2：执行种群选择
            self.selection()
            #print('#####up:#####')
            self.evalution()
            # Step 3: 交叉 
            self.cross_fun()
            #print('#####down:#####')
            #self.evalution()
            # Step 4: 变异
            self.mutation_fun()
            self.chroms_list = copy.deepcopy(self.child_list)
            #input()
            
    def selection(self):
        '''
            Function:
            ---------
                本选择法为竞标赛选择法。每次随机选择3个个体出来竞争，最优秀的那个个体的染色体信息继承到下一代。
            
            Params:
            --------
                None

            Return:
            -------
                child_1:    list-list
                    子代的染色体信息
        '''
        chroms_1 = copy.deepcopy(self.chroms_list)
        child_1 = []
        for i in range(self.population):
        #for i in range(3):
            a_1 = []    # 3个选手
            b_1 = []    # 3个选手的成绩
            for j in range(3):
                a_1.append(rand.randint(0,len(chroms_1)-1))
            for j in a_1:
                b_1.append(self.eval_fun(self.decode(chroms_1[j])))
            if self.want_max == True:
                c_1 = b_1.index(max(b_1))  # 最好的是第几个
            else:
                c_1 = b_1.index(min(b_1))
            child_1.append(chroms_1[a_1[c_1]])  #最好者进入下一代
            #print("待选三人成绩:",b_1,'选中成绩：',b_1[c_1])
        #print('*******************************************************')
        #input()
        
        self.child_list = child_1

    def cross_binary(self):
        '''
            Function:
            ---------
                PMX交叉法，对子代进行交叉
                
            Params:
            -------
                None
            
            Return:
            -------
                child_1:list-list
                    交叉后的子代信息
        '''
        child_1 = []   # 参与交叉的个体
        for i in self.child_list:  #依据交叉概率挑选个体
            if rand.random()<self.cross_pro:
                child_1.append(i)
        if len(child_1)%2 != 0:    #如果不是双数
            child_1.append(child_1[rand.randint(0,len(child_1)-1)])  #随机复制一个个体
        for i in range(0,len(child_1),2):
            child_2 = child_1[i]       #交叉的第一个个体
            child_3 = child_1[i+1]     #交叉的第二个个体
            a = rand.randint(0,len(child_2)-1)  #生成一个剪切点
            b = rand.randint(0,len(child_2)-1)  #生成另一个剪切点
            a = a if a<b else b                 #保证a点在b点左边，即小于
            if (a==b):                            #如果a=b，则b+1或者a-1，取决于a与b值的合法性
                if b<len(child_2)-1:
                    b += 1
                else:
                    a -= 1
            child_2_1 = child_2[0:a]+child_3[a:b]+child_2[b:]   #交叉重组
            child_3_1 = child_3[0:a]+child_2[a:b]+child_3[b:]
            child_1[i] = child_2_1            #新的覆盖原染色体信息
            child_1[i+1] = child_3_1
        for i in child_1:                     #交叉后的染色体个体加入子代群集中
            self.child_list.append(i)

    def cross_decimal(self):
        child_1 = []   # 参与交叉的个体
        for i in self.child_list:  #依据交叉概率挑选个体
            if rand.random()<self.cross_pro:
                child_1.append(copy.deepcopy(i))
        if len(child_1)%2 != 0:    #如果不是双数
            child_1.append(child_1[rand.randint(0,len(child_1)-1)])  #随机复制一个个体
        for i in range(0,len(child_1),2):
            #print(i)
            child_2 = child_1[i]       #交叉的第一个个体
            child_3 = child_1[i+1]     #交叉的第二个个体
            a = rand.randint(0,len(child_2)-1)  #生成一个剪切点
            b = rand.randint(0,len(child_2)-1)  #生成另一个剪切点
            if b<a :
                c = a                 #保证a点在b点左边，即小于
                a = b
                b = c
            if (a==b):                            #如果a=b，则b+1或者a-1，取决于a与b值的合法性
                if b<len(child_2)-1:
                    b += 1
                else:
                    a -= 1
            ######################################
            # 交叉核心代码
            l1 = child_2
            l2 = child_3

            l1_1 = copy.deepcopy(l1)
            l2_1 = copy.deepcopy(l2)
            for i in range(a,b):
                try:
                    x1 = l1_1.index(l2_1[i])
                    l1[i] = l1_1[x1]
                    l1[x1] = l1_1[i]
                except:
                    pass

                try:
                    x2 = l2_1.index(l1_1[i])
                    l2[i] = l2_1[x2]
                    l2[x2] = l2_1[i]
                except:
                    pass
                l1_1 = copy.deepcopy(l1)
                l2_1 = copy.deepcopy(l2)
            child_2_1 = copy.deepcopy(l1)
            child_3_1 = copy.deepcopy(l2)
            ######################################
            #child_2_1 = child_2[0:a]+child_3[a:b]+child_2[b:]   #交叉重组
            #child_3_1 = child_3[0:a]+child_2[a:b]+child_3[b:]
            child_1[i] = child_2_1            #新的覆盖原染色体信息
            child_1[i+1] = child_3_1
        
        for i in child_1:                     #交叉后的染色体个体加入子代群集中
            self.child_list.append(i)

    def mutation_binary(self):
        '''
            Function:
            ---------
                单点变异，随机某染色体的某节点0-1互换。

            Params:
            -------
                None
            
            Return:
            -------
                None
        '''
        for i in range(len(self.child_list)):
            if rand.random()<self.mut_pro:
                a_1 = rand.randint(0,len(self.child_list[0])-1)
                if self.child_list[i][a_1] == 0:
                    self.child_list[i][a_1] = 1
                else:
                    self.child_list[i][a_1] = 0
    
    def mutation_decimal(self):
        '''
            Function:
            ---------
                单点变异，随机某染色体的某节点数据突变。

            Params:
            -------
                None
            
            Return:
            -------
                None
        '''
        for i in range(len(self.child_list)):
            if rand.random()<self.mut_pro:
                a_1 = rand.randint(0,len(self.child_list[0])-1)
                #print('编译前:',self.child_list[i])
                while True:
                    b_1 = rand.randint(self.chro_limit[0],self.chro_limit[1])
                    if not(b_1 in self.child_list[i]):
                        break
                self.child_list[i][a_1] = b_1
                #print('编译后:',self.child_list[i])
                      
    def evalution(self):
        e = []
        x_1 = []
        y_1 = []
        for i in self.child_list:
            #i.reverse()
            x_2 = self.decode(i)
            x_1.append(x_2)
            y_2 = self.eval_fun(x_2)
            y_1.append(y_2)
            e.append(y_2)
        self.plot_ave.append(sum(e)/len(e))
        self.plot_max.append(max(e))
        self.plot_min.append(min(e))
        if self.want_max == True:
            if max(e)>=self.best_y:
                self.best_y = max(e)
                k = e.index(max(e))
                self.best_x = self.child_list[k]
        else:
            if min(e)<=self.best_y:
                self.best_y = min(e)
                k = e.index(min(e))
                self.best_x = self.child_list[k]
            #print('找到更好值:',self.best_y, end='  ')
            #print(ga.decode(self.best_x))
        #print(e)
        
    def setting(self, eval_fun = None, population=None, max_iter = None, cross_pro=None, mut_pro=None):
        '''
            Function:
            ---------
                该方法允许你随时更新GA中的相关参数。你唯一要注意的是使其合法的生效即可。

            Params:
            -------
                pass

            Return:
            -------
                None
        '''
        if eval_fun != None:
            self.eval_fun = eval_fun
        if population != None:
            self.population = population
        if max_iter != None:
            self.max_iter = max_iter
        if cross_pro != None:
            self.cross_pro = cross_pro
        if mut_pro != None:
            self.mut_pro = mut_pro

######################################### 3 基本蛙跳算法##################################################################

class Frog():
    def __init__(self,x) -> None:
        self.x = x
        self.y = self.evaluate(x)


    def evaluate(self,x):
        '''
            Function:
            ---------
            青蛙计算自己位置所在的评价值。

            Params:
            ------
            x : any --> 坐标(解)

            Return:
            -------
            y : float/int --> 位置(解)对应的评价值。
        '''
        return x + 10*mh.sin(5*x) + 7*mh.cos(4*x);


class Shuffled_Frog_Leaping_Algorithm():
    def __init__(self) -> None:
        self.frog_num = 25
        self.lotus_num = 5
        self.lotus_colony = {}
        self.frog_colony = {}
        self.init()
        self.plot_y = []
        self.plot_x = 0

    def run(self):
        #step 0:准备工作
        self.init()
        for j_1 in range(100):
            #Step 1: 取出每片荷叶
            for i in self.lotus_colony:
                #Step 2: 找到其中最差的青蛙
                e_1 = []    
                for j in self.lotus_colony[i]:
                    e_1.append(j.y)
                min_one = self.lotus_colony[i][np.argmin(e_1)] 
                max_one = self.lotus_colony[i][np.argmax(e_1)] 
                #Step 3: 计算计划位移至的位置x,以及对应的评价值
                x_1 = min_one.x + rand.random()*(max_one.x-min_one.x)
                y_1 = min_one.evaluate(x_1)
                #Step 4: 若位移后结果更优，则位移过去
                if y_1>min_one.y:
                    min_one.x = x_1
                    min_one.y = y_1
                else:
                    #Step 5: 否则，青蛙则转而向全局最优解位移(这里默认第一个荷叶上最大是全局最大，这里后续需要改)
                    e_2 = []    
                    for j in self.lotus_colony[0]:
                        e_2.append(j.y)
                    max_abs_one = self.lotus_colony[0][np.argmax(e_2)] 
                    #Step 6: 计算计划位移至的位置x,以及对应的评价值
                    x_1 = min_one.x + rand.random()*(max_abs_one.x-min_one.x)
                    y_1 = min_one.evaluate(x_1)
                    #Step 7：若位移后结果更优，则位移过去
                    if y_1>min_one.y:
                        min_one.x = x_1
                        min_one.y = y_1
                    #Step 8： 否则，伤心欲绝的青蛙将随机跳到一个随机位置探索新世界
                    else:
                        min_one.x = rand.random()*10
                        min_one.y = min_one.evaluate(min_one.x)
            #Step 9: 找全局最优解
            x = []   #记录每个荷叶上最大值的索引
            y = 0      #记录全局最大的是哪个荷叶
            max_num = -99999
            for k,i in enumerate(self.lotus_colony):
                e_1 = []    
                for j in self.lotus_colony[i]:
                    e_1.append(j.y)
                x_1 = np.argmax(e_1)
                x.append(x_1)
                if self.lotus_colony[i][x_1].y>=max_num:
                    y = k
                    max_num = self.lotus_colony[i][x_1].y
            if y != 0:
                self.lotus_colony[0].append(self.lotus_colony[y][x[y]])
                self.lotus_colony[y].append(self.lotus_colony[0][x[0]])
                del self.lotus_colony[y][x[y]]
                del self.lotus_colony[0][x[0]]
                self.plot_y.append(max_num)
                self.plot_x = self.lotus_colony[y][x[y]].x
            else:
                self.plot_y.append(max_num)
                self.plot_x = self.lotus_colony[0][x[0]].x

                

                






    def init(self):
        #Step 1: 创建若干荷叶与青蛙(创建时就随机扔到任意位置)
        for i in range(self.lotus_num):
            self.lotus_colony[i] = []
        for i in range(self.frog_num):
            self.frog_colony[i] = Frog(rand.random()*10)  #蛙各有命，富贵看天
        #Step 2: 把青蛙分布到荷叶上
        evalution = []      #保存青蛙的适应度
        for i in self.frog_colony:
            evalution.append(self.frog_colony[i].y)
        a_1 = np.argsort(evalution).tolist()
        a_1.reverse()
        count = 0
        for i in a_1:
            self.lotus_colony[count].append(self.frog_colony[i])
            count += 1
            if count == self.lotus_num:
                count = 0
###########################################4 基本鲸鱼算法################################################################
class WOA():
    def __init__(self) -> None:
        self.max_iter = 50    #最大迭代
        self.whale_num = 30   #鲸鱼数量
        self.dim  = 2         #问题维度
        self.x = np.random.uniform(0,6,[self.whale_num,2])  #鲸鱼初始位置
        self.p = 0.5          #P(包围)=P(汽泡网)=0.5
        self.a = 2            #用以生成A
        self.deta_a = self.a/self.max_iter#用以生成A
        self.plot_ave = []
        self.plot_min = []
    
    def run(self):
        for i in range(self.max_iter):
            #Step 1:鲸鱼们想个随机数来决定自己的后续行动。
            a_1= np.random.rand(self.whale_num)            #每个鲸鱼想一个随机数
            baowei = self.x[a_1<=0.5].copy()   #鲸鱼(which想到的随机数＜=0.5)将执行包围操作，所有队友出列！
            qipaowang = self.x[a_1>0.5].copy() #鲸鱼(which想到的随机数>0.5)将执行气泡网操作，所有队友出列！
            #Step 2: 选择包围的鲸鱼开始了行动,
            #Step 2-1: 计算两个位置更新公式中的所需参数。
            A = np.random.uniform(-(self.a-self.deta_a*i),(self.a-self.deta_a*i),len(baowei))  #参数1:A
            #A = np.random.uniform(-(self.a-self.deta_a),(self.a-self.deta_a))
            A_upper_1 = abs(A)>1
            A_less_1 = abs(A)<=1
            #baowei_rand = baowei[A_upper_1==False].copy()  #随机数绝对值大于1的鲸鱼将随机向着一个鲸鱼移动。
            rand_whale = self.x[np.random.randint(0,self.whale_num)].copy()  #参数2:随机鲸鱼个体
            fitness = self.evaluate(self.x)        #计算适应度
            best_whale = self.x[np.argmax(fitness)].copy()#参数3:最优鲸鱼
            C = np.random.uniform(0,2,len(baowei))    #参数4: C
            deta_1 = np.ones(shape = (len(baowei),2))
            deta_1[A_upper_1] = C[:,None][A_upper_1]*rand_whale - baowei[A_upper_1]   #参数：deta，就是公式中绝对值内的东西
            deta_1[A_less_1] = C[:,None][A_less_1]*best_whale - baowei[A_less_1]
            baowei[A_upper_1] = rand_whale - A[:,None][A_upper_1]*abs(deta_1[A_upper_1])   #位置更新1
            baowei[A_less_1] = best_whale - A[:,None][A_less_1]*abs(deta_1[A_less_1])      #位置更新2
            #Step 3: 选择气泡网的鲸鱼们开始了行动。
            l = np.random.uniform(-1,1,len(qipaowang)) #公式中的l
            #qipaowang = np.linalg.norm(best_whale-qipaowang,axis = 1)*np.exp(l)*np.cos(2*np.pi*l)+best_whale
            a_1 = np.exp(l)[:,None]*np.cos(2*np.pi*l)[:,None]*abs(best_whale-qipaowang)
            b_1 = best_whale
            qipaowang = a_1 + b_1
            #Step 4: 将行动后的鲸鱼们都复制为父代
            self.x = np.r_[baowei,qipaowang]
            fitness = self.evaluate(self.x)
            self.best_fitness = np.max(fitness)
            self.best_whale = best_whale.copy()
            print('第%d代：平均值：%f，最优值：%f'%(i,sum(fitness)/len(fitness),self.best_fitness))
            self.plot_ave.append(sum(fitness)/len(fitness))
            self.plot_min.append(self.best_fitness)
            #Step 5: 打印坐标看看(自增加过程，可删)
        #     plt.clf()
        #     plt.plot(self.x[:,0],self.x[:,1],'o',color = 'black')
        #     plt.title('Round:'+str(i))
        #     plt.xlim([0,6])
        #     plt.ylim([0,6])
        #     plt.show(block = False)
        #     plt.pause(0.1)
        # else:
        #     plt.show()



    
    def evaluate(self,x):
        return np.sin(x[:,0])-np.cos(x[:,1])

################################################5 基本粒子群算法######################################################################
class PSO():
    def __init__(self,max_iter = 100,p_num = 50,w=0.7,c1 = 2,c2 = 2) -> None:
        pass
        self.max_iter = max_iter       #最大迭代次数
        self.p_num = p_num    #粒子数
        self.w = w            #惯性系数
        self.c1 = c1          #自信系数
        self.c2 = c2          #盲从系数
        self.r1,self.r2 = np.random.rand(2)  #
        self.v = np.random.rand(self.p_num,2) #粒子的初试速度v
        self.x = np.random.uniform(0,6,(self.p_num,2))
        fitness = self.evaluate(self.x)
        self.best_every_x  = self.x.copy()   #每只粒子记录下自己找到的最优位置
        self.best_every_fit = fitness.copy()  #个体最优位置的评分
        self.best_abs = self.x[np.argmax(fitness)].copy()  #全局最优位置
        self.best_abs_fit = np.max(fitness)         #全局最优位置的评分
        self.plot_ave = []     #每代平均
        self.plot_max = []     #每代最大



    def evaluate(self,x):
        r = np.sin(x[:,0]) -np.cos(x[:,1])  
        return r
        #return np.sum(np.square(x), axis=1)

    def run(self):
        for i in range(self.max_iter):
            print('第',i,'代: ',self.best_abs)
            #Step 1：粒子掏出小本本计算着下一步的方向
            self.v = self.w*self.v+self.c1*self.r1*(self.best_every_x-self.x) + self.c2*self.r2*(self.best_abs-self.x)
            #Step 2: 粒子前往计算的位置
            self.x +=self.v
            #Step 3: 计算适应度
            fitness = self.evaluate(self.x)
            #Step 4: 更新自身最优位置.
            whe_better = np.greater(fitness,self.best_every_fit)
            self.best_every_x[whe_better] = self.x[whe_better]
            #Step 5: 更新全局最优位置。
            whe_better = np.max(fitness)>self.best_abs_fit
            if whe_better:
                self.best_abs_fit = np.max(fitness)
                #print('更新前:',self.best_abs,':',self.evaluate(np.array([self.best_abs])),end=' ')
                self.best_abs = self.x[np.argmax(fitness)].copy()
                #print('更新后:',self.best_abs,':',self.evaluate(np.array([self.best_abs])))
            print('第{%d}代，ave:{%f}, max:{%f}'%(i,sum(fitness)/len(fitness),self.best_abs_fit))
            self.plot_ave.append(sum(fitness)/len(fitness))
            self.plot_max.append(self.best_abs_fit)
        #     plt.clf()
        #     plt.plot(self.x[:,0],self.x[:,1],'o',color='black')
        #     plt.xlim((0,6))
        #     plt.ylim((0,6))
        #     plt.title('Round '+str(i))
        #     plt.show(block = False)
        #     plt.pause(0.1)
        # else:
        #     plt.show()

class PSO_min():
    '''
    求函数最小值。
    '''
    def __init__(self,max_iter = 100,p_num = 50,w=0.7,c1 = 2,c2 = 2) -> None:
        pass
        self.max_iter = max_iter       #最大迭代次数
        self.p_num = p_num    #粒子数
        self.w = w            #惯性系数
        self.c1 = c1          #自信系数
        self.c2 = c2          #盲从系数
        self.r1,self.r2 = np.random.rand(2)  #
        self.v = np.random.rand(self.p_num,2) #粒子的初试速度v
        self.x = np.random.uniform(-10,10,(self.p_num,2))
        fitness = self.evaluate(self.x)
        self.best_every_x  = self.x.copy()   #每只粒子记录下自己找到的最优位置
        self.best_every_fit = fitness.copy()  #个体最优位置的评分
        self.best_abs = self.x[np.argmin(fitness)].copy()  #全局最优位置
        self.best_abs_fit = np.min(fitness)         #全局最优位置的评分
        self.plot_ave = []     #每代平均
        self.plot_max = []     #每代最大



    def evaluate(self,x):
        #r = np.sin(x[:,0]) -np.cos(x[:,1])  
        #return r
        return np.sum(np.square(x), axis=1)

    def run(self):
        for i in range(self.max_iter):
            print('第',i,'代: ',self.best_abs)
            #Step 1：粒子掏出小本本计算着下一步的方向
            self.v = self.w*self.v+self.c1*self.r1*(self.best_every_x-self.x) + self.c2*self.r2*(self.best_abs-self.x)
            #Step 2: 粒子前往计算的位置
            self.x +=self.v
            #Step 3: 计算适应度
            fitness = self.evaluate(self.x)
            #Step 4: 更新自身最优位置.
            whe_better = np.less(fitness,self.best_every_fit)
            self.best_every_x[whe_better] = self.x[whe_better]
            #Step 5: 更新全局最优位置。
            whe_better = np.min(fitness)<self.best_abs_fit
            if whe_better:
                self.best_abs_fit = np.min(fitness)
                #print('更新前:',self.best_abs,':',self.evaluate(np.array([self.best_abs])),end=' ')
                self.best_abs = self.x[np.argmin(fitness)].copy()
                #print('更新后:',self.best_abs,':',self.evaluate(np.array([self.best_abs])))
            print('第{%d}代，ave:{%f}, max:{%f}'%(i,sum(fitness)/len(fitness),self.best_abs_fit))
            # plt.clf()
            # plt.plot(self.x[:,0],self.x[:,1],'o',color='black')
            # plt.xlim((-10,10))
            # plt.ylim((-10,10))
            # plt.show(block = False)
            # plt.pause(0.1)
            


###################################### 99 栅格图 ######################################################################
            
class A_Star_path():
    def __init__(self,map_data,start = np.array([0,0]),end = np.array([0,0])) -> None:
        print('A* Task:',start,end)
        self.map_data = np.array(map_data)
        self.size_map = self.map_data.shape[0]
        self.start = start
        self.end   =  end
        self.open_list  = pd.DataFrame([[start[0],start[1],0,abs(self.start[0]-self.end[0])+abs(self.start[1]-self.end[1]),abs(self.start[0]-self.end[0])+abs(self.start[1]-self.end[1]),-1,-1]],columns=['pos_y','pos_x','g','h','f','parent_y','parent_x'])
        self.close_list = pd.DataFrame([[999,999,0,0,0,0,0]],columns=['pos_y','pos_x','g','h','f','parent_y','parent_x'])
        self.best_way_len = 0
        

    def run(self):
        running = True
        while running:
            #step 1: select an element whose f is smallest(if there are multiple elements with the same f value, we will select the one with the lowest s value.)
            smal_index = self.open_list.loc[:,'f'].argmin()
            #step 2: find all the neighbor grid of it
            neighbour_allowed = self._find_neighbour(self.open_list.iloc[smal_index].values)
            #step 3: update open_list by neighbour_allowed
            have_find_term = self._update_open_list(neighbour_allowed,self.open_list.iloc[smal_index].values)
            if have_find_term == True:
                break
            #step 4: delete it in the open_list and copy to the close_list
            self.close_list.loc[self.close_list.shape[0]] = self.open_list.iloc[smal_index].copy()
            self.open_list.drop(smal_index,inplace=True)
            self.open_list.index = range(self.open_list.shape[0])
        self._calc_way()
        #!print('最优路径为:')
        #!(self.best_way_data)
        


              

    def _find_neighbour(self,who):
        '''
            Function:
            ---------
            This Func can find all neighbor grid of the who, and return them.

            Params:
            -------
            who : 1*d-list--> fe:[[0,0],0,19,19,-1]

            Return:
            ---------
            neighbour_allowed : 1*d-list--> all the neighbour can allowed.
        '''
        y = int(who[0])
        x = int(who[1])
        neighbour_1 = [
            [y-1,x-1],[y-1,x],[y-1,x+1],
            [y  ,x-1],        [y  ,x+1],
            [y+1,x-1],[y+1,x],[y+1,x+1],
        ]
        neighbour_allowed = []
        for i in neighbour_1:
            if (0<=i[0]<=self.size_map-1)and(0<=i[1]<=self.size_map-1): #grid within the scope of the map.
                if self.map_data[i[0],i[1]] == 0:
                    neighbour_allowed.append(i)
        return neighbour_allowed

    def _update_open_list(self,neighbour_allowed,who):
        have_find_term = False           # maiks whether the terminal was found
        for i in neighbour_allowed:
            # case 1: if i in close_list, discard it. 
            
            if (i == self.close_list.loc[:,['pos_y','pos_x']].values).all(axis = 1).any():
                continue
            # we must calculate the data first as it will be used in the both following case. 
            dict_1 = {
                'pos_y' : i[0],
                'pos_x' : i[1],
                'g'   : who[2]+(1.414 if (abs(i[0]-who[0])+abs(i[1]-who[1]))==2 else 1),
                'h'   : abs(i[0]-self.end[0])+abs(i[1]-self.end[1]),
                'f'   : 0,
                'parent_y': who[0],
                'parent_x': who[1]
            }
            dict_1['f']  = dict_1['g']+dict_1['h']
            # case 2: provided i in open_list, check whether i's f is greater 
            #              than b's, if True, update the data of i in the open_list;
            #              otherwise, discard new it. 
            r = (i == self.open_list.loc[:,['pos_y','pos_x']].values).all(axis = 1)
            if r.any():
                index = np.where(r==True)[0]
                if self.open_list.loc[index,'f'].values>dict_1['f']:
                    self.open_list.loc[index,'g'] = dict_1['g']
                    self.open_list.loc[index,'h'] = dict_1['h']
                    self.open_list.loc[index,'f'] = dict_1['f']
                    self.open_list.loc[index,'parent_y'] = dict_1['parent_y']
                    self.open_list.loc[index,'parent_x'] = dict_1['parent_x']
                    
                else:
                    pass
            # case 3: add the i in the open_list.(when i is terminal,the return_param will be True)
            else:
                self.open_list.loc[self.open_list.shape[0]] = dict_1
            if (i == self.end).all():
                have_find_term = True
        return have_find_term

    def _calc_way(self):
        '''
            Function:
            ---------
                find the best way from open_list and close_list, and the result will be saved in self.best_way_data.
        '''
        #step 1: Ectract the position and parent of each element in open_list and close_list.
        dict_1 = {

        }
        for k in range(self.open_list.shape[0]):
            i = self.open_list.iloc[k]
            dict_1[str(int(i.values[0]))+','+str(int(i.values[1]))] = str(int(i.values[-2]))+','+str(int(i.values[-1]))
        for k in range(self.close_list.shape[0]):
            i = self.close_list.iloc[k]
            dict_1[str(int(i.values[0]))+','+str(int(i.values[1]))] = str(int(i.values[-2]))+','+str(int(i.values[-1]))
        # step 2: find the best way between the end with start from dict_1.
        y,x = self.end
        self.best_way_data = [[y,x]]
        while True:
            a_1 = dict_1[str(y)+','+str(x)].split(',')
            y,x = eval(a_1[0]),eval(a_1[1])
            b_1 = self.best_way_data[-1]
            self.best_way_len += ((y-b_1[0])**2+(x-b_1[1])**2)**0.5
            self.best_way_data.append([y,x])
            if y==self.start[0] and x == self.start[1]:
                break
        self.best_way_data.reverse()
            





        
        



        
        

        



