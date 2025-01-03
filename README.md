# Air Quality Information Hub - Backend Application

## Project Overview

This project is a backend service that collects air quality data from an open-source API, processes it, and stores it in a SQLite database. The data is then exposed through various endpoints, allowing users to query and access air quality information for New York City neighborhoods.

We are using the following technologies:
- **Python**: A high-level programming language known for its readability and simplicity. It powers the server-side logic, data processing, and interaction with the database.
- **Flask**: A lightweight web framework for building RESTful APIs.
- **SQLite**: A simple, serverless SQL database to store the data.
- **Pandas**: For handling and processing the data fetched from the API.
- **Socrata API**: Used to fetch air quality data from the City of New York’s open data portal.
- **Docker**: For containerizing the application to ensure consistency and portability across different environments.

The collected data provides air quality measurements in various neighborhoods of NYC, with key health implications for urban populations.

---

## API Data Source

This project pulls air quality data from the **New York City Air Quality Surveillance Dataset** provided by the **Department of Health and Mental Hygiene (DOHMH)**. The dataset contains detailed information about air pollution levels across different neighborhoods, over various time periods.

Dataset includes key attributes like:
- **id**: A unique identifier for the record.  
- **name**: The air quality indicator, such as Ozone or Nitrogen.  
- **geo_place_name**: The neighborhood in New York City (e.g., Manhattan, Brooklyn).  
- **time_period**: The year/season when the measurement was taken (e.g., 2022, Summer 2018).  
- **data_value**: The actual measurement value for the indicator (e.g., 34.5, 6.2).
- **measure**: The units of measurement (e.g., ppb, mcg/m³).

