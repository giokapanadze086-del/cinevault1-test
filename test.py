import sqlite3
import re
from flask import Flask, render_template, request, redirect, url_for, g


def get_embed_url(url):
    """Convert any video URL to an embeddable URL."""
    if not url:
        return None

    # YouTube: youtube.com/watch?v=ID  or  youtu.be/ID  or  youtube.com/shorts/ID
    yt = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})", url)
    if yt:
        return f"https://www.youtube.com/embed/{yt.group(1)}"

    # Vimeo: vimeo.com/ID
    vm = re.search(r"vimeo\.com/(\d+)", url)
    if vm:
        return f"https://player.vimeo.com/video/{vm.group(1)}"

    # Dailymotion: dailymotion.com/video/ID
    dm = re.search(r"dailymotion\.com/video/([a-zA-Z0-9]+)", url)
    if dm:
        return f"https://www.dailymotion.com/embed/video/{dm.group(1)}"

    # Direct .mp4 / .webm / .ogg — handled by <video> tag
    if re.search(r"\.(mp4|webm|ogg)(\?.*)?$", url, re.IGNORECASE):
        return url

    # Unknown link — pass through as-is
    return url


app = Flask(__name__)
DB = "movies.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


# ── LIST / FILTER ────────────────────────────────────────────────
@app.route("/")
def index():
    db = get_db()
    genre = request.args.get("genre", "All")
    search = request.args.get("q", "").strip()

    query = "SELECT * FROM movies WHERE 1=1"
    params = []

    if genre != "All":
        query += " AND genre = ?"
        params.append(genre)
    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    query += " ORDER BY rating DESC"
    movies = db.execute(query, params).fetchall()
    genres = [r[0] for r in db.execute("SELECT DISTINCT genre FROM movies ORDER BY genre").fetchall()]

    return render_template("index.html", movies=movies, genres=genres,
                           current_genre=genre, search=search)


# ── WATCH ────────────────────────────────────────────────────────
@app.route("/watch/<int:movie_id>")
def watch(movie_id):
    db = get_db()
    movie = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if not movie:
        return "Movie not found", 404
    if not movie["video_url"]:
        return "No video URL set for this movie.", 400
    embed_url = get_embed_url(movie["video_url"])
    is_direct = bool(re.search(r"\.(mp4|webm|ogg)(\?.*)?$", movie["video_url"], re.IGNORECASE))
    return render_template("player.html", movie=movie, embed_url=embed_url, is_direct=is_direct)


# ── DETAIL ───────────────────────────────────────────────────────
@app.route("/movie/<int:movie_id>")
def detail(movie_id):
    db = get_db()
    movie = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if not movie:
        return "Movie not found", 404
    return render_template("detail.html", movie=movie)


# ── ADD ──────────────────────────────────────────────────────────
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO movies (title, year, rating, duration, genre, director, desc, video_url) VALUES (?,?,?,?,?,?,?,?)",
            (
                request.form["title"],
                request.form["year"] or None,
                request.form["rating"] or None,
                request.form["duration"],
                request.form["genre"],
                request.form["director"],
                request.form["desc"],
                request.form["video_url"] or None,
            ),
        )
        db.commit()
        return redirect(url_for("index"))
    return render_template("add.html")


# ── EDIT ─────────────────────────────────────────────────────────
# ── EDIT ─────────────────────────────────────────────────────────
@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    db = get_db()
    movie = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if not movie:
        return "Movie not found", 404
    if request.method == "POST":
        db.execute(
            "UPDATE movies SET title=?, year=?, rating=?, duration=?, genre=?, director=?, desc=?, video_url=?, image_url=? WHERE id=?",
            (
                request.form["title"],
                request.form["year"] or None,
                request.form["rating"] or None,
                request.form["duration"],
                request.form["genre"],
                request.form["director"],
                request.form["desc"],
                request.form["video_url"] or None,
                request.form["image_url"] or None,
                movie_id,
            ),
        )
        db.commit()
        return redirect(url_for("detail", movie_id=movie_id))
    return render_template("edit.html", movie=movie)


# ── CONFIRM DELETE ───────────────────────────────────────────────
@app.route("/confirm-delete/<int:movie_id>")
def confirm_delete(movie_id):
    db = get_db()
    movie = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if not movie:
        return "Movie not found", 404
    return render_template("confirm_delete.html", movie=movie)


# ── DELETE ───────────────────────────────────────────────────────
@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete(movie_id):
    db = get_db()
    db.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)