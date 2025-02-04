```markdown
# DRM-Free Game Comparison Tool

## Overview

The DRM-Free Game Comparison Tool allows users to check which games available on Steam 
also have a DRM-free version available on GOG. 

It provides users with a simple way to compare games across platforms, 
displaying statistics on which games are exclusive to Steam, exclusive to GOG, or have DRM-free options available on GOG.

This project includes:
- A data pipeline for automated data extraction, transformation, and loading (ETL).
- A web application built with FastAPI to serve as both the API backend and frontend.
- A visualization dashboard using Tableau to provide insights into the game data.
- Cloud infrastructure and deployment using AWS, including ECS, CloudWatch, and Snowflake.

## Key Technologies

- **FastAPI**: Used to build the backend API.
- **Apache Airflow**: For orchestrating ETL tasks (data fetching, cleaning, and loading).
- **Snowflake**: Cloud-based data warehouse for storing processed data.
- **Docker**: Containerizes the application and dependencies.
- **AWS ECS & CloudWatch**: Deployment and monitoring.

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
   ```

2. **Create the `.env` File**:
   Create a `.env` file in the root of the project with the following content:
   ```bash
   FROM_EMAIL=your-email@example.com
   TO_EMAIL=recipient@example.com
   EMAIL_PASSWORD=your-email-password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   FERNET_KEY=your-fernet-key
   ```

3. **Omitting Environment Variables from Source Control**:
   To ensure that sensitive data (like email credentials and API keys) 
   are not tracked in version control, make sure to add the `.env` file to your `.gitignore`.  
   
   Simply add the following line to your `.gitignore` file:
   ```
   .env
   ```

4. **Build the Docker Containers**:
   In the project directory, run the following command to build the containers:
   ```bash
   docker-compose build
   ```

5. **Start the Services**:
   Once the build is complete, run the containers:
   ```bash
   docker-compose up
   ```

   This will start:
   - The FastAPI app on `http://localhost:5000`
   - The Airflow Web UI on `http://localhost:8080`
   - MySQL and Snowflake services (for backend integration)

### Accessing the Application

- **FastAPI**: Open a web browser and go to `http://localhost:5000` to interact with the FastAPI web application.
- **Airflow**: Open `http://localhost:8080` to access the Apache Airflow Web UI for monitoring ETL pipelines.

### Running Tests

Unit tests are located in the `tests/` directory. To run them locally:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
