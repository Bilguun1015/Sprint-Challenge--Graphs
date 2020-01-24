from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def add_to_visited(room_id, visited):
    if room_id not in visited:
        visited[room_id] = {'n':'?', 's':'?', 'e': '?', 'w':'?'}
    return visited

def possible_exits(room_id, player, visited):
    choices = player.current_room.get_exits()
    possible_choices = []
    for direction, new_room_id in visited[room_id].items():
        if direction in choices and new_room_id == '?':
            possible_choices.append(direction)
    return possible_choices

def opposite_direction(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'
    
def random_walk(player):
    visited = {}
    visited_path = []
    queue = Queue()
    queue.enqueue(player.current_room.id)
    
    while queue.size() > 0:
        if len(visited) == len(world.rooms):
            return visited
        room_id = queue.dequeue()
        visited = add_to_visited(room_id, visited)
        if visited_path:
            pre_room_id = visited_path[-1][0]
            pre_room_dir = opposite_direction(visited_path[-1][1])
            visited[room_id][pre_room_dir] = pre_room_id
        choices = possible_exits(room_id, player, visited)
        if choices:
            choice = random.choice(possible_exits(room_id, player, visited))
            player.travel(choice)
            visited[room_id][choice] = player.current_room.id
            visited_path.append([room_id, choice])
        else:
            choice = pre_room_dir
            player.travel(pre_room_dir)
            if visited_path:
                visited_path.pop()
            else:
                traversal_path.append(choice)
                return visited
        traversal_path.append(choice)
        queue.enqueue(player.current_room.id)

player = Player(world.starting_room)
random_walk(player)
# i = 0
# while len(traversal_path) > 980:
#     traversal_path = []
#     random_walk(player)
#     i += 1
# print(i)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


# room = Room('one','one')
# class RoomGraph:
#     def __init__(self):
#         self.rooms = {}
#         self.connected_rooms = {}
#         self.last_id = 0

#     def add_connection(self, room_id, connected_room_id):
#         """
#         Creates a bi-directional connection
#         """
#         if room_id == connected_room_id:
#             print("WARNING: room cannot connect to itself")
#             return False
#         elif connected_room_id in self.connected_rooms[room_id] or room_id in self.connected_rooms[connected_room_id]:
#             print("WARNING: This room connection already exists")
#             return False
#         else:
#             self.connected_rooms[room_id].add(connected_room_id)
#             self.connected_rooms[connected_room_id].add(room_id)
#     def add_room(self, room_id, possible_exits):
#         """
#         Create a room with a sequential integer ID
#         """
#         self.last_id += 1
#         self.rooms[room_id] = room
#         self.connected_rooms[self.last_id] = possible_exits



# # Create a queue/stack as appropriate
#         stack = Stack()
#         # Put the starting point in that
#         stack.push(starting_vertex)
#         # Make a set to keep track of where we've been
#         visited = set()
#         # While there is stuff in the queue/stack
#         while stack.size() > 0:
#         #    Pop the first item
#             vertex = stack.pop()
#         #    If not visited
#             if vertex not in visited:
#         #       DO THE THING!     
#                 visited.add(vertex)
#         #       For each edge in the item
#                 for next_vert in self.get_neighbors(vertex):
#         #           Add that edge to the queue/stack
#                     stack.push(next_vert)