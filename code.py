import pygame
from time import sleep
pygame.init()


# Thiết lập giao diện
screen= pygame.display.set_mode((601,601))  # màn hình 601x601, 601 chừa ra để thấy đường line rõ hơn
pygame.display.set_caption("Snake")  # tiêu đề
running=True
# các biến màu
GREEN=(0,255,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
clock=pygame.time.Clock()

# tọa độ rắn  
snakes= [[5,6],[5,7],[5,8]]
# hướng con rắn ban đầu (dùng lập trình cho con rắn chạy tự động)
direction= "right"
while running:
    clock.tick(60)
    screen.fill(BLACK)
    
    # vẽ lưới (1 ô lưới có kích thước khoảng 30x30)
    for i in range (0,21):
        pygame.draw.line(screen, WHITE,(0,i*30),(600,i*30))  # vẽ đường thẳng nằm ngang
        pygame.draw.line(screen, WHITE, (30*i,0),(30*i,600))  # vẽ đường thẳng dọc

    # vẽ con rắn
    for snake in snakes:  # duyệt qua list snakes
        pygame.draw.rect(screen, GREEN, (snake[0]*30, snake[1]*30, 30, 30))  # vẽ đầu con rắn hình vuông (2 phần đầu là vị trí, 2 phần sau là kích thước)

    # di chuyển rắn tự động
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

    sleep(0.05)  # lệnh này để con rắn chạy chậm lại (dừng màn hình, số càng lớn rắn càng chậm)

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
                pass

    pygame.display.flip()


pygame.quit()