from sqlmodel import Field, SQLModel


# SQLModel по-факту является Pydantic model https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-hero
class TermBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = Field(default=None, index=True)


class TermCreate(TermBase):
    pass


class Term(TermBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TermPublic(TermBase):
    id: int


class TermUpdate(TermBase):
    title: str | None = None
    description: str | None = None
