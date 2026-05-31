from .clear import clear


def pause(action: str = "volver al menú principal"):
    input(f"Presiona Enter para {action}...")


def pause_and_clear(action: str = "volver al menú principal"):
    pause(action)
    clear()
