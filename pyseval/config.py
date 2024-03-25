import os

from dotenv import load_dotenv

load_dotenv()

JSON_SCHEMA_URL = os.getenv(
    "JSON_SCHEMA_URL",
    "https://raw.githubusercontent.com/m-bi-github/pyseval_json_schema/main/pyseval_schema.json",
)

SEMANTIC_MODEL_ID = os.getenv("SEMANTIC_MODEL_ID", "")
