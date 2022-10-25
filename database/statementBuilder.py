
class Statement():

    def __init__(self) -> None:
        pass
    

class StatementBuilder():

    def __init__(self) -> None:
        # reset the builder state
        self.__reset__()

    def __reset__(self) -> None:
        self._statement: Statement = Statement()

