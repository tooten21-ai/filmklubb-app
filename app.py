from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filmklubb.db'
app.config['SECRET_KEY'] = 'dev'  # Byt ut senare till något säkrare
db = SQLAlchemy(app)

# Databasmodell för Film
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Film {self.title}>'

# Skapa databasen när appen startar
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    films = Film.query.all()
    return render_template('index.html', films=films)

@app.route('/add', methods=['GET', 'POST'])
def add_film():
    if request.method == 'POST':
        title = request.form['title']
        country = request.form['country']
        year = request.form['year']
        
        new_film = Film(title=title, country=country, year=year)
        db.session.add(new_film)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_film.html')

if __name__ == '__main__':
    app.run(debug=True)