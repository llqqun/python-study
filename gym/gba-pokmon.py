import gymnasium as gym
import numpy as np
import psutil
import time
from gymnasium import spaces
from enum import Enum
import win32gui
import win32ui
import win32con
import win32process

class Actions(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

class GBAPokemonEnv(gym.Env):
    def __init__(self):
        super(GBAPokemonEnv, self).__init__()
        
        # 定义动作空间 (上下左右, A, B, Start, Select)离散动作
        self.action_space = spaces.Discrete(8)
        self._action_to_direction = {
            Actions.RIGHT.value: np.array([0, 1]),
            Actions.UP.value: np.array([1, 0]),
            Actions.LEFT.value: np.array([0, -1]),
            Actions.DOWN.value: np.array([-1, 0]),
        }
        
        # 获取模拟器窗口句柄
        self.hwnd = None
        self.window_rect = None
        self.emulator_process = None
        self.update_window_info()
        # 获取画面高
        self.screen_height = self.window_rect[3] - self.window_rect[1] - 50
        print('模拟器信息', self.hwnd, self.window_rect, self.emulator_process)
        print('模拟器画面高度', self.screen_height)
        print("---------------")
        # 定义观察空间 (游戏画面状态)
        if self.window_rect:
            width = self.window_rect[2] - self.window_rect[0]
            height = self.window_rect[3] - self.window_rect[1]
            self.observation_space = spaces.Box(low=0, high=255, shape=(height, width, 3), dtype=np.uint8)
        else:
            # 默认大小
            self.observation_space = spaces.Box(low=0, high=255, shape=(240, 160, 3), dtype=np.uint8)
        
        # 初始化探索记录
        self.explored_positions = set()  # 记录已探索的位置
        self.current_position = None     # 当前位置
        self.exploration_reward = 1.0    # 探索新区域的奖励值
        self.step_penalty = -0.1         # 每步的惩罚值

    def is_emulator_running(self):
        """检查GBA模拟器是否在运行"""
        for proc in psutil.process_iter(['name']):
            # 这里需要根据实际使用的模拟器修改进程名
            if proc.info['name'] == 'VisualBoyAdvance(CN).exe':
                # print("GBA模拟器已运行: PID:", proc.pid)
                self.emulator_process = proc
                return True
        return False

    def update_window_info(self):
        """更新模拟器窗口信息"""
        if not self.emulator_process:
            if not self.is_emulator_running():
                return
        
        def callback(hwnd, pid):
            try:
                # 获取窗口对应的进程ID
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                if window_pid == pid:
                    print(f'找到窗口:{window_pid}')
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    # 确保是可见的主窗口
                    if win32gui.IsWindowVisible(hwnd) and not win32gui.GetWindow(hwnd, win32con.GW_OWNER):
                        self.hwnd = hwnd
                        self.window_rect = win32gui.GetWindowRect(hwnd)
                        return False
            except Exception as e:
                print(e)
                pass
            return True
        
        # 使用进程ID查找对应的窗口
        win32gui.EnumWindows(callback, self.emulator_process.pid)

    def get_screen_state(self):
        """获取模拟器窗口的画面状态"""
        if not self.hwnd:
            self.update_window_info()
            if not self.hwnd:
                return np.zeros((240, 160, 3), dtype=np.uint8)
        
        try:
            # 获取窗口DC
            window_dc = win32gui.GetWindowDC(self.hwnd)
            dc_obj = win32ui.CreateDCFromHandle(window_dc)
            mem_dc = dc_obj.CreateCompatibleDC()
            
            # 创建位图对象
            width = self.window_rect[2] - self.window_rect[0]
            height = self.window_rect[3] - self.window_rect[1]
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(dc_obj, width, height)
            mem_dc.SelectObject(bitmap)
            
            # 复制窗口内容到位图
            mem_dc.BitBlt((0, 0), (width, height), dc_obj, (0, 0), win32con.SRCCOPY)
            
            # 获取位图信息
            bmp_info = bitmap.GetInfo()
            bmp_str = bitmap.GetBitmapBits(True)
            img_array = np.frombuffer(bmp_str, dtype=np.uint8)
            img_array = img_array.reshape((height, width, 4))  # RGBA格式
            img_array = img_array[:, :, :3]  # 只保留RGB通道
            
            # 清理资源
            mem_dc.DeleteDC()
            win32gui.DeleteObject(bitmap.GetHandle())
            win32gui.ReleaseDC(self.hwnd, window_dc)
            
            return img_array
            
        except Exception as e:
            print(f"获取屏幕状态失败: {e}")
            return np.zeros((240, 160, 3), dtype=np.uint8)

    def get_current_position(self):
        """获取当前角色在游戏中的位置"""
        # TODO: 实现从模拟器内存中读取角色位置的逻辑
        # 这里临时返回随机位置用于测试
        return (np.random.randint(0, 100), np.random.randint(0, 100))

    def calculate_exploration_reward(self, new_position):
        """计算探索奖励"""
        reward = self.step_penalty  # 基础惩罚值
        
        if new_position not in self.explored_positions:
            reward += self.exploration_reward  # 发现新区域的奖励
            self.explored_positions.add(new_position)
        
        return reward

    def reset(self, seed=None, options=None):
        """重置环境"""
        super().reset(seed=seed)
        
        if not self.is_emulator_running():
            raise RuntimeError("GBA模拟器未运行！请先启动模拟器并加载游戏ROM。")
        
        # 重置探索记录
        self.explored_positions.clear()
        self.current_position = self.get_current_position()
        if self.current_position:
            self.explored_positions.add(self.current_position)
        
        # 获取当前游戏画面状态
        observation = self.get_screen_state()
        info = {}
        
        return observation, info

    def step(self, action):
        """执行动作并获取下一个状态"""
        if not self.is_emulator_running():
            raise RuntimeError("GBA模拟器未运行！")
        
        # TODO: 执行动作
        # 1. 将action映射到按键操作
        # 2. 模拟按键输入
        # 3. 等待游戏响应
        
        # 获取新的游戏画面状态
        observation = self.get_screen_state()
        
        # 获取新位置并计算奖励
        new_position = self.get_current_position()
        reward = self.calculate_exploration_reward(new_position)
        self.current_position = new_position
        
        terminated = False
        truncated = False
        info = {
            "explored_positions": len(self.explored_positions),
            "current_position": self.current_position
        }
        
        return observation, reward, terminated, truncated, info

    def render(self):
        """渲染当前环境状态"""
        # GBA模拟器会自动渲染游戏画面，这里不需要额外实现
        pass

    def close(self):
        """关闭环境"""
        pass

# 测试代码
if __name__ == "__main__":
    env = GBAPokemonEnv()
    if not env.hwnd:
        print("GBA模拟器未运行！请先启动模拟器并加载游戏ROM。")
        env.close()
    try:
        obs, info = env.reset()
        for _ in range(10):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            # print("Reward:", obs, reward, terminated, truncated, info)
            if terminated or truncated:
                obs, info = env.reset()
                
            time.sleep(0.1)  # 控制执行速度
    
    except RuntimeError as e:
        print(e)
    
    finally:
        env.close()