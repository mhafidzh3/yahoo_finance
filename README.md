## Running the Application

### Option 1: Docker (Recommended)

This project is fully containerized using Docker Compose.

#### Start Application
- docker compose up --build (main run, build the container)

#### Optional
Reset containers and database
- docker compose down -v

Load or refresh stock data
- docker compose run --rm app python scripts/run_all.py 

Ensure the app is running
- docker compose up -d 

### Option 2: Local Development (Dev Mode)

For development, debugging, or rapid iteration without Docker:

pip install -r requirements.txt
streamlit run app/streamlit_app.py

To populate or refresh the database manually:
python scripts/run_all.py

#=========================================================================

📊 Stock Market Dashboard

A Streamlit-based stock market dashboard that:

Fetches historical stock data from Yahoo Finance

Stores and processes data in PostgreSQL

Computes technical indicators (MA, RSI, returns)

Visualizes price trends and comparisons

Optionally generates AI-powered technical summaries

#=========================================================================

✨ Features

- 📈 Price & indicator visualization

- 📊 Multi-ticker comparison (normalized performance)

- 📐 Technical indicators (MA, RSI, returns)

- 🤖 Optional AI technical summary (OpenAI)

- 📱 Mobile-friendly layout

- 🗄 PostgreSQL-backed storage

- ⚡ Cached queries for performance

#=========================================================================

🗂 Project Structure

app/        Streamlit UI
src/        Core business logic
scripts/    Data ingestion entry points
config/     Ticker configuration
logs/       Application logs

#=========================================================================

🚀 Running the App (Local)

1. Create virtual environment

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

2. Install dependencies

pip install -r requirements.txt

3. Set environment variables

Create .env:

POSTGRES_HOST=localhost
POSTGRES_DB=stock_data
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
OPENAI_API_KEY=your_key_here

4. Run Streamlit

python -m streamlit run app/streamlit_app.py

#=========================================================================

🛠 Data Pipeline

To fetch and store stock data:

python scripts/run_all.py

Tickers are defined in:

config/tickers.yaml

#=========================================================================

⚠️ Notes

AI features are optional

App works without OpenAI API key

Mobile layout supported

Not financial advice

#=========================================================================

📄 License

[MIT License]

