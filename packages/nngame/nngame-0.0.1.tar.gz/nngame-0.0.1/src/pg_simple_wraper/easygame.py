#coding=utf-8

from time import time
import pygame as pg
import sys
from typing import List,Callable,Sequence,Optional,Union,Dict

__window_surface:pg.Surface = None
__clock:pg.time.Clock = None
__fps:int = 30

# 退出事件处理函数列表
__quit_event_handlers:List[Callable[[],None]] = []

def 添加退出事件处理函数(处理函数:dict(type=Callable[[],None],
                                help='用户点击关闭按钮时需要调用的函数'))->bool:
    if 处理函数 in __quit_event_handlers:
        return False
    else:
        __quit_event_handlers.append(处理函数)
        return True

def 移除退出事件处理函数(处理函数:Callable[[],None])->bool:
    if 处理函数 in __quit_event_handlers:
        __quit_event_handlers.remove(处理函数)
        return True
    else:
        return False
        

# 按键按下事件处理函数列表
__key_down_event_handlers:List[Callable[[int],None]] = []

def 添加按键按下事件处理函数(处理函数:Callable[[int],None])->bool:
    if 处理函数 in __key_down_event_handlers:
        return False
    else:
        __key_down_event_handlers.append(处理函数)
        return True

def 移除按键按下事件处理函数(处理函数:Callable[[int],None])->bool:
    if 处理函数 in __key_down_event_handlers:
        __key_down_event_handlers.remove(处理函数)
        return True
    else:
        return False
        


# 按键弹起事件处理函数列表
__key_up_event_handlers:List[Callable[[int],None]] = []

def 添加按键弹起事件处理函数(处理函数:Callable[[int],None])->bool:
    if 处理函数 in __key_up_event_handlers:
        return False
    else:
        __key_up_event_handlers.append(处理函数)
        return True

def 移除按键弹起事件处理函数(处理函数:Callable[[int],None])->bool:
    if 处理函数 in __key_up_event_handlers:
        __key_up_event_handlers.remove(处理函数)
        return True
    else:
        return False
        

#鼠标左键按下事件处理函数列表
__mouse_left_button_down_event_handlers:List[Callable[[int,int],None]] = []

def 添加鼠标左键按下事件处理函数(处理函数:Callable[[int,int],None])->bool:
    if 处理函数 in __mouse_left_button_down_event_handlers:
        return False
    else:
        __mouse_left_button_down_event_handlers.append(处理函数)
        return True

def 移除鼠标左键按下事件处理函数(处理函数:Callable[[int,int],None])->bool:
    if 处理函数 in __mouse_left_button_down_event_handlers:
        __mouse_left_button_down_event_handlers.remove(处理函数)
        return True
    else:
        return False
        

#鼠标右键按下事件处理函数列表
__mouse_right_button_down_event_handlers:List[Callable[[int,int],None]] = []

def 添加鼠标右键按下事件处理函数(处理函数:Callable[[int,int],None])->bool:
    if 处理函数 in __mouse_right_button_down_event_handlers:
        return False
    else:
        __mouse_right_button_down_event_handlers.append(处理函数)
        return True

def 移除鼠标右键按下事件处理函数(处理函数:Callable[[int,int],None])->bool:
    if 处理函数 in __mouse_right_button_down_event_handlers:
        __mouse_right_button_down_event_handlers.remove(处理函数)
        return True
    else:
        return False
        


#鼠标左键释放事件处理函数列表
__mouse_left_button_release_event_handlers:List[Callable[[int,int],None]] = []

def 添加鼠标左键释放事件处理函数(处理函数:Callable[[int,int],None])->bool:
    if 处理函数 in __mouse_left_button_release_event_handlers:
        return False
    else:
        __mouse_left_button_release_event_handlers.append(处理函数)
        return True

def 移除鼠标左键释放事件处理函数(处理函数:Callable[[int,int],None])->bool:
    if 处理函数 in __mouse_left_button_release_event_handlers:
        __mouse_left_button_release_event_handlers.remove(处理函数)
        return True
    else:
        return False
        

#鼠标右键释放事件处理函数列表
__mouse_right_button_release_event_handlers:List[Callable[[int,int],None]] = []

def 添加鼠标右键释放事件处理函数(处理函数:Callable[[int,int],None])->bool:
    if 处理函数 in __mouse_right_button_release_event_handlers:
        return False
    else:
        __mouse_right_button_release_event_handlers.append(处理函数)
        return True

