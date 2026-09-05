# 커밋 그래프 탐색, PATH, ANCESTORS, LOG

from sort import Sort

class Graph:
    def __init__(self, repository):
        self.repository = repository
        self.sorter = Sort()

# ------------------------
# ANCESTORS
# ------------------------

    def ancestors(self, commit_hash):
        commit = self.repository.get_commit(commit_hash)
        result = []
        visited = set()

        visited.add(commit_hash)
        self._dfs(commit, result, visited)
        return result

    def _dfs(self, commit, result, visited):
        for parent_hash in commit.parents:
            if parent_hash in visited:
                continue

            visited.add(parent_hash)
            parent = self.repository.get_commit(parent_hash)
            result.append(parent) # 해시 문자열만 필요하다면 parent.hash로 변경
            self._dfs(parent, result, visited)

# ------------------------
# PATH
# ------------------------

    def path(self, start_hash, target_hash):
        self.repository.get_commit(start_hash)
        self.repository.get_commit(target_hash)

        if start_hash == target_hash:
            return [start_hash]

        queue = [[start_hash]]
        visited = {start_hash}

        while queue:
            current_path = queue.pop(0)
            current_hash = current_path[-1]

            for neighbor_hash in self._get_neighbors(current_hash):
                if neighbor_hash in visited:
                    continue

                new_path = current_path + [neighbor_hash]
                if neighbor_hash == target_hash:
                    return new_path

                visited.add(neighbor_hash)
                queue.append(new_path)

        return None

    def _get_neighbors(self, commit_hash):
        raw_neighbors = []
        commit = self.repository.get_commit(commit_hash)

        # 부모 노드 수집 (중복 제외)
        for parent_hash in commit.parents:
            if parent_hash not in raw_neighbors:
                raw_neighbors.append(parent_hash)

        # 자식 노드 수집 (중복 제외)
        for other_hash, other_commit in self.repository.commits.items():
            if commit_hash in other_commit.parents:
                if other_hash not in raw_neighbors:
                    raw_neighbors.append(other_hash)

        neighbors = self.sorter.insertion_sort(raw_neighbors, key=lambda x: x)
        return neighbors

# ------------------------
# LOG
# ------------------------

    def log(self):
        commits = list(self.repository.commits.values())
        child_count = {}

        # 남은 자식 수 카운트
        for commit in commits:
            child_count[commit.hash] = 0
        for commit in commits:
            for parent_hash in commit.parents:
                child_count[parent_hash] += 1

        # 자식이 없는 최신 커밋부터 큐에 진입
        queue = []
        for commit in commits:
            if child_count[commit.hash] == 0:
                queue.append(commit.hash)

        result = []

        while queue:
            current_hash = queue.pop(0)
            current_commit = self.repository.get_commit(current_hash)
            result.append(current_commit)

            # 현재 커밋의 부모 처리
            for parent_hash in current_commit.parents:
                child_count[parent_hash] -= 1

                if child_count[parent_hash] == 0 and parent_hash not in queue:
                    queue.append(parent_hash)

        return result