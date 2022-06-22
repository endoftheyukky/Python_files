#スコアの表示
#ターゲットに当たる度にスコアが変化する 
#ドロップターゲットを設置し、当たるとスコアが増え、全て消えると復活する
#プランジャーで初速度を決定し、ボールを発射させる
#斜めに設置された壁で跳ね返る(曖昧な判定)
#パドルでの衝突位置によって、跳ね返る角度を変更する
#側面の壁のレイアウトを変更し、左右にアウトレーンを作る



from tkinter import Tk, Canvas
from dataclasses import dataclass, field
import time



BOX_LEFT = 100
BOX_TOP = 100
BOX_WIDTH = 800
BOX_HEIGHT = 1000

DURATION = 0.01
 
PADDLE_x0= BOX_LEFT+200
PADDLE_y0 = BOX_TOP+800
PADLE_WIDTH = 100
PADDLE_HEIGHT = 10
PAD_VX = 0

BALL_X0=715+BOX_LEFT
BALL_Y0=895+BOX_TOP

BALL_VX = -6
BALL_VY = -17.6

BLOCK_X = 10 + BOX_LEFT
BLOCK_Y = 60 + BOX_TOP
BLOCK_W = 10
BLOCK_H = 30

CANVAS_WIDTH = BOX_LEFT + BOX_WIDTH + 200
CANVAS_HEIGHT = BOX_TOP + BOX_HEIGHT

SCORE = 0

a = 0.17
e1=1.1
e2=0.9

BAR_x0 = 890  #速度ゲージ
BAR_y0 = 700
BAR_VY = 5
              


class CustomCanvas(Canvas):
    def __init__(self,width=CANVAS_WIDTH,height=CANVAS_HEIGHT,bg="lightgray"):
        super().__init__(tk,width=width,height=height+BOX_TOP,bg=bg)
        self.pack()



@dataclass
class MovingObject:
    id: int
    x: int
    y: int
    w: int
    h: int
    vx: int
    vy: int


    def redraw(self):     
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.w, self.y + self.h)


    def move(self):
        pass




class Ball(MovingObject):
    def __init__(self,id,x,y,d,vx,vy):
        super().__init__(id,x,y,d,d,vx,vy)
        self.d = d
 

    def move(ball):
        ball.vy+=a
        ball.x+=ball.vx
        ball.y+=ball.vy




class Paddle(MovingObject):
    def __init__(self,id,x,y,w,h,vx):
        super().__init__(id,x,y,w,h,vx,0)


    def move(self):
        self.x += self.vx


    def set_v(self,v):
        self.vx = v

        
    def stop(self):
        self.vx = 0



@dataclass
class Block:
    id: int
    x: int
    y: int
    w: int
    h: int
    c: str
    

    def make_block(x,y,w=40,h=120,c="red"):
        id=canvas.create_rectangle(x+BOX_LEFT-5,y+BOX_TOP-5,x+BOX_LEFT+w-5,y+BOX_TOP+h-5,fill=c,outline="black",width=2)
        return Block(id,x,y,w,h,c)


    def delete(self):
        canvas.delete(self.id)

    def make_walls(ox,oy,width,height,c,wide):
        canvas.create_rectangle(ox,oy,ox+width,oy+height,fill=c,width=wide)




class Bar(MovingObject):
    def __init__(self,id,x,y,w,h,vx,b):
        super().__init__(id,x,y,w,h,vx,0)
        self.b = b


    def move(bar):
        bar.h-=bar.vy
        if bar.h<=-390: #上限の設定
            bar.h=-390






