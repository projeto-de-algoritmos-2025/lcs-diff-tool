import itertools

from dataclasses import dataclass
from enum import Enum


class Operation(Enum):
    KEEP = "keep"
    DELETE = "delete"
    INSERT = "insert"


@dataclass
class DiffOperation:
    operation: Operation
    line_number_1: int | None
    line_number_2: int | None
    content: str

    def __str__(self):
        op_symbols = {Operation.KEEP: " ", Operation.DELETE: "-", Operation.INSERT: "+"}
        symbol = op_symbols[self.operation]
        return f"{symbol} {self.content}"


class LCSAlgorithm:
    def __init__(self, enable_memoization=True):
        self.enable_memoization = enable_memoization
        self._memo_cache = {}

    def compute_lcs_length_optimized(self, seq1, seq2):
        if len(seq1) < len(seq2):
            seq1, seq2 = seq2, seq1

        m, n = len(seq1), len(seq2)
        prev = [0] * (n + 1)
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i - 1] == seq2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            prev, curr = curr, [0] * (n + 1)

        return prev[n]

    def compute_lcs_matrix(self, seq1, seq2) -> list[list[int]]:
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i, j in itertools.product(range(1, m + 1), range(1, n + 1)):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp

    def compute_lcs_recursive(self, seq1, seq2, i=None, j=None):
        if i is None:
            i = len(seq1)
        if j is None:
            j = len(seq2)

        if i == 0 or j == 0:
            return 0

        if self.enable_memoization and (i, j) in self._memo_cache:
            return self._memo_cache[(i, j)]

        if seq1[i - 1] == seq2[j - 1]:
            result = 1 + self.compute_lcs_recursive(seq1, seq2, i - 1, j - 1)
        else:
            option1 = self.compute_lcs_recursive(seq1, seq2, i - 1, j)
            option2 = self.compute_lcs_recursive(seq1, seq2, i, j - 1)
            result = max(option1, option2)

        if self.enable_memoization:
            self._memo_cache[(i, j)] = result

        return result

    def reconstruct_lcs(self, seq1, seq2, dp_matrix=None):
        if dp_matrix is None:
            dp_matrix = self.compute_lcs_matrix(seq1, seq2)

        lcs = []
        i, j = len(seq1), len(seq2)

        while i > 0 and j > 0:
            if seq1[i - 1] == seq2[j - 1]:
                lcs.append(seq1[i - 1])
                i -= 1
                j -= 1
            elif dp_matrix[i - 1][j] > dp_matrix[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return lcs[::-1]

    def compute_diff_operations(self, seq1, seq2):
        dp_matrix = self.compute_lcs_matrix(seq1, seq2)
        operations = []

        i, j = len(seq1), len(seq2)
        line_num_1, line_num_2 = len(seq1), len(seq2)

        while i > 0 or j > 0:
            if i > 0 and j > 0 and seq1[i - 1] == seq2[j - 1]:
                operations.append(
                    DiffOperation(
                        operation=Operation.KEEP,
                        line_number_1=line_num_1,
                        line_number_2=line_num_2,
                        content=seq1[i - 1],
                    )
                )
                i -= 1
                j -= 1
                line_num_1 -= 1
                line_num_2 -= 1

            elif j > 0 and (i == 0 or dp_matrix[i][j - 1] >= dp_matrix[i - 1][j]):
                operations.append(
                    DiffOperation(
                        operation=Operation.INSERT, line_number_1=None, line_number_2=line_num_2, content=seq2[j - 1]
                    )
                )
                j -= 1
                line_num_2 -= 1

            else:
                operations.append(
                    DiffOperation(
                        operation=Operation.DELETE, line_number_1=line_num_1, line_number_2=None, content=seq1[i - 1]
                    )
                )
                i -= 1
                line_num_1 -= 1

        return operations[::-1]

    def get_statistics(self, operations):
        stats = {"total_lines": len(operations), "lines_kept": 0, "lines_inserted": 0, "lines_deleted": 0}

        for op in operations:
            if op.operation == Operation.KEEP:
                stats["lines_kept"] += 1
            elif op.operation == Operation.INSERT:
                stats["lines_inserted"] += 1
            elif op.operation == Operation.DELETE:
                stats["lines_deleted"] += 1

        return stats

    def get_similarity_percentage(self, seq1, seq2):
        if not seq1 and not seq2:
            return 100.0

        lcs_length = self.compute_lcs_length_optimized(seq1, seq2)
        max_length = max(len(seq1), len(seq2))

        return (lcs_length / max_length) * 100.0 if max_length > 0 else 0.0

    def clear_cache(self) -> None:
        self._memo_cache.clear()

    def get_performance_info(self, seq1, seq2):
        m, n = len(seq1), len(seq2)

        return {
            "time_complexity": f"O({m} × {n})",
            "space_complexity": f"O({m} × {n})",
            "matrix_size": m * n,
            "memoization_enabled": self.enable_memoization,
            "cache_size": len(self._memo_cache) if self.enable_memoization else 0,
        }


def quick_diff(lines1, lines2, enable_memoization):
    lcs = LCSAlgorithm(enable_memoization=enable_memoization)
    return lcs.compute_diff_operations(lines1, lines2)


def compare_files(file1_path, file2_path, ignore_whitespace=False):
    try:
        with open(file1_path, encoding="utf-8") as f1:
            lines1 = f1.read().splitlines()

        with open(file2_path, encoding="utf-8") as f2:
            lines2 = f2.read().splitlines()

        if ignore_whitespace:
            lines1 = [line.strip() for line in lines1]
            lines2 = [line.strip() for line in lines2]

        lcs = LCSAlgorithm()
        operations = lcs.compute_diff_operations(lines1, lines2)
        stats = lcs.get_statistics(operations)

        return operations, stats

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Arquivo não encontrado: {e}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Erro de codificação: {e}")
