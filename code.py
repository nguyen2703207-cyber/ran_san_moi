import pygame
pygame.init()


# Thiết lập giao diện
screen= pygame.display.set_mode((600,602))  # màn hình 600x602, 602 chừa ra để thấy đường line rõ hơn
pygame.display.set_caption("Snake")  # tiêu đề
running=True
# các biến màu
GREEN=(0,200,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
clock=pygame.time.Clock()

# vẽ rắn 
snake= [0,1]
while running:
    clock.tick(60)
    screen.fill(BLACK)
    
    # vẽ lưới (1 ô lưới có kích thước khoảng 30x30)
    for i in range (0,21):
        pygame.draw.line(screen, WHITE,(0,i*30),(600,i*30))  # vẽ đường thẳng nằm ngang
        pygame.draw.line(screen, WHITE, (30*i,0),(30*i,600))  # vẽ đường thẳng dọc

    pygame.draw.rect(screen, GREEN, ()())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    pygame.display.flip()


pygame.quit()