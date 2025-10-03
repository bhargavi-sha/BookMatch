from flask import Flask, render_template, request
from recommendation_engine import get_recommendations

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    """Renders the main page (index.html)."""
    return render_template('index.html')

# Define the route that handles the recommendation logic
@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Handles the form submission, gets recommendations, 
    and displays them on the recommendations page.
    """
    try:
        # Get the user ID from the form submitted on the website
        user_id_str = request.form['user_id']
        user_id = int(user_id_str) # Convert to integer

        # Call the ML engine to get recommendations [cite: 10]
        recommendations = get_recommendations(user_id)

        # Send the recommendations to a new page to be displayed
        return render_template('recommendations.html', books=recommendations, user_id=user_id)
    except (ValueError, KeyError):
        # Handle cases with invalid input
        error_message = "Invalid User ID. Please enter a number."
        return render_template('index.html', error=error_message)

# This block allows you to run the app directly
if __name__ == '__main__':
    app.run(debug=True)