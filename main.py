from sqlalchemy import true
from website import create_app
from flask import redirect, render_template, url_for
from flask_ngrok import run_with_ngrok

app = create_app()

@app.errorhandler(404)
def not_found(e):
  return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)