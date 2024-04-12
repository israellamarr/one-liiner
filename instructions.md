Build an API with an endpoint which takes a single parameter, a datetime string, and returns a list of restaurant names which are open on that date and time. You are provided a dataset in the form of a CSV file of restaurant names and a human-readable, string-formatted list of open hours. Store this data in whatever way you think is best. Optimized solutions are great, but correct solutions are more important. Make sure whatever solution you come up with can account for restaurants with hours not included in the examples given in the CSV. Please include all tests you think are needed.

### Assumptions:
* If a day of the week is not listed, the restaurant is closed on that day
* All times are local — don’t worry about timezone-awareness
* The CSV file will be well-formed, assume all names and hours are correct

### Want bonus points? Here are a few things we would really like to see:
1. A Dockerfile and the ability to run this in a container
3. Using the python standard library as much as possible.
4. Testing

If you have any questions, let me know. Use git to track your progress, and push your solution to a github repository