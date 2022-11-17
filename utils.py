import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from heapq import *
import random
import copy
total_nodes = 50

def get_distance(loc1, loc2, edges):
  queue = [loc1]
  dist = {}
  for i in range(total_nodes):
    dist[i+1] = 100
  dist[loc1] = 0
  while(queue):
    loc = queue.pop(0)
    if(loc == loc2):
      return dist[loc2]
    for neigh in edges[loc]:
      if(dist[neigh] > dist[loc] + 1):
        dist[neigh] = dist[loc] + 1
        queue.append(neigh)
  return dist[loc2]

def move_predator(env , predator_loc,agent_loc):
  choices = env.edges[predator_loc]
  dist = {}
  for choice in choices:
    d = get_distance(choice, agent_loc, env.edges)
    dist[choice] = d
  dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
  #print("For predator dist is ", dist)
  pred_choices = []
  for key, value in dist.items():
    if value == list(dist.values())[0]:
      pred_choices.append(key)
  predator_location = np.random.choice(pred_choices)
  return predator_location

def easily_distracted_predator(env , predator_loc, agent_loc):
  choices = env.edges[predator_loc]
  dist = {}
  for choice in choices:
    d = get_distance(choice, agent_loc, env.edges)
    dist[choice] = d
  dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
  #print("For easily distracted predator dist is ", dist)
  pred_optimal_choices = []
  neighbor_choices = []
  for key, value in dist.items():
    if value == list(dist.values())[0]:
      pred_optimal_choices.append(key)
    neighbor_choices.append(key)
  if random.random() <= 0.4:
    predator_location = np.random.choice(neighbor_choices)
  else:
    predator_location = np.random.choice(pred_optimal_choices)
  #print("distracted predator choose ", predator_location)
  return predator_location

def move_prey(env , prey_loc):
  choices = copy.deepcopy(env.edges[prey_loc])
  choices.append(prey_loc)
  prey_location = random.choice(choices)
  return prey_location

def get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc):
  agent_choice = None
  priority = {}
  for i in pred_locs:
    if pred_locs[i] > pred_distance and prey_locs[i] < prey_distance:
      priority[i] = 1
      continue
    if pred_locs[i] == pred_distance and prey_locs[i] < prey_distance:
      priority[i] = 2
      continue
    if pred_locs[i] > pred_distance and prey_locs[i] == prey_distance:
      priority[i] = 3
      continue
    if pred_locs[i] == pred_distance and prey_locs[i] == prey_distance:
      priority[i] = 4
      continue
    if pred_locs[i] > pred_distance:
      priority[i] = 5
      continue
    if pred_locs[i] == pred_distance:
      priority[i] = 6
      continue
    else:
      priority[i] = 7
  priority = {k: v for k, v in sorted(priority.items(), key=lambda item: item[1])}
  choices = []
  if list(priority.values())[0] == 7:
    return agent_loc
  for key, value in priority.items():
    if value == list(priority.values())[0]:
      choices.append(key)
  agent_choice = random.choice(choices)
  return agent_choice

def init_prey_probs(agent_loc, true_location = None):
  prey_prob = {}
  if true_location:
    for i in range(1, total_nodes+1):
      if(i == true_location):
        prey_prob[i] = 1
      else:
        prey_prob[i] = 0
    return prey_prob
  for i in range(1, total_nodes+1):
    if(i == agent_loc):
      prey_prob[i] = 0
    else:
      prey_prob[i] = 1/(total_nodes-1)
  return prey_prob

def choose_node_for_survey(prey_prob, predator=False, agent_loc = None, edges = None):
  prey_prob = {k: v for k, v in sorted(prey_prob.items(), key=lambda item: item[1], reverse=True)}
  choices = []
  if list(prey_prob.values())[0] == 1:
    # Agent is certain so not choosing anything
    return None
  for key, value in prey_prob.items():
    if value == list(prey_prob.values())[0]:
      choices.append(key)
  if not predator:
    agent_choice = random.choice(choices)
  else:
    distances = {}
    for choice in choices:
      distances[choice] = get_distance(agent_loc, choice, edges)
    distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
    choices = []
    for key, value in distances.items():
      if value == list(distances.values())[0]:
        choices.append(key)
    agent_choice = random.choice(choices)
  #print("Node choosen for surveying is ", agent_choice)
  return agent_choice

def update_prey_probs_by_survey_defective(prey_prob, true_prey_loc, survey_node):
  if survey_node == true_prey_loc:
    if random.random() <= 0.1:
      node_failure = 1 - prey_prob[survey_node]
      for i in range(1, total_nodes+1):
        if(i == survey_node):
          prey_prob[i] = 0
        else:
          prey_prob[i] = prey_prob[i]/node_failure
    else:
      for i in range(1, total_nodes+1):
        if(i == survey_node):
          prey_prob[i] = 1
        else:
          prey_prob[i] = 0
    return prey_prob
  else:
    node_failure = 1 - prey_prob[survey_node]
    for i in range(1, total_nodes+1):
      if(i == survey_node):
        prey_prob[i] = 0
      else:
        prey_prob[i] = prey_prob[i]/node_failure 
    #print("prey probs are ", prey_prob)
    return prey_prob