def 移除鼠标右键释放事件处理函数(处理函数:Callable[[int,int],None])->bool:
    if 处理函数 in __mouse_right_button_release_event_handlers:
        __mouse_right_button_release_event_handlers.remove(处理函数)
        return True
    else:
        return False
        

#鼠标移动事件处理函数列表
__mouse_move_event_handlers:List[Callable[[int,int,bool],None]] = []

def 添加鼠标移动事件处理函数(处理函数:Callable[[int,int,bool],None])->bool:
    if 处理函数 in __mouse_move_event_handlers:
        return False
    else:
        __mouse_move_event_handlers.append(处理函数)
        return True

def 移除鼠标移动事件处理函数(处理函数:Callable[[int,int,bool],None])->bool:
    if 处理函数 in __mouse_move_event_handlers:
        __mouse_move_event_handlers.remove(处理函数)
        return True
    else:
        return False
        

# 鼠标滚轮滚动事件处理函数列表
__mouse_wheel_event_handlers:List[Callable[[bool],None]] = []

def 添加鼠标滚动事件处理函数(处理函数:Callable[[bool],None])->bool:
    if 处理函数 in __mouse_wheel_event_handlers:
        return False
    else:
        __mouse_wheel_event_handlers.append(处理函数)
        return True

def 移除鼠标滚动事件处理函数(处理函数:Callable[[bool],None])->bool:
    if 处理函数 in __mouse_wheel_event_handlers:
        __mouse_wheel_event_handlers.remove(处理函数)
        return True
    else:
        return False
        

#定时器事件处理函数列表
__timer_event_handler:List[Callable[[],None]] = []

def 创建定时器(毫秒:int,定时器处理函数:Callable[[],None])->bool:
    if 定时器处理函数 in __timer_event_handler:
        return False
    else:
        pg.time.set_timer(pg.USEREVENT + len(__timer_event_handler),毫秒)
        __timer_event_handler.append(定时器处理函数)
        return True


def 检测事件()->None:
    for event in pg.event.get():
        #print(event)
        if event.type == pg.QUIT:
            for hander in __quit_event_handlers:
                hander()
        elif event.type == pg.KEYDOWN:
            for hander in __key_down_event_handlers:
                hander(event.key)
        elif event.type == pg.KEYUP:
            for hander in __key_up_event_handlers:
                hander(event.key)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for hander in __mouse_left_button_down_event_handlers:
                    hander(event.pos[0],event.pos[1])
            elif event.button == 3:
                for hander in __mouse_right_button_down_event_handlers:
                    hander(event.pos[0],event.pos[1])
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                for hander in __mouse_left_button_release_event_handlers:
                    hander(event.pos[0],event.pos[1])
            elif event.button == 3:
                for hander in __mouse_right_button_release_event_handlers:
                    hander(event.pos[0],event.pos[1])
        elif event.type == pg.MOUSEMOTION:
            for hander in __mouse_move_event_handlers:
                hander(event.pos[0],event.pos[1],event.buttons[0] == 1)
        elif event.type == pg.MOUSEWHEEL:
            for hander in __mouse_wheel_event_handlers:
                hander(event.y == 1)
        elif event.type >= pg.USEREVENT:
            __timer_event_handler[event.type - pg.USEREVENT]()
        else:
            pass



def 创建窗口(游戏标题:str,游戏窗口宽度:int,游戏窗口高度:int):
    global __window_surface
    global __clock

    pg.init()
    __window_surface = pg.display.set_mode((游戏窗口宽度,游戏窗口高度))
    pg.display.set_caption(游戏标题)
    
    __clock = pg.time.Clock()


def 设置帧频FPS(fps:int)->None:
    global __fps
    __fps = fps

def 获取帧频FPS()->int:
    global __clock
    return __clock.get_fps()

def 获取时间差()->int:
    global __clock
    return __clock.get_time()


def 按住不放(键位:int)->bool:
    keys_pressed: Sequence[bool] = pg.key.get_pressed()
    if keys_pressed[键位]:
        return True
    else:
        return False

def 刷新画面()->None:
    global __clock
    global __fps
    pg.display.update()
    __clock.tick(__fps)


def 退出()-> None:
    sys.exit()


def 空格键()->int:
    return pg.K_SPACE

def 上方向键()-> int:
    return pg.K_UP

def 下方向键()->int:
    return pg.K_DOWN

def 左方向键()->int:
    return pg.K_LEFT

