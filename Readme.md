# Weather Man

Weather Man is a Python application that generates reports from weather data files. It allows users to analyze weather statistics and visualize daily temperature trends using command-line arguments.

## Features

- Analyze yearly data: Analyzes files for specific year and tells the highest temperature and day, lowest temperature and day, most humid day and humidity.
- Analyze monthly data: Compute highest and lowest temperatures, mean humidity, and generates temperature bar charts for specific month.
- No external packages are used, adhering strictly to Python's standard library.
- Supports command-line arguments for specifying directories and optional flags for different types of analysis.

## Setup

1. Ensure you have Python 3.8.10 installed on your system.

2. Clone or download the repository from [git@github.com:ZAINABFATIMA0/Training_Ground.git](git@github.com:ZAINABFATIMA0/Training_Ground.git).


## Usage

Run the program using the command line with the following options:

### 1. **Yearly Report**:
`python weatherman.py /path/to/files-dir -e <year>`
#### Displays:
- Highest temperature and its date.
- Lowest temperature and its date.
- Most humid day and its humidity.

### 2. **Monthly Report**:
`python weatherman.py /path/to/files-dir -a <year>/<month>`
#### Displays:
- Average highest temperature for the specified month.
- Average lowest temperature for the specified month.
- Average mean humidity for the specified month.

### 3. **Monthly Bar Charts**:`
`python weatherman.py /path/to/files-dir -c <year>/<month>`
#### Displays:
- Highest temperature in red (`+` symbols).
- Lowest temperature in blue (`+` symbols).

### 4. **Multiple Reports**:
`python weatherman.py /path/to/files-dir -c <year>/<month> -a <year>/<month> -e <year>`
- Generates multiple reports based on the specified criteria.


