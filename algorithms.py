"""
This module contains the scheduling algorithms used in the scheduling API.

It provides implementations for both Least Deadline First (LDF) and Earliest Deadline First (EDF) scheduling strategies, applicable in single-core and multi-core processor environments. Functions within are designed to be called with specific application and platform data structures.

Functions:
- ldf_singlecore: Schedules tasks on a single-core processor using LDF.
- edf_singlecore: Schedules tasks on a single-core processor using EDF.
- rms_singlecore: Schedules tasks on a single-core processor using RMS.
- ll_singlecore: Schedules tasks on a single-core processor using LL.
- ldf_multicore: Schedules tasks on multiple cores using LDF.
- edf_multicore: Schedules tasks on multiple cores using EDF.
"""


import networkx as nx
from collections import defaultdict

# just an example for the structure of the schedule to be returned and to check the frontend and backend connection
example_schedule = [
    {
        "task_id": 3,
        "node_id": 0,
        "end_time": 20,
        "deadline": 256,
        "start_time": 0,
    },
    {
        "task_id": 2,
        "node_id": 0,
        "end_time": 40,
        "deadline": 300,
        "start_time": 20,
    },
    {
        "task_id": 1,
        "node_id": 0,
        "end_time": 60,
        "deadline": 250,
        "start_time": 40,
    },
    {
        "task_id": 0,
        "node_id": 0,
        "end_time": 80,
        "deadline": 250,
        "start_time": 60,
    },
]



def ldf_single_node(application_data):
    """
    Schedule jobs on a single node using the Latest Deadline First (LDF) strategy.

    This function schedules jobs based on their latest deadlines after sorting them and considering dependencies through a directed graph representation.

    .. todo:: Implement Latest Dealine First Scheduling (LDF) algorithm for single compute node.


    Args:
        application_data (dict): Contains jobs and messages that indicate dependencies among jobs.

    Returns:
        list of dict: Scheduling results with each job's details, including execution time, node assignment,
                      and start/end times relative to other jobs.
    """
    tasks = application_data["tasks"]   # Get the tasks list from "application_data"
    messages = application_data["messages"] # Get the massages list from "application_data"
    
    deadlines = {task["id"]: task["deadline"] for task in tasks}    # Initialize a dictionary to track the deadlines for each task
    wcets = {task["id"]: task["wcet"] for task in tasks}    # Initialize a dictionary to track the worst-case execution times "wcet" for each task
    
    dependencies = {}   # Initialize a dictionary to track task dependencies

    for message in messages:    # for-loop iterates over each message to establish dependencies
        sender = message["sender"]  # Get "sender" from messages list 
        receiver = message["receiver"]  # Get "receiver" from messages list
        dependencies.setdefault(receiver, []).append(sender)    # Add the sender to the list of dependencies for the receiver
    
    ready_task = [] # Initialize a list to track tasks that are ready to be scheduled
    schedule = []   # Initialize a list to store the scheduled tasks
    
    degree_out = defaultdict(int)   # Initialize a dictionary to track the number of dependencies (out-degree) for each task
    
    for sender, receivers in dependencies.items():  # for loop iterates over dependencies to count the out-degree
        for receiver in receivers:  # for-loop that iterates over each receiver for the current sender
            degree_out[receiver] += 1   # Increment the out-degree count for the receiver
        
    for task in deadlines.keys():   # for-loop iterates over each task in deadlines dictionary
        if degree_out[task] == 0:   # if a task has no dependencies:
            ready_task.append(task) # Add the task to the ready_task list

    current_endtime = sum(wcets.values())   # Initialize the current end time as the sum of all worst-case execution times

    while ready_task:    # while loop until there are no ready tasks
        task_id = max(ready_task, key = lambda t: deadlines[t]) # Select the task with the latest deadline from ready tasks
        ready_task.remove(task_id)  # Remove the selected task from ready tasks
        task_dict = {   # Create a dictionary for the scheduled task
        "task_id": task_id,
        "node_id": 0,
        "end_time": current_endtime,
        "deadline": deadlines[task_id],
        "start_time": current_endtime - wcets[task_id] 
        } 
        schedule.insert(0,task_dict)     # Insert the scheduled task at the beginning of the schedule list
        current_endtime = current_endtime - wcets[task_id]  # Update the current end time
        
        for receiver in dependencies.get(task_id, []):  # for-loop iterates over each receiver of the current task
            degree_out[receiver] -= 1   # Decrement the out-degree for the receiver
            if degree_out[receiver] == 0:   # if the receiver has no more dependencies:
                ready_task.append(receiver) # Add the receiver to the ready tasks
    
    return {"schedule": schedule, "name": "LDF Single Node"}




