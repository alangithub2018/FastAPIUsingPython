from pydantic import BaseModel
from typing import List
from models.Skill import Skill
from models.Experience import Experience
from models.Language import Language

class Developer(BaseModel):
    _id: str
    name: str
    age: int
    country: str
    skills: List[Skill]
    experience: List[Experience]
    languages: List[Language]