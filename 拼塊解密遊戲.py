import tkinter as tk
from tkinter import messagebox
from cvzone.HandTrackingModule import HandDetector
import cv2
import sys
import os
import random
import pygame

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# 初始化 pygame 和音樂播放器
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Super Mario Bros. Theme Song.mp3")  # 載入您的音樂文件
correct_sound = pygame.mixer.Sound("YAHOO SOUND EFFECT (MARIO).mp3")  # 正確放置時的音效
win_sound = pygame.mixer.Sound("Super Mario Bros. Music - Level Complete.mp3")  # 贏時的音效
pygame.mixer.music.play(-1)  # 播放音樂，-1 表示循環播放

# 在初始化部分添加五个标志变量来追踪每个框的音效是否已经播放过
sound_played_yellow = False
sound_played_orange = False
sound_played_blue = False
sound_played_red = False
sound_played_green = False
win_sound_status = False

# 創建 tkinter 主視窗
root = tk.Tk()
root.withdraw()  # 隱藏主視窗


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)

pic1 = cv2.imread("blue.jpg")
pic1 = cv2.resize(pic1, (100, 100))

pic2 = cv2.imread("yellow.jpg")
pic2 = cv2.resize(pic2, (100, 100))

pic3 = cv2.imread("orange.jpg")
pic3 = cv2.resize(pic3, (100, 100))

pic4 = cv2.imread("red.jpg")
pic4 = cv2.resize(pic4, (100, 100))

pic5 = cv2.imread("green.jpg")
pic5 = cv2.resize(pic5, (100, 100))

if pic1.shape != pic2.shape:
    pic2 = cv2.resize(pic2, (pic1.shape[1], pic1.shape[0]))

# 定義所有可能的初始座標
coordinates = [(140, 150), (360, 150), (600, 150), (830, 150), (1060, 150)]

# 隨機打亂座標列表
random.shuffle(coordinates)

h, w, _ = pic1.shape
# 分配座標給不同的圖片
ox1, oy1 = coordinates[0]
ox2, oy2 = coordinates[1]
ox3, oy3 = coordinates[2]
ox4, oy4 = coordinates[3]
ox5, oy5 = coordinates[4]


# 調整框之間的距離
distance_between_boxes = 80

# 新增框的狀態變數
status_box1 = 0
status_box2 = 0
status_box3 = 0
status_box4 = 0
status_box5 = 0

# 新增圖片鎖定的變數
lock_pic1 = False
lock_pic2 = False
lock_pic3 = False
lock_pic4 = False
lock_pic5 = False

