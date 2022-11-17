import networkx as nx
import matplotlib.pyplot as plt
from heapq import *
import random
import copy
import os
import sys
import numpy as np
total_nodes = 50
sys.path.append(os.path.abspath(__file__))

class The_Environment():
    def __init__(self):
        self.visual = []
        self.vertex = np.arange(1,total_nodes+1)
        self.edges = {}
        self.prey_location = 0
        self.predator_location = 0
        self.agent_location = 0
        self.the_environment()

    def addEdge(self, u, v):
        self.edges[u].append(v)
        self.visual.append([u, v])
          
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
    
    def generate_ppa(self):
      self.prey_location = self.generate_location()
      self.predator_location = self.generate_location()
      self.agent_location = self.generate_location()
      while(self.agent_location == self.predator_location):
        self.agent_location = self.generate_location()
      while(self.agent_location == self.prey_location):
        self.agent_location = self.generate_location()

    def init_graph(self):
      for i in range(1,total_nodes+1):
        self.edges[i] = []
        if i ==1 : 
          self.addEdge(i,total_nodes)
          self.addEdge(i,i+1)
        elif i == total_nodes:
          self.addEdge(i,1)
          self.addEdge(i,i-1)
        else: 
          self.addEdge(i,i+1)
          self.addEdge(i,i-1)
      self.generate_ppa()
    
    def add_random_edges(self):
      for v in self.edges:
        #print("random edge for v: ", v)
        if(len(self.edges[v]) >= 3):
          continue
        choices = []
        for i in range(2, 6):
          u = v + i
          if(u > total_nodes):
            u = u%total_nodes
          choices.append(u)
        for i in range(-5, -1):
          u = v + i
          if(u < 0):
            u = (u+total_nodes)%total_nodes
          if(u == 0):
            u = total_nodes
          choices.append(u)
        #print("Initial choices aer ", choices)
        remove_choices = []
        for choice in choices:
          #print("for choice , ", choice, "edges is ", self.edges[choice])
          if(len(self.edges[choice]) >= 3):
            #print("removed")
            remove_choices.append(choice)
        choices = [choice for choice in choices if choice not in remove_choices]
        #print("Final choices ", choices)
        if not choices:
          continue
        random_choice = random.choice(choices)
        self.edges[v].append(random_choice)
        self.edges[random_choice].append(v)

    def the_environment(self):
      self.init_graph()
      self.add_random_edges()
    
    def generate_location(self):
      return np.random.randint(1, total_nodes+1)

def main():
  env = The_Environment()

if __name__ == '__main__':
  main()