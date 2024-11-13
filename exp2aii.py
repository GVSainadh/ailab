class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def build_tree():
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
            for c_v in value[1:]:
                if c_v not in nodes:
                    nodes[c_v] = TreeNode(c_v)
                    unique_node_count += 1
                nodes[value[0]].children.append(nodes[c_v])

        if unique_node_count >= num_nodes:
            print("Reached the node limit of", num_nodes)
            break

    return nodes[next(iter(nodes))], nodes

def dfs(root, target_value, path=None, traversal_path=None):
    if path is None:
        path = []
    if traversal_path is None:
        traversal_path = []

    traversal_path.append(root.value)
    path.append(root.value)

    if root.value == target_value:
        return path, traversal_path

    for child in root.children:
        result, traversal_path = dfs(child, target_value, path.copy(), traversal_path)
        if result:
            return result, traversal_path

    return None, traversal_path

def generate_arr(root, nodes, arr=None, index=0):
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
        generate_arr(nodes[arr[index]], nodes, arr, index)

    return arr

def tree_printer(arr, num_lvl):
    current_level = 0
    index = 0

    while current_level <= num_lvl:
        nodes_at_level = 2 ** current_level
        leading_trailing_spaces = 2 ** (num_lvl - current_level) - 1
        spaces_between_nodes = 2 ** (num_lvl - current_level + 1) - 1

        line = ' ' * leading_trailing_spaces

        for _ in range(nodes_at_level):
            if index < len(arr):
                line += arr[index]
                index += 1

                if _ < nodes_at_level - 1:
                    line += ' ' * spaces_between_nodes

        print(line)
        current_level += 1

def find_depth(root):
    if root is None:
        return -1

    if not root.children:
        return 0
    child_depths = [find_depth(child) for child in root.children]

    return 1 + max(child_depths)

def main():
    root, nodes = build_tree()
    if not root:
        return

    arr = generate_arr(root, nodes)
    target_value = input("Enter the value to search for: ")
    path, traversal_path = dfs(root, target_value)
    if path:
        print(f"Traversal path: {' -> '.join(traversal_path)}")
        print(f"Path to node: {' -> '.join(path)}")
        print("Node found")
    else:
        print("Value not found in the tree.")

    tree_depth = find_depth(root)
    tree_printer(arr, tree_depth)

if __name__ == "__main__":
    main()
