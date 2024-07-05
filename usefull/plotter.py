import shutil
import sys

def number_line(n: int, a: int, b: int) -> None:
    # Get the width of the terminal window
    width, _ = shutil.get_terminal_size()
    
    # Leave some space for the border and labels
    bar_width = width - 10

    # Scale the positions to fit the bar width
    scale = bar_width / n
    scaled_a = int(a * scale)
    scaled_b = int(b * scale)
    
    # Create the progress bar
    progress = [" "] * bar_width
    for i in range(scaled_a, scaled_b + 1):
        progress[i] = '\033[94m' + '=' + '\033[0m'

    progress_line = "|" + "".join(progress) + "|"
    sys.stdout.write(f"{progress_line}\r")
    sys.stdout.flush()