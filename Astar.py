import pygame
import sys

# Constants for the game
TILE_SIZE = 20
WINDOW_HEIGHT, WINDOW_WIDTH = 650, 800
SCORE_PER_STEP = 1
SCORE_PER_SECOND = 10

# Load images
agent_image = pygame.image.load('./images/agent.png')
obstacle_image = pygame.image.load('./images/obstacle.png')
start_pos = pygame.image.load('./images/start.png')
stop_pos = pygame.image.load('./images/stop.png')
result_bg_img = pygame.image.load('./images/result_bg.png')
tile_image=pygame.image.load('./images/tile.png')

# Adjust the size of images
obstacle_image = pygame.transform.scale(obstacle_image, (TILE_SIZE, TILE_SIZE))
start_pos = pygame.transform.scale(start_pos, (TILE_SIZE, TILE_SIZE))
stop_pos = pygame.transform.scale(stop_pos, (TILE_SIZE, TILE_SIZE))
agent_image_resized = pygame.transform.scale(agent_image, (TILE_SIZE, TILE_SIZE))
result_bg_img = pygame.transform.scale(result_bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
tile_image = pygame.transform.scale(tile_image,(TILE_SIZE,TILE_SIZE))
# Read File function
def read_map(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

# ++++++++++++++++++++++++Process To Find Shortest Path++++++++++++++++++++++++++++++
# Find valid Neighbours function
def find_neighbors(map, node):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < len(map[0]) and 0 <= ny < len(map) and map[ny][nx] in ('.', 'D'):
            neighbors.append((nx, ny))
    return neighbors

''' Priority Queue implementation using OOP  
-  Encapsulation on listQueu=[] by adding methods to keep the process of data extration hidden
-  Abstract the extrating data through methods(empty,add,get) '''
class priority_queue:    
    def __init__(que): 
        que.listQueu = []

    def empty(que):
        return len(que.listQueu) == 0

    def enQue(que, item, priority):
        que.listQueu.append((priority, item))
        que.listQueu.sort()

    def deQue(que):
        if not que.empty():
            return que.listQueu.pop(0)[1]
        else:
            raise IndexError("Priority queue is empty") # exception handling

# A* search algorithm
def astar(map, start, destination):
    # Calculate Manhattan distance(heuristic) from current Node to destination node
    def heuristic(node1, node2):
       return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
    
    open_set = priority_queue()
    open_set.enQue(start, 0)
    neib_parent = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, destination)}

    while not open_set.empty():
        current = open_set.deQue()
        if current == destination:
            path = []
            while current in neib_parent:
                path.append(current)
                current = neib_parent[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in find_neighbors(map, current):
            combine_g_score = g_score[current] + 1 #g_score of right neighbor if not visited
            if neighbor not in g_score or combine_g_score < g_score[neighbor]:
                neib_parent[neighbor] = current
                g_score[neighbor] = combine_g_score
                f_score[neighbor] = combine_g_score + heuristic(neighbor, destination)
                open_set.enQue(neighbor, f_score[neighbor])

    return None

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('A* Search')

    map =  map = read_map('map.txt')
    start = None
    destination = None

    for x in range(len(map)):
        for y in range(len(map[x])):
            tile = map[x][y]
            if tile == 'S':
               start = (y, x)   
            elif tile == 'D':
                destination = (y, x)

    if start is None or destination is None:
        print("Map must have a start (S) and a destination (D)")
        sys.exit(1)

    # A* SEARCH ALGORITHM CALL
    path = astar(map, start, destination)
    
    clock = pygame.time.Clock()
    index = 0
    score = 0
    steps = 0
    timer = 30000  # 30 seconds

    while timer > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0,0,0))

        # Draw obstacles, start, and destination positions
        for y in range(len(map)):
            for x in range(len(map[y])):
                tile=map[y][x]
                if tile == 'X':
                    screen.blit(obstacle_image, (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 'S':
                    screen.blit(start_pos, (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 'D':
                    screen.blit(stop_pos, (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == '.':
                    screen.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))

        # Draw agent on the path
        if index < len(path):
            char_pos = path[index]
            screen.blit(agent_image_resized, (char_pos[0] * TILE_SIZE, char_pos[1] * TILE_SIZE))
            index += 1
            steps += 1

        # Check if the agent reaches the goal
        if index >= len(path):
        #   score +=       10         * (remaining time/1000)
            score += SCORE_PER_SECOND * (timer // 1000) # calculate the score
            timer = 0

        # Display the score and timer
        font = pygame.font.SysFont(None, 30)
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        time_text = font.render("Time: " + str(timer // 1000), True, (255, 255, 255))
        screen.blit(time_text, (WINDOW_WIDTH - 100, 10))

        pygame.display.flip()
        clock.tick(4)
        timer -= clock.get_time() # decrement the timer counter

    # Game over
    screen.blit(result_bg_img, (0, 0))
    font = pygame.font.SysFont(None, 50)
    gameOverTxt = font.render("Game Over", True, (255, 255, 255))
    screen.blit(gameOverTxt, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 35))
    finalScoreTxt = font.render("Final Score: " + str(score), True, (255, 255, 255))
    screen.blit(finalScoreTxt, (WINDOW_WIDTH // 2 - 125, WINDOW_HEIGHT // 2 + 20 ))
    pygame.display.flip()
    pygame.time.wait(3000)  #Pause game over screen for 3 seconds

if __name__ == '__main__':
    main()