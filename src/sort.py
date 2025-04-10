from enum import Enum
from fastapi import HTTPException, Query, status


class Order(str, Enum):
    """
    Enum для указания порядка сортировки.

    Этот класс перечисляет доступные значения для указания порядка сортировки:
    по возрастанию или по убыванию.

    Возможные значения:
    - **asc**: Сортировка по возрастанию.
    - **desc**: Сортировка по убыванию.
    """

    asc = "asc"
    desc = "desc"

    def __str__(self):
        """
        Преобразует объект Order в строку.

        :return: str: Строковое представление значения порядка сортировки.
        """
        return f"{self.value}"

    def __repr__(self):
        """
        Возвращает строковое представление объекта Order.

        :return: str: Строка, представляющая объект.
        """
        return repr(self.value)


class SortField:
    """
    Класс для представления поля сортировки.

    Этот класс используется для хранения псевдонима (alias) поля,
    по которому будет производиться сортировка.

    :param str alias: Псевдоним для поля сортировки.
    """

    def __init__(self, alias: str) -> None:
        """
        Инициализирует псевдоним для поля сортировки.

        :param str alias: Псевдоним поля для сортировки.
        """
        self.alias = alias


class SimpleSort:
    """
    Класс для обработки параметров сортировки.

    Этот класс позволяет установить поле для сортировки и порядок сортировки
    (по возрастанию или по убыванию). Проверяет, что переданное поле для
    сортировки разрешено, и задаёт порядок сортировки.

    :param str sort_field: Поле для сортировки. По умолчанию None.
    :param Order sort_order: Порядок сортировки (asc или desc).
    По умолчанию **asc**.
    :raises HTTPException: Если сортировка по переданному полю не разрешена.
    """

    SORT_FIELDS = {}

    def __init__(
        self,
        sort_field: str = Query(default=None),
        sort_order: Order = Query(default=Order.asc),
    ) -> None:
        """
        Инициализирует параметры сортировки.

        :param str sort_field: Имя поля для сортировки. Если передано,
        проверяется, разрешено ли сортировать по этому полю.
        :param Order sort_order: Порядок сортировки. Может быть 'asc'
        (по возрастанию) или 'desc' (по убыванию). По умолчанию **asc**.
        :raises HTTPException: Если переданное поле для сортировки не
        разрешено, выбрасывается исключение с кодом 422.
        """
        if sort_field:
            sort_class = self.SORT_FIELDS.get(sort_field)
            if not sort_class:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    f"Sort by field '{sort_field}' is not allowed.",
                )
            self.field = sort_class.alias
            self.order = sort_order
        else:
            self.field = None
            self.order = None
