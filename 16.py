# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Parse input

# %%
inp = []
with open("input.txt", 'r') as f:
    inp = f.read().split("\n")[:-1]

# %%
example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

# %%
inp = [l.split(" ") for l in inp]

# %%
inp = [{
    "valve": l[1],
    "flow_rate": int(l[4].split('=')[1][:-1]),
    "neighbours": [v[:2] for v in l[9:]]
} for l in inp]

# %%
valves = {}
for i in inp:
    valves[i['valve']] = i

# %% [markdown]
# ## Graph search

# %%
initial = valves["AA"]

# %% [markdown]
#  Initial state = (score so far, time left, valves on)
#  - If no possible moves then return score so far
#  - Look at all possible moves, (turn on valve, move to neighbour)
#  - return all max of scores from each move

# %%
global_max = 914

# %%
scoring_valves = [v["valve"] for v in inp if v["flow_rate"] > 0]
def should_stop_early(node, current_score, time_left, valves_on):
    if len(valves_on) >= len(scoring_valves):
        return True
    remaining_valve_score = time_left * sum([valves[v]["flow_rate"] for v in scoring_valves if v not in valves_on])
    if current_score+remaining_valve_score < global_max:
        return True
    return False


# %%
def get_highest_score_from_node(node, current_score, time_left, valves_on):
    global global_max
    if time_left == 0:
        if current_score > global_max:
            print("Found new max ", current_score)
            global_max = current_score
        return current_score
    
    if should_stop_early(node, current_score, time_left, valves_on):
        return current_score

    possible_moves = []
    if node not in valves_on and valves[node]["flow_rate"] > 0:
        return get_highest_score_from_node(node, current_score+((time_left-1)*valves[node]["flow_rate"]), time_left-1, valves_on+[node])
    for adj in sorted(valves[node]["neighbours"], key=lambda x: valves[x]["flow_rate"] if x not in valves_on else 0, reverse=True):
        possible_moves = possible_moves + [get_highest_score_from_node(adj, current_score, time_left-1, valves_on)]
    return max(possible_moves)


# %%
get_highest_score_from_node("AA", 0, 30, [])

# %%