def edf_single_node(application_data):
    """
    Schedule jobs on single node using the Earliest Deadline First (EDF) strategy.

    This function processes application data to schedule jobs based on the earliest
    deadlines. It builds a dependency graph and schedules accordingly, ensuring that jobs with no predecessors are
    scheduled first, and subsequent jobs are scheduled based on the minimum deadline of available nodes.

    .. todo:: Implement Earliest Deadline First Scheduling (EDF) algorithm for single compute node.

    Args:
        application_data (dict): Job data including dependencies represented by messages between jobs.

    Returns:
        list of dict: Contains the scheduled job details, each entry detailing the node assigned, start and end times,
                      and the job's deadline.
    """
    tasks = application_data["tasks"]   # Get the tasks list from "application_data"
    messages = application_data["messages"] # Get the massages list from "application_data"
    
    deadlines = {task["id"]: task["deadline"] for task in tasks }   # Initialize a dictionary to track the deadlines for each node
    wcets = {task["id"]: task["wcet"] for task in tasks }   # Initialize a dictionary to track the worst-case execution times "wcet" for each task
    
    dependencies = {}   # Initialize a dictionary to track task dependencies
    
    for message in messages:    # for-loop iterates over each message to establish dependencies
        sender = message["sender"]  # Get "sender" from messages list 
        receiver = message["receiver"]  # Get "receiver" from messages list
        dependencies.setdefault(sender, []).append(receiver)    # Add the receiver to the list of dependencies for the sender
    
    ready_task = [] # Initialize a list to track tasks that are ready to be scheduled
    schedule = []   # Initialize a list to store the scheduled tasks
    
    degree_in = defaultdict(int)    # Initialize a dictionary to track the number of dependencies (in-degree) for each task
    
    for receivers, senders in dependencies.items(): # for loop iterates over dependencies to count the in-degrees
        for sender in senders:  # for-loop iterates over sender for current receivers
            degree_in[sender] += 1  # Increment the in-degree count for the sender
        
    for task in deadlines.keys():   # for-loop iterates over each task in deadlines
        if degree_in[task] == 0:    # if a task has no dependencies:
            ready_task.append(task) # Add the task to the ready_task list

    current_starttime = 0   # Initialize the current start time

    while ready_task:   # while loop until there are no ready tasks
        task_id = min(ready_task, key = lambda t: deadlines[t]) # Select the task with the earliest deadline from ready tasks
        ready_task.remove(task_id)  # Remove the selected task from ready tasks
        task_dict = {   # Create a dictionary for the scheduled task
        "task_id": task_id, 
        "node_id": 0,
        "end_time": current_starttime + wcets[task_id],
        "deadline": deadlines[task_id],
        "start_time": current_starttime  
        } 
        schedule.insert(0,task_dict)    # Insert the scheduled task at the beginning of the schedule list
        current_starttime = current_starttime + wcets[task_id]  # Update the current start time
        for sender in dependencies.get(task_id, []):    # for-loop iterates over each sender of the current task
            degree_in[sender] -= 1  # Decrement the in-degree for the sender
            if degree_in[sender] == 0:  # if the sender has no more dependencies:
                ready_task.append(sender)   # Add the sender to the ready tasks

    return {"schedule": schedule, "name": "EDF Single Node"}

