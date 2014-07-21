#coding=utf8

import networkx as nx
import matplotlib.pyplot as plt

def read_file(path):
    graph = nx.read_edgelist(path, data = (('weight', float), ))

    # initial graph's node attribute 'lable' with its id
    for n, d in graph.nodes_iter(True):
        d['lable'] = n

    return graph

def lpa(graph):
    for i in graph.nodes_iter():
        d = {}

        # ͳ�����ڽڵ��label
        for n in graph.neighbors_iter(i):
            v = d.setdefault(n, 0) + 1
	    d[n] = v

        # ��ͳ�ƽ������ȡcount����label��������count�ж�������ѡһ��
	print d

if __name__ == '__main__':
    g = read_file('f.data')
    lpa(g)
    node_color = [float(g.degree(v)) for v in g]
    nx.draw(g, node_color = node_color)
    plt.show()
