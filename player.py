from settings import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'right', 0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)
    
        # movement 
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

        # health
        self.max_health = 100
        self.health = self.max_health
        self.last_hit_time = 0
        self.hit_cooldown = 400  # thời gian chịu sát thương tiếp theo (ms)
        self.is_hit = False

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.hit_cooldown:
            self.health -= amount
            self.last_hit_time = current_time
            self.is_hit = True
            # Kiểm tra nếu máu <= 0
            if self.health <= 0:
                self.health = 0
                self.die()

    def die(self):
        # Xử lý khi nhân vật chết
        pass
        # Bạn có thể thêm hiệu ứng chết hoặc kết thúc game ở đây

    def draw_health_bar(self, surface, pos):
        # Vẽ nền thanh máu (màu xám)
        background_rect = pygame.Rect(pos[0], pos[1], 50, 10)
        pygame.draw.rect(surface, (60, 60, 60), background_rect)

        # Vẽ phần máu hiện tại (màu đỏ)
        health_ratio = self.health / self.max_health
        fill_width = max(0, int(50 * health_ratio))  # Đảm bảo không âm
        fill_rect = pygame.Rect(pos[0], pos[1], fill_width, 10)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)

        # Vẽ viền (màu trắng)
        outline_rect = pygame.Rect(pos[0], pos[1], 50, 10)
        pygame.draw.rect(surface, (0, 0, 0), outline_rect, 1)

    def animate(self, dt):
        # get state 
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # animate
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        # Hiệu ứng nhấp nháy khi bị tấn công
        current_time = pygame.time.get_ticks()
        if self.is_hit and current_time - self.last_hit_time < self.hit_cooldown:
            if int((current_time - self.last_hit_time) / 100) % 2 == 0:  # Nhấp nháy mỗi 100ms
                self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
            else:
                # Tạo hiệu ứng trong suốt
                temp_surf = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])].copy()
                temp_surf.set_alpha(128)
                self.image = temp_surf
        else:
            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
            self.is_hit = False

    def update(self, dt):
        if self.health > 0:  # Chỉ di chuyển nếu còn sống
            self.input()
            self.move(dt)
            self.animate(dt)
        else:
            self.die()