import pygame
import pygame_widgets
import os
from conf import *
from pendulum import *

# Initialize pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FADED = [255, 255, 255, 30]
trail_screen = pygame.Surface((WIDTH, HEIGHT))
trail_screen.set_colorkey(WHITE)
fade = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
fade.fill(FADED)

dpen = DoublePendulum(screen, trail_screen)
trail_screen.fill(WHITE)

clock = pygame.time.Clock()
paused = False
vec = pygame.math.Vector2
selected = 0

sliders = [pygame_widgets.Slider(screen, 50, HEIGHT - 50, 100, 10, min=0, max=2, step=0.1, initial=g),
           pygame_widgets.Slider(screen, 50, HEIGHT - 70, 100, 10, min=10, max=100, step=1, initial=MASS1),
           pygame_widgets.Slider(screen, 50, HEIGHT - 90, 100, 10, min=10, max=100, step=1, initial=MASS2),
           pygame_widgets.Slider(screen, 50, HEIGHT - 110, 100, 10, min=20, max=200, step=1, initial=LENGTH1),
           pygame_widgets.Slider(screen, 50, HEIGHT - 130, 100, 10, min=20, max=200, step=1, initial=LENGTH2),
           pygame_widgets.Slider(screen, 50, HEIGHT - 150, 100, 10, min=0, max=255, step=1, initial=30)]

texts = ['Gravity : ', 'Mass 1 : ', 'Mass 2 :', 'Length 1 : ', 'Length 2 : ', 'Trails : ']

slider_values = [g, MASS1, MASS2, LENGTH1, LENGTH2, 30]


def draw_text(size, text, colour, x, y):
    font = pygame.font.SysFont('Comic Sans MS', size)
    text_surface = font.render(text, 1, colour)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


while True:
    now = pygame.time.get_ticks()
    clock.tick(30)
    screen.fill(WHITE)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_r:
                fade.fill(WHITE)
                fade.fill(FADED)

    mouse = pygame.mouse.get_pressed()
    if mouse[0] and not paused:
        paused = True
    elif mouse[2] and paused:
        paused = False
    mouse_pos = vec(pygame.mouse.get_pos())

    # if paused:
    #     # Sliders
    #     for index, slider in enumerate(sliders):
    #         slider.listen(events)
    #         slider.draw()
    #         draw_text(20, f'{texts[index]} : {slider.getValue()}', BLACK, 230, slider.y + 5)
    #         slider_values[index] = (slider.getValue())
    #     FADED[3] = slider_values[5]
    #
    #     # Reset the acc and velocity
    #     dpen.acc1 = 0
    #     dpen.acc2 = 0
    #     dpen.vel1 = 0
    #     dpen.vel2 = 0
    #     if mouse[0]:
    #         if (mouse_pos - dpen.pos1).length() < dpen.m1 + 10 and selected == 0:
    #             selected = 1
    #         elif (mouse_pos - dpen.pos2).length() < dpen.m2 + 10 and selected == 0:
    #             selected = 2
    #         elif (mouse_pos - dpen.start).length() < 20 and selected == 0:
    #             selected = 3
    #     else:
    #         selected = 0

    if selected == 1:
        dpen.ang1 -= math.radians((dpen.pos1 - dpen.start).angle_to(mouse_pos - dpen.start))
    if selected == 2:
        dpen.ang2 -= math.radians((dpen.pos2 - dpen.start).angle_to(mouse_pos - dpen.start))
    if selected == 3:
        dpen.start += (mouse_pos - dpen.start) * 0.25

    dpen.update_values(slider_values)
    if not paused:
        selected = 0
        dpen.update()
    dpen.move_bob()
    dpen.draw_trail()
    trail_screen.blit(fade, (0, 0))
    screen.blit(trail_screen, (0, 0))
    dpen.draw()
    if paused:
        # Sliders
        for index, slider in enumerate(sliders):
            slider.listen(events)
            slider.draw()
            draw_text(20, f'{texts[index]} : {slider.getValue()}', BLACK, 230, slider.y + 5)
            slider_values[index] = (slider.getValue())
        FADED[3] = slider_values[5]

        # Reset the acc and velocity
        dpen.acc1 = 0
        dpen.acc2 = 0
        dpen.vel1 = 0
        dpen.vel2 = 0
        if mouse[0]:
            if (mouse_pos - dpen.pos1).length() < dpen.m1 + 10 and selected == 0:
                selected = 1
            elif (mouse_pos - dpen.pos2).length() < dpen.m2 + 10 and selected == 0:
                selected = 2
            elif (mouse_pos - dpen.start).length() < 20 and selected == 0:
                selected = 3
        else:
            selected = 0
    if dpen.unstable:
        draw_text(100, 'UNSTABLE', RED, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
