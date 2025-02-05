# Topic Generator FastAPI

## Overview

This project is a FastAPI application that generates a structured topic tree based on user-provided parameters. It integrates with the OpenAI API to generate content dynamically, and leverages Pydantic models to ensure data integrity and validation.

## Features

- **Dynamic Topic Tree Generation:** Generates a hierarchical topic tree based on the provided theme and numerical parameters (main topics, subtopics, and curriculum topics).
- **Flexible Request Model:** Accepts parameters such as theme, number of topics, and optional URIs for discipline and educational context.
- **Structured Output:** Returns a JSON object representing the complete topic tree, including metadata and nested collections.
- **Integration with OpenAI API:** Utilizes OpenAI models to generate structured text for topic tree content.

## Project Structure

- `app.py`: The main FastAPI application. Contains the API endpoints, data models (using Pydantic), and functions for processing the topic tree generation.
- `.env`: Environment file that should contain your `OPENAI_API_KEY`, among other configuration variables.
- `requirements.txt`: Lists the Python dependencies required to run the application.

## Setup Instructions

1. **Clone the Repository**
   
   Ensure you are in the correct directory

2. **Create and Configure the .env File**
   
   Create a `.env` file if it does not exist, and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Install Dependencies**
   
   Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   
   Start the FastAPI server using uvicorn:
   ```bash
   uvicorn app:app --reload
   ```
   The API will be available at `http://localhost:8000`.

## API Endpoints

- **`GET /`**: Basic endpoint to check if the service is running.
- **`POST /generate-topic-tree`**: Generates a topic tree based on the provided JSON payload. The expected payload matches the `TopicTreeRequest` model, which includes fields like `theme`, `num_main_topics`, `num_subtopics`, `num_curriculum_topics`, and optional URIs.

### Example Request

```json
{
  "theme": "Physik in Anlehnung an die Lehrpläne der Sekundarstufe 2",
  "num_main_topics": 5,
  "num_subtopics": 3,
  "num_curriculum_topics": 2,
  "include_general_topic": true,
  "include_methodology_topic": true,
  "discipline_uri": "http://w3id.org/openeduhub/vocabs/discipline/460",
  "educational_context_uri": "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_2",
  "model": "gpt-4o-mini"
}
```

## Error Handling

The application uses FastAPI's built-in error handling along with custom exception handling to manage validation errors, OpenAI API errors, and other runtime issues. HTTP status codes and clear error messages are returned on failure.

## Development and Contribution

- **Code Maintenance:** The project is built with modularity in mind. Endpoints, models, and utility functions are well-organized within `app.py`.
- **Contributions:** Contributions are welcome! Please fork the repository and submit pull requests. For major changes, consider opening an issue first to discuss the modifications.

## License

This project is open source and available under the Apache-2.0 License.
