# AI Product Recommender with Python/Flask Backend

This project is an e-commerce product recommender that uses the Gemini API to provide intelligent, human-like explanations for why a product is recommended based on user behavior. This version uses a Python Flask backend for the API and a SQLite database for product storage.

## Project Structure

-   **Frontend (`/`)**: A React application built with Vite that displays the user interface.
-   **Backend (`/backend`)**: A Python Flask server that handles API requests, interacts with the database, and calls the Gemini API.

## How to Run Locally

**Prerequisites:**
*   Node.js (v18 or higher)
*   Python (v3.8 or higher) and `pip`

---

### **Step 1: Backend Setup**

First, set up and run the Python backend server.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Gemini API Key:**
    Create a new file named `.env` inside the `backend` directory and add your API key.
    ```
    # backend/.env
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```

5.  **Initialize the Database:**
    Run the `init_db.py` script once to create and populate the `database.db` file.
    ```bash
    python init_db.py
    ```

6.  **Run the Backend Server:**
    Start the Flask server. It will run on `http://127.0.0.1:5000`.
    ```bash
    flask run
    ```
    Keep this terminal window running.

---

### **Step 2: Frontend Setup**

Now, in a **new terminal window**, set up and run the React frontend.

1.  **Navigate to the project root directory:**
    (If you are in the `backend` directory, go back one level: `cd ..`)

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Run the Frontend Development Server:**
    This will start the React app on `http://localhost:3000`.
    ```bash
    npm run dev
    ```

---

### **Step 3: View the App**

Open your web browser and navigate to **[http://localhost:3000](http://localhost:3000)** to see the application in action!