def 右方向键()->int:
    return pg.K_RIGHT

def 按键A()->int:
    return pg.K_a

def 按键S()->int:
    return pg.K_s

def 按键D()->int:
    return pg.K_d

def 按键W()->int:
    return pg.K_w

def 逃逸键()->int:
    return pg.K_ESCAPE

def 空格键()->int:
    return pg.K_SPACE

# 图片精灵创建和控制
class 图片精灵(pg.sprite.Sprite):
    def __init__(self,图片路劲:str,左边距:float,上边距:float):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(图片路劲)
        self.rect = self.image.get_rect()
        self.rect.left = 左边距
        self.rect.top = 上边距

    @property
    def 横坐标(self)->float:
        return self.rect.left + self.rect.width/2

    @横坐标.setter
    def 横坐标(self,x:float)->None:
        self.rect.left = x - self.rect.width/2

    @property
    def 纵坐标(self)->float:
        return self.rect.top + self.rect.height/2

    @纵坐标.setter
    def 纵坐标(self,y:float)->None:
        self.rect.top = y - self.rect.height/2

    @property
    def 宽(self)->float:
        return self.rect.width

    @property
    def 高(self)->float:
        return self.rect.height

    @property
    def 上边距(self)->float:
        return self.rect.top

    @property
    def 左边距(self)->float:
        return self.rect.left

    @property
    def 右边距(self)->float:
        return self.rect.right

    @property
    def 下边距(self)->float:
        return self.rect.bottom
    

def 创建图片精灵(图片路劲:str,横坐标:float = 0,纵坐标:float = 0)->图片精灵:
    sprite:图片精灵 = 图片精灵(图片路劲,横坐标,纵坐标)
    return sprite

class 图片精灵仓库(pg.sprite.Group):
    def __init(self):
        pg.sprite.Group.__init__(self)

    def 放入(self,精灵:图片精灵)->None:
        self.add(精灵)

    def 取出(self,精灵:图片精灵)->None:
        self.remove(精灵)

    def 碰撞检测(self,精灵:图片精灵)->List[图片精灵]:
        self.remove(精灵)
        result = pg.sprite.spritecollide(精灵,self,False)
        self.add(精灵)
        return result


def 创建图片精灵仓库()->图片精灵仓库:
    return 图片精灵仓库()


def 碰撞检测(精灵:图片精灵,仓库:图片精灵仓库)->List[图片精灵]:
    return pg.sprite.spritecollide(精灵,仓库,False)


def 添加精灵到窗口(显示元素:图片精灵)->None:
    global __window_surface
    if isinstance(显示元素,图片精灵):
        __window_surface.blit(显示元素.image,显示元素.rect)

def 窗口填充颜色(红色分量:int,绿色分量:int,蓝色分量:int)->None:
    global __window_surface
    __window_surface.fill([红色分量,绿色分量,蓝色分量])


class 字体(pg.font.Font):
    def __init__(self,字体路径:Optional[str] = None,大小:int = 28):
        pg.font.Font.__init__(self,字体路径,大小)

def 创建字体(字体路径:Optional[str] = None,字体大小:int = 28)->字体:
    return 字体(字体路径,字体大小)

def 创建文本框(字体:字体,内容:str,
            抗锯齿:bool = True,
            文字颜色红色分量:int = 0,
            文字颜色绿色分量:int = 0,
            文字颜色蓝色分量:int = 0,
            背景颜色红色分量:int = 255,
            背景颜色绿色分量:int = 255,
            背景颜色蓝色分量:int = 255)->pg.Surface:
    sf:pg.Surface = 字体.render(内容,抗锯齿,
            (文字颜色红色分量,文字颜色绿色分量,文字颜色蓝色分量),
            (背景颜色红色分量,背景颜色绿色分量,背景颜色蓝色分量))

    return sf

def 添加文本框到窗口(文本框:pg.Surface,横坐标:float,纵坐标:float)->None:
    __window_surface.blit(文本框,[横坐标,纵坐标])



def 创建音效(声音文件路径:str)->pg.mixer.Sound:
    return pg.mixer.Sound(声音文件路径)

def 播放音效(音效:pg.mixer.Sound)->None:
    音效.play()

def 加载背景音乐(背景音乐文件路劲:str)->None:
    pg.mixer.music.load(背景音乐文件路劲)

def 播放背景音乐(播放次数:dict(type=int,help='小于0时无限重复') = 0)->None:
    pg.mixer.music.play(播放次数)

