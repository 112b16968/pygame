import pygame
import time
import os
import random
# 狀態和前置
pygame.init() #pygame初始化
pygame.font.init() #文字初始化
clock = pygame.time.Clock() #時間設置
window_height = 600  # 視窗高度
window_width = 1100  # 視窗寬度
windowSize = [window_width,window_height] #視窗大小
screen = pygame.display.set_mode(windowSize) #顯示視窗
pygame.display.set_caption('Dinosaur Game') #視窗名字
#顏色
WHITE = (255,255,255) 
BLACK = (0,0,0)

#幀數
FPS = 60

# 載入檔案 
# 圖片
# 小恐龍圖片
dino_start = pygame.image.load(os.path.join("DinoStart.png"))

dino_run = [pygame.image.load(os.path.join("DinoRun1.png")),
            pygame.image.load(os.path.join("DinoRun2.png"))]

dion_jump = pygame.image.load(os.path.join("DinoJump.png"))

dion_duck = [pygame.image.load(os.path.join("DinoDuck1.png")),
             pygame.image.load(os.path.join("DinoDuck2.png"))]

dion_dead = pygame.image.load(os.path.join("DinoDead.png")) 
# 障礙物圖片
# 陸地
small_cactus = [pygame.image.load(os.path.join("SmallCactus1.png")),
                pygame.image.load(os.path.join("SmallCactus2.png")),
                pygame.image.load(os.path.join("SmallCactus3.png"))]

large_cactus = [pygame.image.load(os.path.join("LargeCactus1.png")),
                pygame.image.load(os.path.join("LargeCactus2.png")),
                pygame.image.load(os.path.join( "LargeCactus3.png"))]
# 空中
bird = [pygame.image.load(os.path.join("Bird1.png")),
        pygame.image.load(os.path.join("Bird2.png"))]
# 場景
CLOUD = pygame.image.load(os.path.join("Cloud.png"))
trail = pygame.image.load(os.path.join("Track.png"))

# 聲音
DEATH_MUSIC = pygame.mixer.Sound(os.path.join("death_music.mp3"))
JUMP_MUSIC = pygame.mixer.Sound(os.path.join("JUMP_SOUND.mp3"))
COIN_MUSIC = pygame.mixer.Sound(os.path.join("COIN.mp3"))
#文字物件
class Text:
    def __init__(self , text , size , color , position=(0,0)) -> None: #接受四個參數 文字 大小 顏色 位置
        self.font = pygame.font.SysFont("freesansbold.ttf",size) # 設定用甚麼字形(字形,大小用size決定)
        self.surface = self.font.render(text,False,color) #用renden 方法將文字畫到視窗上 (內容 ,是否鋸齒化,內容顏色)
        self.rect = self.surface.get_rect()  #建立矩形物件將內容框起 目的要更好的定位文字位置
        self.rect.center = position #設定中心位置 位置由position決定
    def draw(self,screen): 
        screen.blit(self.surface,self.rect)  #透過blit將文字畫到視窗上 位置由rect決定

#雲朵物件
class Cloud:
    def __init__(self) -> None: #初始化設定
        self.image = CLOUD #載入圖片
        self.x = window_width + 10 #x初始位置設定在視窗寬度加上隨機位置
        self.y = random.randrange(50 ,200) 
        self.width = self.image.get_width() #設定圖片寬度
    def update(self): #更新
        self.x -= cloud_speed
        if self.x < -self.width: #當雲超出視窗外
            self.x = window_width + 10 #重新設定到初始位置
            self.y = random.randrange(50 ,200) #一樣
    def draw (self,screen): #畫出來
        screen.blit(self.image,(self.x,self.y)) #畫到視窗中