# 初始化 current_pic 變量
current_pic = 1

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    text = "Please put the color squares in order"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_position = ((img.shape[1] - text_size[0]) // 2, 50)
    cv2.putText(img, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    if hands:
        lmList = hands[0]['lmList']
        cursor = [(lmList[8][0] + lmList[12][0]) // 2, (lmList[8][1] + lmList[12][1]) // 2]

        # 檢查食指和中指的距離
        length, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])

        if length < 60:
            # 檢查食指和中指是否在圖片範圍內
            if ox1 < cursor[0] < ox1 + w and oy1 < cursor[1] < oy1 + h:
                ox1, oy1 = cursor[0] - w // 2, cursor[1] - h // 2
                status_box1 = 1
            elif ox2 < cursor[0] < ox2 + w and oy2 < cursor[1] < oy2 + h:
                ox2, oy2 = cursor[0] - w // 2, cursor[1] - h // 2
                status_box2 = 1
            elif ox3 < cursor[0] < ox3 + w and oy3 < cursor[1] < oy3 + h:
                ox3, oy3 = cursor[0] - w // 2, cursor[1] - h // 2
                status_box3 = 1
            elif ox4 < cursor[0] < ox4 + w and oy4 < cursor[1] < oy4 + h:
                ox4, oy4 = cursor[0] - w // 2, cursor[1] - h // 2
                status_box4 = 1
            elif ox5 < cursor[0] < ox5 + w and oy5 < cursor[1] < oy5 + h:
                ox5, oy5 = cursor[0] - w // 2, cursor[1] - h // 2
                status_box5 = 1
            else:
                # 重置所有狀態
                status_box1, status_box2, status_box3, status_box4, status_box5 = 0, 0, 0, 0, 0
                
            

    # 繪製藍色框，置中在視窗中部
    blue_box_start = ((img.shape[1] - w - 50) // 2, (img.shape[0] - h - 50) // 2)
    blue_box_end = (blue_box_start[0] + w + 50, blue_box_start[1] + h + 50)
    cv2.rectangle(img, blue_box_start, blue_box_end, (255, 0, 0), 2)

    # 繪製紅色框，與藍色框左側相鄰並保持相同大小
    red_box_start = (blue_box_start[0] - w - 50 - distance_between_boxes, blue_box_start[1])
    red_box_end = (red_box_start[0] + w + 50, red_box_start[1] + h + 50)
    cv2.rectangle(img, red_box_start, red_box_end, (0, 0, 255), 2)

    # 在紅色框左側新增一個綠色框，大小相同
    green_box_start = (red_box_start[0] - w - 50 - distance_between_boxes, red_box_start[1])
    green_box_end = (green_box_start[0] + w + 50, green_box_start[1] + h + 50)
    cv2.rectangle(img, green_box_start, green_box_end, (0, 255, 0), 2)

    # 繪製黃色框，與藍色框右側相鄰並保持相同大小
    yellow_box_start = (blue_box_end[0] + distance_between_boxes, blue_box_start[1])
    yellow_box_end = (yellow_box_start[0] + w + 50, yellow_box_start[1] + h + 50)
    cv2.rectangle(img, yellow_box_start, yellow_box_end, (0, 255, 255), 2)
    
    # 在黃色框右側新增一個橘色框，大小相同
    orange_box_start = (yellow_box_end[0] + distance_between_boxes, yellow_box_start[1])
    orange_box_end = (orange_box_start[0] + w + 50, orange_box_start[1] + h + 50)
    cv2.rectangle(img, orange_box_start, orange_box_end, (0, 165, 255), 2)
    

    # 檢查藍色框內是否有圖片
    blue_box_check = blue_box_start[0] < ox1 < blue_box_end[0] and blue_box_start[1] < oy1 < blue_box_end[1]

    # 檢查黃色框內是否有圖片，且只有 pic2 會被偵測
    yellow_box_check = yellow_box_start[0] < ox2 < yellow_box_end[0] and yellow_box_start[1] < oy2 < yellow_box_end[1]
    
    # 檢查橘色框內是否有圖片，且只有 pic2 會被偵測
    orange_box_check = orange_box_start[0] < ox3 < orange_box_end[0] and orange_box_start[1] < oy3 < orange_box_end[1]
    
    # 檢查紅色框內是否有圖片
    red_box_check = red_box_start[0] < ox4 < red_box_end[0] and red_box_start[1] < oy4 < red_box_end[1]
    
    # 檢查綠色框內是否有圖片
    green_box_check = green_box_start[0] < ox5 < green_box_end[0] and green_box_start[1] < oy5 < green_box_end[1]
    
    if yellow_box_check and not sound_played_yellow:
        correct_sound.play()  # 播放音效
        sound_played_yellow = True  # 标记音效已播放

    if orange_box_check and not sound_played_orange:
        correct_sound.play()  # 播放音效
        sound_played_orange = True

    if blue_box_check and not sound_played_blue:
        correct_sound.play()  # 播放音效
        sound_played_blue = True

    if red_box_check and not sound_played_red:
        correct_sound.play()  # 播放音效
        sound_played_red = True

    if green_box_check and not sound_played_green:
        correct_sound.play()  # 播放音效
        sound_played_green = True    
        
    if yellow_box_check and orange_box_check and blue_box_check and red_box_check and green_box_check:
     pygame.mixer.music.stop()  # 停止播放背景音乐
     print("Yes")  # Print "Yes" when pic2 is inside the yellow box
     win_sound.play()
     result = messagebox.askokcancel("You Win","Good Job!!")

     
     if result:
        restart_program()
        sound_played_yellow = False
        sound_played_orange = False
        sound_played_blue = False
        sound_played_red = False
        sound_played_green = False
        break  # 確保在重啟之前結束當前的 while 循環

    img[oy1:oy1 + h, ox1:ox1 + w] = pic1
    img[oy2:oy2 + h, ox2:ox2 + w] = pic2
    img[oy3:oy3 + h, ox3:ox3 + w] = pic3
    img[oy4:oy4 + h, ox4:ox4 + w] = pic4
    img[oy5:oy5 + h, ox5:ox5 + w] = pic5

    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()  # 退出 pygame
































