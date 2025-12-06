"""
Optimized Flask Blog Application
Entry point for the application with improved structure
"""
import os
from blog_app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 5000))
    
    # Run the application
    # Note: In production, use a WSGI server like gunicorn
    app.run(host="0.0.0.0", port=port, debug=app.config['DEBUG'])
