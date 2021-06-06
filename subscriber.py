import pygame
from random import randint as rnd
import paho.mqtt.client as mqtt
import time
from queue import Queue

# Параметры для окна
WIDTH, HEIGHT = 626, 417
fps = 60
Green = 0
Red = 0

# Создание окна
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Subscriber")
clock = pygame.time.Clock()

# Параметры текста
green_ = pygame.font.SysFont('Arial', 18, bold=True)
red_ = pygame.font.SysFont('Arial', 18, bold=True)
speed_ = pygame.font.SysFont('Arial', 66, bold=True)


# Параметры шарика
ball_radius = 30
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(WIDTH-2*ball_radius, HEIGHT-ball_rect-30, ball_rect,
                   ball_rect)
dy = -1


# Параметры блоков
block_list = [pygame.Rect(WIDTH // 3, 50 + 120 * j, 250, 80)
              for j in range(3)]

color_list = [(212, 3, 3), (53, 145, 6)]

# Парматры фона
fon_ball = pygame.Rect(WIDTH-2*ball_rect, 0, 2*ball_rect, HEIGHT)
fon_block = pygame.Rect(0, 0, 20*2+100, HEIGHT)


# Функция для получение данных
def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    if message.topic == 'block':
        print("message received cart coords: ",
              str(message.payload.decode("utf-8")))
        print("message topic: ", message.topic)
        q1.put(data)
    elif message.topic == 'speed':
        print("message received ball coords: ",
              str(message.payload.decode("utf-8")))
        print("message topic: ", message.topic)
        q2.put(data)


# Соединение с брокером
q1 = Queue()
q2 = Queue()
client = mqtt.Client("Subscriber")
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_start()
client.subscribe('block')
client.subscribe('speed')


# Начальные данные
block_list_result = []
color_list_result = []
rand_list = []
rand_speed = 0
run = True
j = 0

# Пуск программы
while run:
    client.on_message = on_message
    while not q1.empty():
        message = q1.get()
        rand_list = list(map(int, message.split(',')))
        print("received from queue cart: ", message)
    while not q2.empty():
        rand_speed = int(q2.get())
        print("received from queue ball: ", message)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            exit()
            client.loop_stop()   # Stop loop
            client.disconnect()  # disconnect

    # Отрисовка фона
    sc.fill((36, 135, 166))
    pygame.draw.rect(sc, (250, 150, 0), fon_block)
    pygame.draw.rect(sc, (250, 150, 0), fon_ball)

    # Отрисовка блоков и шарика
    if rand_list and rand_speed:

        # Отрисовка блоков
        [pygame.draw.rect(sc, color_list[color], block) for color, block in
         zip(rand_list, block_list)]

        if all(rand_list) or not any(rand_list):
            block_result = pygame.Rect(20, 20 + 50 * j, 100, 30),
            block_list_result += block_result
            color_list_result.append(color_list[rand_list[0]])
            j += 1
            if rand_list[0]:
                Green += 1
            else:
                Red += 1
            # print(block_list_result, color_list_result)
        if block_list_result:
            [pygame.draw.rect(sc, color, block) for color, block in
             zip(color_list_result, block_list_result)]
        if len(block_list_result) == 8:
            block_list_result = []
            color_list_result = []
            j = 0

        GreenText = green_.render(f'Зеленый: {Green}', 1, (255, 255, 255))
        sc.blit(GreenText, (WIDTH//3, 10))
        RedText = red_.render(f'Красный: {Red}', 1, (255, 255, 255))
        sc.blit(RedText, (WIDTH//2+20, 10))

        pygame.draw.circle(sc, (192, 0, 219), ball.center, ball_radius)

        # скорость шарика
        if rand_speed <= 10:
            ball.y += 10 * dy
            ball_speed = 10
        elif rand_speed <= 20 and rand_speed >= 10:
            ball.y += 20 * dy
            ball_speed = 20
        else:
            ball.y += 30 * dy
            ball_speed = 30

        SpeedText = red_.render(f'Скорость: {ball_speed}', 1, (255, 255, 255))
        sc.blit(SpeedText, (WIDTH//2-30, HEIGHT-30))

        # Изменение направление шарика
        if ball.centery < ball_radius or ball.centery > HEIGHT - ball_radius:
            dy = -dy

    pygame.display.flip()
    clock.tick(fps)
    time.sleep(1)
