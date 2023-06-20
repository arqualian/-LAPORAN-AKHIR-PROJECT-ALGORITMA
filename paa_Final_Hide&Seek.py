import pygame
import random
import math

# Inisialisasi Pygame
pygame.init()

# Lebar dan tinggi layar
screen_width = 800
screen_height = 600

# Ukuran maze
maze_width = 40  # Jumlah kolom
maze_height = 30  # Jumlah baris

# Warna RGB
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0, 0)
green = (0, 255, 0)

# Ukuran sel
cell_size = 20
wall_thickness = 2

# Ukuran papan kontrol
control_panel_width = 200

# Jarak pandang droid hijau
green_droid_visibility = 2  # Jarak pandang maksimum dalam jumlah sel

# Membuat jendela layar
screen = pygame.display.set_mode((screen_width + control_panel_width, screen_height))
pygame.display.set_caption("Projek PAA")

clock = pygame.time.Clock()

# Matriks untuk menyimpan status dinding dan posisi droid
maze = [[1] * maze_width for _ in range(maze_height)]

# Tombol Acak Peta
button_randomize_map = pygame.Rect(screen_width + 20, 20, control_panel_width - 40, 40)

# Tombol Acak Droid
button_randomize_droid = pygame.Rect(screen_width + 20, 80, control_panel_width - 40, 40)

# Tombol Tambah Droid Merah
button_add_red_droid = pygame.Rect(screen_width + 20, 140, control_panel_width - 40, 40)

# Tombol Mulai
button_start = pygame.Rect(screen_width + 20, 200, control_panel_width - 40, 40)

# Tombol Berhenti
button_stop = pygame.Rect(screen_width + 20, 260, control_panel_width - 40, 40)

# Tombol Atur Mata Hijau
button_set_green_droid_visibility = pygame.Rect(screen_width + 20, 320, control_panel_width - 40, 40)

# Variabel untuk menyimpan posisi droid merah dan hijau
red_droid_positions = []
green_droid_pos = None

# Variabel untuk menyimpan status pergerakan droid merah
red_droid_moving = False

