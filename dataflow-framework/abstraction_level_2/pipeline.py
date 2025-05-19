from core import to_uppercase, to_snakecase
from custom_types import ProcessorFn

def build_pipeline(mode: str) -> list[ProcessorFn]:
    if mode == "snakecase":
        return [to_snakecase]
    else:
        return [to_uppercase]
