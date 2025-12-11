"""https://adventofcode.com/2025/day/11"""

from collections import defaultdict, deque

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 11)


example_input1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

example_input2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def parse_network(inputs: str):
    graph = {}
    for line in inputs.splitlines():
        node, edges = line.split(": ")
        graph[node] = edges.split(" ")
    return graph


def topological_sort(graph):
    """Kahn's algorithm: O(V+E)"""
    indegree = dict((node, 0) for node in graph)
    for neighbors in graph.values():
        for neighbor in neighbors:
            indegree[neighbor] = indegree.get(neighbor, 0) + 1

    queue = deque([node for node in indegree if indegree[node] == 0])
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in graph.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return topo_order


def count_paths(graph, source, target):
    """Count all paths from source to target in DAG"""
    topo_order = topological_sort(graph)
    paths_to_target = defaultdict(int)
    paths_to_target[target] = 1

    # Process in reverse topological order (target first)
    for i in range(len(topo_order) - 1, -1, -1):
        node = topo_order[i]
        if node == target:
            continue
        for neighbor in graph.get(node, []):
            paths_to_target[node] += paths_to_target[neighbor]

    return paths_to_target[source]


def dfs(nodes, current, target, path, all_paths):
    """Find all paths from current to target using DFS"""
    if current == target:
        all_paths.append(path.copy())
        return
    for neighbor in nodes.get(current, []):
        path.append(neighbor)
        dfs(nodes, neighbor, target, path, all_paths)
        path.pop()


def solve(inputs_part1: str, inputs_part2: str = ""):

    graph = parse_network(inputs_part1)
    print(f"Part 1: {count_paths(graph, 'you', 'out')}")

    inputs = inputs_part2 or inputs_part1
    graph = parse_network(inputs)

    svr_fft = count_paths(graph, "svr", "fft")
    svr_dac = count_paths(graph, "svr", "dac")
    fft_dac = count_paths(graph, "fft", "dac")
    dac_fft = count_paths(graph, "dac", "fft")
    dac_out = count_paths(graph, "dac", "out")
    fft_out = count_paths(graph, "fft", "out")
    srv_fft_dac_out = svr_fft * fft_dac * dac_out
    srv_dac_fft_out = svr_dac * dac_fft * fft_out
    print(f"Part 2: {srv_fft_dac_out + srv_dac_fft_out}\n")


if __name__ == "__main__":
    solve(example_input1, example_input2)
    solve(actual_input)
