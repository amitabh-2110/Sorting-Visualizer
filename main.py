import pygame
import random
import sys

sys.setrecursionlimit(1500)
pygame.init()

class board_info:
    FONT = pygame.font.SysFont("century", 19)
    GRADIENT = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    def __init__(self, width, height, list) -> None:
        self.width = width
        self.height = height
        self.board = pygame.display.set_mode((width, height))
        
        self.set_list(list)

    def set_list(self, list):
        self.list = list
        self.block_width = round(self.width / len(list))


def create_list(size, min_value, max_value):
    list = []
    i = 0
    while i < size:
        val = random.randint(min_value, max_value)
        list.append(val)
        i += 1

    return list


def draw(window, mouse, algo_text):
    window.board.fill((255, 255, 255))

    controls = window.FONT.render("R - Reset | Q - Quick Sort | M - Merge Sort | I - Insertion Sort", 1, (0, 0, 0))
    window.board.blit(controls, (window.width/2 - controls.get_width()/2, 15))

    if window.width/2-130 <= mouse[0] <= window.width/2+130 and 50 <= mouse[1] <= 80:
        pygame.draw.rect(window.board, (0, 0, 255), (window.width/2-130, 50, 260, 30))
    else:
        pygame.draw.rect(window.board, (0, 255, 0), (window.width/2-130, 50, 260, 30))

    text_button = window.FONT.render(algo_text, 1, (0, 0, 0))
    window.board.blit(text_button, (window.width/2 - text_button.get_width()/2, 50+3))

    text_instruction = window.FONT.render("[ Choose an algorithm by pressing key and then click on the button!! ]", 1, (255, 0, 0))
    window.board.blit(text_instruction, (window.width/2 - text_instruction.get_width()/2, 85))

    draw_list(window)


def draw_list(window, color_position={}, clear_bg = False):
    if clear_bg:
        pygame.draw.rect(window.board, (255, 255, 255), (0, 250, window.width, 350))

    for i, val in enumerate(window.list):
        x = i * window.block_width
        y = window.height - (val)

        color = window.GRADIENT[i % 3]
        if i in color_position:
            color = color_position[i]

        pygame.draw.rect(window.board, color, (x, y, window.block_width, window.height))

    if clear_bg:
        pygame.display.update()


def insertion_sort(window):
    for i in range(1, len(window.list)):
        temp = i-1
        num = window.list[i]

        draw_list(window, {i: (0, 0, 255)}, True)
        while temp >= 0 and window.list[temp] > num:
            draw_list(window, {temp: (255, 0, 0)}, True)
            window.list[temp+1] = window.list[temp]
            
            temp -= 1
            yield True

        window.list[temp+1] = num

    return window.list


def merge_sort(window, p, r):
    if p < r:
        mid = p + (r - p)//2
        yield from merge_sort(window, p, mid)
        yield from merge_sort(window, mid+1, r)
        
        list1 = []
        list2 = []

        for i in range(p, mid+1):
            list1.append(window.list[i])

        for j in range(mid+1, r+1):
            list2.append(window.list[j])

        m = n = 0
        k = p

        while m < len(list1) and n < len(list2):
            if list1[m] <= list2[n]:
                draw_list(window, {m: (255, 0, 0), n+len(list1)-1: (0, 255, 0)}, True)
                window.list[k] = list1[m]
                k += 1
                m += 1
            
            elif list2[n] < list1[m]:
                draw_list(window, {m: (255, 0, 0), n+len(list1)-1: (0, 255, 0)}, True)
                window.list[k] = list2[n]
                k += 1
                n += 1

            yield True

        while m < len(list1):
            draw_list(window, {m: (255, 0, 0)}, True)
            window.list[k] = list1[m]
            k += 1
            m += 1

        while n < len(list2):
            draw_list(window, {n+len(list1)-1: (0, 255, 0)}, True)
            window.list[k] = list2[n]
            k += 1
            n += 1

        yield True


def quick_sort(window, p, r):
    if p < r:
        pivot = r
        i, j = p-1, p

        while j < r:
            draw_list(window, {i+1: (255, 0, 0), j: (0, 0, 255)}, True)
            if window.list[j] < window.list[pivot]:
                window.list[i+1], window.list[j] = window.list[j], window.list[i+1]
                i += 1
            j += 1
            yield True
            
        draw_list(window, {i+1:(0, 255, 0), pivot: (0, 255, 0)}, True)
        window.list[i+1], window.list[pivot] = window.list[pivot], window.list[i+1]

        pos = i+1
        yield True

        yield from quick_sort(window, p, pos-1)
        yield from quick_sort(window, pos+1, r)


def main():
    running = True
    list = create_list(30, 30, 350)
    algo_text = "Visualize"

    window = board_info(600, 600, list)

    sorting = False
    pygame.display.set_caption("Sorting Visualizer")
    sorting_algorithm_generator = None

    clock = pygame.time.Clock()

    while running:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(window, mouse, algo_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    sorting = False
                    algo_text = "Visualize"
                    list = create_list(30, 30, 350)
                    window.set_list(list)
                
                if event.key == pygame.K_m and sorting == False:
                    algo_text = "Visualize Merge Sort"

                if event.key == pygame.K_q and sorting == False:
                    algo_text = "Visualize Quick Sort"
                
                if event.key == pygame.K_i and sorting == False:
                    algo_text = "Visualize Insertion Sort"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if window.width/2-130 <= mouse[0] <= window.width/2+130 and 50 <= mouse[1] <= 80 and sorting == False and algo_text != "Visualize":
                    sorting = True
                    if algo_text == "Visualize Merge Sort": #call merge sort 
                        sorting_algorithm_generator = merge_sort(window, 0, len(window.list)-1)
                    elif algo_text == "Visualize Quick Sort": #call quick sort
                        sorting_algorithm_generator = quick_sort(window, 0, len(window.list)-1)
                    elif algo_text == "Visualize Insertion Sort":  #call insertion sort
                        sorting_algorithm_generator = insertion_sort(window)
                
        pygame.display.update()


if __name__ == "__main__":
    main()

