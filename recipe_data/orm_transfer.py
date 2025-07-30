from typing import List, Optional
from sqlalchemy import create_engine, MetaData, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///C:/Users/neilm/.vscode/BGE_app/instance/eggs.db")

class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipe_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(24))
    temps: Mapped[str] = mapped_column(String(24))
    entree: Mapped[str] = mapped_column(String(8))
    cook_method: Mapped[str] = mapped_column(String(8))
    source: Mapped[str] = mapped_column(String(120))
    meats: Mapped[Optional[str]]

    
    def __repr__(self) -> str:
        return f"Recipe(id={self.id!r}, name={self.name!r})"



Base.metadata.create_all(engine)

session = Session(engine)

def main():
    dishes = []
    with open("recipe_data/recipes.txt") as file:
        for line in file:
            new_row = []
            row = line.rstrip().split("|")
            for part in row:
                new_row.append(part.strip())
            dishes.append(new_row)
    for dish in dishes:
        new = Recipe(name=dish[0], temps=dish[1], entree=dish[2], cook_method=dish[3], source=dish[4])
        session.add(new)
        session.commit()
    session.close()





if __name__ == "__main__":
    main()
