# NuMethods
MADE BY: Andrés Restrepo, Juan Pablo Posso, Sebastián Villegas

---
## Setting up NuMethods

### Frontend
Before running the frontend, update the API URL in frontend/.env with your (possibly private) IP address.

For example, replace:

    VITE_API_URL=http://192.168.1.2:5000

with:

    VITE_API_URL=http://<YOUR PRIVATE IP>:5000

Then, in frontend/, install all dependencies with:

    npm i


### Backend
Before running the backend, go to backend/ and run:

On Windows:

    venv\Scripts\activate

On macOS/Linux:

    source venv/bin/activate

This should activate a virtual environment where you can install all the required Python packages for this project. When you see (venv) in your shell, you can install all Python dependencies with:

    pip install -r requirements.txt

---
## Running NuMethods
### Frontend
After setting up the frontend, run inside frontend/ the following command:

    npm run dev

### Backend
After setting up the backend, run (make sure the virtual environment is activated) inside backend/ the following command:

    python server.py