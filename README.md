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

## Environment Variables

This project requires environment variables to run.

1. Copy `.env.example` to `.env`
2. Fill in the required values
3. Never commit `.env` to version control

## Architecture Overview

- Data source: Yahoo Finance
- ETL pipeline: Python
- Database: PostgreSQL
- Backend: SQLAlchemy
- Frontend: Streamlit
- Deployment: Docker Compose

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

[----]