def ll_multinode(application_data, platform_data):
    """
    Schedule jobs on a distributed system with multiple compute nodes using the Least Laxity (LL) strategy.
    This function schedules jobs based on their laxity, with the job having the least laxity being scheduled first.

    .. todo:: Implement Least Laxity (LL) algorithm to schedule jobs on multiple node in a distributed system.

    Args:
        application_data (dict): Job data including dependencies represented by messages between jobs.

    Returns:
        list of dict: Contains the scheduled job details, each entry detailing the node assigned, start and end times,
                      and the job's deadline.

    """
    tasks = application_data['tasks']   # Get the tasks list from "application_data"
    nodes = platform_data['nodes']  # Get the nodes list from "platform_data"
    
    running_time = 0    # Initiliaze running_time to 0 for the for-loop

    for task in tasks:  # for-loop iterates over each task
        task['laxity'] = task['deadline'] - (running_time + task['wcet'])   # Calculates Laxity of the tasks
    
    sorted_tasks = sorted(tasks, key=lambda x: x['laxity']) # Sort the tasks based on their laxity
    
    schedule = []   # Create a new list to store the tasks
    
    node_times = {node['id']: 0 for node in nodes}  # Initialize a dictionary to track the available times for each node
    dependencies = {task['id']: [] for task in tasks}   # Initialize a dictionary to track the dependencies for each task

    for message in application_data['messages']:    # Iterates over each message in "application_data"
         dependencies[message['receiver']].append(message['sender'])    # Add the sender of the message as a dependency for the receiver task 

    task_scheduled = {task['id']: False for task in tasks}  # Initialize a dictionary to track whether each task has been scheduled, starting with False

    while not all(task_scheduled.values()): # while-loop until every tasks have been scheduled
        for task in sorted_tasks:    # for-loop iterates over each task in sorted_tasks
            if task_scheduled[task['id']]:  # if the current task is already scheduled, continue with the next task
                continue
            
            if all(task_scheduled[d] for d in dependencies[task['id']]):    # if all dependencies of the task are scheduled:
                node_id, node_time = min(node_times.items(), key=lambda x: x[1])     # Get the node with the earliest available time
                start_time = max(node_time, max([sch['end_time'] for sch in schedule if sch['task_id'] in dependencies[task['id']]], default=0))    # Calculate the start time
                end_time = start_time + task['wcet']    # Calculate the end time of the current task by adding it's worst-case-execution time to current running time
                
                schedule.append({    # Append following elements to the schedule list to represent the scheduled task
                    'task_id': task['id'],
                    'node_id': node_id,
                    'start_time': start_time,
                    'end_time': end_time,
                    'deadline': task['deadline']
                })
                
                node_times[node_id] = end_time  # Set the node's available time to the end time of the current task
                task_scheduled[task['id']] = True   # Show the task as scheduled

        for task in tasks:  # for-loop iterates over each task
            if not task_scheduled[task['id']]:  # if the current task is not scheduled:
                task['laxity'] = task['deadline'] - (running_time + task['wcet'])   # Calculate the laxity of the task
        
        sorted_tasks = sorted(tasks, key=lambda x: x['laxity']) # Update "sorted_task" list based on the laxity of the tasks

    return {"schedule": schedule, "name": "LL Multi Node"}



