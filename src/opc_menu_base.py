from enum import Enum


class OpcionesMenu(Enum):
    def __str__(self) -> str:
        return self.value


# así, si todos los menúes heredan de esta para sus opciones,
# cuando choicer mostrará las opciones como sus valores y
# no `EnumName.MEMBER_NAME`
