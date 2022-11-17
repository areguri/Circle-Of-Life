
import copy
import argparse
import numpy as np
import random
import sys
import os
total_cell_n = 51

sys.path.append(os.path.abspath(__file__))
from environment import *
from utils import *

class Agent(The_Environment):
  def __init__(self):
    pass

  def agent_1(self, env , init_step_count):
    agent_loc = env.agent_location
    prey_loc = env.prey_location
    pred_loc = env.predator_location
    edges = env.edges
    step_count = 0
    while(True):
      #print("Agent, prey and predator locations are ", agent_loc, prey_loc, pred_loc)
      if(prey_loc == agent_loc):
        print("Agent  caught the prey")
        return True, False, step_count 
      if(agent_loc == pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      agent_choices = edges[agent_loc]
      #print("Agent choices ", agent_choices)
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        #print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          prey_locs[choice] = get_distance(choice, prey_loc, edges)
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        #print("Agent choices by prey ", prey_locs)
        #print("Agent choices by pred ", pred_locs)
        #print("Prey and pred distance is  ", prey_distance, "and ", pred_distance)
        agent_choice = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
        agent_loc = agent_choice
        #print("Agent choice is ", agent_choice)
      step_count = step_count + 1
      if(step_count == init_step_count):
        print("Agent died because of timeout")
        return False, True, 0
      if(agent_loc == pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      if(prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      prey_loc = move_prey(env,prey_loc)
      pred_loc = move_predator(env,pred_loc,agent_loc)

  def agent_2(self, env,init_step_count):
    agent_loc = env.agent_location
    prey_loc = env.prey_location
    pred_loc = env.predator_location
    edges = copy.deepcopy(env.edges)
    step_count = 0
    while(True and step_count <= init_step_count ):
      #print("Agent, prey and predator locations are ", agent_loc, prey_loc, pred_loc)
      if(prey_loc == agent_loc):
        print("Agent caught the prey")
        return True , False , step_count
      if(agent_loc == pred_loc):
        print("Predator caught Agent 2")
        return False , False ,step_count
      agent_choices = edges[agent_loc]
      # print("Agent choices ", agent_choices)
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("Agent found the prey in neighbour")
        agent_loc = prey_loc
      else:
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          distance = 0
          if get_distance(choice, pred_loc, edges) < 2 : 
            continue
          prey_neighbours = edges[prey_loc]
          for prey_neighbr in prey_neighbours:
            distance += get_distance(choice,prey_neighbr, edges)
          prey_locs[choice] = distance/len(prey_neighbours)
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        if len(prey_locs) > 0 :
          agent_loc = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
      if(agent_loc == pred_loc):
        print("Predator caught the agent")
        return False , False , step_count
      if(prey_loc == agent_loc):
        print("Agent caught the prey")
        return True , False , step_count
      prey_loc = move_prey(env,prey_loc)
      pred_loc = move_predator(env,pred_loc,agent_loc)
      step_count+=1
    print("Agent died because of timeout")
    return False , True , 0
    
  def agent_3(self, env,init_step_count, prey_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    prey_loc = None
    pred_loc = env.predator_location
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    #print("Initial prey probs are ", prey_prob)
    #print("True prey location is ", true_prey_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, pred_loc)
      if(true_prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      survey_node = choose_node_for_survey(prey_prob)
      if survey_node:
        #print("Survey is chosen, updating probabilities by survey for ", survey_node)
        prey_prob = update_prey_probs_by_survey(prey_prob, true_prey_loc, survey_node)
        if 1 in list(prey_prob.values()):
          prey_certainity["agent_3"] = prey_certainity["agent_3"] + 1
      else:
        prey_certainity["agent_3"] = prey_certainity["agent_3"] + 1
      #print("prey probs after survey :", prey_prob)
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
      #print("Agent choice is ", agent_choice)
      #print("prey probs after agent movement :", prey_prob)
      agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      if step_count == init_step_count:
        print("Aborting since reached maxm steps")
        return False, True, 0
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      true_prey_loc = move_prey(env, true_prey_loc)
      #print("prey probs after prey movement :", prey_prob)
      #print("Sum of prey probs is ", find_sum(prey_prob))
      pred_loc = move_predator(env,pred_loc,agent_loc)
 
  def agent_4(self, env,init_step_count, prey_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    prey_loc = None
    pred_loc = env.predator_location
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    while(True and step_count <= init_step_count ):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, pred_loc)
      if(true_prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False , step_count
      if(agent_loc == pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      survey_node = choose_node_for_survey(prey_prob)
      if survey_node:
        #print("Survey is chosen, updating probabilities by survey")
        prey_prob = update_prey_probs_by_survey(prey_prob, true_prey_loc, survey_node)
        if 1 in list(prey_prob.values()):
          prey_certainity["agent_4"] = prey_certainity["agent_4"] + 1
      #print("prey probs after survey :", prey_prob)
      else:
        prey_certainity["agent_4"] = prey_certainity["agent_4"] + 1
      prey_loc = get_highest_prob(prey_prob)
      agent_choices = edges[agent_loc]
      pred_distance = get_distance(agent_loc, pred_loc, edges)
      prey_distance = get_distance(agent_loc, prey_loc, edges)
      prey_locs = {}
      pred_locs = {}
      
      for choice in agent_choices:
        distance = 0
        probabolity_sum = 0
        
        if get_distance(choice, pred_loc, edges) < 2 : 
            continue
        prey_neighbours = edges[prey_loc]
        for prey_neighbr in prey_neighbours:
          if prey_prob[prey_neighbr] == 0 :
            distance += get_distance(choice,prey_neighbr, edges)
          else :
            distance += prey_prob[prey_neighbr]*get_distance(choice,prey_neighbr, edges)
          probabolity_sum += prey_prob[prey_neighbr]
        if probabolity_sum == 0 :
          prey_locs[choice] = distance/len(prey_neighbours)
        else:
          prey_locs[choice] = distance/probabolity_sum
        pred_locs[choice] = get_distance(choice, pred_loc, edges)
      agent_choice = agent_loc
      if len(prey_locs) >0:
        agent_choice = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
      prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
      #print("prey probs after agent movement :", prey_prob)
      agent_loc = agent_choice
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_loc = move_predator(env,pred_loc,agent_loc)
      step_count+=1
    print("Agent died because of timeout")
    return False , True,0

  def agent_5(self, env , init_step_count, predator_certainity):
    agent_loc = env.agent_location
    prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    edges = env.edges
    step_count = 0
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    #print("Initial pred probs are ", pred_prob)
    #print("True pred location is ", true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, prey_loc, true_pred_loc)
      if(prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if survey_node:
        #print("Survey node is chosen, updating probabilities by survey")
        pred_prob = update_prey_probs_by_survey(pred_prob, true_pred_loc, survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_5"] = predator_certainity["agent_5"] + 1
      else:
        predator_certainity["agent_5"] = predator_certainity["agent_5"] + 1
      #print("pred probs after survey :", pred_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      agent_choices = edges[agent_loc]
      pred_distance = get_distance(agent_loc, pred_loc, edges)
      prey_distance = get_distance(agent_loc, prey_loc, edges)
      prey_locs = {}
      pred_locs = {}
      for choice in agent_choices:
        prey_locs[choice] = get_distance(choice, prey_loc, edges)
        pred_locs[choice] = get_distance(choice, pred_loc, edges)
      agent_choice = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
      pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
      #print("pred probs after agent movement :", pred_prob)
      agent_loc = agent_choice
      step_count = step_count + 1
      if(prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      if step_count == init_step_count:
        print("Aborting since reached maxm steps")
        return False, True, 0
      prey_loc = move_prey(env, prey_loc)
      #print("Before update:, pred probs are ", pred_prob)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      #print("After update:, pred probs are ", pred_prob)
      #print("pred probs after pred movement :", pred_prob)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
      #print("Predator location is ", true_pred_loc)

  def agent_6_old(self, env , init_step_count):
    agent_loc = env.agent_location
    prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    edges = env.edges
    step_count = 0
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    print("Initial pred probs are ", pred_prob)
    #print("True pred location is ", true_pred_loc)
    while(True):
      print("Agent location, prey and predator location are ", agent_loc, prey_loc, true_pred_loc)
      if(prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if survey_node:
        print("Survey node is chosen, updating probabilities by survey")
        pred_prob = update_prey_probs_by_survey(pred_prob, true_pred_loc, survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_6"] = predator_certainity["agent_6"] + 1
      else:
        predator_certainity["agent_6"] = predator_certainity["agent_6"] + 1
      print("pred probs after survey :", pred_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      agent_choices = edges[agent_loc]
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          if get_distance(choice, pred_loc, edges) < 2 : 
              continue
          distance = 0
          prey_neighbours = edges[prey_loc]
          removed_prey_edge = copy.deepcopy(edges)
          for prey_neighbr in prey_neighbours:
            removed_prey_edge[prey_neighbr].remove(prey_loc)
          for prey_neighbr in prey_neighbours:
            distance += get_distance(choice,prey_neighbr, removed_prey_edge)
          prey_locs[choice] = distance/len(prey_neighbours)
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        agent_choice = agent_loc
        if len(prey_locs) >0:
          #agent_choice =  min(prey_locs, key=prey_locs.get)
          agent_choice = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        print("pred probs after agent movement :", pred_prob)
        agent_loc = agent_choice
        print("prey and pred locs are ", prey_locs, pred_locs)
      step_count = step_count + 1
      if(prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      if step_count == init_step_count:
        print("Aborting since reached maxm steps")
        return False, True, 0
      prey_loc = move_prey(env, prey_loc)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      #print("pred probs after pred movement :", pred_prob)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)

  def agent_7(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    #print("Initial pred probs are ", pred_prob)
    #print("True pred location is ", true_pred_loc)
    #print("Initial prey probs are ", prey_prob)
    #print("True prey location is ", true_prey_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_7"] = predator_certainity["agent_7"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_7"] = predator_certainity["agent_7"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_7"] = prey_certainity["agent_7"] + 1
        else:
          prey_certainity["agent_7"] = prey_certainity["agent_7"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
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
      #print("Agent choice is: ", agent_choice)
      pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
      prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
      #print("pred probs after agent movement :", pred_prob)
      #print("Prey probs after agent movement :", prey_prob)
      agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      if step_count == init_step_count:
        #print("Aborting since reached maxm steps")
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
      #print("pred probs after pred movement :", pred_prob)
      #print("prey probs after prey movement :", prey_prob)

  def agent_7_defective_no_account(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey_defective(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_7_def_drone"] = predator_certainity["agent_7_def_drone"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_7_def_drone"] = predator_certainity["agent_7_def_drone"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey_defective(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_7_def_drone"] = prey_certainity["agent_7_def_drone"] + 1
        else:
          prey_certainity["agent_7_def_drone"] = prey_certainity["agent_7_def_drone"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
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
      #print("Agent choice is: ", agent_choice)
      pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
      prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
      #print("pred probs after agent movement :", pred_prob)
      #print("Prey probs after agent movement :", prey_prob)
      agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      if step_count == init_step_count:
        #print("Aborting since reached maxm steps")
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
      #print("pred probs after pred movement :", pred_prob)
      #print("prey probs after prey movement :", prey_prob)

  def agent_7_defective_account(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey_defective_account(pred_prob, true_pred_loc, pred_survey_node)
        #print("Updated pred probs are ", pred_prob)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_7_def_acc_drone"] = predator_certainity["agent_7_def_acc_drone"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_7_def_acc_drone"] = predator_certainity["agent_7_def_acc_drone"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey_defective_account(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_7_def_acc_drone"] = prey_certainity["agent_7_def_acc_drone"] + 1
          #print("Updated prey probs are ", prey_prob)
        else:
          prey_certainity["agent_7_def_acc_drone"] = prey_certainity["agent_7_def_acc_drone"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
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
      #print("Agent choice is: ", agent_choice)
      pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
      prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
      #print("pred probs after agent movement :", pred_prob)
      #print("Prey probs after agent movement :", prey_prob)
      agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      if step_count == init_step_count:
        #print("Aborting since reached maxm steps")
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
      #print("pred probs after pred movement :", pred_prob)
      #print("prey probs after prey movement :", prey_prob)
    
  def agent_8_old(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_8"] = predator_certainity["agent_8"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_8"] = predator_certainity["agent_8"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_8"] = prey_certainity["agent_8"] + 1
        else:
          prey_certainity["agent_8"] = prey_certainity["agent_8"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      prey_loc = get_highest_prob(prey_prob)
      agent_choices = edges[agent_loc]
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          distance = 0
          probabolity_sum = 0
          if get_distance(choice, pred_loc, edges) < 2 : 
              continue
          prey_neighbours = edges[prey_loc]
          for prey_neighbr in prey_neighbours:
            if prey_prob[prey_neighbr] == 0 :
              distance += get_distance(choice,prey_neighbr, edges)
            else :
              distance += prey_prob[prey_neighbr]*get_distance(choice,prey_neighbr, edges)
            probabolity_sum += prey_prob[prey_neighbr]
          if probabolity_sum == 0 :
            prey_locs[choice] = distance/len(prey_neighbours)
          else:
            prey_locs[choice] = distance/probabolity_sum
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        agent_choice = agent_loc
        if len(prey_locs) >0:
            #agent_choice =  min(prey_locs, key=prey_locs.get)
          agent_choice = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
        #print("Agent choice is: ", agent_choice)
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
        
        agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        return False, False, step_count
      if step_count == init_step_count:
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
  
  def agent_8_defective_no_account_old(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey_defective(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_8_def_drone"] = predator_certainity["agent_8_def_drone"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_8_def_drone"] = predator_certainity["agent_8_def_drone"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey_defective(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_8_def_drone"] = prey_certainity["agent_8_def_drone"] + 1
        else:
          prey_certainity["agent_8_def_drone"] = prey_certainity["agent_8_def_drone"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      prey_loc = get_highest_prob(prey_prob)
      agent_choices = edges[agent_loc]
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          if get_distance(choice, pred_loc, edges) < 2 : 
              continue
          prey_locs[choice] = get_distance(choice, prey_loc, edges)
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        agent_choice = agent_loc
        if len(prey_locs) >0:
          #agent_choice =  min(prey_locs, key=prey_locs.get)
          agent_choice = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
        #print("Agent choice is: ", agent_choice)
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
        
        agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        return False, False, step_count
      if step_count == init_step_count:
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
  
  def agent_8_defective_account_old(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey_defective_account(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_8_def_acc_drone"] = predator_certainity["agent_8_def_acc_drone"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_8_def_acc_drone"] = predator_certainity["agent_8_def_acc_drone"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey_defective_account(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_8_def_acc_drone"] = prey_certainity["agent_8_def_acc_drone"] + 1
        else:
          prey_certainity["agent_8_def_acc_drone"] = prey_certainity["agent_8_def_acc_drone"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      prey_loc = get_highest_prob(prey_prob)
      agent_choices = edges[agent_loc]
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          if get_distance(choice, pred_loc, edges) < 2 : 
              continue
          prey_locs[choice] = get_distance(choice, prey_loc, edges)
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        agent_choice = agent_loc
        if len(prey_locs) >0:
            #agent_choice =  min(prey_locs, key=prey_locs.get)
          agent_choice = get_full_information_choice(prey_locs, pred_locs, prey_distance, pred_distance, agent_loc)
        #print("Agent choice is: ", agent_choice)
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
        
        agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        return False, False, step_count
      if step_count == init_step_count:
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)

  def bonus_agent(self, env, init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      if(true_prey_loc == agent_loc):
        print("Prey entered Agent cell")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Predator enetered agent cell")
        return False, False, step_count
      pred_prob = {k: v for k, v in sorted(pred_prob.items(), key=lambda item: item[1], reverse=True)}
      #print("prey predator and agent locs are ", true_prey_loc, true_pred_loc, agent_loc)
      
      u1 = get_utility(pred_prob, prey_prob, agent_loc, prey_loc, pred_loc, edges, by='suvrey')
      u2 = get_utility(pred_prob, prey_prob, agent_loc, prey_loc, pred_loc, edges, by='move')
      if 1 in list(pred_prob.values()):
        predator_certainity["bonus_agent"] = predator_certainity["bonus_agent"] + 1
      agent_choice = agent_loc
      if u1 > u2:
        #print("Utility of survey is more. Hence surveying.")
        pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
        if pred_survey_node:
          #print("Agent is not certain where the predator is, surveying for predator")
          pred_prob = update_prey_probs_by_survey_defective_account(pred_prob, true_pred_loc, pred_survey_node)
          if 1 in list(pred_prob.values()):
            predator_certainity["bonus_agent"] = predator_certainity["bonus_agent"] + 1
        else:
          #print("Agent is certain where the predator is, surveying for prey")
          predator_certainity["bonus_agent"] = predator_certainity["bonus_agent"] + 1
          prey_survey_node = choose_node_for_survey(prey_prob)
          #print("Node chosen for prey survey is  ", prey_survey_node)
          if prey_survey_node:
            prey_prob = update_prey_probs_by_survey_defective_account(prey_prob, true_prey_loc, prey_survey_node)
            if 1 in list(prey_prob.values()):
              prey_certainity["bonus_agent"] = prey_certainity["bonus_agent"] + 1
          else:
            prey_certainity["bonus_agent"] = prey_certainity["bonus_agent"] + 1
            #print("Agent is certain where the prey is")
      else:
        #print("Utility of movement is more. Hence moving.")
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
        #print("Agent choice is: ", agent_choice)
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
        #print("pred probs after agent movement :", pred_prob)
        #print("Prey probs after agent movement :", prey_prob)
      agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Agent entered predator cell")
        return False, False, step_count
      if step_count == init_step_count:
        print("Aborting since reached maxm steps")
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
      #print("pred probs after pred movement :", pred_prob)
      #print("prey probs after prey movement :", prey_prob)

  def agent_6(self, env , init_step_count, predator_certainity):
    agent_loc = env.agent_location
    prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    edges = env.edges
    step_count = 0
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    #print("Initial pred probs are ", pred_prob)
    #print("True pred location is ", true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, prey_loc, true_pred_loc)
      if(prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if survey_node:
        #print("Survey node is chosen, updating probabilities by survey")
        pred_prob = update_prey_probs_by_survey(pred_prob, true_pred_loc, survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_6"] = predator_certainity["agent_6"] + 1
      else:
        predator_certainity["agent_6"] = predator_certainity["agent_6"] + 1
      #print("pred probs after survey :", pred_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      agent_choices = edges[agent_loc]
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        simulated_pred_loc = easily_distracted_predator(env, pred_loc, agent_loc)
        pred_distance = get_distance(agent_loc, simulated_pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        restricted_choices = []
        for choice in agent_choices:
          if get_distance(choice, pred_loc, edges) < 2 : 
              restricted_choices.append(choice)
              continue
          distance = 0
          prey_neighbours = edges[prey_loc]
          removed_prey_edge = copy.deepcopy(edges)
          for prey_neighbr in prey_neighbours:
            removed_prey_edge[prey_neighbr].remove(prey_loc)
          for prey_neighbr in prey_neighbours:
            distance += get_distance(choice,prey_neighbr, removed_prey_edge)
          prey_locs[choice] = distance/len(prey_neighbours)
        pred_choices = []
        neighbor_choices = []
        dist = {}
        for p_choice in edges[pred_loc]:
          d = get_distance(p_choice, agent_loc, edges)
          dist[p_choice] = d
        dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
        for key, value in dist.items():
          if value == list(dist.values())[0]:
            pred_choices.append(key)
          neighbor_choices.append(key)
        optimal_choice_len = len(pred_choices)
        neighbor_choice_len = len(neighbor_choices)
        simulate_prob = {}
        for i in edges[pred_loc]:
          simulate_prob[i] = 0
          if i in pred_choices:
            simulate_prob[i] += 0.6/optimal_choice_len
          if i in neighbor_choices:
            simulate_prob[i] += 0.4/neighbor_choice_len
        
        for choice in agent_choices:
          if choice in restricted_choices:
            continue
          d = 0
          for pred_choice in edges[pred_loc]:
              d += get_distance(pred_choice, choice, edges)*simulate_prob[pred_choice]
          pred_locs[choice] = d
        
        #print("prey and pred locs are ", prey_locs, pred_locs)
        agent_choice = agent_loc
        prey_locs = {k: v for k, v in sorted(prey_locs.items(), key=lambda item: item[1])}
        maxm = 0
        for i in prey_locs:
          if (pred_locs[i] > maxm):
            maxm = pred_locs[i]
            agent_choice = i
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        #print("pred probs after agent movement :", pred_prob)
        agent_loc = agent_choice
      step_count = step_count + 1
      if(prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      if step_count == init_step_count:
        print("Aborting since reached maxm steps")
        return False, True, 0
      prey_loc = move_prey(env, prey_loc)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
  
  def agent_8(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_8"] = predator_certainity["agent_8"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_8"] = predator_certainity["agent_8"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_8"] = prey_certainity["agent_8"] + 1
        else:
          prey_certainity["agent_8"] = prey_certainity["agent_8"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      prey_loc = get_highest_prob(prey_prob)
      agent_choices = edges[agent_loc]
      restricted_choices = []
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          distance = 0
          probabolity_sum = 0
          if get_distance(choice, pred_loc, edges) < 2 : 
              restricted_choices.append(choice)
              continue
          prey_neighbours = edges[prey_loc]
          for prey_neighbr in prey_neighbours:
            if prey_prob[prey_neighbr] == 0 :
              distance += get_distance(choice,prey_neighbr, edges)
            else :
              distance += prey_prob[prey_neighbr]*get_distance(choice,prey_neighbr, edges)
            probabolity_sum += prey_prob[prey_neighbr]
          if probabolity_sum == 0 :
            prey_locs[choice] = distance/len(prey_neighbours)
          else:
            prey_locs[choice] = distance/probabolity_sum
        
        agent_choice = agent_loc
        pred_choices = []
        neighbor_choices = []
        dist = {}
        for p_choice in edges[pred_loc]:
          d = get_distance(p_choice, agent_loc, edges)
          dist[p_choice] = d
        dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
        for key, value in dist.items():
          if value == list(dist.values())[0]:
            pred_choices.append(key)
          neighbor_choices.append(key)
        optimal_choice_len = len(pred_choices)
        neighbor_choice_len = len(neighbor_choices)
        simulate_prob = {}
        for i in edges[pred_loc]:
          simulate_prob[i] = 0
          if i in pred_choices:
            simulate_prob[i] += 0.6/optimal_choice_len
          if i in neighbor_choices:
            simulate_prob[i] += 0.4/neighbor_choice_len
        
        for choice in agent_choices:
          if choice in restricted_choices:
            continue
          d = 0
          for pred_choice in edges[pred_loc]:
              d += get_distance(pred_choice, choice, edges)*simulate_prob[pred_choice]
          pred_locs[choice] = d
        
        #print("prey and pred locs are ", prey_locs, pred_locs)
        agent_choice = agent_loc
        prey_locs = {k: v for k, v in sorted(prey_locs.items(), key=lambda item: item[1])}
        maxm = 0
        for i in prey_locs:
          if (pred_locs[i] > maxm):
            maxm = pred_locs[i]
            agent_choice = i
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
        
        agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        print("Predator caught the agent")
        return False, False, step_count
      if step_count == init_step_count:
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)

  def agent_8_defective_no_account(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey_defective(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_8_def_drone"] = predator_certainity["agent_8_def_drone"] + 1
      else:
        restricted_choices = []
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_8_def_drone"] = predator_certainity["agent_8_def_drone"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey_defective(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_8_def_drone"] = prey_certainity["agent_8_def_drone"] + 1
        else:
          prey_certainity["agent_8_def_drone"] = prey_certainity["agent_8_def_drone"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      prey_loc = get_highest_prob(prey_prob)
      agent_choices = edges[agent_loc]
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          if get_distance(choice, pred_loc, edges) < 2 : 
              restricted_choices.append(choice)
              continue
          prey_locs[choice] = get_distance(choice, prey_loc, edges)
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        agent_choice = agent_loc
        pred_choices = []
        neighbor_choices = []
        dist = {}
        for p_choice in edges[pred_loc]:
          d = get_distance(p_choice, agent_loc, edges)
          dist[p_choice] = d
        dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
        for key, value in dist.items():
          if value == list(dist.values())[0]:
            pred_choices.append(key)
          neighbor_choices.append(key)
        optimal_choice_len = len(pred_choices)
        neighbor_choice_len = len(neighbor_choices)
        simulate_prob = {}
        for i in edges[pred_loc]:
          simulate_prob[i] = 0
          if i in pred_choices:
            simulate_prob[i] += 0.6/optimal_choice_len
          if i in neighbor_choices:
            simulate_prob[i] += 0.4/neighbor_choice_len
        
        for choice in agent_choices:
          if choice in restricted_choices:
            continue
          d = 0
          for pred_choice in edges[pred_loc]:
              d += get_distance(pred_choice, choice, edges)*simulate_prob[pred_choice]
          pred_locs[choice] = d
        
        #print("prey and pred locs are ", prey_locs, pred_locs)
        agent_choice = agent_loc
        prey_locs = {k: v for k, v in sorted(prey_locs.items(), key=lambda item: item[1])}
        maxm = 0
        for i in prey_locs:
          if (pred_locs[i] > maxm):
            maxm = pred_locs[i]
            agent_choice = i

        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
        
        agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        return False, False, step_count
      if step_count == init_step_count:
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)
  
  def agent_8_defective_account(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey_defective_account(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_8_def_acc_drone"] = predator_certainity["agent_8_def_acc_drone"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_8_def_acc_drone"] = predator_certainity["agent_8_def_acc_drone"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey_defective_account(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_8_def_acc_drone"] = prey_certainity["agent_8_def_acc_drone"] + 1
        else:
          prey_certainity["agent_8_def_acc_drone"] = prey_certainity["agent_8_def_acc_drone"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      prey_loc = get_highest_prob(prey_prob)
      agent_choices = edges[agent_loc]
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        restricted_choices = []
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          if get_distance(choice, pred_loc, edges) < 2 : 
              restricted_choices.append(choice)
              continue
          prey_locs[choice] = get_distance(choice, prey_loc, edges)
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        agent_choice = agent_loc
        pred_choices = []
        neighbor_choices = []
        dist = {}
        for p_choice in edges[pred_loc]:
          d = get_distance(p_choice, agent_loc, edges)
          dist[p_choice] = d
        dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
        for key, value in dist.items():
          if value == list(dist.values())[0]:
            pred_choices.append(key)
          neighbor_choices.append(key)
        optimal_choice_len = len(pred_choices)
        neighbor_choice_len = len(neighbor_choices)
        simulate_prob = {}
        for i in edges[pred_loc]:
          simulate_prob[i] = 0
          if i in pred_choices:
            simulate_prob[i] += 0.6/optimal_choice_len
          if i in neighbor_choices:
            simulate_prob[i] += 0.4/neighbor_choice_len
        
        for choice in agent_choices:
          if choice in restricted_choices:
            continue
          d = 0
          for pred_choice in edges[pred_loc]:
              d += get_distance(pred_choice, choice, edges)*simulate_prob[pred_choice]
          pred_locs[choice] = d
        
        #print("prey and pred locs are ", prey_locs, pred_locs)
        agent_choice = agent_loc
        prey_locs = {k: v for k, v in sorted(prey_locs.items(), key=lambda item: item[1])}
        maxm = 0
        for i in prey_locs:
          if (pred_locs[i] > maxm):
            maxm = pred_locs[i]
            agent_choice = i
        #print("Agent choice is: ", agent_choice)
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
        
        agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        return False, False, step_count
      if step_count == init_step_count:
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)

  def agent_9(self, env , init_step_count, prey_certainity, predator_certainity):
    agent_loc = env.agent_location
    true_prey_loc = env.prey_location
    true_pred_loc = env.predator_location
    pred_loc = true_pred_loc
    prey_loc = None
    edges = env.edges
    step_count = 0
    prey_prob = init_prey_probs(agent_loc)
    pred_prob = init_prey_probs(agent_loc, true_location=true_pred_loc)
    while(True):
      #print("Agent location, prey and predator location are ", agent_loc, true_prey_loc, true_pred_loc)
      if(true_prey_loc == agent_loc):
        #print("Agent caught the prey")
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        #print("Predator caught the agent")
        return False, False, step_count
      pred_survey_node = choose_node_for_survey(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      if pred_survey_node:
        #print("Agent is not certain where the predator is, surveying for predator")
        pred_prob = update_prey_probs_by_survey_defective_account(pred_prob, true_pred_loc, pred_survey_node)
        if 1 in list(pred_prob.values()):
          predator_certainity["agent_9"] = predator_certainity["agent_9"] + 1
      else:
        #print("Agent is certain where the predator is, surveying for prey")
        predator_certainity["agent_9"] = predator_certainity["agent_9"] + 1
        prey_survey_node = choose_node_for_survey(prey_prob)
        #print("Node chosen for prey survey is  ", prey_survey_node)
        if prey_survey_node:
          prey_prob = update_prey_probs_by_survey_defective_account(prey_prob, true_prey_loc, prey_survey_node)
          if 1 in list(prey_prob.values()):
            prey_certainity["agent_9"] = prey_certainity["agent_9"] + 1
        else:
          prey_certainity["agent_9"] = prey_certainity["agent_9"] + 1
          print("Agent is certain where the prey is")
      #print("pred probs after survey :", pred_prob)
      #print("prey probs after survey : ", prey_prob)
      pred_loc = get_highest_prob(pred_prob, predator=True, agent_loc=agent_loc, edges=edges)
      prey_loc = get_highest_prob(prey_prob)
      agent_choices = edges[agent_loc]
      if (prey_loc in agent_choices and prey_loc != pred_loc):
        print("found the prey in neighbour")
        agent_loc = prey_loc
      else:
        restricted_choices = []
        pred_distance = get_distance(agent_loc, pred_loc, edges)
        prey_distance = get_distance(agent_loc, prey_loc, edges)
        prey_locs = {}
        pred_locs = {}
        for choice in agent_choices:
          if get_distance(choice, pred_loc, edges) < 2 : 
              restricted_choices.append(choice)
              continue
          prey_locs[choice] = get_distance(choice, prey_loc, edges)
          pred_locs[choice] = get_distance(choice, pred_loc, edges)
        agent_choice = agent_loc
        pred_choices = []
        neighbor_choices = []
        dist = {}
        for p_choice in edges[pred_loc]:
          d = get_distance(p_choice, agent_loc, edges)
          dist[p_choice] = d
        dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
        for key, value in dist.items():
          if value == list(dist.values())[0]:
            pred_choices.append(key)
          neighbor_choices.append(key)
        optimal_choice_len = len(pred_choices)
        neighbor_choice_len = len(neighbor_choices)
        simulate_prob = {}
        for i in edges[pred_loc]:
          simulate_prob[i] = 0
          if i in pred_choices:
            simulate_prob[i] += 0.6/optimal_choice_len
          if i in neighbor_choices:
            simulate_prob[i] += 0.4/neighbor_choice_len
        
        for choice in agent_choices:
          if choice in restricted_choices:
            continue
          d = 0
          for pred_choice in edges[pred_loc]:
              d += get_distance(pred_choice, choice, edges)*simulate_prob[pred_choice]
          pred_locs[choice] = d
        
        #print("prey and pred locs are ", prey_locs, pred_locs)
        agent_choice = agent_loc
        prey_locs = {k: v for k, v in sorted(prey_locs.items(), key=lambda item: item[1])}
        maxm = 0
        for i in prey_locs:
          if (pred_locs[i] > maxm):
            maxm = pred_locs[i]
            agent_choice = i
        #print("Agent choice is: ", agent_choice)
        pred_prob = update_prey_probs_by_agent(pred_prob, true_pred_loc, agent_choice)
        prey_prob = update_prey_probs_by_agent(prey_prob, true_prey_loc, agent_choice)
        
        agent_loc = agent_choice
      step_count = step_count + 1
      if(true_prey_loc == agent_loc):
        return True, False, step_count
      if(agent_loc == true_pred_loc):
        return False, False, step_count
      if step_count == init_step_count:
        return False, True, 0
      true_prey_loc = move_prey(env, true_prey_loc)
      prey_prob = update_prey_probs_by_prey_movement(prey_prob, edges)
      pred_prob = update_pred_probs_by_pred_movement(pred_prob, agent_loc, edges)
      true_pred_loc = easily_distracted_predator(env, true_pred_loc, agent_loc)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--agent_1', action='store_true', default=False)
  parser.add_argument('--agent_2', action='store_true', default=False)
  parser.add_argument('--agent_3', action='store_true', default=False)
  parser.add_argument('--agent_4', action='store_true', default=False)
  parser.add_argument('--agent_5', action='store_true', default=False)
  parser.add_argument('--agent_7', action='store_true', default=False)
  parser.add_argument('--agent_7_defective_no_account', action='store_true', default=False)
  parser.add_argument('--agent_7_defective_account', action='store_true', default=False)
  parser.add_argument('--agent_8', action='store_true', default=False)
  parser.add_argument('--bonus_agent', action='store_true', default=False)
  parser.add_argument('--agent_6', action='store_true', default=False)
  parser.add_argument('--agent_8_defective_no_account', action='store_true', default=False)
  parser.add_argument('--agent_8_defective_account', action='store_true', default=False)
  parser.add_argument('--agent_9', action='store_true', default=False)
  
  prey_certainity = {'agent_7_def_acc_drone': 0,
 'agent_3': 0,
 'agent_4': 0,
 'agent_7': 0,
 'agent_7_def_drone': 0,
 'agent_8': 0,
 'agent_8_def_drone':0,
 'agent_8_def_acc_drone':0,
 'bonus_agent':0}
  predator_certainity = {'agent_7_def_acc_drone': 0,
 'agent_5': 0,
 'agent_6': 0,
 'agent_7': 0,
 'agent_7_def_drone': 0,
 'agent_8': 0,
 'agent_8_def_drone':0,
 'agent_8_def_acc_drone':0,
 'bonus_agent':0}
  args = parser.parse_args()
  env = The_Environment()

  agent = Agent()
  if args.agent_1:
    print(agent.agent_1(env, 50))
  if args.agent_2:
    print(agent.agent_2(env, 50))
  if args.agent_3:
    print(agent.agent_3(env, 100, prey_certainity))
    print("Prey certainity is ", prey_certainity)
  if args.agent_4:
    print(agent.agent_4(env, 100, prey_certainity))
    print("Prey certainity is ", prey_certainity)
  if args.agent_5:
    print(agent.agent_5(env, 100, predator_certainity))
    print("Predator certainity is ", predator_certainity)
  if args.agent_6:
    print(agent.agent_6(env, 100, predator_certainity))
    print("Predator certainity is ", predator_certainity)
  if args.agent_7:
    print(agent.agent_7(env, 150, prey_certainity, predator_certainity))
    print("Prey certainity is ", prey_certainity)
    print("Predator certainity is ", predator_certainity)
  if args.agent_7_defective_no_account:
    print(agent.agent_7_defective_no_account(env, 150, prey_certainity, predator_certainity))
    print("Prey certainity is ", prey_certainity)
    print("Predator certainity is ", predator_certainity)
  if args.agent_7_defective_account:
    print(agent.agent_7_defective_account(env, 150, prey_certainity, predator_certainity))
    print("Prey certainity is ", prey_certainity)
    print("Predator certainity is ", predator_certainity)
  if args.agent_8:
    print(agent.agent_8(env, 150, prey_certainity, predator_certainity))
    print("Prey certainity is ", prey_certainity)
    print("Predator certainity is ", predator_certainity)
  if args.bonus_agent:
    print(agent.bonus_agent(env,150, prey_certainity, predator_certainity))
    print("Prey certainity is ", prey_certainity)
    print("Predator certainity is ", predator_certainity)
  if args.agent_9:
    print(agent.agent_9(env, 100, prey_certainity, predator_certainity))
    print("Prey certainity is ", prey_certainity)
    print("Predator certainity is ", predator_certainity)
  if args.agent_8_defective_no_account:
    print(agent.agent_8_defective_no_account(env, 150, prey_certainity))
    print("Prey certainity is ", prey_certainity)
    print("Predator certainity is ", predator_certainity)
  if args.agent_8_defective_account:
    print(agent.agent_8_defective_account(env, 150, predator_certainity))
    print("Prey certainity is ", prey_certainity)
    print("Predator certainity is ", predator_certainity)

if __name__ == '__main__':
  main()