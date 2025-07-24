import pygame 
import time 
import random
pygame.font.init()

POWERUP_WIDTH = 10
POWERUP_HEIGHT = 20
POWERUP_VEL = 2
MAX_POWER_LEVEL = 3

BULLET_TIMER = 0
BULLET_WIDTH = 10
BULLET_HEIGHT = 7
BULLET_DELAY = 15

SCORE_VAL = 0

STAR_WIDTH = 15
STAR_HEIGHT = 20
STAR_VEL = 3

PLAYER_VEL = 5
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("C:/Users/aksha/python/FirstGame/space.jpg"), (WIDTH, HEIGHT))

start_time = time.time()
FONT = pygame.font.SysFont("comicsans", 20)

def draw(player, elapsed_time, stars, bullets, power_ups, power_level):
    WIN.blit(BG, (0, 0))

    score = FONT.render(f"Score: {round(SCORE_VAL)}", 1, "white")
    WIN.blit(score, (900, 10))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s" , 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    level = FONT.render(f"Power Level: {round(power_level)}", 1, "green")
    WIN.blit(level, (850, 30))

    for bullet in bullets:
        pygame.draw.rect(WIN, "red", bullet)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    for p in power_ups:
        pygame.draw.rect(WIN, "green", p)

    pygame.display.update()

def main():
    global BULLET_TIMER 
    global SCORE_VAL 

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False
    bullets = []

    powerups = []
    powerup_timer = 0
    powerup_delay = 720
    power_level = 1

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if power_level <= 3:
            powerup_timer += 1
            if powerup_timer >= powerup_delay:
                powerup_x = random.randint(0, WIDTH - POWERUP_WIDTH)
                power = pygame.Rect(powerup_x, -POWERUP_HEIGHT, POWERUP_WIDTH, POWERUP_HEIGHT)
                powerups.append(power)
                powerup_timer = 0

        BULLET_TIMER += 1
        if BULLET_TIMER >= BULLET_DELAY:
            if power_level == 1:
                bullets.append(pygame.Rect(player.x + PLAYER_WIDTH // 2 - 2, player.y, 5, 10))
            elif power_level == 2:
                bullets.append(pygame.Rect(player.x + PLAYER_WIDTH // 2 - 12, player.y, 5, 10))
                bullets.append(pygame.Rect(player.x + PLAYER_WIDTH // 2 + 7, player.y, 5, 10))
            elif power_level >= 3:
                bullets.append(pygame.Rect(player.x + PLAYER_WIDTH // 2 - 15, player.y, 5, 10))
                bullets.append(pygame.Rect(player.x + PLAYER_WIDTH // 2 - 2, player.y, 5, 10))
                bullets.append(pygame.Rect(player.x + PLAYER_WIDTH // 2 + 11, player.y, 5, 10))
            BULLET_TIMER = 0


        for b in bullets[:]:
            b.y -= 10
            if b.y < 0:
                bullets.remove(b)

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for power in powerups[:]:
            power.y += POWERUP_VEL
            if power.y > HEIGHT:
                powerups.remove(power)
            elif power.colliderect(player):
                powerups.remove(power)  
                if power_level < MAX_POWER_LEVEL:
                    power_level += 1 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL > 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL < WIDTH - PLAYER_WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL > 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL < HEIGHT - PLAYER_HEIGHT:
            player.y += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break 

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")  
            WIN.blit(lost_text, (500 - lost_text.get_width() / 2, 400 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        for b in bullets[:]:
            for s in stars[:]:
                if b.colliderect(s): 
                    SCORE_VAL = SCORE_VAL + 10
                    bullets.remove(b)
                    stars.remove(s)
                    break

        draw(player, elapsed_time, stars, bullets, powerups, power_level)

    pygame.quit()        

if __name__ == "__main__":
    main()