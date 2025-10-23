from fastapi import FastAPI, HTTPException, Query
import hashlib
from datetime import datetime
import re



app = FastAPI()

database ={}

def palindrome_check(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

def count_word(s: str) -> int:
    words = s.split()
    return len(words)

def unique_characters_count(s: str) -> int:
    return len(set(s.lower()))

def check_char_frequency(s: str):
    freq = {}
    for ch in s.lower():
        freq[ch] = freq.get(ch, 0) + 1
    return freq

'''
def unique_characters_count(s:str):
    unique_char =[]
    for char in s:
        if char not in unique_char:
            unique_char.append(char)
    return len(unique_char)

def check_char_frequency(s:str):
    data ={}
    for char in s:
        if char in data:
            data[char] +=1
        else:
            data[char] =1 

    return data
'''

    

@app.get("/")
async def root():
    return {"message":"Hello, welcome to string analyzer API!"}


@app.post("/strings/", status_code=201)
async def analyze_string(value:str):

    if not isinstance(value, str):
        raise HTTPException(status_code=422, detail="Invalid data type for value, it must be a string")

    if value.strip() == "":
        raise HTTPException(status_code=400, detail="String value cannot be empty")

    if value in database:
        raise HTTPException(status_code=409, detail="String value already exists")
    
    length = len(value)
    is_palindrome = palindrome_check(value)
    unique_characters = unique_characters_count(value)
    hash_object = hashlib.sha256(value.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    word_count = count_word(value)
    string_frequency = check_char_frequency(value)
    timestamp = datetime.utcnow().isoformat()

    

    result = {
        "id": hex_dig,
        "value": value,
        "properties": {
            "length": length,
            "is_palindrome": is_palindrome,
            "unique_characters": unique_characters,
            "word_count": word_count,
            "sha256_hash": hex_dig,
            "character_frequency_map":string_frequency
        },
        "created_at": timestamp
    }

    database[value] = result

    return result





@app.get("/strings")
async def get_all_strings(
    is_palindrome: bool | None = Query(None, description="Filter by palindrome status"),
    min_length: int | None = Query(None, description="Minimum string length"),
    max_length: int | None = Query(None, description="Maximum string length"),
    word_count: int | None = Query(None, description="Exact word count"),
    contains_character: str | None = Query(None, description="Filter by containing a character")
):

    try:
        results = list(database.values())

    # Apply filters one by one
        if is_palindrome is not None:
           results = [s for s in results if s["properties"]["is_palindrome"] == is_palindrome]
    
        if min_length is not None:
            results = [s for s in results if s["properties"]["length"] >= min_length]
    
        if max_length is not None:
            results = [s for s in results if s["properties"]["length"] <= max_length]
        
        if word_count is not None:
            results = [s for s in results if s["properties"]["word_count"] == word_count]
            
        if contains_character is not None:
            char = contains_character.lower()
        results = [s for s in results if char in s["value"].lower()]


   

    # Build response
        return {
            "data": results,
            "count": len(results),
            "filters_applied": {
            "is_palindrome": is_palindrome,
            "min_length": min_length,
            "max_length": max_length,
            "word_count": word_count,
            "contains_character": contains_character
        }
    }
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid query parameter values or types"
        )


@app.get("/strings/filter-by-natural-language")
async def filter_by_natural_language(query: str):
    try:
        filters = {}
        q = query.lower().strip()

        # Detect palindrome-related queries
        if "palindrome" in q or "palindromic" in q:
            filters["is_palindrome"] = True

        # Word count filters
        if re.search(r"\b(single|one)\b word", q):
            filters["word_count"] = 1
        elif m := re.search(r"exactly (\d+) words?", q):
            filters["word_count"] = int(m.group(1))

        # Length-based filters
        if m := re.search(r"(?:longer|more) than (\d+)", q):
            filters["min_length"] = int(m.group(1)) + 1
        if m := re.search(r"(?:shorter|less) than (\d+)", q):
            filters["max_length"] = int(m.group(1)) - 1
        if m := re.search(r"(?:length of|length|exactly) (\d+)", q):
            filters["min_length"] = int(m.group(1))
            filters["max_length"] = int(m.group(1))

        # Character-based filters
        if m := re.search(r"(?:containing|contains|contain)(?: the letter)? ([a-z])", q):
            filters["contains_character"] = m.group(1)
        elif "first vowel" in q:
            filters["contains_character"] = "a"

        # No recognizable filters
        if not filters:
            raise HTTPException(
                status_code=400,
                detail="Unable to parse natural language query"
            )

        # Conflicting filters
        if "min_length" in filters and "max_length" in filters:
            if filters["min_length"] > filters["max_length"]:
                raise HTTPException(
                    status_code=422,
                    detail="Query parsed but resulted in conflicting filters"
                )

        # Apply filters to stored strings
        results = list(database.values())

        if "is_palindrome" in filters:
            results = [s for s in results if s["properties"]["is_palindrome"]]
        if "word_count" in filters:
            results = [s for s in results if s["properties"]["word_count"] == filters["word_count"]]
        if "min_length" in filters:
            results = [s for s in results if s["properties"]["length"] >= filters["min_length"]]
        if "max_length" in filters:
            results = [s for s in results if s["properties"]["length"] <= filters["max_length"]]
        if "contains_character" in filters:
            c = filters["contains_character"].lower()
            results = [s for s in results if c in s["value"].lower()]

        # Always return 200 OK — even if no matches
        return {
            "data": results,
            "count": len(results),
            "interpreted_query": {
                "original": query,
                "parsed_filters": filters
            }
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to parse natural language query"
        )
    
@app.get("/strings/{string_value}")
async def get_string_properties(string_value: str):
    if string_value in database:
        return database[string_value]
    else:
        raise HTTPException(status_code=404, detail="String value not found")
    
    
@app.delete("/strings/{string_value}", status_code = 204)
async def delete_string(string_value: str):
    if string_value in database:
        del database[string_value]
        return 
    else:
        raise HTTPException(status_code=404, detail="String value not found")
    