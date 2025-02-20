from fastapi import APIRouter, HTTPException
import snowflake.connector

router = APIRouter()

def get_snowflake_connection():
    # Implement the connection logic to Snowflake here (from snowflake_config.py or similar)
    pass

@router.get("/game/comparison/{game_title}/{developer}/{publisher}/{game_release_date}")
def get_game_comparison(game_title: str, developer: str, publisher: str, game_release_date: str):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        query = f"""
        SELECT 
            s.game_id, 
            s.game_title AS steam_game_title, 
            s.steam_link, 
            g.game_title AS gog_game_title, 
            g.gog_link
        FROM steam_games s
        LEFT JOIN gog_games g
        ON s.game_title = g.game_title
        AND s.developer = g.developer
        AND s.publisher = g.publisher
        AND s.game_release_date = g.game_release_date
        
        WHERE s.game_title = '{game_title}'
        AND s.developer = '{developer}'
        AND s.publisher = '{publisher}'
        AND s.game_release_date = '{game_release_date}'
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        if result:
            return {"game_comparison": result[0]}
        else:
            raise HTTPException(status_code=404, detail="Game not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()
