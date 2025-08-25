# DEMO LINK :
https://project-sof-analysis.netlify.app/

# Maritime SOF Analytics 🚢

This full-stack web application extracts, analyzes, and visualizes data from maritime Statement of Facts (SOF) documents. It offers a user-friendly interface to upload SOF files (PDF, DOCX), intelligently parses them, and structures the data into a clean JSON format. The processed information is displayed on an interactive dashboard featuring sortable tables and a Gantt chart timeline of events.

-----

## 🚀 Key Features

  * **Intelligent Document Parsing**: Uses **LlamaParse** to accurately extract text from PDF and DOCX files.
  * **AI-Powered Data Structuring**: Leverages the **Google Gemini API** with JSON mode to convert raw text into a structured, validated schema.
  * **Modern Backend**: Built with **FastAPI**, providing a robust and asynchronous API for efficient file processing.
  * **Interactive Frontend**: A sleek, responsive user interface built with HTML, CSS, and vanilla JavaScript without any heavy frameworks.
  * **Rich Data Visualization**: Includes a detailed table view and a dynamic Gantt chart to visualize the timeline of maritime operations.
  * **Flexible Data Export**: Allows users to download the structured data in both **CSV** and **JSON** formats for easy integration.
    
-----

## 🛠️ How It Works

1.  **Upload**: The user uploads one or more SOF documents (PDF, DOC, DOCX) through the web interface.
2.  **Parse**: The FastAPI backend receives the files and uses **LlamaParse** to extract the raw text content from each document.
3.  **Structure**: The extracted text is sent to the **Google Gemini API**. A detailed prompt instructs the model to return a structured JSON object that matches a predefined Pydantic schema.
4.  **Display**: The structured JSON data is sent back to the frontend, where JavaScript dynamically renders it into an interactive dashboard. Users can toggle between a table view and a Gantt chart timeline.
5.  **Export**: The user can export the processed data as a CSV or JSON file with a single click.

-----

## 📂 Project Structure

```
.
├── uploads/              # Temporary directory for file uploads
├── .env                  # Environment variables (API keys)
├── data.html             # Data visualization page
├── document_parser.py    # Handles text extraction with LlamaParse
├── index.html            # Homepage
├── main.py               # FastAPI backend server
├── processor.py          # Handles data structuring with Gemini
├── readme.md             # This file
├── requirements.txt      # Python dependencies
├── script.js             # Frontend JavaScript logic
├── styles.css            # CSS for styling
└── upload.html           # File upload page
```

-----

## ⚙️ Setup and Installation

Follow these instructions to get the project running locally.

### Prerequisites

  * Python 3.8+
  * `pip` package manager
  * A modern web browser (e.g., Chrome, Firefox)

### 1\. Clone the Repository

Clone this repository to your local machine:

```bash
# [INSERT YOUR REPOSITORY CLONE URL HERE]
git clone https://your-repository-url.com/repo.git
cd repo
```

### 2\. Set Up Environment Variables

This project requires API keys for LlamaParse and Google Gemini.

1.  Create a file named `.env` in the root project directory.

2.  Add your API keys to the `.env` file like this:

    ```env
    LLAMA_CLOUD_API_KEY="llx-..."
    GOOGLE_API_KEY="AIz..."
    ```

### 3\. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4\. Run the Application

Start the backend server with Uvicorn:

```bash
uvicorn main:app --reload
```

### 5\. Open the Web Interface

While the backend is running, you can access the application by opening the `index.html` file directly in your web browser.

#### **Note on Hosting:**

If you intend to serve the frontend directly from FastAPI instead of just opening the local HTML files, you'll need to add routes to your `main.py` to serve the static pages. Make sure to import `FileResponse` from `fastapi.responses`.

```python
from fastapi.responses import FileResponse

# NOTE: Update the file paths if your HTML files are in a different directory.
@app.get("/")
async def serve_index():
    return FileResponse('index.html')

@app.get("/upload")
async def serve_upload_page():
    return FileResponse('upload.html')

@app.get("/data")
async def serve_data_page():
    return FileResponse('data.html')
```

-----

## 🔗 Links and Resources

  * **LlamaParse**: [Get your API key](https://docs.cloud.llamaindex.ai/api_key)
  * **Google AI Studio**: [Get your Gemini API key](https://aistudio.google.com/app/apikey)
  * **FastAPI**: [Official Documentation](https://fastapi.tiangolo.com/)
  * **Pydantic**: [Documentation](https://docs.pydantic.dev/latest/)
