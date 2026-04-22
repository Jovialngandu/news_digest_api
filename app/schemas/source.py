from pydantic import BaseModel

class SourceSchema(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        from_attributes = True