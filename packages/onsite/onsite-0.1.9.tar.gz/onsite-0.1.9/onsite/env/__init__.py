from .env_openx import EnvOpenx

def make(path:str,output_dir:str,plot=False):
    """初始化当前回放测试场景
    
    Parameters
    ----------
    scenario_dir : str
        输入场景文件的具体路径。
        
    output_dir : str
        输出测试结果文件的路径。

    Returns
    -------
    env :  
        测试环境的对象，便于下方更新环境状态使用。

    observation : numpy.array, shape = (?, 6)
        初始状态观察值，包含本车及场景内所有车辆的信息。
        格式为numpy.array，一个n×6的二维矩阵，n为场景中的车辆数量。
        其中每一行为一辆车辆的信息，第一行为本车信息。
        六列分别为：
        x坐标(m)、y坐标(m)、速度(m/s)、朝向θ(rad)、车辆长度(m)、车辆宽度(m)

    opendrive : str
        .xodr格式的OpenDrive路网文件所在的路径

    goal : numpy.array, shape = (2, 2)
        本回放测试场景的行驶目标，为一个矩形的目标区域。
        格式为numpy.array，一个2×2的矩阵
        第一行为x坐标的目标范围
        第二行为y坐标的目标范围

    dt : float
        场景运行每一帧的时间间隔，根据回放测试场景的来源，会有不同。
        目前：
            HighD数据集提取的场景，一秒25帧，dt=0.04s；
            自然驾驶数据提取的场景，一秒10帧，dt=0.1s。
        
    """
    env = EnvOpenx(output_dir,plot=plot)
    observation,opendrive,goal,dt = env.init(path)
    return env,observation,opendrive,goal,dt