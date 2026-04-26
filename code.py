import pygame
from time import sleep
from random import randint

pygame.init()
# Thiết lập giao diện
screen= pygame.display.set_mode((601,601))  # màn hình 601x601, 601 chừa ra để thấy đường line rõ hơn
pygame.display.set_caption("Snake")  # tiêu đề
running=True

# các biến màu
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
clock=pygame.time.Clock()

# tọa độ rắn  
snakes= [[5,6],[5,7],[5,8]]
# hướng con rắn ban đầu (dùng lập trình cho con rắn chạy tự động)
direction= "right"
# quả táo
apple=[randint(0,19), randint(0,19)]
# chữ
font_small = pygame.font.SysFont("sans",20)
font_big = pygame.font.SysFont("sans",50)
score=0
# biến dừng lại
pausing = False

while running:
    clock.tick(60)
    screen.fill(BLACK)

    # lưu tọa độ x, y của đuôi, giá trị độc lập không bị thay đổi theo phần tử đuôi snakes (tạo 1 copy mới)
    tail_x = snakes[0][0]
    tail_y = snakes[0][1]

    # vẽ lưới (1 ô lưới có kích thước khoảng 30x30)
    # for i in range (0,21):
    #     pygame.draw.line(screen, WHITE,(0,i*30),(600,i*30))  # vẽ đường thẳng nằm ngang
    #     pygame.draw.line(screen, WHITE, (30*i,0),(30*i,600))  # vẽ đường thẳng dọc

    # vẽ con rắn
    for snake in snakes:  # duyệt qua list snakes
        pygame.draw.rect(screen, BLUE1, (snake[0]*30, snake[1]*30, 30, 30))  # vẽ đầu con rắn hình vuông (2 phần đầu là vị trí, 2 phần sau là kích thước)
        pygame.draw.rect(screen, BLUE2, (snake[0]*30-4, snake[1]*30-4, 16, 16))  # vẽ sọc rắn

    #vẽ quả táo
    pygame.draw.rect(screen, RED, (apple[0]*30, apple[1]*30, 30, 30))

    # check rắn chạm vào thân
    for i in range (len(snakes)-1):
        if snakes[-1][0] == snakes[i][0] and snakes[-1][1] == snakes[i][1]:
            pausing = True

    # vẽ màn hình game over
    if pausing == True:
        game_over_txt = font_big.render("Game over, score:" +str(score), True, WHITE)
        press_space_txt = font_big.render("Press Space to continue", True, WHITE)
        screen.blit(game_over_txt, (50,200))
        screen.blit(press_space_txt, (50,300))

    # tính điểm
    if snakes[-1][0] == apple[0] and snakes[-1][1] == apple[1]: # check giá trị x, y có bằng nhau không (đầu rắn có chạm quả táo hay không)
        snakes.insert(0,[tail_x,tail_y])
        apple=[randint(0,19), randint(0,19)] # khi chạm thì random ra 1 apple mới
        score+=1
    
    # draw score
    score_txt = font_small.render("SCore:" +str(score), True, WHITE)
    screen.blit(score_txt, (5,5))

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

    sleep(0.1)  # lệnh này để con rắn chạy chậm lại (dừng màn hình, số càng lớn rắn càng chậm)

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
            if event.key== pygame.K_SPACE and pausing== True:  # khi đã thua và nhấn space
                pausing = False  
                snakes= [[5,6],[5,7],[5,8]] # reset lại rắn
                apple=[randint(0,19), randint(0,19)]  # random lại quả táo
                score = 0

    pygame.display.flip()


pygame.quit()