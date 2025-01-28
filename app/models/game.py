from pydantic import BaseModel

class Game(BaseModel):
    name: str
    on_steam: bool
    on_gog: bool
