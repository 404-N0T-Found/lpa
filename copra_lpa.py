#coding=utf8

import sys
import random
import networkx as nx
import matplotlib.pyplot as plt

def read_graph_from_file(path):
    # read edge-list from file
    graph = nx.read_edgelist(path, data = (('weight', float), ))

    # initial graph's node's attribute 'label' with its id
    for node, data in graph.nodes_iter(True):
        data['prev_label'] = dict()
        data['current_label'] = {node : 1.0}

    return graph

def read_game_info_from_file(path):
    game = {}

    with file(path, 'r') as f:
        for line in f:
            line = line.strip()
            data = line.split('\t')
            game[data[0]] = data[1]

    return game

# COPRA - label-propagation algorithm
# (can find overlapping communities)
#
# note:
#     use synchronous updating for better results
#
# parameter:
#     v : number of labels of a vertex can contain
def lpa(graph, v):
    def propagate(node):
        'calculate belonging coefficient'
        # we assume that current label dict is empty
        # store vertex -> belonging coefficient
        current_label = graph.node[node]['current_label']

        degree = float(graph.degree(node))
        for neighbor in graph.neighbors_iter(node):
            prev_label = graph.node[neighbor]['prev_label']

            for label in prev_label:
                current_label[label] = current_label.get(label, 0.0)\
                    + prev_label[label] / degree

        normalize(current_label)

        # delete pair that is less then threshold
        threshold = 1.0 / v
        label_max, coefficient_max = '', 0.0
        for label, coefficient in current_label.items():
            if coefficient < threshold:
                del current_label[label]
                if coefficient > coefficient_max:
                    label_max, coefficient_max = label, coefficient

        if len(current_label) == 0:
            current_label[label_max] = coefficient_max
        else:
            normalize(current_label)

    def normalize(labels):
        'normalize coefficients so that they can sums to 1'
        sum_val = sum(labels.values())

        if sum_val == 1:
            return

        for label in labels:
            labels[label] = labels[label] / sum_val

    def reset_current_label():
        for node in graph.nodes_iter():
            graph.node[node]['prev_label'] = graph.node[node]['current_label']
            graph.node[node]['current_label'] = dict()

    def label_set(label_type):
        labels = set()
        for node in graph.nodes_iter():
            labels.update(graph.node[node][label_type].keys())

        return labels

    def label_count(label_type):
        labels = dict()
        for node in graph.nodes_iter():
            for label in graph.node[node][label_type]:
                labels[label] = labels.get(label, 0) + 1

        return labels

    def mc(cs1, cs2):
        cs = dict()
        for c in cs1:
            cs[c] = min(cs1[c], cs2[c])

        return cs

    def estimate_stop_cond():
        #prev_label_set = label_set('prev_label')
        #current_label_set = label_set('current_label')

        #if len(prev_label_set) == len(current_label_set):
        #    pass
        #else:
        #    min = mc(min)

        return False

    loop_count = 0

    while True:
        loop_count += 1
        print 'loop', loop_count

        reset_current_label()

        for node in graph.nodes_iter():
            propagate(node)

        if estimate_stop_cond() is True or loop_count >= 4:
            return

def print_graph_info(graph):
    game_info = read_game_info_from_file('sample/id_name.info')
    info = {}

    for node in graph.nodes_iter():
        current_label = graph.node[node]['current_label']

        for label in current_label:
            info.setdefault(label, []).append(game_info.get(node, node))

    print 'node num:', len(graph.nodes())
    print 'class num:', len(info.keys())
    print 'class:', info.keys()
    print 'info:'
    for clazz in info:
        print '\t', clazz, ':',
        for label in info[clazz]:
            print '\'' + label + '\'',
        print '\n',

if __name__ == '__main__':
    g = read_graph_from_file('sample/f.data')
    lpa(g, 1)
    print_graph_info(g)

    #node_color = [float(g.node[v]['current_label'].keys()[0]) for v in g]
    #labels = dict([(node, node) for node in g.nodes_iter()])
    #nx.draw_networkx(g, node_color = node_color)
    #plt.show()
