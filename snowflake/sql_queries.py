def create_games_table():
    return """
    CREATE TABLE IF NOT EXISTS games (
        game_id INT PRIMARY KEY,
        game_name STRING,
        platform STRING,
        price FLOAT,
        release_date DATE
    );
    """
