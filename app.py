import csv
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load restaurant data from CSV file into a dictionary
restaurant_data = {}


def create_tuples(day_hours, array):
    parts = day_hours.split(' ')
    days = parts[0] if ',' not in parts[0] else parts[0] + parts[1]
    hours = ' '.join(parts[1:]) if ',' not in parts[0] else ' '.join(parts[2:])
    hour_array = hours.split(' - ')
    start_hour = hour_array[0]
    end_hour = hour_array[1]
    time_frames = {}

    if ',' in days:
        # handles (Mon-Thu, Sun) or (Mon, Thu-Fri) type scenario
        day_array = days.split(',')
        for day in day_array:
            if '-' not in day:
                time_frames[day] = (start_hour, end_hour)
            else:
                start_day, end_day = day.split('-')
                handle_day_list(end_day, end_hour, start_day, start_hour, time_frames)
    elif '-' not in days:
        # single day timeframe scenario
        time_frames[days] = (start_hour, end_hour)
    else:
        # handles Mon-Fri type scenario
        start_day, end_day = days.split('-')
        handle_day_list(end_day, end_hour, start_day, start_hour, time_frames)

    array.append(time_frames)


def handle_day_list(end_day, end_hour, start_day, start_hour, time_frames):
    days_of_week = ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    start_day_index = days_of_week.index(start_day)
    end_day_index = days_of_week.index(end_day)
    days_list = days_of_week[start_day_index:end_day_index + 1]
    for day in days_list:
        time_frames[day] = (start_hour, end_hour)


with open('public-data/restaurants.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        name = row[0]
        time = row[1].split('/')
        multi_hours = []
        if len(time) == 2:
            for hour_range in time:
                create_tuples(hour_range.strip(), multi_hours)

        else:
            create_tuples(time[0], multi_hours)

        restaurant_data[name] = multi_hours
    for name, val in restaurant_data.items():
        print(name, val)


# API endpoint
def is_open(restHours, target_datetime):
    return True


@app.route('/restaurants', methods=['GET'])
def get_open_restaurants():
    datetime_str = request.args.get('datetime')
    if not datetime_str:
        return jsonify({'error': 'You must provide a date time value'}), 400

    try:
        target_datetime = datetime.strptime(datetime_str, '%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use MM-DD HH:MM'}), 400

    open_restaurants = []
    for restaurant, restHours in restaurant_data.items():
        if is_open(restHours, target_datetime):
            open_restaurants.append(restaurant)

    return jsonify({'open_restaurants': open_restaurants})


if __name__ == '__main__':
    app.run(debug=True)
