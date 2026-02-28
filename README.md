Healthiee 🎯
Basic Details
Team Name: [SheCodes]

Team Members

Member 1: [Aarcha Sidharthan] - [VAST,Thrissur]
Member 2: [Dhrishya Anil] - [VAST,Thrissur]
Project Description
Healthiee is a web application designed to help users check the safety and ingredient risk levels of everyday products. It cross-references products and ingredients against a database to warn users about potential health risks and international bans.

The Problem Statement
Consumers often lack clear, accessible information about the hidden risks of ingredients in the products they buy. It is difficult to know if an ingredient used in everyday items is truly safe or if it has been banned in other countries due to health and toxicity concerns.

The Solution
Healthiee solves this by providing a simple search interface where users can look up products or ingredients. The backend queries an SQLite database of known ingredients, evaluates their risk levels (Low, Medium, High), and checks international ban records (e.g., in the EU, Canada, India) to generate an easy-to-understand product report.

Technical Details
Technologies/Components Used

Languages used: Python, HTML, CSS, JavaScript

Frameworks used: FastAPI

Libraries used: SQLAlchemy, Pydantic, Uvicorn

Tools used: SQLite (Database)

Features
Product Safety Search: Search by product name, ingredient, or manufacturer to retrieve safety details.

Risk Level Assessment: Automatically categorizes ingredients into High, Medium, or Low risk levels based on toxicity data.

Global Ban Checker: Displays if an item is banned in specific countries and provides the medical/legal reason for the restriction (e.g., carcinogenic risk).

Multi-Category Support: Covers Food Additives, Cosmetics & Personal Care, and Pharmaceutical Products.

Implementation
Installation
# Clone the repository and navigate into it
# Create and activate a virtual environment (recommended)
# Install backend dependencies
cd backend
pip install -r ../requirements.txt
# 1. Seed the database with initial data (Countries, Ingredients, Bans)
python seed_data.py

# 2. Start the FastAPI backend server
uvicorn main:app --reload
Once the backend is running at http://127.0.0.1:8000, open frontend/index.html in your web browser to use the application interface.

Project Documentation
Screenshots
<img width="1891" height="884" alt="image" src="https://github.com/user-attachments/assets/a47483f4-49bb-44e4-8d19-762d3e2e7c17" />
<img width="1861" height="883" alt="image" src="https://github.com/user-attachments/assets/1b22e525-5731-492c-a99c-f4273593cb1c" />
Diagrams
System Architecture: The user interacts with a static HTML/JS frontend which sends JSON payloads via fetch API to a FastAPI backend. The backend processes these requests using SQLAlchemy ORM to query an SQLite database holding relational data on Products, Ingredients, and Country-specific Bans.
Additional Documentation
API Documentation
Base URL: http://127.0.0.1:8000

Endpoints

GET /

Description: Health check endpoint.

Response: {"message": "Healthiee API Running"}

GET /products/

Description: Retrieves a list of all products in the database.

Response: Array of product objects including their IDs, names, descriptions, and banned countries.

POST /products/

Description: Creates a new product entry along with its banned country list.

Request Body:
{
  "name": "string",
  "description": "string",
  "banned_countries": [
     {"country": "string", "reason": "string"}
  ]
}
POST /check-product (Frontend Integration)

Description: Checks a product/ingredient for its risk profile and ban status.

Request Body:
{
  "name": "Product Name"
}



