# DRM-Free Game Comparison Tool

## Overview

The DRM-Free Game Comparison Tool allows users to check which games available on Steam also have a DRM-free version available on GOG. It provides users with a simple way to compare games across platforms, displaying statistics on which games are exclusive to Steam, exclusive to GOG, or have DRM-free options available on GOG.

This project includes:
- A data pipeline for automated data extraction, transformation, and loading (ETL).
- A web application built with FastAPI to serve as both the API backend and frontend.
- A visualization dashboard using Tableau to provide insights into the game data.
- Cloud infrastructure and deployment using AWS, including ECS, CloudWatch, and Snowflake.

## Key Features

- **Game Search**: Search for games on Steam and check if a DRM-free version is available on GOG.
- **Game Comparison**: Compare games across platforms (Steam vs GOG) and check which are DRM-free.
- **Interactive Dashboard**: Visualize game availability statistics through an interactive Tableau dashboard.
- **Real-Time Data**: Data is updated daily via an automated pipeline to ensure up-to-date information.
- **Cloud Infrastructure**: Hosted on AWS for scalability and reliability.
- **Automated Pipeline**: Data extraction, transformation, and loading are automated with Apache Airflow and Apache Spark.

## Architecture & Technologies

### Data Pipeline
- **Apache Spark**: Distributed data processing for cleaning and transforming game data.
- **Apache Airflow**: Orchestrates the ETL tasks to ensure data is fetched, cleaned, and loaded automatically.

### Data Storage
- **Snowflake**: A cloud-based data warehouse for storing and querying the processed game data.

### Web Application
- **FastAPI**: A fast web framework for building the REST API that powers the application, enabling users to query and compare games.

### Visualization
- **Tableau**: A dashboard tool for generating interactive charts and visualizations from the game data stored in Snowflake.

### Cloud Infrastructure
- **AWS**: Hosting the application on AWS for scalability and reliability.
- **Docker**: The app and its dependencies are containerized to ensure consistency between development and production environments.
- **AWS ECS (Elastic Container Service)**: Manages the deployment and scaling of Docker containers.
- **AWS CloudWatch**: Monitors and logs the application for troubleshooting and performance insights.

## How to Use the Tool

### Access the Web Application
- Navigate to the web application URL (hosted on AWS).
- Use the search bar to search for a game by title, which will show whether it’s available on Steam and if a DRM-free version is available on GOG.

### View the Tableau Dashboard
- The Tableau dashboard provides interactive visualizations such as:
  - Games exclusive to Steam
  - Games exclusive to GOG
  - Games with DRM-free versions on GOG

### Filter and Sort
- Filter games based on criteria like platform, DRM-free status, release date, and price.
- Sort games by attributes such as price, title, or release date.

## How It Works (Workflow)

1. **Data Extraction**:
   - Game data is fetched from the Steam and GOG APIs. Steam provides metadata, and GOG provides DRM-free status.
   - This data is fetched daily using Apache Airflow to ensure it is up-to-date.

2. **Data Processing**:
   - Apache Spark processes the data by applying transformations, cleaning, removing duplicates, handling missing values, and ensuring consistent formatting.

3. **Data Storage**:
   - Cleaned data is loaded into Snowflake for fast querying and analysis.

4. **Data Access**:
   - Users interact with the FastAPI web application to query and display game data.

5. **Visualization**:
   - Tableau queries Snowflake for live data and generates interactive visualizations showing game availability statistics.

## How to Run the Project Locally

### Requirements

- **Docker**: Required to run the application in a containerized environment.
- **Python 3.9+**: Required for the data pipeline and FastAPI app.
- **Snowflake Account**: Needed for querying the Snowflake data warehouse.
- **Tableau**: Tableau Desktop or Tableau Public (free) for creating and viewing dashboards.

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/drm-free-game-comparison
   cd drm-free-game-comparison

    Build the Docker Container:

docker build -t drm-game-comparison .

Run the Docker Container:

    docker run -p 5000:5000 drm-game-comparison

    This will start the FastAPI application locally at localhost:5000.

    Access the Application: Open a web browser and navigate to http://localhost:5000 to interact with the web application.

Deployment on AWS

The project is deployed on AWS and includes:

    Docker container deployment using AWS ECS.
    Daily data fetching, processing, and loading using Apache Airflow and Spark.
    Data stored in Snowflake for querying.
    CloudWatch monitoring for application performance and logging.

Testing

Unit tests for the project are located in the tests/ directory. They include tests for:

    API routes and endpoints (test_api.py)
    Data fetching and processing (test_data_pipeline.py)
    Data validation checks (test_data_validation.py)
    Snowflake integration (test_snowflake.py)
    Infrastructure tests (test_infrastructure.py)

To run the tests locally, use:

pytest

Acknowledgments

    Apache Airflow: For orchestrating the ETL pipeline.
    Apache Spark: For distributed data processing.
    Snowflake: For scalable cloud data storage and querying.
    FastAPI: For building the web application and API.
    Tableau: For data visualization and dashboarding.

License

This project is licensed under the MIT License. See the LICENSE file for details.