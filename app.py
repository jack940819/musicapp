from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Music

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 建立資料庫
with app.app_context():
    db.create_all()

# RESTful API
@app.route('/api/music', methods=['GET'])
def get_music_list():
    music_list = Music.query.all()
    return jsonify([music.to_dict() for music in music_list])

@app.route('/api/music', methods=['POST'])
def create_music():
    data = request.json
    new_music = Music(name=data['name'], source=data['source'], numbers=data['numbers'])
    db.session.add(new_music)
    db.session.commit()
    return jsonify(new_music.to_dict()), 201

@app.route('/api/music/<int:music_id>', methods=['GET'])
def get_music_detail(music_id):
    music = Music.query.get_or_404(music_id)
    return jsonify(music.to_dict())

@app.route('/api/music/<int:music_id>', methods=['PUT'])
def update_music(music_id):
    music = Music.query.get_or_404(music_id)
    data = request.json
    music.name = data['name']
    music.source = data['source']
    music.numbers = data['numbers']
    db.session.commit()
    return jsonify(music.to_dict())

@app.route('/api/music/<int:music_id>', methods=['DELETE'])
def delete_music(music_id):
    music = Music.query.get_or_404(music_id)
    db.session.delete(music)
    db.session.commit()
    return '', 204

# 前端頁面
@app.route('/')
def index():
    music_list = Music.query.all()
    return render_template('index.html', music_list=music_list)

@app.route('/music/new')
def create_music_page():
    return render_template('create.html')

@app.route('/music', methods=['POST'])
def add_music():
    name = request.form['name']
    source = request.form['source']
    numbers = request.form['numbers']
    new_music = Music(name=name, source=source, numbers=numbers)
    db.session.add(new_music)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/music/<int:music_id>')
def music_detail(music_id):
    music = Music.query.get_or_404(music_id)
    return render_template('detail.html', music=music)

@app.route('/music/<int:music_id>/edit')
def edit_music_page(music_id):
    music = Music.query.get_or_404(music_id)
    return render_template('edit.html', music=music)

@app.route('/music/<int:music_id>', methods=['POST'])
def update_music_page(music_id):
    music = Music.query.get_or_404(music_id)
    music.name = request.form['name']
    music.source = request.form['source']
    music.numbers = request.form['numbers']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/music/<int:music_id>/delete', methods=['POST'])
def delete_music_page(music_id):
    music = Music.query.get_or_404(music_id)
    db.session.delete(music)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)