def ldf_multinode(application_data, platform_data):
    """
    Schedule jobs on a distributed system with multiple compute nodes using the Latest Deadline First(LDF) strategy.
    This function schedules jobs based on their periods and deadlines, with the shortest period job being scheduled first.

    .. todo:: Implement Latest Deadline First(LDF) algorithm to schedule jobs on multiple nodes in a distributed system.

    Args:
        application_data (dict): Job data including dependencies represented by messages between jobs.
        platform_data (dict): Contains information about the platform, nodes and their types, the links between the nodes and the associated link delay.

    Returns:
        list of dict: Contains the scheduled job details, each entry detailing the node assigned, start and end times,
                      and the job's deadline.

    """
    tasks = application_data['tasks']   # Get the tasks list from "application_data"
    nodes = platform_data['nodes']  # Get the nodes list from "platform_data"
    
    sorted_tasks = sorted(tasks, key=lambda x: x['deadline'], reverse=True) # Sort the tasks reversed -> Latest Deadline First
    
    schedule = []   # Create a new list to store the tasks
    
    node_times = {node['id']: 0 for node in nodes}    # Initialize a dictionary to track the available times for each node
    dependencies = {task['id']: [] for task in tasks}   # Initialize a dictionary to track the dependencies for each task

    for message in application_data['messages']:    # Iterates over each message in "application_data"
        dependencies[message['receiver']].append(message['sender']) # Add the sender of the message as a dependency for the receiver task 

    task_scheduled = {task['id']: False for task in tasks}  # Initialize a dictionary to track whether each task has been scheduled, starting with False

    while not all(task_scheduled.values()): # while-loop until every tasks have been scheduled
        for task in sorted_tasks:   # for-loop iterates over each task in sorted_tasks
            if task_scheduled[task['id']]:  # if the current task is already scheduled, continue with the next task
                continue
            
            if all(task_scheduled[d] for d in dependencies[task['id']]):    # if all dependencies of the task are scheduled:
                node_id, node_time = min(node_times.items(), key=lambda x: x[1])    # Get the node with the earliest available time
                start_time = max(node_time, max([sch['end_time'] for sch in schedule if sch['task_id'] in dependencies[task['id']]], default=0))    # Calculate the start time
                end_time = start_time + task['wcet']    # Calculate the end time of the current task by adding it's worst-case-execution time to current running time
                
                schedule.append({    # Append following elements to the schedule list to represent the scheduled task
                    'task_id': task['id'],
                    'node_id': node_id,
                    'start_time': start_time,
                    'end_time': end_time,
                    'deadline': task['deadline']
                })
                
                node_times[node_id] = end_time  # Set the node's available time to the end time of the current task
                task_scheduled[task['id']] = True   # Show the task as scheduled

    return {"schedule": schedule, "name": "LDF Multi Node"}



def edf_multinode(application_data, platform_data):
    """
    Schedule jobs on a distributed system with multiple compute nodes using the Earliest Deadline First (EDF) strategy.
    This function processes application data to schedule jobs based on the earliest
    deadlines.

    .. todo:: Implement Earliest Deadline First(EDF) algorithm to schedule jobs on multiple nodes in a distributed system.

    Args:
        application_data (dict): Job data including dependencies represented by messages between jobs.
        platform_data (dict): Contains information about the platform, nodes and their types, the links between the nodes and the associated link delay.

    Returns:
        list of dict: Contains the scheduled job details, each entry detailing the node assigned, start and end times,
                      and the job's deadline.

    """
    tasks = application_data['tasks']   # Get the tasks list from "application_data"
    nodes = platform_data['nodes']  # Get the nodes list from "platform_data"
    
    sorted_tasks = sorted(tasks, key=lambda x: x['deadline'])   # Sort the tasks -> Earliest Deadline First
    
    schedule = []   # Create a new list to store the tasks
    
    node_times = {node['id']: 0 for node in nodes}  # Initialize a dictionary to track the available times for each node
    dependencies = {task['id']: [] for task in tasks}   # Initialize a dictionary to track the dependencies for each task

    for message in application_data['messages']:    # Iterates over each message in "application_data"
        dependencies[message['receiver']].append(message['sender']) # Add the sender of the message as a dependency for the receiver task 

    task_scheduled = {task['id']: False for task in tasks}   # Initialize a dictionary to track whether each task has been scheduled, starting with False

    while not all(task_scheduled.values()):  # while-loop until every tasks have been scheduled
        for task in sorted_tasks:   # for-loop iterates over each task in sorted_tasks
            if task_scheduled[task['id']]:  # if the current task is already scheduled, continue with the next task
                continue
            
            if all(task_scheduled[d] for d in dependencies[task['id']]):    # if all dependencies of the task are scheduled:
                node_id, node_time = min(node_times.items(), key=lambda x: x[1])     # Get the node with the earliest available time
                start_time = max(node_time, max([sch['end_time'] for sch in schedule if sch['task_id'] in dependencies[task['id']]], default=0))     # Calculate the start time
                end_time = start_time + task['wcet']    # Calculate the end time of the current task by adding it's worst-case-execution time to current running time
                
                schedule.append({    # Append following elements to the schedule list to represent the scheduled task
                    'task_id': task['id'],
                    'node_id': node_id,
                    'start_time': start_time,
                    'end_time': end_time,
                    'deadline': task['deadline']
                })
                
                node_times[node_id] = end_time   # Set the node's available time to the end time of the current task
                task_scheduled[task['id']] = True   # Show the task as scheduled

    return {"schedule": schedule, "name": "EDF Multi Node"}