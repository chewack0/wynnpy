def dl_distance(a: str, b: str,
                insertion_weight: int = 1,
                deletion_weight: int = 1,
                substitution_weight: int = 1,
                transposition_weight: int = 1) -> int:


    arr = [[0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        arr[i][0] = i
    for j in range(len(b) + 1):
        arr[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            substitution_cost = 0 if a[i - 1] == b[j - 1] else substitution_weight
            arr[i][j] = min(
                arr[i - 1][j] + deletion_weight, 
                arr[i][j - 1] + insertion_weight,  
                arr[i - 1][j - 1] + substitution_cost  
            )
        if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
            arr[i][j] = min(arr[i][j], arr[i - 2][j - 2] + transposition_weight)
            
    return arr[-1][-1]

def fuzzy_match(a: str, b: str) -> int:
    dl = dl_distance(a, b)
    return dl