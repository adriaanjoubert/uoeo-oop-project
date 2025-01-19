def distance_between(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    # Distance formula per Stewart & Kokoska (2023: 1204)
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
