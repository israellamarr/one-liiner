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

    if ',' in days:
        # handles (Mon-Thu, Sun) or (Mon, Thu-Fri) type scenario
        day_array = days.split(',')
        for day in day_array:
            if '-' not in day:
                time_frames[day] = (start_datetime, end_datetime)
            else:
                start_day, end_day = day.split('-')
                weekly_hours(end_day, end_datetime, start_day, start_datetime, time_frames)
    elif '-' not in days:
        # single day timeframe scenario
        time_frames[days] = (start_datetime, end_datetime)
    else:
        # handles Mon-Fri type scenario
        start_day, end_day = days.split('-')
        weekly_hours(end_day, end_datetime, start_day, start_datetime, time_frames)

    array.append(time_frames)


def convert_string_time(hour_string):
    start_format = '%I:%M %p' if ':' in hour_string else '%I %p'
    return datetime.strptime(hour_string, start_format).time()


def weekly_hours(end_day, end_hour, start_day, start_hour, time_frames):
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
        for hour_range in time:
            create_schedules(hour_range.strip(), multi_hours)
        # convert list of dict into single dict of weekday: (time, time)
        hours_dict = multi_hours[0]
        for hour in multi_hours:
            hours_dict.update(hour)
        restaurant_data[name] = hours_dict


# API endpoint
def is_open(rest_hours, target_datetime):
    day_of_week = target_datetime.strftime('%a')
    now_time = target_datetime.time()
    start_time, end_time = rest_hours[day_of_week]
    return start_time <= now_time <= end_time


@app.route('/restaurants', methods=['GET'])
def get_open_restaurants():
    datetime_str = request.args.get('datetime')
    if not datetime_str:
        return jsonify({'error': 'You must provide a date time value'}), 400

    try:
        target_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use MM-DD HH:MM'}), 400

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
