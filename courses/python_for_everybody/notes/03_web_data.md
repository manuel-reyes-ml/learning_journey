# 03: Using Python to Access Web Data

**Course:** Using Python to Access Web Data  
**Platform:** Coursera  
**Instructor:** Dr. Charles Severance  
**Started:** [Your date]  
**Completed:** [Your date or "In Progress"]

---

## 📚 Overview

Learn to extract and process data from the web using Python. Covers regular expressions for pattern matching, network programming for HTTP requests, and working with structured data formats (XML, JSON, APIs). Essential skills for gathering real-world data.

---

## ✅ Progress

- [x] Module 11: Regular Expressions
- [x] Module 12: Network Programming
- [x] Module 13: Web Services and APIs

---

## 🎯 Key Concepts

### Module 11: Regular Expressions

**What it is:**  
Pattern matching language for finding and extracting specific text patterns. Like "Find all email addresses" or "Extract all phone numbers."

**Why it matters:**  
Text data is messy. Regex lets you find patterns without writing complex string logic. Essential for data extraction and validation.

**Key points:**
- **Import:** `import re`
- **re.search():** Find first match in string
- **re.findall():** Find all matches, return list
- **Special characters:** `.` (any), `^` (start), `$` (end), `*` (0+), `+` (1+), `?` (0 or 1)
- **Character sets:** `[a-z]` (lowercase), `[0-9]` (digits), `\S` (non-whitespace)
- **Greedy vs non-greedy:** `.*` (greedy) vs `.*?` (non-greedy)
- **Parentheses:** `()` capture groups for extraction
- **Escape special chars:** `\.` to match literal period

---

### Module 12: Network Programming

**What it is:**  
Making HTTP requests to fetch data from web servers. Like your browser does, but programmatically.

**Why it matters:**  
Real data lives on the web. APIs, websites, services - all accessed via HTTP. Foundation for web scraping and API integration.

**Key points:**
- **Socket library:** Low-level networking (rarely used directly)
- **urllib:** Built-in library for HTTP requests
- **urllib.request.urlopen():** Fetch URL, returns file-like object
- **HTTP:** Protocol browsers use (GET requests for data)
- **Encoding:** Web data is bytes, decode to string: `.decode()`
- **BeautifulSoup:** Parse HTML (extract data from web pages)
- **HTML parsing:** Find tags, extract text, navigate document structure
- **Web scraping ethics:** Respect robots.txt, rate limit, don't overload servers

---

### Module 13: Web Services and APIs

**What it is:**  
Structured data exchange using XML and JSON. APIs provide data in machine-readable formats instead of HTML.

**Why it matters:**  
Modern applications exchange data via APIs. JSON is everywhere - Twitter, Google, financial data, weather, etc. Essential skill.

**Key points:**
- **XML:** Markup language with tags (like HTML but for data)
- **XML parsing:** `xml.etree.ElementTree` for parsing XML
- **JSON:** JavaScript Object Notation - lightweight data format
- **json.loads():** Parse JSON string to Python dict/list
- **json.dumps():** Convert Python object to JSON string
- **API:** Application Programming Interface - structured way to request data
- **API keys:** Authentication for API access
- **Rate limiting:** APIs limit requests per hour/day
- **API endpoints:** Specific URLs for different data types

---

## 💻 Code Examples

### Regular Expressions - Basics
```python
import re

# Simple search
text = "My email is john@example.com"
match = re.search(r'@\S+', text)
if match:
    print(match.group())  # Output: @example.com

# Find all email addresses
text = "Contact: john@example.com or mary@test.org"
emails = re.findall(r'\S+@\S+', text)
print(emails)  # Output: ['john@example.com', 'mary@test.org']

# Extract specific parts
line = "From: john@example.com Sat Jan 5"
match = re.search(r'From: (\S+@\S+)', line)
if match:
    email = match.group(1)  # Captured group
    print(email)  # Output: john@example.com
```

---