def generate_maze(x, y):
    maze[y][x] = 0  # Tandai posisi saat ini sebagai celah
    directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    random.shuffle(directions)

    for dx, dy in directions:
        next_x = x + dx
        next_y = y + dy

        if 0 <= next_x < maze_width and 0 <= next_y < maze_height and maze[next_y][next_x] == 1:
            maze[next_y][next_x] = 0
            maze[y + (dy // 2)][x + (dx // 2)] = 0

            generate_maze(next_x, next_y)

            # Langkah tambahan untuk membuat lorong terhubung lebih banyak
            for i in range(2):
                nx = x + (dx // 2) * i
                ny = y + (dy // 2) * i
                if 0 <= nx < maze_width and 0 <= ny < maze_height and maze[ny][nx] == 1:
                    maze[ny][nx] = 0
                    if random.random() < 0.4:  # Peluang untuk mempertahankan lorong
                        generate_maze(nx, ny)
                        
    # Langkah tambahan untuk menciptakan tembok terisolasi
    if random.random() < 0.1:  # Peluang untuk menciptakan tembok terisolasi
        isolated_x = random.randint(0, maze_width - 1)
        isolated_y = random.randint(0, maze_height - 1)
        maze[isolated_y][isolated_x] = 1

def randomize_map():
    global maze
    maze = [[1] * maze_width for _ in range(maze_height)]
    generate_maze(0, 0)

def randomize_droid():
    global green_droid_pos, red_droid_positions
    green_droid_pos = None
    red_droid_positions = []

    # Pilih posisi acak untuk droid hijau
    while green_droid_pos is None:
        x = random.randint(0, maze_width - 1)
        y = random.randint(0, maze_height - 1)
        if maze[y][x] == 0:
            green_droid_pos = (x, y)

    # Pilih posisi acak untuk satu droid merah
    while True:
        x = random.randint(0, maze_width - 1)
        y = random.randint(0, maze_height - 1)
        if maze[y][x] == 0 and (x, y) != green_droid_pos:
            red_droid_positions.append((x, y))
            break


def draw_maze():
    screen.fill(gray)

    # Gambar sel dinding
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, black, rect)

    # Gambar sel droid merah
    for red_droid_pos in red_droid_positions:
        x, y = red_droid_pos
        radius = cell_size // 2  # Jari-jari lingkaran adalah setengah dari ukuran sel
        center = (x * cell_size + radius, y * cell_size + radius)
        pygame.draw.circle(screen, red, center, radius)

    # Gambar sel droid hijau
    if green_droid_pos:
        x, y = green_droid_pos
        center = (x * cell_size + radius, y * cell_size + radius)
        pygame.draw.circle(screen, green, center, radius)

    # Gambar tombol
    pygame.draw.rect(screen, white, button_randomize_map)
    pygame.draw.rect(screen, white, button_randomize_droid)
    pygame.draw.rect(screen, white, button_add_red_droid)
    pygame.draw.rect(screen, white, button_start)
    pygame.draw.rect(screen, white, button_stop)
    pygame.draw.rect(screen, white, button_set_green_droid_visibility)

    # Gambar teks pada tombol
    font = pygame.font.Font(None, 24)
    text_randomize_map = font.render("Randomize Map", True, black)
    text_randomize_droid = font.render("Randomize Droid", True, black)
    text_add_red_droid = font.render("Add Red Droid", True, black)
    text_start = font.render("Start", True, black)
    text_stop = font.render("Stop", True, black)
    text_set_green_droid_visibility = font.render("Set Green Droid Visibility", True, black)

    screen.blit(text_randomize_map, (screen_width + 30, 30))
    screen.blit(text_randomize_droid, (screen_width + 30, 90))
    screen.blit(text_add_red_droid, (screen_width + 30, 150))
    screen.blit(text_start, (screen_width + 30, 210))
    screen.blit(text_stop, (screen_width + 30, 270))
    screen.blit(text_set_green_droid_visibility, (screen_width + 30, 330))

    pygame.display.flip()

def move_red_droids():
    for i, red_droid_pos in enumerate(red_droid_positions):
        x, y = red_droid_pos

        # Cek apakah droid merah berada dalam jarak pandang droid hijau
        if green_droid_pos and math.sqrt((x - green_droid_pos[0]) ** 2 + (y - green_droid_pos[1]) ** 2) <= green_droid_visibility:
            dx = green_droid_pos[0] - x
            dy = green_droid_pos[1] - y

            # Pilih langkah terbaik untuk mendekati droid hijau
            if abs(dx) > abs(dy):
                if dx > 0:
                    x += 1
                else:
                    x -= 1
            else:
                if dy > 0:
                    y += 1
                else:
                    y -= 1
        else:
            # Pilih langkah acak jika droid hijau tidak terlihat
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            dx, dy = random.choice(directions)
            x += dx
            y += dy

        # Cek apakah langkah berikutnya masih dalam batas peta dan tidak menabrak dinding
        if 0 <= x < maze_width and 0 <= y < maze_height and maze[y][x] == 0:
            red_droid_positions[i] = (x, y)


def move_green_droid():
    global green_droid_pos

    if not green_droid_pos:  # Tambahkan pengecekan jika posisi droid hijau belum ditentukan
        return

    x, y = green_droid_pos

    # Pilih langkah acak untuk droid hijau
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    dx, dy = random.choice(directions)
    new_x = x + dx
    new_y = y + dy

    # Cek apakah langkah berikutnya masih dalam batas peta dan tidak menabrak dinding
    if 0 <= new_x < maze_width and 0 <= new_y < maze_height and maze[new_y][new_x] == 0:
        green_droid_pos = (new_x, new_y)

def game_loop():
    global red_droid_moving
    while True:
        handle_events()
        draw_maze()

        if red_droid_moving:
            move_red_droids()
            move_green_droid()  # Pindahkan pemanggilan fungsi move_green_droid() ke dalam kondisi red_droid_moving

        # Cek apakah droid merah menangkap droid hijau
        for red_droid_pos in red_droid_positions:
            if red_droid_pos == green_droid_pos:
                red_droid_moving = False
                break

        clock.tick(10)


def handle_events():
    global red_droid_moving, green_droid_visibility

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if button_randomize_map.collidepoint(mouse_pos):
                randomize_map()
            elif button_randomize_droid.collidepoint(mouse_pos):
                randomize_droid()
            elif button_add_red_droid.collidepoint(mouse_pos):
                if len(red_droid_positions) < 10:
                    x = random.randint(0, maze_width - 1)
                    y = random.randint(0, maze_height - 1)
                    if maze[y][x] == 0 and (x, y) != green_droid_pos:
                        red_droid_positions.append((x, y))
            elif button_start.collidepoint(mouse_pos):
                red_droid_moving = True
            elif button_stop.collidepoint(mouse_pos):
                red_droid_moving = False
            elif button_set_green_droid_visibility.collidepoint(mouse_pos):
                visibility = input("Masukkan jarak pandang droid hijau (dalam jumlah sel): ")
                try:
                    green_droid_visibility = int(visibility)
                except ValueError:
                    print("Masukan tidak valid. Jarak pandang droid hijau tetap tidak berubah.")

randomize_map()
randomize_droid()
game_loop()