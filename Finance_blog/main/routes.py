from flask import render_template, request, Blueprint, flash
from Flaskblog.models import Post, StockData  # Assuming this model is used for blog posts  
from Flaskblog import db 
import os
import requests

main = Blueprint('main', __name__)

# Alpha Vantage API Key
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'CLPWWQKA0PDIKXQS')

@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

def get_stock_data(symbol):
    """Fetch stock data from Alpha Vantage API for the given stock symbol."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]
        else:
            print("Error in response:", data)  # Debugging line
            return None
    else:
        print("Request failed with status code:", response.status_code)  # Debugging line
        return None

@main.route('/finance', methods=['GET', 'POST'])
def finance():
    """Render finance page and fetch stock data if requested via POST."""
    stock_data = None
    stock_symbol = None

    if request.method == 'POST':
        stock_symbol = request.form.get('symbol').upper()  # Get stock symbol from form input
        
        if not stock_symbol:  # Check if stock symbol is provided
            flash("Please enter a stock symbol.", "danger")
            return render_template('finance.html', stock_data=None, stock_symbol=None)

        # Fetch the stock data
        stock_data = get_stock_data(stock_symbol)

        if stock_data is None:  # Handle cases where data fetching fails
            flash("Invalid stock symbol or API limit reached!", "danger")
            return render_template('finance.html', stock_data=None, stock_symbol=None)

        # Format the stock data for rendering
        formatted_data = []
        for date, info in stock_data.items():
            formatted_data.append({
                'date': date,
                'open': info['1. open'],
                'close': info['4. close']
            })
        
        return render_template('finance.html', stock_data=formatted_data, stock_symbol=stock_symbol)

    # Render the finance page without stock data if it's a GET request
    return render_template('finance.html', stock_data=None, stock_symbol=None)

# Optional index route for redirecting to finance
@main.route('/index', methods=['GET', 'POST'])
def index():
    return finance()  # Redirects to finance logic
