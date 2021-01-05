import networkx as nx
import sys

def read_csv_file(path):
    try:
        f = open(path, 'r')
    except:
        print('Could not open',path)
        exit(1)

    text = f.read()
    lines = text.split('\n')
    lines = list(map(lambda x: x.split(','), lines))
    f.close()
    return lines

def flatten(wordlist):
    return [item for sublist in wordlist for item in sublist]

def create_edges(wordlist):
    if len(wordlist) == 0:
        return ()
    word = wordlist[0]
    nyms = wordlist[1:]
    edges = list(map(lambda e: (word,e), nyms))
    return edges

def create_graph(wordlists):
    g = nx.Graph()
    all_words = flatten(wordlists)
    g.add_nodes_from(all_words)
    edges = list(map(create_edges, wordlists))
    for entry in edges:
        g.add_edges_from(entry)
    return g

def path_between_words(graph, w1, w2):
    path = []
    try:
        path = nx.shortest_path(graph, w1, w2)
        print(path)
    except nx.exception.NetworkXNoPath:
        print("No path exists between {} and {}".format(w1, w2))

def nyms_through_depth(graph, word, depth):
    edges = list(nx.bfs_edges(graph, source=word, depth_limit=depth))
    nodes = [word] + [v for u, v in edges]
    print(nodes)

def repl(graph):
    inp = ""
    while not inp == "quit":
        print("query> ", end='')
        inp = input().split(' ')
        if inp[0] in graph.nodes():
            if len(inp) == 2:
                depth = int(inp[1])
                nyms_through_depth(graph, inp[0], depth)
            elif len(inp) == 3:
                if inp[1] == "->":
                    if inp[2] in graph.nodes():
                        path_between_words(graph, inp[0], inp[2])
                    else:
                        print("{}: word not found".format(inp[2]))
        else:
            print("invalid query")
        

def main():
    if not len(sys.argv) == 2:
        print("Forgot .csv file")
        exit(0)
    wordlists = read_csv_file(sys.argv[1])
    wordgraph = create_graph(wordlists)
    repl(wordgraph)

main()
