import argparse
import os
import sys
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath(__file__))

from environment import The_Environment
from agent import Agent

wins = {"agent_1":0, "agent_2":0, "agent_3":0, "agent_4":0, "agent_5":0, "agent_6":0, "agent_7":0, "agent_7_def_drone":0, "agent_7_def_acc_drone": 0, "agent_8":0, "agent_8_def_drone":0, "agent_8_def_acc_drone": 0, 'bonus_agent':0, 'agent_9':0}
timeouts = {"agent_1":0, "agent_2":0, "agent_3":0, "agent_4":0, "agent_5":0, "agent_6":0, "agent_7":0, "agent_7_def_drone":0, "agent_7_def_acc_drone": 0, "agent_8":0, "agent_8_def_drone":0, "agent_8_def_acc_drone": 0, 'bonus_agent':0, 'agent_9':0}
step_counts = {"agent_1":0, "agent_2":0, "agent_3":0, "agent_4":0, "agent_5":0, "agent_6":0, "agent_7":0, "agent_7_def_drone":0, "agent_7_def_acc_drone": 0, "agent_8":0, "agent_8_def_drone":0, "agent_8_def_acc_drone": 0, 'bonus_agent':0, 'agent_9':0}
prey_certainity = {'agent_7_def_acc_drone': 0,
 'agent_3': 0,
 'agent_4': 0,
 'agent_7': 0,
 'agent_7_def_drone': 0,
 'agent_8': 0,
 'agent_8_def_drone':0,
 'agent_8_def_acc_drone':0,
 'agent_9':0,
 'bonus_agent':0}
predator_certainity = {'agent_7_def_acc_drone': 0,
 'agent_5': 0,
 'agent_6': 0,
 'agent_7': 0,
 'agent_7_def_drone': 0,
 'agent_8': 0,
 'agent_8_def_drone':0,
 'agent_8_def_acc_drone':0,
 'bonus_agent':0,
 'agent_9':0}
