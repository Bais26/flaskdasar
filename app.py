from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dummy database untuk menyimpan pengguna
users_db = {}

# Route untuk halaman utama
@app.route('/')
def index():
    return 'titit gede'

# Route untuk halaman registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Mengambil data dari form
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validasi sederhana: apakah username sudah digunakan
        if username in users_db:
            flash('Username sudah terdaftar, coba yang lain.')
            return redirect(url_for('register'))
        
        # Simpan pengguna baru di "database" dummy
        users_db[username] = password
        flash('Registrasi berhasil, silakan login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Route untuk halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Mengambil data dari form
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validasi login
        if username in users_db and users_db[username] == password:
            flash(f'Selamat datang, {username}!')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Route untuk profil pengguna
@app.route('/user/<username>')
def profile(username):
    return f'{escape(username)}\'s profile'

# Halaman untuk menampilkan subpath
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'

if __name__ == "__main__":
    app.run(debug=True)
