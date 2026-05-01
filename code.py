import pygame
from time import sleep
from random import randint

pygame.init()
screen= pygame.display.set_mode((601,601))  # màn hình 601x601, 601 chừa ra để thấy đường line rõ hơn
pygame.display.set_caption("Snake")  # tiêu đề
running=True

# các biến màu
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
clock=pygame.time.Clock()

# tọa độ rắn  
snakes= [[5,6],[5,7],[5,8]]
# hướng con rắn ban đầu (dùng lập trình cho con rắn chạy tự động)
direction= "right"
# quả táo
apple=[randint(0,19), randint(0,19)]
#táo vàng
golden_apple = None


# chữ
font_small = pygame.font.SysFont("arial",20)
font_big = pygame.font.SysFont("arial",50)
score=0
# biến dừng lại
pausing = False

gameovermusic = False
state = "menu"
logo = pygame.image.load("menu.png")
logo = pygame.transform.scale(logo, (601, 601))
play_button = pygame.Rect(250, 520, 150, 60)  # x, y, width, height
# thêm biến đếm thời gian
blink_timer = 0
while running:
    clock.tick(60)
    # vẽ nền cỏ
    for row in range(20):
        for col in range(20):
            if (row + col) % 2 == 0:
                color = (124,205,124)   # xanh đậm
            else:
                color = (152,251,152)   # xanh nhạt
            pygame.draw.rect(screen, color, (col*30, row*30, 30, 30))


    # vẽ giao diện ban đầu
    if state == "menu":
        blink_timer += 1
        screen.blit(logo, (screen.get_width()/2 - logo.get_width()/2, screen.get_height()/2 - logo.get_height()/2))
        # vẽ nút Play
        pygame.draw.rect(screen, GREEN, play_button)
        # hiệu ứng nhấp nháy chữ PLAY
        if (blink_timer // 30) % 2 == 0:  # đổi màu mỗi 30 khung hình
            play_txt = font_big.render("PLAY", True, WHITE)
        else:
            play_txt = font_big.render("PLAY", True, RED)

        screen.blit(play_txt, (play_button.x + play_button.width/2 - play_txt.get_width()/2,play_button.y + play_button.height/2 - play_txt.get_height()/2))

        # chỉ phát nhạc menu một lần
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("menu.wav")
            pygame.mixer.music.play(-1)  # -1 để lặp vô hạn

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                state = "playing"  # chuyển sang trạng thái chơi
                pausing = False
                score = 0
                snakes = [[5,6],[5,7],[5,8]]
                direction = "right"
                apple = [randint(0,19), randint(0,19)]
                gameovermusic = False
                # dừng nhạc menu
                pygame.mixer.music.stop()

    elif state == "playing":
        # lưu tọa độ x, y của đuôi, giá trị độc lập không bị thay đổi theo phần tử đuôi snakes (tạo 1 copy mới)
        tail_x = snakes[0][0]
        tail_y = snakes[0][1]

        # vẽ con rắn
        for snake in snakes:  # duyệt qua list snakes
            pygame.draw.rect(screen, BLUE1, (snake[0]*30, snake[1]*30, 30, 30))  # vẽ đầu con rắn hình vuông (2 phần đầu là vị trí, 2 phần sau là kích thước)
            pygame.draw.rect(screen, BLUE2, (snake[0]*30-4, snake[1]*30-4, 16, 16))  # vẽ sọc rắn
        head= snakes[-1]
        pygame.draw.circle(screen, WHITE, (head[0]*30+10, head[1]*30+10), 5)  # mắt trái
        pygame.draw.circle(screen, WHITE, (head[0]*30+20, head[1]*30+10), 5)  # mắt phải
        pygame.draw.circle(screen, BLACK, (head[0]*30+10, head[1]*30+10), 2)  
        pygame.draw.circle(screen, BLACK, (head[0]*30+20, head[1]*30+10), 2) 

        #vẽ quả táo đỏ
        pygame.draw.rect(screen, RED, (apple[0]*30, apple[1]*30, 30, 30))
        # vẽ cành táo
        pygame.draw.rect(screen, BROWN, (apple[0]*30 + 10, apple[1]*30 - 10, 10, 10))
        # vẽ lá táo
        pygame.draw.polygon(screen, GREEN, [
            (apple[0]*30 + 10, apple[1]*30 - 10),
            (apple[0]*30 + 10, apple[1]*30 - 15),
            (apple[0]*30, apple[1]*30 - 20)])
        
        # vẽ táo vàng
        if golden_apple:  # chỉ vẽ táo vàng khi nó tồn tại
            pygame.draw.rect(screen, (255, 215, 0), (golden_apple[0]*30, golden_apple[1]*30, 30, 30))  
            # cành táo
            pygame.draw.rect(screen, BROWN, (golden_apple[0]*30 + 10, golden_apple[1]*30 - 10, 10, 10))  
            # lá táo
            pygame.draw.polygon(screen, GREEN, [
                (golden_apple[0]*30 + 10, golden_apple[1]*30 - 10),
                (golden_apple[0]*30 + 10, golden_apple[1]*30 - 15),
                (golden_apple[0]*30, golden_apple[1]*30 - 20)])
            

        # check rắn chạm vào thân
        for i in range (len(snakes)-1):
            if snakes[-1][0] == snakes[i][0] and snakes[-1][1] == snakes[i][1]:
                pausing = True

        # vẽ màn hình game over
        if pausing == True:
            # tạo hình chữ nhật nền
            pygame.draw.rect(screen, BLACK, (60, 180, 480, 150))  # nền đen
            pygame.draw.rect(screen, WHITE, (60, 180, 480, 150), 3)  # viền trắng  
            # viết chữ
            game_over_txt = font_big.render("Game over, score:" +str(score), True, (255,255,0))
            press_space_txt = font_big.render("Press Space to continue", True, WHITE)
            screen.blit(game_over_txt, (screen.get_width()/2 - game_over_txt.get_width()/2, 200))
            screen.blit(press_space_txt, (screen.get_width()/2 - press_space_txt.get_width()/2, 250))
            
            # code này để kết thúc nhạc chỉ phát 1 lần
            if not  gameovermusic:
                pygame.mixer.music.load("thua.wav")  # nạp file nhạc vào
                pygame.mixer.music.play()
                gameovermusic = True

        # tính điểm

        # ăn táo đỏ +1
        if snakes[-1][0] == apple[0] and snakes[-1][1] == apple[1]: # check giá trị x, y có bằng nhau không (đầu rắn có chạm quả táo hay không)
            snakes.insert(0,[tail_x,tail_y])
            apple=[randint(0,19), randint(0,19)] # khi chạm thì random ra 1 apple mới
            score+=1
            pygame.mixer.music.load("an_tao.wav")  # nạp file nhạc vào
            pygame.mixer.music.play()  #phát file nhạc

            # xác suất 1/5 để sinh táo vàng, chỉ sinh táo vàng nếu chưa có
            if golden_apple is None and randint(1,5) == 1:
                golden_apple = [randint(0,19), randint(0,19)]
                while golden_apple == apple:  # tránh trùng
                    golden_apple = [randint(0,19), randint(0,19)]

        
        # ăn táo vàng +5
        if golden_apple and snakes[-1][0] == golden_apple[0] and snakes[-1][1] == golden_apple[1]:
            snakes.insert(0,[tail_x,tail_y])
            score += 5
            golden_apple = None  # ăn xong thì biến mất
            pygame.mixer.music.load("an_tao.wav")
            pygame.mixer.music.play()


        
        # draw score, Esc
        score_txt = font_small.render("Score:" +str(score), True, WHITE)
        screen.blit(score_txt, (5,5))
        Esc_txt = font_small.render("Press Esc to Quit", True, WHITE)
        screen.blit(Esc_txt, (5,25))

        # di chuyển rắn tự động
        if pausing == False:   # check xem nếu rắn không chạm cạnh thì di chuyển
            if direction == "right":
                snakes.append([snakes[-1][0]+1, snakes[-1][1]])
                snakes.pop(0)
            if direction == "left":
                snakes.append([snakes[-1][0]-1, snakes[-1][1]])
                snakes.pop(0)
            if direction == "up":
                snakes.append([snakes[-1][0], snakes[-1][1]-1])  # thêm 1 phần tử vào cuối có tọa độ x, y vào list snakes (đi lên thì x giữ nguyên, y giảm 1)
                snakes.pop(0)
            if direction == "down":
                snakes.append([snakes[-1][0], snakes[-1][1]+1])
                snakes.pop(0)
        
        # check chạm cạnh
        if snakes[-1][0] < 0 or snakes[-1][0] > 19 or snakes[-1][1] < 0 or snakes[-1][1] > 19:
            pausing = True

            

        sleep(0.09)  # lệnh này để con rắn chạy chậm lại (dừng màn hình, số càng lớn rắn càng chậm)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                
            if event.type == pygame.KEYDOWN:  # kiểm tra khi nhấn nút trên bàn phím
                if event.key == pygame.K_UP and direction!= "down":
                    direction = "up"
                if event.key ==pygame.K_DOWN and direction != "up":
                    direction = "down"
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                if event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                #phím Space chơi lại
                if event.key== pygame.K_SPACE and pausing== True:  
                    pausing = False  
                    snakes= [[5,6],[5,7],[5,8]] # reset lại rắn
                    direction= "right"  # reset lại hướng
                    apple=[randint(0,19), randint(0,19)]  # random lại quả táo
                    score = 0
                    gameovermusic = False
                    
                # phím Esc: thoát nhanh
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.display.flip()


pygame.quit()