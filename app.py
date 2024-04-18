import csv
from datetime import datetime, time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load restaurant data from CSV file into a dictionary
restaurant_data = {}


def create_schedules(day_hours, array):
    parts = day_hours.split(' ')
    days = parts[0] if ',' not in parts[0] else parts[0] + parts[1]
    hours = ' '.join(parts[1:]) if ',' not in parts[0] else ' '.join(parts[2:])
    hour_array = hours.split(' - ')
    start_datetime = convert_string_time(hour_array[0])
    end_datetime = convert_string_time(hour_array[1])
    time_frames = {}

    day_array = days.split(',')
    for day in day_array:
        if '-' not in day:
            time_frames[convert_day_to_integer(day)] = (start_datetime, end_datetime)
        else:
            time_frames.update(weekly_hours(day.split('-'), end_datetime, start_datetime))

    array.append(time_frames)


def convert_string_time(hour_string):
    start_format = '%I:%M %p' if ':' in hour_string else '%I %p'
    return datetime.strptime(hour_string, start_format).time()


def convert_day_to_integer(day_string):
    if day_string == 'Tues':
        day_string = 'Tue'
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return days_of_week.index(day_string)


def weekly_hours(array_of_days, end_hour, start_hour):
    start_day_index = convert_day_to_integer(array_of_days[0])
    end_day_index = convert_day_to_integer(array_of_days[1])
    local_dict = {}
    for day_digit in range(start_day_index, end_day_index + 1):
        local_dict[day_digit] = (start_hour, end_hour)
    return local_dict


with open('public-data/restaurants.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        name = row[0]
        time = row[1].split('/')
        multi_hours = []
        for hour_range in time:
            create_schedules(hour_range.strip(), multi_hours)
        # convert list of dict into single dict of weekday: (time, time)
        hours_dict = multi_hours[0]
        for hour in multi_hours:
            hours_dict.update(hour)
        restaurant_data[name] = hours_dict


# API endpoint
def is_open(rest_hours, target_datetime):
    day_of_week = convert_day_to_integer(target_datetime.strftime('%a'))
    now_time = target_datetime.time()
    start_time, end_time = rest_hours[day_of_week] if rest_hours.get(day_of_week) else (None, None)
    if not start_time or not end_time:
        return False

    return start_time <= now_time <= end_time


@app.route('/', methods=['GET'])
def get_open_restaurants():
    datetime_str = request.args.get('datetime')
    if not datetime_str:
        return jsonify({'error': 'You must provide a date time value'}), 400

    try:
        target_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use YYYY-MM-DD HH:MM'}), 400

    # need to make tests more robust
    # if target_datetime.strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
    #     return jsonify({'error': 'Date must be today or in the future'}), 400

    open_restaurants = []
    for restaurant, restHours in restaurant_data.items():
        if is_open(restHours, target_datetime):
            open_restaurants.append(restaurant)

    return jsonify({
        'Day of the week': target_datetime.strftime('%a'),
        'Requested hour': target_datetime.strftime('%I:%M %p'),
        'open_restaurants': open_restaurants
    })


if __name__ == '__main__':
    app.run(debug=True)