for i in range(0, 3000):
  env = The_Environment()
  agent = Agent()
  success, timeout, step_count = agent.agent_1(env, 50)
  if success:
    wins["agent_1"] = wins["agent_1"] +1
  if timeout:
    timeouts["agent_1"] = timeouts["agent_1"] + timeout
  step_counts["agent_1"] = step_counts["agent_1"] + step_count
 
  success , timeout , step_count = agent.agent_2(env , 50)
  if success:
    wins["agent_2"] = wins["agent_2"] +1
  if timeout:
    timeouts["agent_2"] = timeouts["agent_2"] + timeout
  step_counts["agent_2"] = step_counts["agent_2"] + step_count
 
  success, timeout, step_count = agent.agent_3(env, 100, prey_certainity)
  if success:
    wins["agent_3"] = wins["agent_3"] +1
  if timeout:
    timeouts["agent_3"] = timeouts["agent_3"] + timeout
  step_counts["agent_3"] = step_counts["agent_3"] + step_count
 
  success, timeout, step_count  = agent.agent_4(env, 100, prey_certainity)
  if success:
    wins["agent_4"] = wins["agent_4"] +1
  if timeout:
    timeouts["agent_4"] = timeouts["agent_4"] + timeout
  step_counts["agent_4"] = step_counts["agent_4"] + step_count

  success, timeout, step_count = agent.agent_5(env, 100, predator_certainity)
  if success:
    wins["agent_5"] = wins["agent_5"] + 1
  if timeout:
    timeouts["agent_5"] = timeouts["agent_5"] + timeout
  step_counts["agent_5"] = step_counts["agent_5"] + step_count

  success, timeout, step_count = agent.agent_6(env, 100, predator_certainity)
  if success:
    wins["agent_6"] = wins["agent_6"] + 1
  if timeout:
    timeouts["agent_6"] = timeouts["agent_6"] + timeout
  step_counts["agent_6"] = step_counts["agent_6"] + step_count

  success, timeout, step_count = agent.agent_7(env, 150, prey_certainity, predator_certainity)
  if success:
    wins["agent_7"] = wins["agent_7"] + 1
  if timeout:
    timeouts["agent_7"] = timeouts["agent_7"] + timeout
  step_counts["agent_7"] = step_counts["agent_7"] + step_count

  success, timeout, step_count = agent.agent_7_defective_no_account(env, 150, prey_certainity, predator_certainity)
  if success:
    wins["agent_7_def_drone"] = wins["agent_7_def_drone"] + 1
  if timeout:
    timeouts["agent_7_def_drone"] = timeouts["agent_7_def_drone"] + timeout
  step_counts["agent_7_def_drone"] = step_counts["agent_7_def_drone"] + step_count

  success, timeout, step_count = agent.agent_7_defective_account(env, 150, prey_certainity, predator_certainity)
  if success:
    wins["agent_7_def_acc_drone"] = wins["agent_7_def_acc_drone"] + 1
  if timeout:
    timeouts["agent_7_def_acc_drone"] = timeouts["agent_7_def_acc_drone"] + timeout
  step_counts["agent_7_def_acc_drone"] = step_counts["agent_7_def_acc_drone"] + step_count

  success, timeout, step_count = agent.agent_8(env, 150, prey_certainity, predator_certainity)
  if success:
    wins["agent_8"] = wins["agent_8"] + 1
  if timeout:
    timeouts["agent_8"] = timeouts["agent_8"] + timeout
  step_counts["agent_8"] = step_counts["agent_8"] + step_count

  success, timeout, step_count = agent.agent_8_defective_no_account(env, 150, prey_certainity, predator_certainity)
  if success:
    wins["agent_8_def_drone"] = wins["agent_8_def_drone"] + 1
  if timeout:
    timeouts["agent_8_def_drone"] = timeouts["agent_8_def_drone"] + timeout
  step_counts["agent_8_def_drone"] = step_counts["agent_8_def_drone"] + step_count

  success, timeout, step_count = agent.agent_8_defective_account(env, 150, prey_certainity, predator_certainity)
  if success:
    wins["agent_8_def_acc_drone"] = wins["agent_8_def_acc_drone"] + 1
  if timeout:
    timeouts["agent_8_def_acc_drone"] = timeouts["agent_8_def_acc_drone"] + timeout
  step_counts["agent_8_def_acc_drone"] = step_counts["agent_8_def_acc_drone"] + step_count

  success, timeout, step_count = agent.bonus_agent(env, 100, prey_certainity, predator_certainity)
  if success:
    wins["bonus_agent"] = wins["bonus_agent"] + 1
  if timeout:
    timeouts["bonus_agent"] = timeouts["bonus_agent"] + timeout
  step_counts["bonus_agent"] = step_counts["bonus_agent"] + step_count

  success, timeout, step_count = agent.agent_9(env, 100, prey_certainity, predator_certainity)
  if success:
    wins["agent_9"] = wins["agent_9"] + 1
  if timeout:
    timeouts["agent_9"] = timeouts["agent_9"] + timeout
  step_counts["agent_9"] = step_counts["agent_9"] + step_count

for key in step_counts.keys():
  step_counts[key] = step_counts[key]/wins[key]

for k in wins.keys():
  if 'acc' in k:
    worker = k
    worker = worker.replace("_def_acc_drone", " defective drone accounting")
  elif 'def' in k:
    worker = k
    worker = worker.replace("_def_drone", " defective drone scenario")
  else:
    worker = k
  print("Analysis of ", worker)
  print("Success rate: ", (wins[k]/3000)*100)
  print("Timeout rate: ", k, (timeouts[k]/3000)*100)
  print("Average stepcount :", step_counts[k])
  if k in prey_certainity:
    print("Prey ceratinity :", prey_certainity[k]/3000)
  if k in predator_certainity:
    print("Predator certainity :", predator_certainity[k]/3000)
  print("****************************************************************************")