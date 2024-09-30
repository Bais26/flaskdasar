from flask import Flask, render_template, request, redirect, url_for,jsonify
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# Buat class Base
class Base(DeclarativeBase):
    pass

# Buat aplikasi Flask
app = Flask(__name__)

# Konfigurasi MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1/myflask"


# Inisialisasi database
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True  )

@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    # Membuat daftar pengguna dalam format JSON
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,  # Ganti ';' dengan ':'
    } for user in users])

@app.route('/')
def index():
    return 'Lu semua ngentot'

# @app.route("/users")
# def user_list():
#     users = db.session.execute(db.select(User).order_by(User.username)).scalars()
#     return render_template("user/list.html", users=users)


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)

# # Dummy database untuk menyimpan pengguna
# users_db = {}

# # Route untuk halaman utama
# @app.route('/')
# def index():
#     return 'titit gede'

# # Route untuk halaman registrasi
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Mengambil data dari form
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         # Validasi sederhana: apakah username sudah digunakan
#         if username in users_db:
#             flash('Username sudah terdaftar, coba yang lain.')
#             return redirect(url_for('register'))
        
#         # Simpan pengguna baru di "database" dummy
#         users_db[username] = password
#         flash('Registrasi berhasil, silakan login.')
#         return redirect(url_for('login'))
    
#     return render_template('register.html')

# # Route untuk halaman login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Mengambil data dari form
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         # Validasi login
#         if username in users_db and users_db[username] == password:
#             flash(f'Selamat datang, {username}!')
#             return redirect(url_for('index'))
#         else:
#             flash('Username atau password salah!')
#             return redirect(url_for('login'))
    
#     return render_template('login.html')

# # Route untuk profil pengguna
# @app.route('/user/<username>')
# def profile(username):
#     return f'{escape(username)}\'s profile'

# # Halaman untuk menampilkan subpath
# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     return f'Subpath {escape(subpath)}'

# if __name__ == "__main__":
#     app.run(debug=True)