For more details:
You can visit the NYC Open Data portal: [NYC Open Data - Air Quality](https://data.cityofnewyork.us/Environment/Air-Quality/c3uy-2p5r/about_data)

You can also refer Additional Resources: [Air Quality](https://dev.socrata.com/foundry/data.cityofnewyork.us/c3uy-2p5r)

---

## Getting Started

Follow these steps to set up and run the Air Quality API backend:

### 1. Clone the repository:
Start by cloning the repository to your local machine:
```bash
git clone https://github.com/murali16krishna/AirQualityBackend.git
cd AirQualityBackend
```

### 2. Build the Docker Image:
This application is containerized using Docker. Once you have cloned the repo, ensure Docker is installed and running before executing the build and run commands.

Build the Docker image using the following command:
```bash
docker build -t air-quality-backend .
```

### 3. Run the Docker Container:
Start the container and map the Flask app port to your local port:
```bash
docker run -p 5000:5000 --name air-quality-backend-container air-quality-backend
```
The Flask app will now be running on port 5000 of your local machine.

### 4. Set Up the Database:
To initialize and migrate the database, follow these steps:

#### 1. Enter the container using the following command:
```bash
docker exec -it air-quality-backend-container bash
```

#### 2. Initialize the database (run this only once for the first time):
```
flask db init
```

#### 3. If you have any schema changes, or if it's your first time setting up the database:
```
flask db migrate -m "Initial Migration"
```

#### 4. Apply the migration:
```
flask db upgrade
```
At this point the database is ready. We need to insert the data into db by making a POST request to fetch endpoint, which will be covered in further steps.

### 5. Fetch Air Quality Data:
To fetch data from the NYC Open Data API and insert it into the database, use the POST /air-quality/fetch endpoint. This will collect the air quality data and populate your database.

Example Request:
### `POST http://localhost:5000/api/v1/air-quality/fetch`

#### Response:
```json
{
  "message": "Data fetched successfully!"
}
```

### 6. Access the API Endpoints:
Once the data is populated, you can start using the following endpoints to retrieve the air quality data:

### API Endpoints
### 1. `GET http://localhost:5000/api/v1/`
Returns a welcome message.

#### Response:
```json
{
    "message": "Welcome to the Air Quality API!"
}
```

### 2. `GET http://localhost:5000/api/v1/air-quality`

This endpoint fetches paginated air quality data with optional filters.

### Request

#### Optional Query Parameters:
- `page`: The page number (default: `1`).
- `per_page`: The number of items per page (default: `10`).
- `name`: Filter by the name of the indicator (e.g., `PM2.5`).
- `geo_place_name`: Filter by the neighborhood or geographic location (e.g., `Manhattan`).
- `time_period`: Filter by the time period (e.g., `2022`).

#### Example Request:
`GET http://localhost:5000/api/v1/air-quality?page=1&per_page=10&name=PM2.5`

#### Example Response:
The response is a JSON object that includes the requested air quality data.
```json
{
  "data": [
    {
      "unique_id": "12345",
      "indicator_id": 1,
      "name": "PM2.5",
      "measure": "micrograms per cubic meter",
      "geo_place_name": "Manhattan",
      "time_period": "2022",
      "start_date": "2022-01-01",
      "data_value": 35.2
    },
    {
      "unique_id": "67890",
      "indicator_id": 2,
      "name": "Ozone",
      "measure": "micrograms per cubic meter",
      "geo_place_name": "Brooklyn",
      "time_period": "2022",
      "start_date": "2022-01-01",
      "data_value": 42.7
    },
    "..."
  ],
  "total": 100,
  "pages": 10,
  "current_page": 1,
  "per_page": 10
}
```

### 3. `GET http://localhost:5000/api/v1/air-quality/distinct-geo-place-names`

Fetches distinct neighborhood names where air quality data is available.

#### Example Response:
```json
{
  "distinct_geo_place_names": [
    "Manhattan",
    "Brooklyn",
    "Queens",
    "Bronx",
    "Staten Island"
  ]
}
```

## Development Setup (Without Docker):

If you'd like to work on the Air Quality API project locally without using Docker, follow these steps:

### 1. Install Python and Required Packages:
Ensure you have **Python 3.10+** installed on your machine. Then, create a virtual environment and install the required dependencies:

- **Create a Virtual Environment**:
  ```bash
  python3 -m venv venv

- **Activate the Virtual Environment**:
    
  On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
  
    On Windows:
  ```bash
  venv\Scripts\activate
  ```

- **Install the Dependencies**:
  ```bash
  pip install -r requirements.txt

### 2. Set Up the Database:
You will need to set up the SQLite database and apply migrations.

#### 1. Initialize the database (run this only once for the first time):
```
flask db init
```

#### 2. If you have any schema changes, or if it's your first time setting up the database:
```
flask db migrate -m "Initial Migration"
```

#### 3. Apply the migration:
```
flask db upgrade
```
At this point the database is ready. We need to insert the data into db by making a POST request to fetch endpoint, which will be covered in further steps.

### 3. Start the Flask Development Server:
To run the Flask application locally, use the following command:

```
flask run
```
The backend will now be running on http://localhost:5000/api/v1.

### 4. Fetch Air Quality Data:
To fetch data from the NYC Open Data API and insert it into the database, use the POST /air-quality/fetch endpoint. This will collect the air quality data and populate your database.

Example Request:
### `POST http://localhost:5000/api/v1/air-quality/fetch`

#### Response:
```json
{
  "message": "Data fetched successfully!"
}
```
Now the data is populated, and you can start using the available endpoints to retrieve the air quality data.

---

# Proposed Features and Enhancements

### 1. Multi-Source Data Fetching
- Add support for fetching air quality data from multiple external sources.
- Extend functionality to handle various data formats such as JSON, CSV, XML etc.
- Normalize and map data fields from different sources and formats to a unified schema before storing them in the database.

### 2. Database Enhancements

#### Relational Database (e.g., PostgreSQL):
- **Best for well-defined schemas**: When your data structure/schema is well-defined, and you need complex analytics, aggregation, and relationships between entities, relational databases like PostgreSQL are the best option.
- **Enable indexing** on frequently queried fields (e.g., unique IDs, timestamps, and location data) to improve query performance.

#### NoSQL Database (e.g., MongoDB):
- **Best for evolving schemas**: If the schema may evolve over time or if data comes from multiple sources with varying formats, NoSQL databases like MongoDB are more suitable as they allow for flexible storage and scaling.
- Flexible schema support for semi-structured or evolving data formats.

### 3. Real-Time Data Updates
- Integrate with **streaming APIs** (if available) or set up scheduled jobs using **Celery** or **Cron** to fetch and insert new data periodically.
- Use message queues like **Apache Kafka** or **RabbitMQ** to handle real-time streaming data and ensure asynchronous updates to the database.

### 4. Data Aggregation & Analytics
- Add endpoints for aggregated air quality statistics (e.g., average air quality by neighborhood, time period, or indicator).

### 5. Air Quality Alerts Feature
- Create a system that allows users to sign up for alerts if air quality in their neighborhood crosses a threshold.

### 6. Authentication & Authorization
- Admin-only access for specific endpoints (e.g., POST endpoint to feed data into the database).
- Token-based authentication (e.g., JWT) to secure all API endpoints.

### 7. Data Export
- Allow users to export air quality data in various formats (CSV, JSON, Excel).

### 8. Error Handling & Logging
- Improved error handling with custom error messages for specific exceptions (e.g., database errors, network issues, invalid input).

### 9. API Versioning
- Implement versioning for the API to handle future changes without breaking existing clients.

### 10. API Documentation (Swagger/OpenAPI)
- Add automatic API documentation using Swagger or OpenAPI.
