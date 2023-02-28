### Advanced Search Corrector

def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    if m < n:
        return levenshtein_distance(s2, s1)
    if n == 0:
        return m
    previous_row = list(range(n + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def wagner_fischer_distance(s1, s2, max_distance):
    m, n = len(s1), len(s2)
    if abs(m - n) > max_distance:
        return max_distance + 1
    if n == 0:
        return m
    previous_row = list(range(n + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        min_distance = max_distance + 1
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            distance = min(insertions, deletions, substitutions)
            if distance < min_distance:
                min_distance = distance
            current_row.append(distance)
        if min_distance > max_distance:
            return max_distance + 1
        previous_row = current_row
    return previous_row[-1]

def asc(target_word,list,max_dist):
    # Liste de mots avec une distance de Levenshtein de moins de 2 par rapport au mot recherché
    results = []
    for word in list:
        distance = wagner_fischer_distance(target_word, word, max_dist)
        if distance <= max_dist:
            results.append(word)
    return results


class Autocomplete:
    def __init__(self, word_list):
        self.word_list = word_list
        self.graph = self._construct_graph(word_list)
    
    def _construct_graph(self, word_list):
        graph = {}
        for word in word_list:
            for i in range(len(word)):
                prefix = word[:i+1]
                if prefix not in graph:
                    graph[prefix] = set()
                graph[prefix].add(word)
        return graph
    
    def autocomplete(self, prefix):
        if prefix not in self.graph:
            return []
        return list(self.graph[prefix])
    
def reconstruct(el):
    res = el['book_reference']
    res['occurrence'] = el['occurrence']
    return res