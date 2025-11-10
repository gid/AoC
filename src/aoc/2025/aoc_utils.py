import functools
import os
import requests
import time


def download_input_data(year: int, day: int) -> str:
    session_cookie = os.environ.get("AOC_SESSION_COOKIE")
    if not session_cookie:
        raise ValueError("AOC_SESSION_COOKIE environment variable not set")
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": session_cookie})
    response.raise_for_status()
    return response.text.strip("\n")


def get_input_data(year: int, day: int) -> str:
    """Get inout data for the specified year/day (saving locally if not yet downloaded)"""
    root_dir = os.path.dirname(__file__)
    filename = f"{root_dir}/inputs/day{str(day).zfill(2)}_input.txt"
    try:
        with open(filename) as file:
            input_data = file.read()
    except FileNotFoundError:
        input_data = download_input_data(year, day)
        with open(filename, "w") as file:
            file.write(input_data)
    return input_data


def download_archive_inputs(start_year: int = 2015, end_year: int = 2023):
    """Download input data for for the specified years and store in the inputs folder"""
    for year in range(start_year, end_year):
        directory = f"{year}/inputs"
        if not os.path.exists(directory):
            os.makedirs(directory)
        for day in range(1, 26):
            get_input_data(year, day)


def generate_stub_files(year: int, number_of_days: int = 25):
    """Generate stub files for the specified year"""
    year_directory = os.path.dirname(__file__)
    inputs_directory = os.path.join(year_directory, "inputs")
    if not os.path.exists(inputs_directory):
        os.makedirs(inputs_directory)
    with open(os.path.join(year_directory, "__init__.py"), "w") as f:
        pass
    for day in range(1, number_of_days + 1):
        with open(os.path.join(year_directory, f"day{day:02d}.py"), "w") as f:
            f.write(f'"""https://adventofcode.com/{year}/day/{day}"""\n\n')
            f.write("from aoc_utils import get_input_data\n\n")
            f.write(f"actual_input = get_input_data({year}, {day})\n\n\n")
            f.write('example_input = """xxx"""\n\n\n')
            f.write("def solve(inputs: str):\n")
            f.write("    values = tuple(map(int, inputs.splitlines()))\n\n")
            f.write('    print(f"Part 1: {False}")\n')
            f.write('    print(f"Part 2: {False}\\n")\n\n\n')
            f.write("solve(example_input)\n")
            f.write("# solve(actual_input)\n")


def print_time_taken(func):
    @functools.wraps(func)
    def _wrapped_func(*args, **kwargs):
        start_time = time.time()
        retval = func(*args, **kwargs)
        time_taken = time.time() - start_time
        if time_taken > 1.0:
            time_str = f"{time_taken:.2f}s"
        elif time_taken > 0.001:
            time_str = f"{time_taken*1_000:.2f}ms"
        elif time_taken > 0.000_001:
            time_str = f"{time_taken*1_000_000:.2f}µs"
        else:
            time_str = f"{time_taken*1_000_000_000:.2f}ns"
        print(f"Time taken: {time_str}\n")
        return retval

    return _wrapped_func


if __name__ == "__main__":
    generate_stub_files(2025, 12)
