from collections import deque

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def construct_tree():
    nodes = {}
    unique_node_count = 0
    
    while True:
        try:
            num_nodes = int(input("Enter the number of nodes (<= 50, positive integer only): "))
            if num_nodes > 50 or num_nodes <= 0:
                print("Please enter a number between 1 and 50.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
    
    print("Enter the node value and the child nodes, if no children then enter ' - ' : ")

    while unique_node_count < num_nodes:
        value = input().strip()
        value = value.split()

        if value[0] not in nodes:
            nodes[value[0]] = TreeNode(value[0])
            unique_node_count += 1

        if value[1] != '-':
            for child_value in value[1:]:
                if child_value not in nodes:
                    nodes[child_value] = TreeNode(child_value)
                    unique_node_count += 1
                nodes[value[0]].children.append(nodes[child_value])

        if unique_node_count >= num_nodes:
            print("Reached the node limit of", num_nodes)
            break

    return nodes[next(iter(nodes))], nodes

def breadth_first_search(root, target_value):
    queue = deque([(root, [root.value])])

    while queue:
        current_node, path = queue.popleft()

        if current_node.value == target_value:
            return path

        for child in current_node.children:
            queue.append((child, path + [child.value]))

    return None

def generate_tree_array_representation(root, nodes, arr=None, index=0):
    if arr is None:
        arr = []

    if index >= len(arr):
        arr.append(root.value)

    if not root.children:
        arr.extend(['-'] * 2)
    else:
        child_values = [child.value for child in root.children]
        arr.extend(child_values)
        if len(child_values) < 2:
            arr.append('-')

    index += 1

    if index < len(arr) and arr[index] in nodes:
        generate_tree_array_representation(nodes[arr[index]], nodes, arr, index)

    return arr

def print_tree_structure(arr, max_depth):
    current_level = 0
    index = 0

    while current_level <= max_depth:
        nodes_at_level = 2 ** current_level
        leading_trailing_spaces = 2 ** (max_depth - current_level) - 1
        spaces_between_nodes = 2 ** (max_depth - current_level + 1) - 1

        line = ' ' * leading_trailing_spaces

        for _ in range(nodes_at_level):
            if index < len(arr):
                line += arr[index]
                index += 1

                if _ < nodes_at_level - 1:
                    line += ' ' * spaces_between_nodes

        print(line)
        current_level += 1

def calculate_tree_depth(root):
    if root is None:
        return -1

    if not root.children:
        return 0
    child_depths = [calculate_tree_depth(child) for child in root.children]

    return 1 + max(child_depths)

def main():
    root, nodes = construct_tree()
    if not root:
        return

    tree_array = generate_tree_array_representation(root, nodes)
    target_value = input("Enter the value to search for: ")
    path = breadth_first_search(root, target_value)

    if path:
        print(f"Path = {' -> '.join(path)}")
        print("Node found")
    else:
        print("Value not found in the tree.")

    tree_depth = calculate_tree_depth(root)
    print_tree_structure(tree_array, tree_depth)

if __name__ == "__main__":
    main()
