# OpenAPI LLM Test Generator

Static test generation is too slow for modern infrastructure. This project is a lightweight AI pipeline that reads OpenAPI/Swagger JSON schemas and auto-generates parameterized Pytest scenarios for edge cases and boundary conditions. 

It calculates state deltas between runs to prevent overwriting custom assertions and automatically flags newly added edge cases in a CI/CD-friendly Markdown report.

## 🏗️ Architecture

```mermaid
graph TD
    subgraph Data Extraction
        SPEC["OpenAPI Spec<br/>swagger.json"] --> PARSER["Parser<br/>Extracts Endpoint Schema"]
    end

    subgraph AI Generation Layer
        PARSER --> LLM["LLM API<br/>Gemini / OpenAI"]
        PROMPT["System Prompt<br/>Boundary Rules"] --> LLM
        LLM --> JSON_OUT["JSON Test Data<br/>Generated Boundary Cases"]
    end

    subgraph CI/CD Execution
        JSON_OUT --> DELTA["Delta Reporter<br/>Calculates Added/Removed Tests"]
        DELTA --> PYTEST["Pytest Runner<br/>Data-Driven Execution"]
        PYTEST --> API["Target REST API<br/>Swagger Petstore"]
        API -.->|"Status Code Validation"| PYTEST
    end

    %% Styling with forced black text for visibility
    style SPEC fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#000000
    style PARSER fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#000000
    style LLM fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000000
    style PROMPT fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000000
    style JSON_OUT fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000000
    style DELTA fill:#ffe6cc,stroke:#d79b00,stroke-width:2px,color:#000000
    style PYTEST fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000000
    style API fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#000000
```
    
## 🚀 Features
* **Schema Parsing:** Isolates specific routes (e.g., `POST /pet`) from massive OpenAPI definitions.
* **LLM Edge-Case Detection:** Prompts AI models (Google Gemini or OpenAI) to identify boundary conditions like null values, empty strings, and out-of-bounds integers directly from the schema.
* **Data-Driven Execution:** Decouples AI generation from test execution by outputting structured JSON arrays, allowing Pytest to dynamically run parameterized tests.
* **State-Aware Delta Reporting:** Calculates set differences between pipeline runs to track added and removed parameters without blindly overwriting test files.

## 🛠️ Quick Start

**1. Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Configure Environment**
Create a .env file in the root directory and add your API keys:
```bash
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```
**3. Run the AI Generator Pipeline**
This this command executes a pipeline that parses the schema, prompts the LLM to identify boundary conditions and generate a structured JSON array of test cases, calculates the state delta between runs, and generates a CI/CD-friendly Markdown report.

```bash
python main.py --spec swagger.json --endpoint /pet --method post --llm gemini
```
**4. Execute the Test Suite**
Executes the Pytest runner, which dynamically loads the generated JSON boundary cases and runs the parameterized tests against the target API.

```bash
pytest generated_tests/test_petstore_runner.py -v
```

