# 🧠 String Analyzer API

A simple RESTful API built with FastAPI that analyzes strings, computes their properties, stores them, and allows retrieval, filtering, and deletion.
It also supports natural language filtering like “all single word palindromic strings”

---

## 🚀 Features

Analyze Strings: Compute properties such as:

Length

Word count

Unique character count

Palindrome check

Character frequency map

SHA-256 hash

Store & Retrieve: Persist analyzed strings in-memory.

Filter Results: Query strings with filters like is_palindrome, min_length, max_length, etc.

Natural Language Filtering: Search using human-like queries ("strings longer than 10 characters").

Delete Strings: Remove any stored string from the system.




---

## 🧩 Project Structure
```
hng_stage0/
├── app.py
├── requirements.txt
├── README.md

---
```

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/mik3lson/hng_stage1
cd hng_stage0

```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## ▶️ Running the Server

### Start the FastAPI development server:
```bash
uvicorn app:app --reload
```
### You should see output similar to
```arduino
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Endpoints Overview

| Method   | Endpoint                              | Description                                     |
| -------- | ------------------------------------- | ----------------------------------------------- |
| `GET`    | `/`                                   | Welcome message                                 |
| `POST`   | `/strings/`                           | Analyze and store a new string                  |
| `GET`    | `/strings/`                           | Get all stored strings (supports query filters) |
| `GET`    | `/strings/filter-by-natural-language` | Filter using natural language                   |
| `DELETE` | `/strings/{string_value}`             | Delete a stored string by its value             |

## 🌐 Example Request
### Endpoint:
```vbnet
POST /strings
{
   "value":"madam"
}
```

### Response: 
```json
{
  {
  "id": "hash123...",
  "value": "madam",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "word_count": 1,
    "unique_characters": 3
  },
  "created_at": "2025-10-22T17:45:00Z"
}
```


## 🧪 Testing
###You can test the API using:
curl<br>
Postman<br>
http://127.0.0.1:8000/docs— FastAPI’s built-in Swagger UI


# Alternatively the api is hosted here:
```link
https://hngstage0-production-8c35.up.railway.app/
```
