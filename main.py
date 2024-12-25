from typing import Annotated, Sequence, Type

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, SQLModel, create_engine, select

from models import TermUpdate, TermPublic, TermCreate, Term

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_model=list[str], description="Получение списка всех терминов")
@app.get('/terms', response_model=list[str], description="Получение списка всех терминов")
def read_terms(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[str]:
    terms = session.exec(select(Term.title).offset(offset).limit(limit)).all()
    return terms


@app.post("/terms", response_model=TermPublic, description="Добавление нового термина с описанием")
def create_term(term: TermCreate, session: SessionDep) -> TermPublic:
    db_term = session.exec(select(Term).where(Term.title == term.title)).first()
    if db_term:
        raise HTTPException(status_code=400, detail="Term already exists")
    db_term = Term.model_validate(term)
    session.add(db_term)
    session.commit()
    session.refresh(db_term)
    return db_term


@app.get("/terms/{term_keyword}", response_model=TermPublic,
         description="Получение информации о конкретном термине по ключевому слову")
def read_term_by_keyword(term_keyword: str, session: SessionDep) -> Term:
    term = session.exec(select(Term).where(Term.title == term_keyword)).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term


@app.patch("/terms/{term_id}", response_model=TermPublic, description="Обновление существующего термина")
def update_term(term_id: int, term: TermUpdate, session: SessionDep) -> Type[Term]:
    term_db = session.get(Term, term_id)
    if not term_db:
        raise HTTPException(status_code=404, detail="Term not found")
    term_data = term.model_dump(exclude_unset=True)
    term_db.sqlmodel_update(term_data)
    session.add(term_db)
    session.commit()
    session.refresh(term_db)
    return term_db


@app.delete("/terms/{term_id}", description="Удаление термина из глоссария")
def delete_term(term_id: int, session: SessionDep):
    term = session.get(Term, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    session.delete(term)
    session.commit()
    return {"ok": True}
