import math

# start = 'A'
# end = 'G'
def dik_algo(graph, start, end):

    # A, B, C, D, E, F, G
    nodes = list(graph.keys())

    f = float('inf')
    # Set all to Inf
    dist_from_start = {n: f for n in nodes}
    # {'A' : inf, 'B': inf, 'G': inf}

    # {'A' : 0, 'B' : inf, 'G': inf}
    dist_from_start[start] = 0

    # predecessors => optimal path to n
    pres = {n: None for n in nodes}

    while len(nodes) > 0:
        candidates = {n: dist_from_start[n] for n in nodes}
        closet = None
        minn = float('inf')
        for i in candidates:
            if candidates[i] < minn:
                closet = i
                minn = candidates[i]

        if closet:
            for n in graph[closet]:
                dist_to_n = graph[closet][n]
                d = dist_from_start[closet] + dist_to_n
                if dist_from_start[n] > d:
                    dist_from_start[n] = d
                    pres[n] = closet

        nodes.remove(closet)

    if pres[end] is None and start != end:
        return []

    path = [end]
    current = end
    while current != start:
        path.append(pres[current])
        current = pres[current]

    path.reverse()
    return path, dist_from_start[end]


class IPDatagram:
    def __init__(self, totalLength, headerLength, offset, fragmentBits):
        self.totalLength = totalLength
        self.headerLength = headerLength
        self.fragmentBits = fragmentBits  # MF, DF
        self.offset = offset
        self.dataLength = self.totalLength - self.headerLength

    def __str__(self) -> str:
        return f"({self.totalLength=}, {self.headerLength=}, {self.fragmentBits=}, {self.offset=}, {self.dataLength=})"


def fragmentFuther(fragments, MTU):
    newFragments = []
    for frag in fragments:
        # IP Datagram can be fragmented
        if frag.fragmentBits[1] == 0:
            if frag.totalLength > MTU:

                totalDataLength = (MTU - frag.headerLength)
                # no_of_fragments = math.ceil(frag.dataLength / totalDataLength)

                availableData = frag.dataLength
                cummulativeData = frag.offset * 8
                while availableData > 0:
                    if availableData > totalDataLength:
                        newFragments.append(
                            IPDatagram(totalDataLength + frag.headerLength, frag.headerLength,
                                       ((cummulativeData - (cummulativeData % 8)) // 8), [1, 0])
                        )
                        cummulativeData += totalDataLength
                        availableData -= totalDataLength
                    else:
                        if frag.fragmentBits[0] == 1:
                            newFragments.append(
                                IPDatagram(availableData + frag.headerLength, frag.headerLength,
                                           ((cummulativeData - (cummulativeData % 8)) // 8), [1, 0])
                            )
                            cummulativeData += availableData
                            availableData -= availableData
                        else:
                            newFragments.append(
                                IPDatagram(availableData + frag.headerLength, frag.headerLength,
                                           ((cummulativeData - (cummulativeData % 8)) // 8), [0, 0])
                            )
                            cummulativeData += availableData
                            availableData -= availableData

            else:
                newFragments.append(frag)
        else:
            if frag.totalLength < MTU:
                newFragments.append(frag)

    return newFragments


# Find the shortest path


graph = {
    'A': {'B': 5, 'C': 6},
    'B': {'A': 5, 'E': 8, 'D': 7, 'C': 15},
    'C': {'B': 15, 'A' : 6, 'D' : 2, 'F' : 4},
    'D': {'B': 7, 'C' : 2, 'F' : 9, 'G' : 10, 'E' : 2},
    'E': {'B' : 8, 'D' : 2, 'G' : 3},
    'F': {'C' : 4, 'D' : 9, 'G' : 8},
    'G' : {'E' : 3, 'D' : 10, 'F' : 8}
}

MTU = {
    'B': 620,
    'C': 620,
    'D' :500,
    'E' : 620,
    'F' : 500,
}

InitialDatagram = IPDatagram(5000, 20, 0, [0, 0])
fragments = [InitialDatagram]

start = 'A'
end = 'G'
shortestPath = dik_algo(graph, start, end)
print(shortestPath)

print(f"Node: {start}")
for frag in fragments:
    print(frag)
print()

for node in shortestPath[1:]:
    if node == end:
        break

    print(f"Node : {node} | MTU : {MTU[node]}")
    fragments = fragmentFuther(fragments, MTU[node])
    for frag in fragments:
        print(frag)
    print()

print(f"Node: {end}")
for frag in fragments:
    print(frag)
print()
