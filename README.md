# Setup

1. Create virtual environment: `python -m venv .venv`
2. Activate: `source .venv/bin/activate` (Mac/Linux) or `.\venv\scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Initialize database: `python init.py`
5. Run: `python app.py`

## Notes

- `init.py` creates a SQLite sample database and generates a `.env` file with a secret key
- The admin credentials are defined in `seed.sql`
- This is a personal learning project
