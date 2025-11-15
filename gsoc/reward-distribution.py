"""
This script implements our policy for distributing money that we receive from Google
to mentors of Rust Project GSoC projects.
"""
import dataclasses
import math
from collections import defaultdict
from typing import List


@dataclasses.dataclass
class Mentor:
    name: str
    # Does the mentor accept the mentor reward?
    reward: bool

@dataclasses.dataclass
class Project:
    name: str
    mentors: List[Mentor]
    # Is the project eligible to receive money from Google?
    # In other words, did we receive money for this project?
    eligible: bool = True

projects = [Project(
    name="GSoC project 1",
    mentors=[Mentor(name="Mentor 1", reward=True),
             Mentor(name="Mentor 2", reward=False)],
)]

# Modify this if Google changes the reward amount
reward_per_project = 500
eligible_projects = projects

total_reward_received = reward_per_project * len(eligible_projects)

# A project participates in rewards if at least one of its mentors accepts the reward
projects_that_receive_reward = [p for p in projects if any(m.reward for m in p.mentors)]

# Calculate the reward per project, taking only the participating projects into account
reward_per_project = total_reward_received / len(projects_that_receive_reward)

print(f"Total reward received: {total_reward_received}")
print(f"Projects that receive reward: {len(projects_that_receive_reward)}")
print(f"Reward per project: {reward_per_project}")

reward_per_mentor = defaultdict(int)
for project in projects_that_receive_reward:
    # Split the reward within each project by the number of its mentors that want to accept it
    eligible_mentors = [m for m in project.mentors if m.reward]
    for mentor in eligible_mentors:
        reward_per_mentor[mentor.name] += reward_per_project / len(eligible_mentors)
reward_per_mentor = sorted(reward_per_mentor.items(), key=lambda v: (-v[1], v[0]))
reward_per_mentor = [(k, math.floor(v)) for (k, v) in reward_per_mentor]

# Accumulate total rewards per mentor
rewarded = 0
for (mentor, reward) in reward_per_mentor:
    print(f"{mentor}: ${reward}")
    rewarded += reward

# How much money was left over because of rounding
print(f"\n(leftover): ${total_reward_received - rewarded}")
