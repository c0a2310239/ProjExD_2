import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
delta_dic = {                      #練習1:移動量と押下キーの辞書
    pg.K_UP:(0,-5), 
    pg.K_DOWN:(0,5), 
    pg.K_LEFT:(-5,0), 
    pg.K_RIGHT:(5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect, または、爆弾Rectの画面外判定用の関数
    引数:こうかとんRect、または、爆弾Rect
    戻り値:横方向判定結果、縦方向判定結果（True:画面内/False:画面外）                     
    """
    yoko, tate= True, True
    
    if obj_rct.left < 0 or WIDTH < obj_rct.right:                #練習3
        yoko = False
    
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bm_img = pg.Surface((20, 20))
    bm_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bm_img, (255,0,0), (10,10), 10)       #練習2:爆弾の設定
    bm_rct = bm_img.get_rect()
    bm_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bm_vx, bm_vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bm_rct):       #練習4:ゲームオーバー判定
            blackout(kk_rct, bm_rct, screen)
            print("Game Over")
            return
        
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k,v in delta_dic.items():    #練習1:コードの簡略化
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                change()

       
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])          #練習3
        screen.blit(kk_img, kk_rct)
        bm_rct.move_ip(bm_vx, bm_vy)            #練習2:爆弾の描画と爆弾を動かす
        screen.blit(bm_img,bm_rct)
        yoko, tate = check_bound(bm_rct)     #練習3
        if not yoko:
            bm_vx *= -1
        if not tate:
            bm_vy *= -1
        
        pg.display.update()
        tmr += 1
        clock.tick(50)

def change():
    """
    引数 :
    戻り値 :なし
    概要:辞書でx,yの増減とrotozoomで回転させたこうかとんの画像を紐づけ
    押下キーによって対応したこうかとんの画像を表示する
    """

    #change_dic = {
    #    (0, 0):pg.transform.rotozoom(kk_img, 0, 1.0), #デフォルト
    #    (-5, 0):pg.transform.rotozoom(kk_img, 0, 1.0),#左
    #    (-5, +5):pg.transform.rotozoom(kk_img, 45, 1.0),#左下
    #    (0, +5):pg.transform.rotozoom(kk_img, 90, 1.0),#下
    #    (+5, +5):pg.transform.rotozoom(kk_img, 135, 1.0),#右下
    #    (+5,0):pg.transform.rotozoom(kk_img, 180, 1.0),#右
    #    (-5, -5):pg.transform.rotozoom(kk_img, -45, 1.0),#左上
    #    (0, -5):pg.transform.rotozoom(kk_img, -90, 1.0),#上
    #    (+5, -5):pg.transform.rotozoom(kk_img, -135, 1.0)#右上
    #}
    return 0
  

def blackout(kk_rct,bm_rct,screen):
    """
    引数: こうかとん:rect, 爆弾:rect, screen:int
    戻り値: なし
    概要:ゲームオーバーになったときに画面をブラックアウトし、
    Game Overの文字を表示する関数
    """
    bk_img = pg.image.load("fig/8.png")   #泣きこうかとんをロード
    bk_font = pg.font.Font(None, 80)       #フォントサイズを80に設定
    go = bk_font.render("Game Over", True, (255, 255, 255))  #白字でGameOverと書かれたSurfaceインスタンスを生成
    
    if kk_rct.colliderect(bm_rct):  
        screen.fill((0, 0, 0))   #スクリーンを暗転
        screen.blit(go, [800, 450])   #Game Overを描画
        screen.blit(bk_img, [750,450])   #泣いているこうかとんを表示
    
    pg.display.update()
    time.sleep(5)         #五秒待つ

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
