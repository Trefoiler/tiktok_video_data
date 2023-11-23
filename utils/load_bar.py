def load_bar(current: int, total: int, bar_length: int = 50) -> str:
    percent = current / total
    num_filled = int(percent * bar_length)
    num_empty = bar_length - num_filled
    return f"[{'#' * num_filled}{' ' * num_empty}] {int(percent * 100)}% ({current}/{total})"