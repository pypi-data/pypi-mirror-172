import matplotlib.pyplot as plt
import pygame as pg
import lddya.Ipygame as ipg

class ShanGeTu():
    def __init__(self,map_path = 'map.dll',map_data = None,reverse = False):
        self.grid_size = 0
        self.cell_size = 0
        self.line_size = 0
        self.__load_map(map_path,map_data,reverse = reverse)                        #读取地图数据
        self.pic_backgroud = self.__backgroud()  #画网格
        self.__draw_barrier()                    #画障碍物方格，跟上一步共同组合成完整的背景图片
        #self.draw_way(way_data=way_data)
        #self.save()                            #保存起来
        
    def __backgroud(self):
        '''
            Function:
            ---------
                绘制栅格图的背景(即不包含路径线条的栅格图),并以返回Surface形式返回

            Params:
            -------
                None

            Return:
            -------
                backgroud : pygame.Surface
                    栅格图背景
        '''
        size = self.grid_size
        if size == 20:
            self.cell_size = 25
            self.line_size = 1
            pic_size = size*self.cell_size+(size+1)*self.line_size
            self.backgroud_size = pic_size
            backgroud = pg.Surface([pic_size,pic_size])
            backgroud.fill([255,255,255])
            for i in range(size+1):
                pg.draw.line(backgroud,[0,0,0],[i*(self.cell_size+self.line_size),0],[i*(self.cell_size+self.line_size),pic_size])
                pg.draw.line(backgroud,[0,0,0],[0,i*(self.cell_size+self.line_size)],[pic_size,i*(self.cell_size+self.line_size)])
            return backgroud
        #elif size == 30:
        else:
            self.cell_size = 15
            self.line_size = 1
            pic_size = size*self.cell_size+(size+1)*self.line_size
            self.backgroud_size = pic_size
            backgroud = pg.Surface([pic_size,pic_size])
            backgroud.fill([255,255,255])
            for i in range(size+1):
                pg.draw.line(backgroud,[0,0,0],[i*(self.cell_size+self.line_size),0],[i*(self.cell_size+self.line_size),pic_size])
                pg.draw.line(backgroud,[0,0,0],[0,i*(self.cell_size+self.line_size)],[pic_size,i*(self.cell_size+self.line_size)])
            return backgroud

    def __load_map(self,map_path,map_data,reverse = False):
        '''
        Function:
        ---------
            读取map数据存于self.map_data，数据为0-1矩阵，位置同栅格图节点位置，默认左上角为起点，右下角为终点。
        
        Params:
        -------
            None
        
        Return:
        -------
            None
        '''
        if map_data == None:
            with open(map_path,'r') as f:
                self.map_data = f.readlines()
            for k,i in enumerate(self.map_data):
                self.map_data[k]= i.strip('\n')
        else:
            self.map_data = []
            for  i in map_data:
                i = [str(j) for j in i]
                self.map_data.append(''.join(i))
        if reverse == True:
            self.map_data.reverse()
        self.grid_size = len(self.map_data[0])
    def __draw_barrier(self):
        for i in range(len(self.map_data[0])):
            for j in range(len(self.map_data[0])):
                if self.map_data[i][j] == '1':
                    x_1 = (j+1)*self.line_size + j*self.cell_size
                    y_1 = (i+1)*self.line_size + i*self.cell_size
                    pg.draw.rect(self.pic_backgroud,[0,0,0],[x_1,y_1,self.cell_size,self.cell_size])

    def draw_way(self,way_data,_2D, y_x_change = False,new_pic = True,color = [0,0,0],line_type = '-'):
        '''
        '_2D':'标志输入量是否为[x,y]格式',
        'x_y_change': '调换x——y坐标',
        'new_pic' : '新建一个背景画线段？默认未True',
        'color' : '线段的颜色'
        '''
        if new_pic == True:
            self.pic_shangetu = self.pic_backgroud.copy()
        # 转换成二维坐标格式
        if _2D == False:
            way_data_1 = []
            for i in way_data:
                way_data_1.append([i%self.grid_size,i//self.grid_size])
        else:
            way_data_1 = way_data
        if y_x_change == True:
            for i in range(len(way_data_1)):
                way_data_1[i][0],way_data_1[i][1] =  way_data_1[i][1],way_data_1[i][0]
        # 画线喽
        for k,i in enumerate(way_data_1):
            try:
                j = way_data_1[k+1]
            except:
                return None
            point_1_x = (i[0]+1)*self.line_size + i[0]*self.cell_size+self.cell_size/2
            point_1_y = (i[1]+1)*self.line_size + i[1]*self.cell_size+self.cell_size/2
            point_2_x = (j[0]+1)*self.line_size + j[0]*self.cell_size+self.cell_size/2
            point_2_y = (j[1]+1)*self.line_size + j[1]*self.cell_size+self.cell_size/2
            # 下面两行起到上下翻转的目的
            #point_1_y = self.backgroud_size - point_1_y
            #point_2_y = self.backgroud_size - point_2_y
            if line_type == '-':
                pg.draw.line(self.pic_shangetu,color,[point_1_x,point_1_y],[point_2_x,point_2_y],2)
            elif line_type == '--': 
                ipg.dot_line(self.pic_shangetu,color,[point_1_x,point_1_y],[point_2_x,point_2_y],2)
                
    def save(self,filename = '栅格图.jpg',reverse = False):
        '''
            Function:
            ---------
                将画好的栅格图存储起来。

            Params:
            -------
                文件存放路径(含文件名)
        '''
        
        try:
            if  reverse == True:
                self.pic_shangetu = pg.transform.flip(self.pic_shangetu,False,True)
            pg.image.save(self.pic_shangetu,filename)
        except:
            if  reverse == True:
                self.pic_backgroud = pg.transform.flip(self.pic_backgroud,False,True)
            pg.image.save(self.pic_backgroud,filename)
    

class IterationGraph():
    def __init__(self,data_list,style_list,legend_list,xlabel='x',ylabel='y') -> None:
        self.fig,self.ax = plt.subplots()
        for i in range(len(data_list)):
            self.ax.plot(range(len(data_list[i])),data_list[i],style_list[i])
        if type(legend_list) == list:
            self.ax.legend(legend_list)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def show(self):
        plt.show()
    def save(self,figname = 'figure.jpg'):
        self.fig.savefig(figname)