### Regular Expressions - Common Patterns
```python
import re

# Extract numbers
text = "The price is $19.99"
price = re.findall(r'[0-9.]+', text)
print(price)  # Output: ['19.99']

# Validate email (simple)
email = "user@example.com"
if re.match(r'\S+@\S+\.\S+', email):
    print("Valid email")

# Extract domain from email
email = "john@example.com"
domain = re.findall(r'@(\S+)', email)
print(domain)  # Output: ['example.com']

# Greedy vs non-greedy
text = "From: "
greedy = re.findall(r'', text)      # ['']
nongreedy = re.findall(r'', text)  # Same here, but matters with multiple matches

# Real example: Extract all "From:" emails
text = """
From: john@example.com
From: mary@test.org
Subject: Hello
"""
emails = re.findall(r'From: (\S+@\S+)', text)
print(emails)  # Output: ['john@example.com', 'mary@test.org']
```

---

### Network Programming - Basic HTTP Request
```python
import urllib.request

# Fetch web page
url = 'http://data.pr4e.org/romeo.txt'
response = urllib.request.urlopen(url)
data = response.read().decode()  # Decode bytes to string
print(data[:100])  # First 100 characters

# Count words in web page
words = data.split()
print(f"Total words: {len(words)}")

# Read line by line
url = 'http://data.pr4e.org/romeo.txt'
response = urllib.request.urlopen(url)
for line in response:
    line = line.decode().strip()
    if len(line) > 0:
        print(line)
```

---

### Web Scraping with BeautifulSoup
```python
import urllib.request
from bs4 import BeautifulSoup

# Fetch and parse HTML
url = 'http://www.dr-chuck.com/page1.htm'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Extract all links
tags = soup('a')  # Find all  tags
for tag in tags:
    url = tag.get('href', None)
    print(url)

# Find specific elements
# Get all paragraph text
paragraphs = soup.find_all('p')
for p in paragraphs:
    print(p.get_text())

# Extract table data
rows = soup.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if cells:
        data = [cell.get_text() for cell in cells]
        print(data)
```

---

### XML Parsing
```python
import xml.etree.ElementTree as ET

# Parse XML string
xml_data = '''

    
        John
        25
        john@example.com
    
    
        Mary
        30
        mary@example.com
    

'''

tree = ET.fromstring(xml_data)

# Find all person elements
for person in tree.findall('person'):
    name = person.find('name').text
    age = person.find('age').text
    email = person.find('email').text
    print(f"{name}: {age}, {email}")

# Output:
# John: 25, john@example.com
# Mary: 30, mary@example.com
```

---

### JSON Parsing
```python
import json

# Parse JSON string
json_data = '''
{
    "name": "Manuel",
    "age": 25,
    "email": "manuel@example.com",
    "skills": ["Python", "SQL", "Data Analysis"]
}
'''

data = json.loads(json_data)
print(data['name'])    # Output: Manuel
print(data['skills'])  # Output: ['Python', 'SQL', 'Data Analysis']

# Access nested data
for skill in data['skills']:
    print(skill)

# Parse list of objects
json_data = '''
[
    {"name": "John", "age": 25},
    {"name": "Mary", "age": 30}
]
'''

people = json.loads(json_data)
for person in people:
    print(f"{person['name']}: {person['age']}")
```

---

### Working with APIs
```python
import urllib.request
import json

# Call API (example: geocoding)
address = 'Ann Arbor, MI'
url = f'http://py4e-data.dr-chuck.net/json?address={address}&key=42'

# Fetch data
response = urllib.request.urlopen(url)
data = response.read().decode()

# Parse JSON
result = json.loads(data)
print(json.dumps(result, indent=2))  # Pretty print

# Extract specific data
if 'results' in result:
    place = result['results'][0]
    print(place['formatted_address'])

# Real example: Weather API (conceptual)
# import requests  # Better than urllib for APIs
# api_key = 'your_key_here'
# city = 'Greenville,SC'
# url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
# response = requests.get(url)
# weather = response.json()
# temp = weather['main']['temp']
# print(f"Temperature: {temp}K")
```

---

