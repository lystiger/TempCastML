## How to Run the Connected Application

To see the backend and frontend working together, follow these steps:

### 1. Start the Backend

Navigate to the `Backend` directory and start the FastAPI application. You'll need `uvicorn` installed (`pip install uvicorn`).

```bash
cd Backend
# It's recommended to activate your virtual environment first
# source venv/bin/activate
uvicorn main:app --reload --port 8000
```
This will start the backend server, typically on `http://localhost:8000`.

### 2. Start the Frontend

Open a **new terminal window**, navigate to the `frontend` directory, and start the Vite development server.

```bash
cd frontend
npm install # Only if you haven't run it before or dependencies changed
npm run dev
```
This will start the frontend development server, typically on `http://localhost:5173`.

### 3. View the Application

Open your web browser and navigate to the address provided by the `npm run dev` command (usually `http://localhost:5173`). The React application will now attempt to fetch data from the Python backend.

**Important Notes:**

*   **CORS:** The backend has been configured with CORS middleware to allow requests from `http://localhost:5173`. If your frontend runs on a different port or domain, you will need to update the `origins` list in `Backend/main.py`.
*   **Database:** Ensure your database is set up and has some data, especially if you are testing the `/history` or `/latest` endpoints. The `create_db_and_tables()` function in `main.py` will create the tables on startup. You might need to ingest some data using `collect_data.py` or manually add entries for testing.
*   **Prediction Model:** For the `/predict` endpoint to work, the `backend/AI/LTSM.py` model needs to be functional and able to generate predictions based on the data it retrieves.
