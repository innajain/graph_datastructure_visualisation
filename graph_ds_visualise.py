import pygame
import numpy


class Colors:
    red = (255,0,0)
    green = (50, 168, 78)
    blue = (0,0,255)
    yellow = (212, 173, 17)
    black = (0,0,0)
    white = (255,255,255)
    orange = (252, 111, 3)
    pink = (252, 3, 244)
    purple = (152, 3, 252)
    grey = (65, 59, 69)
    reddish_pink = (235, 12, 64)

class Node:
    STATE_COLOR_DICT = {"normal" : Colors.reddish_pink, "clicked": Colors.purple, "moving": Colors.orange}
    RADIUS = 20
    def __init__(self, x, y) -> None:
        self.data = None
        self.x = x
        self.y = y
        self.state = "normal"

    def draw(self, screen):
        color = Node.STATE_COLOR_DICT[self.state]
        pygame.draw.circle(screen, Colors.white, (self.x, self.y), Node.RADIUS, 2)
        pygame.draw.circle(screen, color, (self.x, self.y), Node.RADIUS - 2)
        if self.state == "clicked" and self.data!=None:
            font = pygame.font.SysFont('Arial', int(1.5 * Node.RADIUS))
            text_surface = font.render(self.data, True, (255, 255, 255))
            screen.blit(text_surface, (int(self.x - 0.4 * Node.RADIUS), int(self.y - 0.9 * Node.RADIUS)))

    def check_hover(self, pos):

        return (self.x-pos[0])**2 + (self.y-pos[1])**2 <= Node.RADIUS**2
    
def find_hovered_node(vertices:list[Node], pos):
    for vertex in vertices:
        if vertex.check_hover(pos):
            return vertex
    return False
# class Buttons:
#     class new_vertex_button:
#         def __init__(self, screen):
#             pygame.draw.rect(screen, Colors().white, pygame.Rect(0.9*WIDTH, 0.2 * HEIGHT, 0.1*WIDTH, 0.2*HEIGHT), 3)
#             pygame.draw.rect(screen, Colors().green, pygame.Rect(0.9*WIDTH + 3, 0.2 * HEIGHT +  3, 0.1 * WIDTH - 6, 0.2 * HEIGHT - 6))
#         def 
def main():

    vertices:list[Node] = []
    edges:list[tuple[Node]] = []





    pygame.init()
    WIDTH = 640
    HEIGHT = 480
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph Datastructure")
    v = Node(50,50)
    v.data = "5"
    vertices.append(v)

    # Set up the clock
    clock = pygame.time.Clock()

    # Double-click detection variables
    last_click_time = 0
    double_click_delay = 250  # in milliseconds
    is_dragging = False
    moving_vertex = None 
    start_pos = None
    creating_new_edge = False
    create_vertex_button = pygame.Rect(0.9*WIDTH, 0.3 * HEIGHT, 0.1*WIDTH, 0.2*HEIGHT)
    create_edge_button =pygame.Rect(0.9*WIDTH, 0.5 * HEIGHT + 3, 0.1*WIDTH, 0.2*HEIGHT)
    starting_vertex = None
    ending_vertex = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User clicked the close button
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # User pressed the escape key
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # User clicked left mouse button
                if pygame.time.get_ticks() - last_click_time < double_click_delay:
                    temp = find_hovered_node(vertices, event.pos)
                    if temp:
                        temp.state = "clicked"
                        moving_vertex = None
                        if pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
                            temp.data = input(("Enter data: "))
                elif moving_vertex != None:
                    moving_vertex.state = "normal"
                    if create_vertex_button.collidepoint(moving_vertex.x, moving_vertex.y):
                        vertices.pop()
                        del moving_vertex
                    moving_vertex = None
                elif creating_new_edge and starting_vertex!=None:
                    temp = find_hovered_node(vertices, event.pos)
                    if temp:
                        ending_vertex = temp
                    # starting_vertex = None
                last_click_time = pygame.time.get_ticks()

            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:
                    pos = event.pos
                    if create_vertex_button.collidepoint(pos[0], pos[1]):
                        temp = Node(pos[0], pos[1])
                        temp.state = "moving"
                        moving_vertex = temp
                        vertices.append(temp)
                    elif create_edge_button.collidepoint(pos[0], pos[1]):
                        creating_new_edge = True
                    else:
                        temp = find_hovered_node(vertices, pos)
                        if temp:
                            if not creating_new_edge:
                                temp.state = "moving"
                                moving_vertex = temp
                            else:
                                if not starting_vertex:
                                    starting_vertex = temp
                    

            elif event.type == pygame.MOUSEMOTION:
                if moving_vertex != None:
                    pos = event.pos
                    moving_vertex.x = pos[0]
                    moving_vertex.y = pos[1]
                elif creating_new_edge and starting_vertex:
                    ending_vertex = pygame.mouse.get_pos()
        screen.fill(Colors.black) 


        if type(ending_vertex) == tuple:
            pygame.draw.line(screen, Colors().white, (starting_vertex.x, starting_vertex.y), ending_vertex, 2)
        elif type(ending_vertex) == Node:
            pygame.draw.line(screen, Colors.white, (starting_vertex.x, starting_vertex.y), (ending_vertex.x, ending_vertex.y), 2)
            edges.append((starting_vertex, ending_vertex))
            starting_vertex = None
            ending_vertex = None
            creating_new_edge = False


        pos = pygame.mouse.get_pos()
        for edge in edges:
            a = numpy.array([edge[0].x, edge[0].y])
            b = numpy.array([edge[1].x, edge[1].y])
            c = numpy.array([pos[0], pos[1]])
            temp1 = b-a
            temp2 = c-a
            if abs(temp1[1]/temp1[0] - temp2[1]/temp2[0]) < 0.1 and abs(temp2[0])<=abs(temp1[0]) and abs(temp2[1])<=abs(temp1[1]):
                pygame.draw.line(screen, Colors.white, (edge[0].x, edge[0].y), (edge[1].x, edge[1].y), 6)
            else:
                pygame.draw.line(screen, Colors.white, (edge[0].x, edge[0].y), (edge[1].x, edge[1].y), 2)
                
        for vertex in vertices: vertex.draw(screen)


        pygame.draw.rect(screen, Colors().green, create_vertex_button)
        font = pygame.font.SysFont('Times New Roman', int(0.035 * WIDTH))
        text_surface = font.render("Vertex", True, (255, 255, 255))
        screen.blit(text_surface, create_vertex_button.midleft)


        if not creating_new_edge: pygame.draw.rect(screen, Colors().yellow, create_edge_button)
        else: pygame.draw.rect(screen, Colors().purple, create_edge_button)
        font = pygame.font.SysFont('Times New Roman', int(0.035 * WIDTH))
        text_surface = font.render("Edge", True, (255, 255, 255))
        screen.blit(text_surface, create_edge_button.midleft)



        pygame.display.update()
        clock.tick(60)




main()