### Combining It All - Email Frequency from Web
```python
import urllib.request
import re

# Fetch data from web
url = 'http://data.pr4e.org/mbox-short.txt'
response = urllib.request.urlopen(url)

# Count emails
counts = {}
for line in response:
    line = line.decode().strip()
    # Use regex to extract email
    emails = re.findall(r'From: (\S+@\S+)', line)
    for email in emails:
        counts[email] = counts.get(email, 0) + 1

# Find most common
max_count = 0
max_email = None
for email, count in counts.items():
    if count > max_count:
        max_count = count
        max_email = email

print(f"Most frequent: {max_email} ({max_count} times)")
```

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Regex** | Pattern matching language | `r'\S+@\S+'` for emails |
| **HTTP** | Protocol for web requests | Browser uses HTTP |
| **API** | Structured data interface | Twitter API, Weather API |
| **JSON** | Lightweight data format | `{"name": "Manuel"}` |
| **XML** | Markup language for data | `<name>Manuel</name>` |
| **Parsing** | Converting string to structure | JSON string → dict |
| **Web scraping** | Extracting data from websites | BeautifulSoup |
| **Endpoint** | API URL for specific data | `/weather`, `/users` |
| **BeautifulSoup** | HTML/XML parsing library | `soup.find_all('a')` |
| **urllib** | Built-in HTTP library | `urlopen(url)` |
| **Greedy** | Match as much as possible | `.*` matches everything |
| **Capture group** | Extract part of regex match | `r'From: (\S+)'` |

---

## 🔧 Practice Exercises

**Exercise 1: Email Extractor**
- **Task:** Read file, extract all unique email addresses using regex
- **Solution:** Use `re.findall(r'\S+@\S+', text)`, store in set
- **Learning:** Regex patterns, set for uniqueness

**Exercise 2: Link Scraper**
- **Task:** Fetch web page, extract all links using BeautifulSoup
- **Solution:** Parse HTML, find all `<a>` tags, get `href` attribute
- **Learning:** Web scraping, HTML parsing

**Exercise 3: JSON Data Processor**
- **Task:** Fetch JSON from API, extract and sum specific values
- **Solution:** Parse JSON, loop through results, calculate total
- **Learning:** API calls, JSON parsing, data extraction

**Exercise 4: XML Parser**
- **Task:** Parse XML file, create summary report
- **Solution:** Use ElementTree, loop through elements, aggregate data
- **Learning:** XML structure, data aggregation

**Exercise 5: Weather Dashboard**
- **Task:** Build simple weather lookup using API
- **Solution:** Get city input, call weather API, parse JSON, display results
- **Learning:** Real API integration, user input, data display

---

## 💡 Key Takeaways

1. **Regex is powerful but complex** - Start simple, build up patterns gradually
2. **JSON is everywhere** - Most modern APIs use JSON (easier than XML)
3. **APIs need keys** - Most require registration for authentication
4. **Rate limits exist** - Don't make too many requests, add delays
5. **Web scraping is last resort** - Use APIs when available (more reliable)
6. **Always decode bytes** - Web data comes as bytes, need `.decode()`
7. **BeautifulSoup simplifies HTML** - Much easier than regex for HTML
8. **Test patterns incrementally** - Build regex step by step

---

## 🔗 Resources

- [Regular Expressions 101](https://regex101.com/) - Test regex patterns
- [Python Regex Documentation](https://docs.python.org/3/library/re.html)
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Free fake API for testing
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [HTTP Status Codes](https://httpstatuses.com/) - Understand API responses
- [Public APIs List](https://github.com/public-apis/public-apis) - Free APIs to practice

---

## 📝 My Notes

**What clicked:**  
- JSON is just Python dictionaries/lists in text form
- Regex `()` parentheses extract the important part
- APIs are way better than web scraping (structured data!)
- BeautifulSoup makes HTML parsing actually manageable

**Challenges:**  
- Regex syntax is cryptic - takes practice to read
- Remembering to decode bytes to strings
- Understanding nested JSON structures
- API authentication and keys setup

**Aha moments:**  
- `re.findall()` with capture groups extracts exactly what you want
- JSON parsing is literally one line: `data = json.loads(text)`
- Most APIs return JSON nowadays (XML is older)
- Can test regex patterns at regex101.com before putting in code

**To review:**  
- Complex regex patterns (lookahead, lookbehind)
- Error handling for network requests
- XML namespaces (when they appear)
- OAuth authentication for APIs

**Real-world applications:**
- Used regex to extract stock symbols from financial news
- Fetched stock prices via yfinance API (uses JSON)
- Wikipedia API for pageview data (Trading Attention Tracker!)
- BeautifulSoup for scraping when no API exists

---

## ➡️ Next Steps

**Next course:** 04_databases.md (Object-Oriented Programming, SQL, Data Visualization)  
**To practice:**  
- Build API-powered apps (weather, stocks, news)
- Practice regex on real email/log files
- Scrape data from websites (ethically!)
- Combine with dictionaries for data analysis
- Explore free public APIs and build small projects