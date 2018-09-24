import pygame
import sys
from bullet import Bullet
from alien import Alien


def get_number_alien_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def get_number_alien_y(ai_settings, alien_height, ship_height):
    available_space_y = ai_settings.screen_height - 2 * alien_height - ship_height
    rows_number = int(available_space_y / alien_height)
    return rows_number


def creat_alien(ai_settings, screen, aliens, alien_number, rows_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * rows_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def creat_fleets(ai_settings, ship, aliens, screen):
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_alien_x(ai_settings, alien.rect.width)
    rows_number = get_number_alien_y(ai_settings, alien_height=alien.rect.height, ship_height=ship.rect.height)

    for row_number in range(rows_number):
        for alien_number in range(number_alien_x):
            creat_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(bullets, ai_settings, screen, ship):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullets = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullets)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, aliens, bullets):
    # 每次循环都重新绘制屏幕
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.y < 0:
            bullets.remove(bullet)