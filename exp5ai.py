from collections import deque

def is_valid(state, M_total, C_total):
    M_left, C_left, _, M_right, C_right = state
    if M_left >= 0 and C_left >= 0 and M_right >= 0 and C_right >= 0:
        if (M_left == 0 or M_left >= C_left) and (M_right == 0 or M_right >= C_right):
            return True
    return False

def get_successors(state, boat_capacity, M_total, C_total):
    M_left, C_left, boat, M_right, C_right = state
    successors = []
    if boat == 1:  # Boat on left side
        for m in range(0, boat_capacity + 1):
            for c in range(0, boat_capacity + 1 - m):
                if m + c > 0 and m + c <= boat_capacity:
                    new_state = (M_left - m, C_left - c, 0, M_right + m, C_right + c)
                    if is_valid(new_state, M_total, C_total):
                        successors.append(new_state)
    else:  # Boat on right side
        for m in range(0, boat_capacity + 1):
            for c in range(0, boat_capacity + 1 - m):
                if m + c > 0 and m + c <= boat_capacity:
                    new_state = (M_left + m, C_left + c, 1, M_right - m, C_right - c)
                    if is_valid(new_state, M_total, C_total):
                        successors.append(new_state)
    return successors

def bfs(initial_state, boat_capacity, M_total, C_total):
    """Perform BFS to find the solution."""
    queue = deque([(initial_state, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        if state == (0, 0, 0, M_total, C_total):  # Goal state
            return path + [state]
        for successor in get_successors(state, boat_capacity, M_total, C_total):
            queue.append((successor, path + [state]))
    return None

def get_positive_integer(prompt):
    while True:
        user_input = input(prompt)
        if user_input.lower() == "exit":
            print("Exiting the program.")
            exit()
        try:
            value = int(user_input)
            if value > 0:
                return value
            elif value == 0:
                print("Enter a value greater than 0")
            elif value < 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def missionaries_and_cannibals():
    M_total = get_positive_integer("Enter the number of missionaries: ")
    C_total = get_positive_integer("Enter the number of cannibals: ")
    
    while True:
        boat_capacity = get_positive_integer("Enter the boat capacity: ")
        if boat_capacity <= M_total and boat_capacity <= C_total:
            break
        else:
            print(f"Boat capacity must be less than or equal to both the number of missionaries ({M_total}) and the number of cannibals ({C_total}). Please enter a valid boat capacity.")
    
    initial_state = (M_total, C_total, 1, 0, 0)  # (M_left, C_left, boat_position, M_right, C_right)
    solution = bfs(initial_state, boat_capacity, M_total, C_total)

    if solution:
        print("\nPath from initial state to solution state:\n")
        for i in range(len(solution)):
            step = solution[i]
            if i == 0:
                print(f"Initial State: ({step[0]}M, {step[1]}C, 1B) | (0M, 0C, 0B)")
            else:
                prev_step = solution[i - 1]
                
                missionaries_moved = abs(step[0] - prev_step[0])
                cannibals_moved = abs(step[1] - prev_step[1])
                
                direction = "->" if step[2] == 0 else "<-"
                action_details = []

                if missionaries_moved > 0:
                    action_details.append(f"{missionaries_moved} missionar{'ies' if missionaries_moved > 1 else 'y'}")
                if cannibals_moved > 0: 
                    action_details.append(f"{cannibals_moved} cannibal{'s' if cannibals_moved > 1 else ''}")
                
                action = " and ".join(action_details) + f" from {'Left' if direction == '->' else 'Right'} to {'Right' if direction == '->' else 'Left'}"
                boat_position = 1 - step[2]
                print(f"step {i}:  {action}")
                print(f"({step[0]}M, {step[1]}C, {step[2]}B) {direction} ({step[3]}M, {step[4]}C ,{boat_position}B)")
                print()
        print("Goal state Reached..")
    else:
        print("No solution found.")

missionaries_and_cannibals()