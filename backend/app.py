import os
import sqlite3
import logging
from typing import Dict, Any, Optional, List
import pandas as pd
import plotly.express as px
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI setup
app = FastAPI(title="E-commerce AI Data Agent", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Models
class QuestionRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sql_query: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None
    visualization: Optional[str] = None
    error: Optional[str] = None

# Database Manager
class DatabaseManager:
    def __init__(self, db_path: str = "ecommerce.db"):
        self.db_path = db_path
        self.initialize_database()
        self.import_data_from_sheets()

    def initialize_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS Product_Level_Ad_Sales_Metrics")
            cursor.execute("DROP TABLE IF EXISTS Product_Level_Total_Sales_Metrics")
            cursor.execute("DROP TABLE IF EXISTS Product_Eligibility")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Product_Level_Ad_Sales_Metrics (
                    eligibility_datetime_utc TEXT,
                    item_id INTEGER,
                    eligibility INTEGER,
                    message TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Product_Level_Total_Sales_Metrics (
                    date TEXT,
                    item_id INTEGER,
                    ad_sales REAL,
                    impressions INTEGER,
                    ad_spend REAL,
                    clicks INTEGER,
                    units_sold INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Product_Eligibility (
                    date TEXT,
                    item_id INTEGER,
                    total_sales REAL,
                    total_units_ordered INTEGER
                )
            """)
            conn.commit()
            conn.close()
            logger.info("✅ Database schema initialized")
        except Exception as e:
            logger.error(f"❌ Init error: {e}")
            raise

    def import_data_from_sheets(self):
        try:
            urls = {
                "Product_Level_Ad_Sales_Metrics": "https://docs.google.com/spreadsheets/d/1Loc32KsHwEGhLAahSfMA6t1aZdEvxJIPADxpdzZEZTw/gviz/tq?tqx=out:csv",
                "Product_Level_Total_Sales_Metrics": "https://docs.google.com/spreadsheets/d/1ZATJteA4sU7DXN-fqJxG8Td_Nwif5QB2fTQvGK8LegY/gviz/tq?tqx=out:csv",
                "Product_Eligibility": "https://docs.google.com/spreadsheets/d/1ftXt9Z6uEXUMlIHSZK0CR2kLlNZyj8TUi4lQmMF6qWo/gviz/tq?tqx=out:csv"
            }

            conn = sqlite3.connect(self.db_path)
            for table, url in urls.items():
                df = pd.read_csv(url)
                df.to_sql(table, conn, if_exists="replace", index=False)
                logger.info(f"✅ Imported {table} from Google Sheets")

            conn.close()
        except Exception as e:
            logger.error(f"❌ Google Sheets import failed: {e}")
            raise

    def execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            raise

# LLM Manager
class LLMManager:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={self.api_key}"
        self.schema = """
Database Schema:

1. Product_Level_Ad_Sales_Metrics
   - eligibility_datetime_utc (TEXT)
   - item_id (INTEGER)
   - eligibility (INTEGER)
   - message (TEXT)

2. Product_Level_Total_Sales_Metrics
   - date (TEXT)
   - item_id (INTEGER)
   - ad_sales (REAL)
   - impressions (INTEGER)
   - ad_spend (REAL)
   - clicks (INTEGER)
   - units_sold (INTEGER)

3. Product_Eligibility
   - date (TEXT)
   - item_id (INTEGER)
   - total_sales (REAL)
   - total_units_ordered (INTEGER)

Guidelines:
- Use JOINs on `item_id` and `date` when combining tables.
- To calculate RoAS: SUM(ad_sales) / SUM(ad_spend)
- For latest eligibility: use MAX(eligibility_datetime_utc)
- Use SQLite syntax.
- Return only the SQL query (no explanation or markdown).
"""

    def natural_language_to_sql(self, question: str) -> str:
        try:
            prompt = f"""
{self.schema}

Convert the following natural language question into a SQL query:
"{question}"
"""
            data = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            }
            response = requests.post(self.base_url, json=data, timeout=30)
            if response.status_code == 200:
                sql = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                sql = sql.strip().removeprefix("```sql").removesuffix("```").strip()
                return sql
            else:
                logger.error(f"Gemini API Error: {response.status_code}: {response.text}")
                raise HTTPException(status_code=500, detail="Gemini API failed")
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            raise HTTPException(status_code=500, detail="LLM processing failed")

# Visualization
class VisualizationManager:
    @staticmethod
    def create_visualization(data: List[Dict[str, Any]], question: str) -> Optional[str]:
        try:
            if not data:
                return None
            df = pd.DataFrame(data)
            q = question.lower()

            if 'date' in df.columns and any(x in q for x in ["trend", "over time", "daily"]):
                y = df.select_dtypes(include='number').columns[0]
                fig = px.line(df, x='date', y=y, title="Trend")
                return fig.to_json()

            elif 'item_id' in df.columns and any(x in q for x in ["compare", "top", "vs"]):
                y = df.select_dtypes(include='number').columns[0]
                fig = px.bar(df, x='item_id', y=y, title="Comparison")
                return fig.to_json()

            return None
        except Exception as e:
            logger.error(f"Viz error: {e}")
            return None

# Managers
db = DatabaseManager()
llm = LLMManager()
viz = VisualizationManager()

# Routes
@app.get("/")
async def root():
    return {"status": "healthy", "message": "E-commerce AI Data Agent is running!"}

@app.get("/schema")
async def get_schema():
    return {
        "tables": [
            {"name": "Product_Level_Ad_Sales_Metrics", "columns": ["eligibility_datetime_utc", "item_id", "eligibility", "message"]},
            {"name": "Product_Level_Total_Sales_Metrics", "columns": ["date", "item_id", "ad_sales", "impressions", "ad_spend", "clicks", "units_sold"]},
            {"name": "Product_Eligibility", "columns": ["date", "item_id", "total_sales", "total_units_ordered"]}
        ]
    }

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QuestionRequest):
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question is empty")

        logger.info(f"Question: {question}")
        sql = llm.natural_language_to_sql(question)
        logger.info(f"SQL: {sql}")
        results = db.execute_query(sql)

        answer = f"Found {len(results)} result(s)." if results else "No results found."
        chart = viz.create_visualization(results, question)

        return QueryResponse(
            answer=answer,
            sql_query=sql,
            data=results,
            visualization=chart
        )
    except Exception as e:
        logger.error(f"Error in /ask: {e}")
        return QueryResponse(answer="Error occurred.", error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
