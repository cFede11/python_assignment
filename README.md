# Description
This project utilizes the Python API Alpha Vantage to retrieve stock data for IBM and AAPL. The data is then stored in a local mySQL database. A Flask API is implemented to facilitate access to the stock data based on a specified time period. Additionally, it provides functionality to calculate the average price within a given time range.

# Techstack
I opted for a lightweight tech stack since the project is very simple. I chose mySQL, because it is a lightweight and simple to use database management system and I am familiar with its syntax, making it a good fit. Similarly, I selected Flask, a straightforward and lightweight framework. Since there is no front-end involved, Flask's simplicity and ease of use made it an ideal choice.

# How to run locally
1 - Docker Initialization:
- After downloading the code, navigate to the same folder as the Dockerfile.
- Execute the following command to start the Docker environment for the API and the Database:
```sh
docker-compose up --build
```

2 - Populating the Tables:
- Run the following command within the Docker api shell to populate the tables:
```sh
python get_raw_data.py
```
3 - Sending Requests to the API:
Example request URL:
```sh
http://localhost:5000/api/financial_data?start_date=2023-01-01&end_date=2023-02-24&symbol=IBM&limit=5&page=1
```

# AlphaVantage API key
For the local environment, the API key is set as an environment variable in the Dockerfile. The reason for this is first, simplifies the evaluation and testing of the project, and second, it aligns with the file structure outlined in the original project's README.md file. However, to handle the API key more effectively, it is recommended to use a configuration file that stores the API key separately. This configuration file can then be imported into the required scripts as needed.

For the production environment, would be better to utilize environment variables offered by web services such as Google Cloud or AWS. These services provide convenient methods for updating and managing keys in a production setting.
