import random, datetime, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

current_day = datetime.datetime.now().weekday()
cron_expressions = []

def generate_minutes(count):
    valid_numbers = list(range(60))
    selected_numbers = []

    while len(selected_numbers) < count:
        num = random.choice(valid_numbers)  # Randomly select a number
        selected_numbers.append(num)

        # Remove the selected number and numbers within a difference of 5
        valid_numbers = [x for x in valid_numbers if abs(x - num) > 5]

    return sorted(selected_numbers)  # Sort for readability, optional

def helper(hour, num_posts_arr, weights):
    # Choose a number based on the defined weights
    count = random.choices(num_posts_arr, weights, k=1)[0]

    minutes = generate_minutes(count)

    for minute in minutes:
        cron_expressions.append(f'    - cron: \'{minute} {hour} * * *\'')

if current_day in [4,5,6]:
    logging.info("It is a weekend.")
    skip_day = 0.01
    if random.random() < skip_day:
        logging.info("SKIPPED POSTING TODAY")
    else:
        num_posts_arr = [1, 2, 3]
        weights = [0.3, 0.5, 0.2]
        afternoon_percent = 0.62
        if random.random() < afternoon_percent:
            # psot in afternoon tinmes
            hour = random.randint(0,4)
        else:
            # post in lunch times
            hour = random.randint(18,20)
        helper(hour, num_posts_arr, weights)
else:
    # Weekday
    logging.info("It is a weekday.")
    skip_day = 0.03
    if random.random() < skip_day:
        logging.info("SKIPPED POSTING TODAY")
    else:
        num_posts_arr = [1, 2, 3]
        weights = [0.6, 0.2, 0.1]
        afternoon_percent = 0.83
        if random.random() < afternoon_percent:
            # psot in afternoon tinmes
            hour = random.randint(0,4)
        else:
            # post in lunch times
            hour = random.randint(18,20)
        helper(hour, num_posts_arr, weights)

# Print the cron expressions in YAML format
for cron in cron_expressions:
    print(cron)
