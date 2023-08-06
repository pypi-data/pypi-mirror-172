
from dataclasses import dataclass
from typing import Callable, List, TypeVar
from stack_bot.src.database_base.driver import Driver
from stack_bot.src.database_base.table import Table

from stack_bot.src.database_base.table_row import TableRow

tables: List[Callable[[Driver], Table]] = []

T = TypeVar("T", bound=TableRow)


def table(table_name: str = None):
    def w(cls: T):
        if issubclass(cls, TableRow):
            if not cls.get_columns():
                print(f"Can't create table instance for class {cls.__name__}:\n" 
                    + f"\t{cls.__name__} has no candidates for id column")
            else:
                new_table = lambda driver: Table[cls](
                    driver,
                    table_name if table_name else cls.__name__ + "_table",
                    cls
                )
                tables.append(new_table)
        else:
            print(f"Can't create table instance for class {cls.__name__}:\n"
                + f"\t{cls.__name__} is not subclass of TableRow")
        return cls
    return w
