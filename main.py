# 3D-анимация звёзд на tkinter.Canvas.
# Каждая звезда хранится в 3D-координатах (x, y, z),
# проецируется на 2D-экран через перспективу.

import tkinter as tk
import random

# константы
WIDTH = 900          # ширина окна и холста
HEIGHT = 600         # высота окна и холста

CENTER_X = WIDTH // 2    # центр экрана по X (ось "камеры")
CENTER_Y = HEIGHT // 2   # центр экрана по Y

STAR_COUNT = 250     # сколько звёзд одновременно в поле

# создание окна
root = tk.Tk()
root.title("Полёт через звёздное поле")
root.resizable(False, False)   # запрет изменения размера окна

# Холст, на котором рисуется анимация
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",              # чёрный космос
    highlightthickness=0     # убираем рамку вокруг холста
)
canvas.pack()

# Палитра цветов звёзд (белый, голубой, золотой, розовый, фиолетовый)
colors = ["white", "#87CEFA", "#FFD700", "#FFB6C1", "#9370DB"]

# Список всех звёзд (каждая — словарь)
stars = []

# анимация
speed = 3            # текущая скорость полёта (1..20)
direction_x = 0      # наклон камеры по X (-1..1), задаётся мышью
direction_y = 0      # наклон камеры по Y (-1..1)


def create_star():
    """
    Создаёт одну звезду в 3D-пространстве.
    x, y — смещение от центра (в условных единицах),
    z    — глубина: чем меньше, тем ближе звезда к камере (1..1000),
    color — случайный цвет из палитры.
    """
    return {
        "x": random.uniform(-WIDTH / 2, WIDTH / 2),
        "y": random.uniform(-HEIGHT / 2, HEIGHT / 2),
        "z": random.uniform(1, 1000),
        "color": random.choice(colors)
    }


# Заполняем поле звёздами при старте
for i in range(STAR_COUNT):
    stars.append(create_star())


def move_mouse(event):
    """
    Обработчик движения мыши.
    Вычисляет направление наклона камеры:
    в центре окна -> 0, у краёв -> ±1.
    Звёзды будут смещаться в противоположную сторону (эффект поворота).
    """
    global direction_x, direction_y

    direction_x = (event.x - CENTER_X) / CENTER_X
    direction_y = (event.y - CENTER_Y) / CENTER_Y


def change_speed(event):
    """
    Обработчик клавиш:
    Стрелка вверх  — увеличить скорость (не больше 20),
    Стрелка вниз   — уменьшить скорость (не меньше 1).
    """
    global speed

    if event.keysym == "Up":
        speed = min(speed + 1, 20)

    elif event.keysym == "Down":
        speed = max(speed - 1, 1)


def draw_stars():
    """
    Главный кадр анимации. Вызывается каждые 30 мс через root.after.
    Для каждой звезды:
      1. Приближаем её к камере (уменьшаем z на speed).
      2. Смещаем x, y в сторону, противоположную наклону мыши.
      3. Если звезда "улетела" (z <= 1) или вышла за экран —
         пересоздаём её в новом случайном месте.
      4. Проецируем 3D -> 2D: scale = 300 / z.
         Ближние звёзды (малый z) получаются крупнее и дальше от центра,
         дальние — мельче и ближе к центру.
      5. Рисуем звезду овалом, размер зависит от scale.
    В конце — обновляем текст-подсказки и планируем следующий кадр.
    """
    canvas.delete("all")   # очищаем холст перед отрисовкой нового кадра

    for star in stars:
        # Приближение к камере
        star["z"] -= speed

        # Смещение звёзд относительно наклона мыши (обратное направление)
        star["x"] -= direction_x * speed * 0.5
        star["y"] -= direction_y * speed * 0.5

        # Если звезда "пролетела мимо" камеры — пересоздаём её
        if star["z"] <= 1:
            star.update(create_star())
            continue

        # проекция
        scale = 300 / star["z"]              # коэффициент масштаба

        # Экранные координаты: центр + смещение * масштаб
        x = CENTER_X + star["x"] * scale
        y = CENTER_Y + star["y"] * scale

        # Размер звезды на экране (минимум 1 пиксель)
        size = max(1, 5 * scale)

        # Если звезда вышла за границы экрана — пересоздаём её
        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            star.update(create_star())
            continue

        # Рисуем звезду (овал с заливкой без обводки)
        canvas.create_oval(
            x - size,
            y - size,
            x + size,
            y + size,
            fill=star["color"],
            outline=""
        )

    # тест в левом верхнем углу
    canvas.create_text(
        15, 15,
        anchor="nw",
        text=f"Скорость: {speed}",
        fill="white",
        font=("Arial", 12)
    )

    canvas.create_text(
        15, 40,
        anchor="nw",
        text="Стрелка вверх — ускорение | Стрелка вниз — замедление",
        fill="white",
        font=("Arial", 10)
    )

    canvas.create_text(
        15, 60,
        anchor="nw",
        text="Перемещай мышь, чтобы менять направление",
        fill="white",
        font=("Arial", 10)
    )

    # Планируем следующий кадр через 30 фпс
    root.after(30, draw_stars)


# функции
canvas.bind("<Motion>", move_mouse)     # движение мыши -> изменение направления
root.bind("<KeyPress>", change_speed)   # нажатие клавиш -> изменение скорости

# запуск
draw_stars()       # стартуем анимацию
root.mainloop()    # входим в главный цикл обработки событий