#玩家物件
class Dino:
    X_position = 80  # player X的座標
    Y_position = 290 # player Y的座標
    Y_position_DUCK = 340  #player 蹲下的起始值
    Y_JUMP = 7  #player 起跳的值
    def __init__(self) -> None:
        self.dino_duck = False  #蹲下條件
        self.dino_run = True    #跑的條件
        self.dino_jump = False  #跳的條件
        self.step_index = 0  # 腳步動畫
        self.jump_vel = self.Y_JUMP  # 跳上、下的速度

        # Load 圖檔
        self.duck_img_list = dion_duck  #蹲下的圖檔列表
        self.run_img_list = dino_run    #跑步的圖檔列表
        self.jump_img = dion_jump       #跳的圖檔
        self.image = self.run_img_list[0]  # 設定恐龍跑的第一步

        # 把恐龍腳色框列
        self.dino_rect = self.image.get_rect()
        #定位座標
        self.dino_rect.x = self.X_position  
        self.dino_rect.y = self.Y_position
    def run (self):
        #跑的函式
        self.image = self.run_img_list[self.step_index // 5]  # 依 step_index 決定恐龍的跑步圖片，每五個step_index換一張圖
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_position
        self.dino_rect.y = self.Y_position
        self.step_index += 1
    def duck(self):
        #蹲下的函式
        self.image = self.duck_img_list[self.step_index // 5]  # 依 step_index 決定恐龍的蹲下圖片，每五個step_index換一張圖
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_position
        self.dino_rect.y = self.Y_position_DUCK
        self.step_index += 1
    def jump(self):
        #跳的函式
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4  # 依目前的跳躍速度來移動小恐龍的y座標值
            self.jump_vel -= 0.5  # 若jump_vel小於0則代表小恐龍逐漸往下掉
        if self.jump_vel < - self.Y_JUMP: #當跳躍速度小於初始跳躍速度執行下面
            self.dino_jump = False #關掉
            self.jump_vel = self.Y_JUMP
    def update(self, user_input):
        #更新
        if user_input[pygame.K_UP] or user_input[pygame.K_SPACE] and not self.dino_jump:  #當按下上跟當不是在跳的條件下啟動
            self.dino_duck = False  
            self.dino_run = False
            self.dino_jump = True
            JUMP_MUSIC.play()
        elif user_input[pygame.K_DOWN] and not self.dino_jump:  #當按下下跟當不是在蹲下的條件下啟動
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or user_input[pygame.K_DOWN]): #當不在跳跟蹲下的條件下啟動
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        # 以變數判斷小恐龍目前該做甚麼動作
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0
    def draw(self, screen):   
        #畫出恐龍
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
#敵人基本物件
class Enemy:
    def __init__(self , imagelist , type) -> None:
        self.image = imagelist  #敵人類型
        self.type = type   #敵人種類
        self.rect = self.image[self.type].get_rect()  #將敵人框起來
        self.rect.x = window_width   #設定位置
    def update(self):
        self.rect.x -= evemy_speed  #敵人速度
    def draw(self, screen):
        screen.blit(self.image[self.type], (self.rect.x, self.rect.y))  #畫出來
#大仙人掌物件 並且繼承敵人基本物件
class  Largecactus(Enemy):
    def __init__(self, imagelist) -> None:
        self.type = random.randrange(0,2) #隨機選擇圖片
        super().__init__(imagelist, self.type)   #繼承物件類別
        self.rect.y = 300   #設定Y座標
#小仙人掌物件 並且繼承敵人基本物件      
class  Smallcactus(Enemy):
    def __init__(self, imagelist) -> None:
        self.type = random.randrange(0,2) #隨機選擇圖片
        super().__init__(imagelist, self.type)   #繼承物件類別
        self.rect.y = 325   #設定Y座標
#鳥物件 並且繼承敵人基本物件
class  Bird(Enemy):
    def __init__(self, imagelist) -> None:
        self.type = 0  #選擇圖片
        super().__init__(imagelist, self.type)   #繼承物件類別
        self.rect.y = 250   #設定Y座標
        self.rect.x = window_width #設定X座標
        self.index = 0 #飛行型態變化
    def draw(self, screen):
        if self.index >= 10 :
            self.index = 0
        screen.blit(self.image[self.index // 6], self.rect)  # 以index決定飛行的動作，每五個index為一種飛行動作
        self.index += 1
cloud = Cloud() #生成一朵雲
player = Dino()  #生成一隻恐龍
enemys = []

# 物件座標位置
start_text_position1 = (window_width/2,window_height/2) #開始畫面文字位置
start_text_position2 = (window_width/2,window_height/2 +100) #開始畫面文字位置
start_picture_position = (window_width/2-20,window_height/2-140) #開始畫面圖片位置

global game_speed
game_speed = 15 #背景速度
evemy_speed = 15 #敵人速度
cloud_speed = 5  #雲朵速度
#跑道位置
trail_positionX = 0 
trail_positionY = 360
#分數
global points
points = 0

start_screen = True
done = False
while not done :
    # 遊戲事件
    #開始介面
    if start_screen :
        
        #開始畫面
       
        screen.fill(WHITE)
        start_text = Text("Press Space to Start", 40, BLACK , start_text_position1) #設立變數 傳入參數給class Text
        start_point = Text(f"Your Point is {points}" , 40 , BLACK ,start_text_position2 )
        start_text.draw(screen)  #畫出內容到視窗上
        start_point.draw(screen)
        screen.blit(dino_run[0],start_picture_position) #畫出圖片 (圖片,位置)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            #進入遊戲畫事件
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen = False
                    points = 0 # 分數重新計算
                    enemys.clear()  # 為了讓重新開始時，不要馬上碰到障礙物
                    DEATH_MUSIC.stop()
                elif event.key == pygame.K_ESCAPE:
                    done = True
     
                
    #遊戲介面背景
    else:
        #背景
        screen.fill(WHITE)
        image_width = trail.get_width()
        screen.blit(trail,(trail_positionX,trail_positionY))
        screen.blit(trail,(image_width + trail_positionX,trail_positionY))
        trail_positionX -= game_speed #背景移動 

        if trail_positionX <= -image_width: #當跑道移動到視窗外時 會再次印出新的在跑道的尾巴
            screen.blit(trail,(window_width + trail_positionX , trail_positionY))
            trail_positionX = 0

        #雲朵生成
        cloud.update()
        cloud.draw(screen)
        #分數
        points += 1 #
        if points % 1000 == 0: #難度增加
            COIN_MUSIC.play()
            game_speed += 1
        point_position = (1000,40)
        point_text = Text(f"Point:{points}" , 30 , BLACK ,point_position)  #創建一個新的文字
        point_text.draw(screen)  #畫出分數到視窗上
        #玩家
        user_input = pygame.key.get_pressed()  ##獲取玩家鍵盤輸入的資訊
        player.update(user_input)  # 依據玩家指令更新恐龍的動作
        player.draw(screen)  # 將恐龍換上

        #敵人
        if len(enemys) == 0:
            choice = random.randrange(0,3)
            if choice == 0:
                enemys.append(Smallcactus(small_cactus)) 
            elif choice == 1 :
                enemys.append(Largecactus(large_cactus))
            elif choice == 2:
                enemys.append(Bird(bird))
        
        for enemy in enemys:
            enemy.update()  # 障礙物移動
            enemy.draw(screen)  # 更新動畫
            if enemy.rect.x < -enemy.rect.width:
                enemys.remove(enemy)
            if player.dino_rect.colliderect(enemy.rect):
                DEATH_MUSIC.play()
                start_screen = True
                
        #碰撞事件

        
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    pygame.display.flip() #畫面更新
pygame.quit()