def update_prey_probs_by_survey_defective_account(prey_prob, true_prey_loc, survey_node):
  if survey_node == true_prey_loc:
    if random.random() <= 0.1:
      node_failure = 1*(1 - prey_prob[survey_node]) + 0.1*prey_prob[survey_node]
      for i in range(1, total_nodes+1):
        if(i == survey_node):
          prey_prob[i] = (prey_prob[i]*0.1)/node_failure
        else:
          prey_prob[i] = (prey_prob[i]*1)/node_failure
    else:
      for i in range(1, total_nodes+1):
        if(i == survey_node):
          prey_prob[i] = 1
        else:
          prey_prob[i] = 0
    return prey_prob
  else:
    node_failure = 1*(1 - prey_prob[survey_node]) + 0.1*prey_prob[survey_node]
    for i in range(1, total_nodes+1):
      if(i == survey_node):
        prey_prob[i] = (prey_prob[i]*0.1)/node_failure
      else:
        prey_prob[i] = (prey_prob[i]*1)/node_failure
    #print("Updated prey probs are ", prey_prob)
    return prey_prob
    
def update_prey_probs_by_survey(prey_prob, true_prey_loc, survey_node):
  if survey_node == true_prey_loc:
    for i in range(1, total_nodes+1):
      if(i == survey_node):
        prey_prob[i] = 1
      else:
        prey_prob[i] = 0
    return prey_prob
  else:
    node_failure = 1 - prey_prob[survey_node]
    for i in range(1, total_nodes+1):
      if(i == survey_node):
        prey_prob[i] = 0
      else:
        prey_prob[i] = prey_prob[i]/node_failure 
    #print("prey probs are ", prey_prob)
    return prey_prob

def update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice):
  if agent_choice == true_prey_loc:
    return prey_prob
  elif prey_prob[agent_choice] != 1:
    node_failure = 1 - prey_prob[agent_choice]
    #print("the prob of agent choice is ", prey_prob[agent_choice])
    for i in range(1, total_nodes+1):
      if(i == agent_choice):
        prey_prob[i] = 0
      else:
        prey_prob[i] = prey_prob[i]/node_failure
    return prey_prob

def update_prey_probs_by_prey_movement(prey_prob, edges):
  new_prey_prob = copy.deepcopy(prey_prob)
  for i in new_prey_prob:
    new_prey_prob[i] = 0
  for i in edges.keys():
    num_neighs = len(edges[i]) + 1
    for neigh in edges[i]:
      new_prey_prob[neigh] = new_prey_prob[neigh] + prey_prob[i]/num_neighs
    new_prey_prob[i] = new_prey_prob[i] + prey_prob[i]/num_neighs
  return new_prey_prob

def get_highest_prob(prey_prob, predator=False, agent_loc = None, edges = None):
  prey_prob_by_priority = {k: v for k, v in sorted(prey_prob.items(), key=lambda item: item[1], reverse=True)}
  choices = []
  for key, value in prey_prob_by_priority.items():
    if value == list(prey_prob_by_priority.values())[0]:
      choices.append(key)
  if not predator:
    agent_choice = random.choice(choices)
  else:
    distances = {}
    for choice in choices:
      distances[choice] = get_distance(agent_loc, choice, edges)
    distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
    choices = []
    for key, value in distances.items():
      if value == list(distances.values())[0]:
        choices.append(key)
    agent_choice = random.choice(choices)
  #print("Node choosen for surveying is ", agent_choice)
  return agent_choice

def update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges):
  pred_nodes = {}
  for i in pred_prob:
    if pred_prob[i] > 0:
      pred_nodes[i] = pred_prob[i]
    pred_prob[i] = 0
  #print("Predicting predator node locations : ", pred_nodes)
  for node in pred_nodes:
    pred_choices = []
    neighbor_choices = []
    choices = edges[node]
    dist = {}
    #print("Analysing probs for node ", node)
    for choice in choices:
      d = get_distance(choice, agent_loc, edges)
      dist[choice] = d
    dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
    for key, value in dist.items():
      if value == list(dist.values())[0]:
        pred_choices.append(key)
      neighbor_choices.append(key)
    optimal_choice_len = len(pred_choices)
    neighbor_choice_len = len(neighbor_choices)
    #print("Final pred choices that can take are ", pred_choices)
    #print("Final distracted choices that can take are ", distracted_choices)
    for i in pred_prob:
      if i in pred_choices:
        pred_prob[i] = pred_prob[i] + (0.6/optimal_choice_len)*pred_nodes[node]
      if i in neighbor_choices:
        pred_prob[i] = pred_prob[i] + (0.4/neighbor_choice_len)*pred_nodes[node]
  return pred_prob

def get_utility(pred_probs, prey_probs, agent_loc, true_prey_loc, true_pred_loc, edges, by=None):
  prey_prob = copy.deepcopy(prey_probs)
  pred_prob = copy.deepcopy(pred_probs)
  agent_choice = agent_loc
  if by == 'survey':
    pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
    if pred_survey_node:
      pred_prob = update_prey_probs_by_survey(pred_prob, true_pred_loc, pred_survey_node)
    else:
      prey_survey_node = choose_node_for_survey(prey_prob)
      if prey_survey_node:
        prey_prob = update_prey_probs_by_survey(prey_prob, true_prey_loc, prey_survey_node)
  else:
    pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
    prey_loc = get_highest_prob(prey_prob)
    agent_choices = edges[agent_loc]
    pred_distance = get_distance(agent_loc, pred_loc, edges)
    prey_distance = get_distance(agent_loc, prey_loc, edges)
    prey_locs = {}
    pred_locs = {}
    for choice in agent_choices:
      prey_locs[choice] = get_distance(choice, prey_loc, edges)
      pred_locs[choice] = get_distance(choice, pred_loc, edges)
    agent_choice = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
    prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
    pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
  pred_weighted_dist = 0
  prey_weighted_dist = 0
  for i in pred_prob:
    pred_weighted_dist += get_distance(agent_choice, i, edges)*pred_prob[i]
    prey_weighted_dist += get_distance(agent_choice, i, edges)*prey_prob[i]
  cost = prey_weighted_dist/pred_weighted_dist
  utility = 1/cost
  return utility