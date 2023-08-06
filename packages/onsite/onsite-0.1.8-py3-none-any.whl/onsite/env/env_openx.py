'''
Version:0.1.7
Datetime:2022/3/14 17:30
'''
import numpy as np
import xml.dom.minidom
from shapely.ops import unary_union
from shapely.geometry import Polygon
from itertools import combinations
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import re
'''
### To-do
2.路网解析与可视化 
### Done
# 0.1.6
1.背景车的车头角
2.帧数适应性,NDS是10帧,highD25帧,也要输出给测试,增加了dt这一输出量。
3.车辆的长宽
4.轴距可以以比值的形式设计，改说明文档
'''
class EnvOpenx():
    """根据OpenScenario文件进行测试，目前仅根据轨迹数据进行回放测试

    """

    def __init__(self,output_dir,plot=False):
        # self.car_length = 4.924
        # self.car_width = 1.872
        self.l_l = 1.7  # 车辆车长与轴距的比值
        self.dt = None # 时间间隔，根据场景自适应调整。
        self.metric = 'danger'
        self.vehicle_array = None #存储当前场景车辆信息
        self.vehicle_list = None
        self.max_t = 0 #纪录场景持续的时间
        self.output_dir = output_dir
        self.plot_key = plot
        if plot:
            plt.ion()

    def init(self, path):
        # assert(path.split('.')[-1] == "xosc")
        # 在目录中寻找.xosc文件和.xodr文件
        for item in os.listdir(path):
            if item.split(".")[-1] == 'xosc':
                self.opens = path + "/" + item
            if item.split(".")[-1] == 'xodr':
                self.opend = path + "/" + item

        # 读取OpenScenario文件
        self.data = xml.dom.minidom.parse(self.opens).documentElement
        # 读取车辆长度与宽度信息
        wl_node = self.data.getElementsByTagName('Dimensions')
        len_list,wid_list = [],[]
        for wl in wl_node:
            len_list.append(float(wl.getAttribute('length')))
            wid_list.append(float(wl.getAttribute('width')))
        self.l = len_list[0]/self.l_l # 计算本车轴距
        # 读取本车信息，目标信息
        ego_node = self.data.getElementsByTagName('Private')[0]
        ego_init = ego_node.childNodes[3].data
        ego_v,ego_x,ego_y,ego_head = [float(i.split('=')[1]) for i in ego_init.split(',')]
        # 获取行驶目标
        goal_init = ego_node.childNodes[5].data
        goal = [float(i) for i in re.findall('-*\d+\.\d+',goal_init)]
        goal = np.array(goal).reshape(2,2)
        # 读取其他车辆信息
        # 记录每辆车的轨迹，存在dic里面。
        # 注：本车不存在Act项
        # dic的第一次keys是车子的名字，第二层是时间t
        self.traj = {}
        for act in self.data.getElementsByTagName('Act'):
            name = act.getAttribute('name')
            self.traj[name] = {}
            for point in act.getElementsByTagName('Vertex'):
                t = point.getAttribute('time')
                t = round(float(t), 2)
                if t > self.max_t:
                    self.max_t = t
                loc = point.getElementsByTagName('WorldPosition')[0]
                self.traj[name][t] = {}
                self.traj[name][t]['x'] = loc.getAttribute('x')
                self.traj[name][t]['y'] = loc.getAttribute('y')
                self.traj[name][t]['h'] = loc.getAttribute('h')
        t_l = list(self.traj[name].keys())
        self.dt = t_l[1] - t_l[0]
        
        # 存储原始轨迹
        df = None
        for act in self.traj.keys():
            if df is None:
                df = pd.DataFrame(self.traj[act]).T
            else:
                df_add = pd.DataFrame(self.traj[act]).T
                df = pd.concat([df,df_add],join='outer',axis=1)
        self.df = df

        # 计时器归0, 测试结果归0
        self.t = round(0, 2)
        self.result = 0
        self.vehicle_array = np.zeros((len(self.traj.keys())+1, 6))
        self.vehicle_list = list(self.traj.keys())
        self.vehicle_list = ['ego'] + self.vehicle_list

        # 将本车设置到0时刻位置，速度和航向角的关系要明确！
        flag = abs(ego_head) < np.pi/2
        self.vehicle_array[0,:] = [ego_x,ego_y,ego_v,ego_head,len_list[0],wid_list[0]]
        # 将所有其他车辆设置到0时刻位置
        i = 1
        t_n = round(self.t + self.dt, 2)
        for vehi in self.traj.keys():
            if self.t in self.traj[vehi].keys():
                self.vehicle_array[i,0] = self.traj[vehi][self.t]['x']
                self.vehicle_array[i,1] = self.traj[vehi][self.t]['y']
                self.vehicle_array[i,3] = self.traj[vehi][self.t]['h'] # 转向角
                if t_n in self.traj[vehi].keys():
                    x_n = float(self.traj[vehi][t_n]['x']) 
                    x = float(self.traj[vehi][self.t]['x']) 
                    self.vehicle_array[i,2] = np.abs((x_n - x)/self.dt)
                else:
                    self.vehicle_array[i,2] = 0 # speed 没有数值
            else:
                self.vehicle_array[i,:] = 0
            self.vehicle_array[i,4] = len_list[i]
            self.vehicle_array[i,5] = wid_list[i]
            i += 1
        state = self.get_state()
        return state,self.opend,goal,self.dt

    def update(self, action):
        # 根据前向欧拉更新，根据旧速度更新位置，然后更新速度
        ##############更新时间步
        # 前进一个时间步长
        self.t += self.dt
        self.t = round(self.t,2)
        t_n = round(self.t + self.dt, 2)
        ###############更新本车信息
        a, rot = action
        # 首先根据旧速度更新本车位置
        # 更新X坐标
        self.vehicle_array[0, 0] += self.vehicle_array[0,
                                           2] * self.dt * np.cos(
                self.vehicle_array[0, 3])  # *np.pi/180
        # 更新Y坐标
        self.vehicle_array[0, 1] += self.vehicle_array[0,
                                        2] * self.dt * np.sin(
            self.vehicle_array[0, 3])  # *np.pi/180
        # 更新本车转向角
        self.vehicle_array[0, 3] += self.vehicle_array[0,
                                       2] / self.l * np.tan(rot) * self.dt
        # 更新本车速度
        self.vehicle_array[0, 2] += a * self.dt
        # self.vehicle_array[0, 2] = np.clip(self.vehicle_array[0, 2], 0,
        #                                       1e5)
        ##############更新背景车信息
        i = 1
        for vehi in self.vehicle_list[1:]: #对于除本车以外的车辆，直接从字典中取数据
            if self.t in self.traj[vehi].keys():
                self.vehicle_array[i,0] = self.traj[vehi][self.t]['x']
                self.vehicle_array[i,1] = self.traj[vehi][self.t]['y']
                self.vehicle_array[i,3] = self.traj[vehi][self.t]['h'] # 转向角
                if t_n in self.traj[vehi].keys():
                    x_n = float(self.traj[vehi][t_n]['x']) 
                    x = float(self.traj[vehi][self.t]['x']) 
                    self.vehicle_array[i,2] = (x_n - x)/self.dt
                else:
                    self.vehicle_array[i,2] = 0 # speed 没有数值
                
            else:
                self.vehicle_array[i,:] = 0
                self.vehicle_array[i,4] = self.car_length
                self.vehicle_array[i,5] = self.car_width
            i += 1

        judge_value,done = self.judge()
        # 如果此次更新完，时间已走完，则终止测试
        if round(float(self.t), 2) >= self.max_t:
            done = 1
        return judge_value, done

    def judge(self):
        if self.metric in ['danger']:   
            result = 0
            done = 0
            intersection = []
            # 遍历所有位置>5的车辆，绘制对应的多边形
            poly_zip = [self.get_poly(param)[0] for param in self.vehicle_list if self.vehicle_array[self.vehicle_list.index(param), 0]>5]
            # 从所有多边形中，排列组合取出两个，检测是否有交集
            intersection = unary_union(
                [a.intersection(b) for a, b in combinations(poly_zip, 2)]
                ).area
            # print(self.vehicle_array)
            # print(intersection)
        if self.metric == "danger":
            if intersection > 0:
                result = 1
                done = 1

        return result,done

    def get_state(self):
        '''返回所有数据
        
        '''
        state = self.vehicle_array.copy()
        return state

    def step(self,action):
        """根据规控器输出的控制信息，更新env

        Parameters
        ----------
        action : numpy.array or turple or list, shape = (2,)
            本车在当前时刻的动作，包含两部分：
            [本车加速度(m/s^2)，本车转向角速度(rad/s)]

        Returns
        -------
        observation : numpy.array, shape = (?, 6)
            env更新后的新观察值，具体介绍同上。
        reward : bool
            测试状态，目前只检测是否碰撞
            如果碰撞则返回1，否则0
        done: bool
            回放测试是否结束
            如果回放测试结束，返回1，否则0
        info: 
            保留接口，暂时无作用
        """
        reward, done = self.update(action)
        obeservation = self.get_state()

        self.df.loc[np.round(self.t,2),'reward'] = reward
        self.df.loc[np.round(self.t,2),'done'] = done
        self.df.loc[np.round(self.t,2),'ego_x'] = obeservation[0,0]
        self.df.loc[np.round(self.t,2),'ego_y'] = obeservation[0,1]
        self.df.loc[np.round(self.t,2),'rotation'] = obeservation[0,2]
        self.df.loc[np.round(self.t,2),'v'] = obeservation[0,3]
        self.df.loc[np.round(self.t,2),'length'] = obeservation[0,4]
        self.df.loc[np.round(self.t,2),'width'] = obeservation[0,5]
        
        if self.plot_key:
            plt.cla()
            self.plot_all()
            plt.ylim(-40, 40)
            x_center = self.vehicle_array[0,0]
            plt.xlim(x_center-70, x_center+70)
            plt.annotate("reward:%.4f"%reward,xy=(x_center+30,35))
            plt.annotate("speed:%.4f"%obeservation[0,2],xy=(x_center+30,30))
            plt.annotate("acc:%.4f"%action[0],xy=(x_center+30,25))
            plt.pause(1e-3)
            plt.show()

        if done:
            self.df.to_csv(self.output_dir +'/'+self.opens.split('/')[-1] +'.csv')
        

        return obeservation, reward, done, None

    def get_poly(self, name):
        """根据车辆名字获取对应的，符合shapely库要求的矩形。

        这是为了方便地使用shapely库判断场景中的车辆是否发生碰撞

        :param name:车辆的名字
        :return: 一列对应的shapely图形
        """
        ego = self.vehicle_array[self.vehicle_list.index(name), :].copy()
        alpha = np.arctan(ego[5] / ego[4])
        diagonal = np.sqrt(ego[5] ** 2 + ego[4] ** 2)
        poly_list = []
        x0 = ego[0] + diagonal / 2 * np.cos(ego[3] + alpha)
        y0 = ego[1] + diagonal / 2 * np.sin(ego[3] + alpha)
        x2 = ego[0] - diagonal / 2 * np.cos(ego[3] + alpha)
        y2 = ego[1] - diagonal / 2 * np.sin(ego[3] + alpha)
        x1 = ego[0] + diagonal / 2 * np.cos(ego[3] - alpha)
        y1 = ego[1] + diagonal / 2 * np.sin(ego[3] - alpha)
        x3 = ego[0] - diagonal / 2 * np.cos(ego[3] - alpha)
        y3 = ego[1] - diagonal / 2 * np.sin(ego[3] - alpha)
        poly_list = [Polygon(((x0, y0), (x1, y1),
                                   (x2, y2), (x3, y3),
                                   (x0, y0))).convex_hull]
        return poly_list

    @staticmethod
    def _plot_car(x, y, direction=0,txt=None,c='blue', l=3, w=1.8):
        """利用 matplotlib 和 patches 绘制小汽车，以 x 轴为行驶方向

        :param x: 本车x坐标
        :param y: 本车y坐标
        :param direction: 本车车头角
        :param c: 本车颜色
        :param detection_dis: 本车检测范围
        :param l: 本车长度
        :param w: 本车宽度
        """
        angle = np.arctan(w / l) + direction
        diagonal = np.sqrt(l ** 2 + w ** 2)
        plt.gca().add_patch(
            patches.Rectangle(
                xy=(x - diagonal / 2 * np.cos(angle),
                    y - diagonal / 2 * np.sin(angle)),
                width=l,
                height=w,
                angle=direction / np.pi * 180,
                color=c
            ))
        plt.annotate(np.around(x,2),(x,y))

    def plot_all(self):
        """利用 plot_car 方法，绘制存储在vehicle_array中的所有小汽车

        """
        plt.ylim(-50, 50)
        plt.xlim(-20, 80)
        plt.gca().set_aspect('equal')
        if len(self.vehicle_array.shape) == 3:
            plot_array = self.vehicle_array[0, :, :].copy()
        else:
            plot_array = self.vehicle_array.copy()

        for i in range(len(self.vehicle_list)):
            if self.vehicle_list[i] == 'ego':
                self._plot_car(plot_array[i, 0], plot_array[i, 1],
                               plot_array[i, 3], c='red', l=plot_array[i, 4],
                               w=plot_array[i, 5])
            else:
                self._plot_car(plot_array[i, 0], plot_array[i, 1],
                               plot_array[i, 3], c='k', l=plot_array[i, 4],
                               w=plot_array[i, 5])



if __name__ == "__main__":
    env = EnvOpenx("./output")
    env.init('./test_scenario/cutin1.xosc')
    while True:
        observation,reward,done,info = env.step((10,0))
        if done:
            break