from collections import deque

def is_goal_state(state, target):
    return state[0] == target or state[1] == target

def get_production_rules(a, b):
    return [
        {"action": "Fill Jug1", "rule": lambda u: (a, u[1])},    # Rule 1: Fill jug1
        {"action": "Empty Jug1", "rule": lambda u: (0, u[1])},   # Rule 2: Empty jug1
        {"action": "Fill Jug2", "rule": lambda u: (u[0], b)},    # Rule 3: Fill jug2
        {"action": "Empty Jug2", "rule": lambda u: (u[0], 0)},   # Rule 4: Empty jug2
        {"action": "Empty Jug1 into Jug2",  # Rule 5: Empty jug1 into jug2
         "rule": lambda u: (0, u[0] + u[1]) if u[0] + u[1] <= b else (u[0] - (b - u[1]), b)},
        {"action": "Empty Jug2 into Jug1",  # Rule 6: Empty jug2 into jug1
         "rule": lambda u: (u[0] + u[1], 0) if u[0] + u[1] <= a else (a, u[1] - (a - u[0]))},
        {"action": "Pour water from Jug1 into Jug2 until Jug2 is full",  # Rule 7: Jug2 reaches max capacity
         "rule": lambda u: (u[0] - (b - u[1]), b) if u[0] > 0 and u[1] < b else (u[0], u[1])},  # Jug1 might have excess water
        {"action": "Pour water from Jug2 into Jug1 until Jug1 is full",  # Rule 8: Jug1 reaches max capacity
         "rule": lambda u: (a, u[1] - (a - u[0])) if u[1] > 0 and u[0] < a else (u[0], u[1])}   # Jug2 might have excess water
    ]

def solve_with_production_rules(a, b, target):
    visited_states = {}
    parent_map = {}
    action_map = {}
    path = []
    q = deque([(0, 0)])

    is_solvable = False
    final_state = None

    rules = get_production_rules(a, b)

    while q:
        current_state = q.popleft()

        if current_state in visited_states:
            continue

        visited_states[current_state] = True

        if is_goal_state(current_state, target):
            is_solvable = True
            final_state = current_state
            break

        for rule in rules:
            next_state = rule["rule"](current_state)

            # Ensure the next state is valid (no negative values)
            if next_state[0] < 0 or next_state[1] < 0 or next_state[0] > a or next_state[1] > b:
                continue

            if next_state not in visited_states:
                q.append(next_state)
                parent_map[next_state] = current_state
                action_map[next_state] = rule["action"]

    if is_solvable:
        steps = []
        actions = []
        while final_state != (0, 0):
            steps.append(final_state)
            actions.append(action_map[final_state])
            final_state = parent_map[final_state]

        steps.append((0, 0))
        steps.reverse()
        actions.reverse()

        print("Path from initial state to solution state:")
        print("Step 1:\nInitial state - (0, 0)")

        step_num = 2
        for i in range(1, len(steps)):
            state = steps[i]
            print(f"\nStep {step_num}:")
            print(f"{actions[i-1]} - {state}")
            step_num += 1

        print("\nThe final target reached....")
    else:
        print("Solution not possible")

if __name__ == '__main__':
    while True:
        try:
            Jug1 = int(input("Enter capacity of first jug: "))
            if Jug1 <= 0:
                print("Capacities must be positive integers. Please re-enter.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
    
    while True:        
        try:    
            Jug2 = int(input("Enter capacity of second jug: "))
            if Jug2 <= 0:
                print("Capacities must be positive integers. Please re-enter.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
    
    while True:
        try:    
            target = int(input("Enter your target: "))
            if target <= 0:
                print("Target must be a positive integer. Please re-enter.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
            
    solve_with_production_rules(Jug1, Jug2, target)
