import random

# Define hours for the cron jobs
hours = list(range(12, 24)) + list(range(0, 7))
cron_expressions = []

# Generate cron expressions with random minutes for each hour
for hour in hours:
    minute = random.randint(0, 59)
    cron_expressions.append(f'    - cron: \'{minute} {hour} * * *\'')

# Print the cron expressions in YAML format
for cron in cron_expressions:
    print(cron)
