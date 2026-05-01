import pygame, sys,random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(8,9), Vector2(9,9), Vector2(10,9)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                        screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1  or  previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)



    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down


    def move_snake(self):
        # Nếu rắn vừa ăn fruit
        if self.new_block == True:
            # Copy lại toàn bộ thân rắn, không bỏ đuôi
            body_copy = self.body[:]
            # Thêm đầu mới vào vị trí đầu list
            body_copy.insert(0, body_copy[0] + self.direction)
            # Cập nhật lại thân rắn
            self.body = body_copy[:]
            # Đổi self.new_block thành false để rắn không luôn dài ra mãi mà chỉ dài ra 1 block
            self.new_block = False
        else:
            # Di chuyển bình thường:
            # Bỏ đuổi
            body_copy = self.body[:-1]
            # Thêm đầu mới vào trước
            body_copy.insert(0,body_copy[0] + self.direction)
            # Cập nhật lại thân rắn
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(8, 9), Vector2(9, 9), Vector2(10, 9)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self):
        # Tạo vị trí ngẫu nhiên ban đầu cho fruit
        self.randomize()

    def draw_fruit(self):
        # Đổi tọa độ ô của fruit sang tọa độ pixel
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)  # trừ 1 do có trường hợp bằng 20 thì sẽ bị nằm ngoài màn hình
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        # Cập nhật game sau mỗi khoảng thời gian
        self.snake.move_snake()
        # Kiểm tra rắn có ăn fruit không
        self.check_collision()
        # Kiểm tra rắn có thua không
        self.check_fail()

    def draw_element(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()


    def check_collision(self):
        # Nếu vị trí fruit trùng với đầu rắn thì nghĩa là rắn ăn fruit
        if self.fruit.pos == self.snake.body[0]:
        # Random lại fruit ở vị trí mới
            self.fruit.randomize()
        # Báo cho rắn dài ra
            self.snake.add_block()
        # Phát tiếng ăn táo
            self.snake.play_crunch_sound()

        # kiểm tra xem táo có spawn ngay thân rắn không, nếu có thì spawn lại chỗ khác
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # Kiểm tra rắn đụng tường
        if not 0 <= self.snake.body[0].x <= cell_number - 1 or not 0 <= self.snake.body[0].y <= cell_number - 1:
            self.game_over()

        # Kiểm tra tự cắn chính nó
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self):
        # Vẽ cỏ
        grass_color =(167,209,61)
        for  row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
                        
    def game_over(self):
        self.snake.reset()

    def draw_score(self):# tạo bảng điểm
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True ,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + apple_rect.width,apple_rect.height )

        pygame.draw.rect(screen,(255,255,255),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect,2)



pygame.init()
# kích thước ô
cell_size = 40
# số lượng ô
cell_number = 20
screen= pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
clock=pygame.time.Clock()
# Tạo sự kiện riêng để rắn tự di chuyển theo thời gian
SCREEN_UPDATE = pygame.USEREVENT
# Cứ mỗi 150 mili giây thì tạo ra SCREEN_UPDATE
pygame.time.set_timer(SCREEN_UPDATE, 150)
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('font/PoetsenOne-Regular.ttf', 25)
main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)


    screen.fill((175,215,70))
    main_game.draw_element()
    pygame.display.update()
    clock.tick(60)
