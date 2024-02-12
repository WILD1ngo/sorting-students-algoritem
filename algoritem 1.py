import networkx as nx
import random
import os
import matplotlib.pyplot as plt



def ceildiv(a, b):
    return -(a // -b)



def draw(visited_nodes, red_edges, name):
    plt.clf()
    # Define a color map for node colors
    color_map = ['red' if node in visited_nodes else 'lightblue' for node in G.nodes()]

    # Draw the graph with node colors
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_size=500, node_color=color_map, font_size=10)

    # Draw edges that were followed in red
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if os.path.isfile(name):
       os.remove(name)   # Opt.: os.system("rm "+strFile)
    plt.savefig(name)
def culc_utility():
    for i in range(len(chain_list)):
        print("chain number " + str(i) + " has " + str(chain_utilty(chain_list[i])) + " utility")
def chain_utilty(group):
    utility = 0
    for node in group:
        for successor in C.successors(node):
            if successor in group:
                utility += C[node][successor]['weight']
    return utility
    
def find_chain():
    for node in G.nodes:
        # Randomly select one node to change its color to blue
        #random_node = random.choice(nodes)

        print(node)
        # Create a set to keep track of visited nodes
        visited_nodes = set()

        # Create a list to store edges that will be marked as red
        red_edges = []

        # Start from the random node and follow edges with weight 3
        current_node = node
        while len(visited_nodes) <= CLASS_SIZE:
            if current_node in visited_nodes:
                print("found a chain")
                print("size:" + str(len(visited_nodes)))
                return visited_nodes, red_edges
            visited_nodes.add(current_node)
            max_weight_successor = 0
            max_successor = -1
            for successor in G.successors(current_node):
                if G[current_node][successor]['weight'] > max_weight_successor:
                    max_weight_successor = G[current_node][successor]['weight']
                    max_successor = successor

            if(max_successor == -1):
                break
            red_edges.append((current_node, max_successor))
            current_node = max_successor
            print(current_node)
    print("can't find chain normaly")
    return find_suf_chain()
    
def find_suf_chain():
    for node in G.nodes:
        # Randomly select one node to change its color to blue
        #random_node = random.choice(nodes)

        print(node)
        # Create a set to keep track of visited nodes
        visited_nodes = set()

        # Create a list to store edges that will be marked as red
        red_edges = []

        # Start from the random node and follow edges with weight 3
        current_node = node
        while len(visited_nodes) <= ceildiv(N,NUM_OF_CLASSES):
            if current_node in visited_nodes:
                print("found a chain")
                print("size:" + str(len(visited_nodes)))
                return visited_nodes, red_edges
            visited_nodes.add(current_node)
            max_weight_successor = 0
            max_successor = -1
            for successor in G.successors(current_node):
                if successor in visited_nodes:
                    red_edges.append((current_node, successor))
                    return visited_nodes, red_edges
                if G[current_node][successor]['weight'] > max_weight_successor:
                    max_weight_successor = G[current_node][successor]['weight']
                    max_successor = successor

            if(max_successor == -1):
                break
            red_edges.append((current_node, max_successor))
            current_node = max_successor
            print(current_node)
    print("can't find chain even fast")
    return False, [] 
def chain_group():
    chain_list = []  # Initialize chain_list globally
    i=0
    while True:
        visited_nodes, red_edges = find_chain()
        if visited_nodes:
            print(visited_nodes)
            i+=1
            name = "graph" + str(i) + ".png"
            draw(visited_nodes, red_edges, name)
            chain_list.append(visited_nodes)
            #color_map2 = [distinct_colors[len(chain_list) - 1] for _ in visited_nodes]
            for node in visited_nodes:
                if G.has_node(node):
                    G.remove_node(node)
            print("Remaining nodes:" + str(G.nodes))
        else:
            return chain_list
def myFunc(e):
  return len(e)
def binPacking(group):
    classes = []
    c_group = group.copy()
    c_group.sort(key=myFunc, reverse=True)
    for cur_chain in c_group[NUM_OF_CLASSES:]:
        max_util = 0
        max_class = -1
        c_class = nx.DiGraph()
        for cur_class in range(NUM_OF_CLASSES):
            #chrck if the current chain fits the first chains
            if len(cur_chain) <= CLASS_SIZE - len(c_group[cur_class]):
                #compute the utility
                c_class.clear()
                c_class.add_nodes_from(cur_chain)
                c_class.add_nodes_from(c_group[cur_class])
                conected_group_util = chain_utilty(c_class)
                if max_util <= conected_group_util:
                    max_util = conected_group_util
                    max_class = cur_class
        temp = cur_chain.copy()
        print(temp)
        c_group[max_class] = c_group[max_class] | temp
        print("sizes:")
        for i in c_group:
            print (len(i))
    for i in range(NUM_OF_CLASSES):
        print("class " + str(i) + " has: " + str(c_group[i]))
        print("size : " + str(len(c_group[i])))
        print("utility : " + str(chain_utilty(c_group[i])))
        classes.append(c_group[i])
    return classes
    
# Create a directed graph
G = nx.DiGraph()
N = 93

NUM_OF_CLASSES=3
CLASS_SIZE = ceildiv(N,NUM_OF_CLASSES)

# Create nodes
nodes = list(range(N))
G.add_nodes_from(nodes)

for i in range(N):
    remaining_nodes = [node for node in nodes if node != i]
    target_nodes = random.sample(remaining_nodes, min(3, len(remaining_nodes)))

    # Assign different values to edges
    edge_values = [3, 2, 1]
    for j, target in enumerate(target_nodes):
        G.add_edge(i, target, weight=edge_values[j])
C = G.copy()
print(C.nodes)
chain_list = chain_group()

print("the chains that have been found :" + str(chain_list))
print("remaining nodes : " + str(G.nodes))
culc_utility()
for node in G.nodes:
    arr = {node}
    chain_list.append(arr)
classes = binPacking(chain_list)
#distinct_colors = list(mcolors.TABLEAU_COLORS)
plt.clf()
color_map2 = []

for node in C.nodes():
    returned = False
    for i in range(len(classes)):
        if node in classes[i]:
            color_map2.append(i*5)
    
    
# Draw the graph with node colors
pos = nx.spring_layout(C, seed=42)
edge_labels = nx.get_edge_attributes(C, 'weight')


nx.draw_networkx_nodes(C, pos,node_size=500, node_color=color_map2)
nx.draw_networkx_labels(C, pos, font_size=10)


curved_edges = [edge for edge in C.edges() if reversed(edge) in C.edges()]
straight_edges = list(set(C.edges()) - set(curved_edges))
nx.draw_networkx_edges(C, pos, edgelist=straight_edges)
arc_rad = 0.15
nx.draw_networkx_edges(C, pos, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}')
# Draw edges that were followed in red
#nx.draw_networkx_edges(C, pos, edgelist=red_edges, edge_color='red')

curved_edge_labels = {edge: edge_labels[edge] for edge in curved_edges}
straight_edge_labels = {edge: edge_labels[edge] for edge in straight_edges}

#my_nx.my_draw_networkx_edge_labels(C, pos, edge_labels=curved_edge_labels,rotate=False,rad = arc_rad)
#edge_labels=dict([((u,v,),d['length']) for u,v,d in G.edges(data=True)])
nx.draw_networkx_edge_labels(C, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)
#nx.draw_networkx_edge_labels(C, pos, edge_labels=straight_edge_labels,rotate=False)

#nx.draw_networkx_edge_labels(C, pos, edge_labels=edge_labels)
plt.show()
