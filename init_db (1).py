import sqlite3

def init_db():
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT NOT NULL,
            year      INTEGER,
            rating    REAL,
            duration  TEXT,
            genre     TEXT,
            director  TEXT,
            desc      TEXT,
            video_url TEXT,
            image_url TEXT
        )
    """)

    movies = [
        (
            "The Shawshank Redemption", 
            1994, 9.3, "142 min", "Drama", "Frank Darabont", 
            "Two imprisoned men bond over years, finding solace and redemption through acts of common decency.", 
            "https://streamimdb.ru/embed/movie/tt0468569", 
            "https://image.tmdb.org/t/p/w500/lyQBXzOQSuE59IsHyhrp0qIiPAz.jpg"
        ),
        (
            "The Godfather", 
            1972, 9.2, "175 min", "Crime", "Francis Ford Coppola", 
            "The aging patriarch of an organized crime dynasty transfers control of his empire to his reluctant son.", 
            None, 
            "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"
        ),
        (
            "The Dark Knight", 
            2008, 9.0, "152 min", "Action", "Christopher Nolan", 
            "Batman must confront one of the greatest psychological tests of his ability to fight injustice.", 
            None, 
            "https://image.tmdb.org/t/p/w500/qJ2tWw7B66Z36gN3ZgGvYm61asv.jpg"
        ),
        (
            "Pulp Fiction", 
            1994, 8.9, "154 min", "Crime", "Quentin Tarantino", 
            "The lives of two mob hitmen, a boxer, and a gangster intertwine in four tales of violence and redemption.", 
            None, 
            "https://image.tmdb.org/t/p/w500/d5iIlbOM0g7w7wOI6N3fsZ9g6s7.jpg"
        ),
        (
            "Interstellar", 
            2014, 8.7, "169 min", "Sci-Fi", "Christopher Nolan", 
            "A team of explorers travel through a wormhole in space to ensure humanity's survival.", 
            None, 
            "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
        ),
        (
            "Inception", 
            2010, 8.8, "148 min", "Sci-Fi", "Christopher Nolan", 
            "A thief plants an idea into a target's mind through dream-sharing technology.", 
            None, 
            "https://image.tmdb.org/t/p/w500/9O7gLzmreU0nGkIB6K3BsJbzvNv.jpg"
        ),
        (
            "Parasite", 
            2019, 8.5, "132 min", "Drama", "Bong Joon-ho", 
            "Greed and class discrimination threaten a symbiotic relationship between two families.", 
            None, 
            "https://image.tmdb.org/t/p/w500/7IiTTvvCHgIdPV87dLNWbK6St3n.jpg"
        ),
        (
            "Knives Out", 
            2019, 7.9, "130 min", "Thriller", "Rian Johnson", 
            "A detective investigates the death of a patriarch of an eccentric, combative family.", 
            None, 
            "https://image.tmdb.org/t/p/w500/p6O4GUB9gDgFo66H3GTYYZs7wEw.jpg"
        ),
        (
            "Whiplash", 
            2014, 8.5, "107 min", "Drama", "Damien Chazelle", 
            "A young drummer is pushed to his limits by a ruthless music conservatory instructor.", 
            None, 
            "https://image.tmdb.org/t/p/w500/lIv1QinFqz4dlp5U4lQ6HaiskOZ.jpg"
        ),
        (
            "The Grand Budapest Hotel", 
            2014, 8.1, "99 min", "Comedy", "Wes Anderson", 
            "The adventures of a legendary concierge and his trusted lobby boy across a fading European empire.", 
            None, 
            "https://image.tmdb.org/t/p/w500/e6v1Y8Iof29m2AunD6vN8gUatK6.jpg"
        ),
        (
            "Get Out", 
            2017, 7.7, "104 min", "Horror", "Jordan Peele", 
            "A Black man visits his white girlfriend's family estate only to discover a disturbing secret.", 
            None, 
            "https://image.tmdb.org/t/p/w500/jgG6Yp9XfA6p996W8XfG7gD2R8M.jpg"
        ),
        (
            "Her", 
            2013, 8.0, "126 min", "Romance", "Spike Jonze", 
            "A lonely writer develops an unlikely relationship with an AI operating system.", 
            None, 
            "https://image.tmdb.org/t/p/w500/ykNuY9g8mGZAyl7n76wZAn67z83.jpg"
        ),
    ]

    c.executemany("""
        INSERT INTO movies (title, year, rating, duration, genre, director, desc, video_url, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, movies)

    conn.commit()
    conn.close()
    print("Database created and seeded: movies.db")

if __name__ == "__main__":
    init_db()