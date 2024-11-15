A. To Request Data from the Fragrance Recommender Microservice
The program should send a request by creating a CSV file (season_request.csv) with the desired season. The fragrance recommender then processes the request and provides recommendations in another CSV file (recommendations.csv).

Example Call: Send a Request for Fragrance Recommendations
Write Request for a Season: Write the desired season to season_request.csv. For example, to request recommendations for "spring," the file content would look like this:

```
# Create the request file
    with open(request_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([season])
    print(f"Request written for season '{season}' in '{request_file}'.")

```
Process the Request: Run the microservice by executing the fragrance_recommender.py script. This reads the request from season_request.csv, processes the data, and writes the response to recommendations.csv.
Read the Response: After processing, the microservice writes recommendations to recommendations.csv.

```
import csv

# Read the recommendations file
with open('recommendations.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    print("--- Fragrance Recommendations ---")
    for row in reader:
        print(f"Name: {row['Name']}, Brand: {row['Brand']}, Notes: {row['Notes']}")

```


B. To Receive Data from the Fragrance Recommender Microservice
To receive data, the microservice writes results into recommendations.csv based on the requested season.
The output will be either:
A list of recommended fragrances (Name, Brand, Notes) if matches are found.
A message: "No recommendations found for this season." if no matches exist.

Example call to display recommendations:

```
# Display recommendations
try:
    with open('recommendations.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        print("--- Fragrance Recommendations ---")
        for row in reader:
            print(f"Name: {row['Name']}, Brand: {row['Brand']}, Notes: {row['Notes']}")
except FileNotFoundError:
    print("Error: Recommendations file not found.")

```

C. 
