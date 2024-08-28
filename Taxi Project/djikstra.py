import heapq

def dijkstra_shortest_path(graph, start, target):
    # Initialize distances with infinity and set the distance to the start node to 0
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Priority queue to hold (distance, node) tuples
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we reached the target node, return the distance
        if current_node == target:
            return distances[target]

        # If the current distance is greater than the known shortest distance, skip it
        if current_distance > distances[current_node]:
            continue

        # Check the neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # If a shorter path is found, update the distance and add to the priority queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    # If the target is unreachable, return None
    if distances[target] == float('inf'):
        return None
