import random

# Define hours for the cron jobs
cron_expressions = []

# Generate cron expressions with random minutes for each hour
for hour in range(0,24):
    for minute in range (0,59):
        rand_num = random.random()
        if rand_num < 0.003:
            cron_expressions.append(f'    - cron: \'{minute} {hour} * * *\'')

# Print the cron expressions in YAML format
for cron in cron_expressions:
    print(cron)
