from flask import Flask, render_template, request, redirect
from Url_Shortener import UrlShortener
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Deactivate Flask caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)

# Create Table Model
class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    short_url = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Urls %s>' % self.short_url

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/shortener')
def shortener():
    return render_template('pages/shortener.html')


@app.route('/shortener', methods=["GET", "POST"])
def short():
    if request.method == 'POST':
        long_url = request.form["my_url"]
        shortener = UrlShortener(long_url)
        shortened_url = shortener.shorten_url()
        # record the urls in the db
        try:
            status = "New"
            url_model = Urls(url=long_url, short_url=shortened_url)
            db.session.add(url_model)
            db.session.commit()
        except Exception as e:
            status = "Present"
            db.session.rollback()
            entree = url_model.query.filter_by(url=long_url).first_or_404()
            shortened_url = entree.short_url
    
    return render_template('pages/shortener.html', status=status, shortened_url=shortened_url)

@app.route('/rj/<shortened_url>')
def unshort_url(shortened_url):
    url_recorded = Urls.query.filter_by(short_url = shortened_url).first_or_404()
    url = url_recorded.url
    if url:
        return redirect(url)
    return render_template('pages/page_not_found.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('pages/page_not_found.html'), 404

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)