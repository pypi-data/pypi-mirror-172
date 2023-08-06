
from configparser import RawConfigParser
from typing import Callable, Dict, List, Optional, Tuple
from stack_bot.src.database_base.driver import Driver
from stack_bot.src.database_base.table import Table
from stack_bot.src.state_base.state import State

from stack_bot.src.state_base.state_bot import StateBot


class Manager:

    def __init__(self):
        self.bot: Optional[StateBot] = None
        self.bot_table_generators: List[Callable[[Driver], Tuple[type, Table]]] = []
        self.bot_commands: List[Tuple[str, str, State]] = []
        self.tables: Dict[type, Table] = {}


    def add_table(self, generator: Callable[[Driver], Table]):
        self.bot_table_generators.append(generator)
    

    def register_bot(self, properties_file: str):
        self.bot = StateBot(properties_file)

        config = RawConfigParser()
        config.read(properties_file)

        driver = Driver(
            database=config.get("DataBase", "database.database"),
            endpoint=config.get("DataBase", "database.endpoint"),
            oauth=config.get("Utils", "utils.oauth")
        )

        for generator in self.bot_table_generators:
            tp, table = generator(driver)
            self[tp] = table
            table.create_table()
        
        self.bot.set_commands(list(map(lambda x: (x[0], x[1]), self.bot_commands)))
        

        





    


