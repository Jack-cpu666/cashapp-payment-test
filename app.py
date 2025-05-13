import os
import sqlite3
import uuid
import datetime
from flask import Flask, render_template_string, redirect, request, send_file, url_for, Response
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'python-guide-secret-key')

# HTML Templates as strings
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learn Python - $1 Complete Guide</title>
    <style>
        /* Base Styles */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header */
        header {
            text-align: center;
            margin-bottom: 40px;
        }

        h1 {
            color: #2c3e50;
        }

        h2 {
            color: #3498db;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }

        /* Feature Sections */
        .feature {
            margin-bottom: 30px;
        }

        .feature ul {
            padding-left: 20px;
        }

        .feature li {
            margin-bottom: 8px;
        }

        /* Payment Section */
        .payment {
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 25px;
            text-align: center;
            margin: 40px 0;
            border: 1px solid #e0e0e0;
        }

        .cta-button {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 20px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }

        .cta-button:hover {
            background-color: #2980b9;
        }

        /* Footer */
        footer {
            margin-top: 50px;
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }

        /* Responsive Adjustments */
        @media (max-width: 600px) {
            body {
                padding: 15px;
            }
            
            .payment {
                padding: 15px;
            }
            
            .cta-button {
                width: 100%;
                box-sizing: border-box;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Learn Python Programming</h1>
        <p>A comprehensive guide for beginners - Just $1</p>
    </header>
    
    <main>
        <section class="feature">
            <h2>What You'll Learn</h2>
            <ul>
                <li>Python fundamentals and syntax</li>
                <li>Working with variables and data types</li>
                <li>Control flow: if statements, loops, and more</li>
                <li>Functions and modules</li>
                <li>Working with files and handling exceptions</li>
                <li>Introduction to popular Python libraries</li>
            </ul>
        </section>
        
        <section class="feature">
            <h2>Why This Guide?</h2>
            <p>This guide is designed to be straightforward and easy to follow, even if you've never programmed before. For just $1, you get lifetime access to a resource that will help you master Python step by step.</p>
        </section>
        
        <section class="payment">
            <h2>Get Instant Access</h2>
            <p>Click the button below to pay $1 and get immediate access to the complete Python guide.</p>
            
            <!-- Square payment button -->
            <div id="square-payment">
                <a href="{{ square_payment_link }}" id="square-button" class="cta-button">Buy Now ($1)</a>
            </div>
            
            <p><small>Secure payment processed via Square</small></p>
        </section>
    </main>
    
    <footer>
        <p>© 2025 Learn Python Guide. All rights reserved.</p>
    </footer>
</body>
</html>
"""

THANK_YOU_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You for Your Purchase!</title>
    <style>
        /* Base Styles */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Thank You Container */
        .container {
            text-align: center;
            background-color: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 30px;
            margin-top: 40px;
        }

        h1 {
            color: #2c3e50;
        }

        .download-button {
            display: inline-block;
            background-color: #27ae60;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 20px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }

        .download-button:hover {
            background-color: #219653;
        }

        /* Bonus Section */
        .bonus-section {
            margin-top: 40px;
            background-color: #eaf2f8;
            padding: 20px;
            border-radius: 6px;
            text-align: left;
        }

        .bonus-section ul {
            list-style-type: none;
            padding-left: 10px;
        }

        .bonus-section li {
            margin-bottom: 10px;
        }

        .bonus-section a {
            color: #3498db;
            text-decoration: none;
        }

        .bonus-section a:hover {
            text-decoration: underline;
        }

        .contact-info {
            margin-top: 40px;
            font-size: 0.9em;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Thank You for Your Purchase!</h1>
        <p>Your Python programming guide is ready for download.</p>
        
        {% if download_id %}
        <a href="/download/{{ download_id }}" class="download-button">Download Your Guide</a>
        {% else %}
        <p>There was an issue processing your download. Please check your email for download instructions or contact support.</p>
        {% endif %}
        
        <div class="bonus-section">
            <h2>Bonus Resources</h2>
            <p>Here are some additional resources to help you on your Python journey:</p>
            <ul>
                <li><a href="https://docs.python.org/3/" target="_blank">Official Python Documentation</a></li>
                <li><a href="https://www.w3schools.com/python/" target="_blank">W3Schools Python Tutorial</a></li>
                <li><a href="https://realpython.com/" target="_blank">Real Python - Practical Tutorials</a></li>
            </ul>
        </div>
        
        <p class="contact-info">If you have any questions or need assistance, please contact us at <a href="mailto:your@email.com">your@email.com</a></p>
    </div>
</body>
</html>
"""

# Sample Python guide content (replace with your actual guide or read from a file)
PYTHON_GUIDE_CONTENT = """
# Python Programming Guide

## Introduction to Python
Python is a high-level, interpreted programming language that is easy to learn and powerful to use.

## Getting Started
1. Installing Python
2. Your First Python Program
3. Using the Python IDLE

## Python Basics
- Variables and Data Types
- Operators
- Control Flow
- Functions

## Advanced Topics
- Object-Oriented Programming
- File Handling
- Error Handling
- Modules and Packages

## Python Libraries
- NumPy
- Pandas
- Matplotlib
- Requests

## Practice Projects
- Simple Calculator
- To-Do List Application
- Web Scraper
- Data Analysis
"""

# Initialize database
def init_db():
    """Initialize the SQLite database."""
    try:
        conn = sqlite3.connect('sales.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id TEXT PRIMARY KEY,
            email TEXT,
            purchase_date TIMESTAMP,
            download_count INTEGER DEFAULT 0
        )
        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        sys.exit(1)

# Ensure guide file exists
def ensure_guide_exists():
    """Create a sample Python guide file if it doesn't exist."""
    os.makedirs('guides', exist_ok=True)
    guide_path = os.path.join('guides', 'python_guide.pdf')
    
    if not os.path.exists(guide_path):
        # For this example, we'll create a simple text file
        # In a real scenario, you would have an actual PDF
        with open(guide_path, 'w') as f:
            f.write(PYTHON_GUIDE_CONTENT)
        logger.info(f"Created sample guide file at {guide_path}")
    else:
        logger.info(f"Guide file already exists at {guide_path}")

# Initialize the app
@app.before_first_request
def before_first_request():
    """Setup operations before the first request."""
    init_db()
    ensure_guide_exists()

# Routes
@app.route('/')
def index():
    """Main landing page with Square payment button."""
    # Use the provided Square payment link
    square_payment_link = os.getenv('SQUARE_PAYMENT_LINK', 'https://square.link/u/OPz9UZRH')
    return render_template_string(INDEX_HTML, square_payment_link=square_payment_link)

@app.route('/success', methods=['GET'])
def success():
    """Thank you page after successful purchase."""
    # Get transaction ID and email from Square callback
    transaction_id = request.args.get('transactionId', '')
    email = request.args.get('buyer_email', request.args.get('email', ''))
    
    # In a real app, you would verify the transaction with Square API here
    
    # Store purchase info in database
    if transaction_id or email:  # In real app, require both
        try:
            conn = sqlite3.connect('sales.db')
            cursor = conn.cursor()
            download_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO purchases (id, email, purchase_date) VALUES (?, ?, ?)",
                (download_id, email, datetime.datetime.now())
            )
            conn.commit()
            conn.close()
            logger.info(f"New purchase recorded for email: {email}")
            return render_template_string(THANK_YOU_HTML, download_id=download_id)
        except Exception as e:
            logger.error(f"Database error when recording purchase: {e}")
    
    # Fall back to a generic thank you page
    return render_template_string(THANK_YOU_HTML, download_id=None)

@app.route('/download/<download_id>')
def download(download_id):
    """Handle the download of the Python guide."""
    try:
        # Verify download ID
        conn = sqlite3.connect('sales.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM purchases WHERE id = ?", (download_id,))
        purchase = cursor.fetchone()
        
        if purchase:
            # Update download count
            cursor.execute("UPDATE purchases SET download_count = download_count + 1 WHERE id = ?", (download_id,))
            conn.commit()
            conn.close()
            
            # Path to your guide file
            guide_path = os.path.join('guides', 'python_guide.pdf')
            
            # If the file exists, send it
            if os.path.exists(guide_path):
                return send_file(guide_path, as_attachment=True, download_name='Python_Programming_Guide.pdf')
            else:
                # If file doesn't exist, send the content as text
                response = Response(PYTHON_GUIDE_CONTENT, mimetype='text/plain')
                response.headers.set('Content-Disposition', 'attachment', filename='Python_Programming_Guide.txt')
                return response
        
        conn.close()
        return "Invalid or expired download link", 404
    except Exception as e:
        logger.error(f"Error during download: {e}")
        return "An error occurred during download. Please try again later.", 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Ensure guide exists
    ensure_guide_exists()
    
    # Use environment variables for production deployment
    port = int(os.environ.get('PORT', 5000))
    
    # Log startup info
    logger.info(f"Starting server on port {port}")
    logger.info("Set SQUARE_PAYMENT_LINK environment variable to your Square checkout link")
    
    # Run the app
    app.run(host='0.0.0.0', port=port)