class Box:
    def __init__(self,x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.balls = []
        self.paddle = []
        self.blocks = []
        self.paddle_v = 7
        self.id = canvas.create_rectangle(x, y, x + w, y + h, fill="white")
        self.duration = duration
        self.b = 0
        self.score = 0
        self.score_txt = None


    def create_ball(self, x, y, d,vx,vy):  # ボールを生成し、初期描画する
        id = canvas.create_oval(x, y, x + d, y + d, fill="gray")
        return Ball(id, x, y, d,vx,vy)


    def create_paddle(self, x, y, w, h,vx):  # パドルを初期表示し、戻す。
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")
        return Paddle(id, x, y, w, h,vx )


    def create_block(self, x, y, w, h,c = "red"):   # ブロックを初期表示し、戻す。
        id = canvas.create_rectangle(x, y, x + w, y + h,
                                     fill=c, outline="black",width = 3)
        return Block(id, x, y, w, h, c)


    def create_bar(self,x,y,w,h,c="yellow"):
        id=canvas.create_rectangle(x,y+h,x+w,y+h,fill=c,outline=c)
        return Bar(id,x,y,w,h,0,self.b)


    def check_wall(self, ball):  # ボールの壁での反射
        if ball.y <= self.north or ball.y + ball.w >= self.south:
            ball.vy = - ball.vy - a


    def check_paddle(self,paddle,ball):
        center = self.ball.x + self.ball.w/2
        if center >= self.paddle.x and center <= self.paddle.x + self.paddle.w:
            if self.ball.y + self.ball.w >= self.paddle.y:
                self.ball.vy = -self.ball.vy
                print(self.ball.vy)


    def check_blocks(self, ball):  # ブロックを消す
        center = ball.x + ball.w/2
        for block in self.blocks:
            if center >= block.x and center <= block.x + block.w:
                if self.ball.y <= block.y + block.h:
                    self.ball.vy = - self.ball.vy
                    block.delete()
                    self.blocks.remove(block)



    def right_paddle(self, event):
        self.paddle.set_v(self.paddle_v)


    def left_paddle(self, event):
        self.paddle.set_v(-self.paddle_v)


    def stop_paddle(self, event):
        self.paddle.stop()

    
    def stop_bar(self,event): 
        self.bar.vy=0
        self.bar.b = 1
    

    def extend_bar(self,event):
        self.bar.vy = BAR_VY



    def set(self):  # ボールを生成し、リストに入れる
        canvas.create_polygon(BOX_LEFT+5,BOX_TOP,BOX_LEFT+5,BOX_TOP+BOX_HEIGHT,BOX_LEFT+BOX_WIDTH,BOX_TOP+BOX_HEIGHT,BOX_LEFT+BOX_WIDTH,BOX_TOP+200,BOX_LEFT+600,BOX_TOP,fill="gainsboro",outline="black",width=10)    
        #ボックスの生成


        canvas.create_polygon(BOX_LEFT+685,BOX_TOP+920,BOX_LEFT+770,BOX_TOP+920,BOX_LEFT+770,BOX_TOP+930,BOX_LEFT+740,BOX_TOP+930,BOX_LEFT+740,BOX_TOP+995,BOX_LEFT+715,BOX_TOP+995,BOX_LEFT+715,BOX_TOP+930,BOX_LEFT+685,BOX_TOP+930,fill="silver",outline="black",width=2)
        #発射台の生成


        canvas.create_text(BOX_LEFT+895,BOX_TOP+850,text="SCORE",font=("FixedSys",30))


        canvas.create_line(BOX_LEFT+100,BOX_TOP+645,BOX_LEFT+100,BOX_TOP+748,width=8)
        canvas.create_line(BOX_LEFT+100,BOX_TOP+745,BOX_LEFT+200,BOX_TOP+850,width=8)


        canvas.create_line(BOX_LEFT+545,BOX_TOP+645,BOX_LEFT+545,BOX_TOP+748,width=8)
        canvas.create_line(BOX_LEFT+545,BOX_TOP+745,BOX_LEFT+445,BOX_TOP+850,width=8)

        
        canvas.create_rectangle(BOX_LEFT+880,BOX_TOP+700,BOX_LEFT+920,BOX_TOP+300,fill="black")   #ゲージの囲い
        canvas.create_text(BOX_LEFT+895,BOX_TOP+720,text="SPEED",font=("FixedSys",25))            
        canvas.create_text(BOX_LEFT+945,BOX_TOP+325,text="MAX",fill="black",font=("FixedSys",24))


        canvas.create_rectangle(650+BOX_LEFT,250+BOX_TOP,650+BOX_LEFT+10,250+BOX_TOP+750,fill="black",width=1)


        self.paddle = self.create_paddle(PADDLE_x0,PADDLE_y0,PADLE_WIDTH,PADDLE_HEIGHT,PAD_VX)


        self.ball = self.create_ball(BALL_X0,BALL_Y0,25,BALL_VX,BALL_VY)


        self.bar = self.create_bar(885+BOX_LEFT,695+BOX_TOP,30,-1,c="yellow")

  
        self.score_txt = canvas.create_text(BOX_LEFT+900,BOX_TOP+900,text=self.score,font=("FixedSys",40),tag="score01")  
    


        self.blocks=[self.create_block(150+BOX_LEFT,370,50,30,"white"), #blockの生成
        self.create_block(300+BOX_LEFT,550+BOX_TOP,50,30,"white"),
        self.create_block(250+BOX_LEFT,200+BOX_TOP,50,30,"white"),
        self.create_block(480+BOX_LEFT,300+BOX_TOP,50,30,"white"),      
        self.create_block(380+BOX_LEFT,400+BOX_TOP,50,30,"white"),]

        self.d_blocks1=[self.create_block(BLOCK_X,BLOCK_Y+400,BLOCK_W+10,BLOCK_H),
        self.create_block(BLOCK_X,BLOCK_Y+450,BLOCK_W+10,BLOCK_H),
        self.create_block(BLOCK_X,BLOCK_Y+500,BLOCK_W+10,BLOCK_H),]

        self.d_blocks2=[self.create_block(BLOCK_X+620,BLOCK_Y+400,BLOCK_W+10,BLOCK_H),
        self.create_block(BLOCK_X+620,BLOCK_Y+450,BLOCK_W+10,BLOCK_H),
        self.create_block(BLOCK_X+620,BLOCK_Y+500,BLOCK_W+10,BLOCK_H),]


        canvas.bind_all("<KeyPress-Right>", self.right_paddle)
        canvas.bind_all("<KeyRelease-Right>", self.stop_paddle)
        canvas.bind_all("<KeyPress-Left>", self.left_paddle)
        canvas.bind_all("<KeyRelease-Left>", self.stop_paddle)

        canvas.bind_all("<KeyPress-space>",self.extend_bar)  #プランジャー操作
        canvas.bind_all("<KeyRelease-space>",self.stop_bar)


    def animate(self):
        c = 0
        while True:
            movingObjs = [self.paddle,self.ball,self.bar]
        
            if self.bar.b == 0:
                self.bar.move()


            if self.bar.b == 1:
                if c==0:
                    self.ball.vy -=0.002*abs(self.bar.h) #プランジャーによる初速度の決定
                for obj in movingObjs:
                    obj.move()

                if self.ball.x>=BOX_LEFT+645: #右側
                    if self.ball.y+self.ball.vy<=BOX_TOP+245:
                        if self.ball.vx>0:
                            if self.ball.x+self.ball.vx<=BOX_LEFT+5 or self.ball.x+self.ball.vx>=BOX_LEFT+645:
                                self.ball.vx=-self.ball.vx        

                    else:
                        if self.ball.x+self.ball.vx<=BOX_LEFT+5 or self.ball.x+self.ball.vx>=BOX_LEFT+645:
                            self.ball.vx=-self.ball.vx               
        
                if self.ball.x<650:                               #左側
                    if self.ball.x+self.ball.vx<=BOX_LEFT+5 or self.ball.x+self.ball.vx>=BOX_LEFT+655:
                        self.ball.vx=-e2*self.ball.vx

                if self.ball.y+self.ball.vy<=BOX_TOP+10: #天井
                    self.ball.vy=-e2*(self.ball.vy+a)
    
                if self.ball.y+self.ball.vy>=BOX_TOP+995:  #床
                    canvas.create_text(BOX_LEFT+345,BOX_TOP+470,text="Game Over",fill="crimson",font=("FixedSys",60))
                    break
        
                if (BOX_LEFT+100<=self.ball.x+self.ball.vx<=BOX_LEFT+200 and self.ball.y<=self.ball.x+self.ball.vx+BOX_LEFT+645<=self.ball.y+self.ball.vy) or (BOX_LEFT+445<=self.ball.x+self.ball.vx<=BOX_LEFT+545 and self.ball.y<=-(self.ball.x+self.ball.vx)+BOX_LEFT+1395<=self.ball.y+self.ball.vy): #斜めの壁
                    self.ball.vy=-e1*(self.ball.vy+a)
                    self.ball.vx=-e1*(self.ball.vy+a)

                if BOX_TOP+645<=self.ball.y<=BOX_TOP+748 and BOX_LEFT+100<=self.ball.x<=BOX_LEFT+545 and (self.ball.x+self.ball.vx>BOX_LEFT+545 or self.ball.x+self.ball.vx<BOX_LEFT+100): #斜めの上
                    self.ball.vx=-e2*self.ball.vx
        
                if BOX_TOP+645<=self.ball.y<=BOX_TOP+748 and (BOX_LEFT+5<self.ball.x<BOX_LEFT+100 or BOX_LEFT+545<self.ball.x<BOX_LEFT+645) and (BOX_LEFT+100<=self.ball.x+self.ball.vx<=BOX_LEFT+545):
                    self.ball.vx=-e2*self.ball.vx
        

                if(self.ball.y+self.ball.d>=self.paddle.y\
                    and self.paddle.x<=self.ball.x<=self.paddle.x+self.paddle.w):
                    self.ball.vy=-e1*(self.ball.vy+a)           
                    if abs(self.ball.vy)>15:
                        if self.ball.vy>0:
                            self.ball.vy=15 
                        if self.ball.vy<15:
                            self.ball.vy=-15                              
                    self.ball.vx=(1+0.02*abs(self.ball.x-(2*self.paddle.x+self.paddle.w)/2))*self.ball.vx
                    if abs(self.ball.vx)>15:     #最高速度の設定
                        if self.ball.vx>0:
                            self.ball.vx=15
                        if self.ball.vx<0:
                            self.ball.vx=-15
                                                                      #パドルの中心からずれるほどx方向の速度の絶対値が大きくなる
 
        
                for block in self.blocks:                  #通常ブロックとの衝突判定
                    if(block.y<=self.ball.y<=block.y+block.h and block.x<=self.ball.x<=block.x+block.w):
                        if self.ball.vy > self.ball.vx:
                            self.ball.vy=-e2*(self.ball.vy+a)
                        else:
                            self.ball.vx=-e2*(self.ball.vx)
                        self.score+=10
                        canvas.delete("score01")
                        canvas.create_text(BOX_LEFT+895,BOX_LEFT+895,text=self.score,font=("FixedSys",40),tag="score01")
            
            
                for block in self.d_blocks1:            #ドロップターゲットとの衝突判定  
                    if(block.y<=self.ball.y<=block.y+block.h and block.x<=self.ball.x<=block.x+block.w):
                        if self.ball.vy > self.ball.vx:
                            self.ball.vy=-e2*(self.ball.vy+a)
                        else:
                            self.ball.vx=-e2*(self.ball.vx)
                        block.delete()
                        self.d_blocks1.remove(block)
                        self.score+=30
                        canvas.delete("score01")
                        canvas.create_text(BOX_LEFT+895,BOX_TOP+895,text=self.score,font=("FixedSys",40),tag="score01")
                

                    if self.d_blocks1==[]:                                                     #全て消えたら復活
                        self.d_blocks1=[self.create_block(BLOCK_X,BLOCK_Y+400,BLOCK_W+10,BLOCK_H),
                        self.create_block(BLOCK_X,BLOCK_Y+450,BLOCK_W+10,BLOCK_H),
                        self.create_block(BLOCK_X,BLOCK_Y+500,BLOCK_W+10,BLOCK_H),]

                        self.score+=100
                        canvas.delete("score01")
                        canvas.create_text(BOX_LEFT+895,BOX_TOP+895,text=self.score,font=("FixedSys",40),tag="score01")


                for block in self.d_blocks2:            #ドロップターゲットとの衝突判定  
                    if(block.y<=self.ball.y<=block.y+block.h and block.x<=self.ball.x<=block.x+block.w):
                        if self.ball.vy > self.ball.vx:
                            self.ball.vy=-e2*(self.ball.vy+a)
                        else:
                            self.ball.vx=-e2*(self.ball.vx)
                        block.delete()
                        self.d_blocks2.remove(block)
                        self.score+=30
                        canvas.delete("score01")
                        canvas.create_text(BOX_LEFT+895,BOX_TOP+895,text=self.score,font=("FixedSys",40),tag="score01")


                        if self.d_blocks2==[]:                                                 #全て消えたら復活
                            self.d_blocks2=[self.create_block(BLOCK_X+620,BLOCK_Y+400,BLOCK_W+10,BLOCK_H),
                            self.create_block(BLOCK_X+620,BLOCK_Y+450,BLOCK_W+10,BLOCK_H),
                            self.create_block(BLOCK_X+620,BLOCK_Y+500,BLOCK_W+10,BLOCK_H),]

                            self.score+=100
                            canvas.delete("score01")
                            canvas.create_text(BOX_LEFT+895,BOX_TOP+895,text=self.score,font=("FixedSys",40),tag="score01")

                c += 1
     
            for obj in movingObjs:
                obj.redraw()
                

            time.sleep(DURATION)
            tk.update()
     

tk=Tk()
canvas = CustomCanvas()




box = Box(BOX_LEFT,BOX_TOP,BOX_WIDTH,BOX_HEIGHT,DURATION)
box.set()
box.animate()


tk.mainloop() 




  