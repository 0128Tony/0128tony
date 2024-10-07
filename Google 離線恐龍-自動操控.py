import pyautogui as pyg
import time

pyg.sleep(2)

# 初始位置和颜色
pos_x, pos_y = 528, 276
obstacle_color = (83, 83, 83)
obstacle_color3 = (172, 172, 172)
night_color = (0, 0, 0)

# 特定位置的颜色
special_color_position1 = (650, 250)
special_color1 = (83, 83, 83)

# 移动鼠标到开始的位置并启动游戏
pyg.moveTo(pos_x, pos_y, duration=1)
pyg.click()


# 定义障碍物检测函数
def isObstacle(im, y):
    for i in range(22):  # 增加循环次数
        c = im.getpixel((pos_x + i * 3,  pos_y))  # 增加步长
        if c == obstacle_color:
            return True
    return False

# 定义飛鳥障礙物检测函数
def isBirdObstacle(im):
    c = im.getpixel(special_color_position1)
    return c == special_color1

def isObstacle2(im, y):
    for i in range(22):  # 增加循环次数
        c = im.getpixel((pos_x + i * 5,  pos_y))  # 增加步长
        if c == obstacle_color3:
            return True
    return False

try:
    while True:
        im = pyg.screenshot()

        if isObstacle(im, pos_y):
            # 添加一些随机性
            pyg.keyDown('up')
            pyg.keyUp('up')
            time.sleep(0.05)
            pyg.keyDown('down')
            pyg.keyUp('down')
            im = pyg.screenshot()

            if isObstacle(im, 247):
                pyg.keyDown('up')
                pyg.keyUp('up')


        elif isBirdObstacle(im):
            pyg.keyDown('up')
            pyg.keyUp('up')
    

        
        

except KeyboardInterrupt:
    pass










