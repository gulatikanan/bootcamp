from pathlib import Path
from typing import Iterator, Optional, List
from router import StateRouter, RoutingError
from processor_types import TaggedLine

def read_raw(input_path: Path) -> Iterator[TaggedLine]:
    """
    Read lines and tag each as 'start'.
    """
    with input_path.open('r', encoding='utf-8') as f:
        for line in f:
            yield 'start', line.rstrip('\n')


def write_output(
    lines: Iterator[TaggedLine],
    output_path: Optional[Path]
) -> None:
    """
    Collect all 'end' lines and format:
    - INFO (prefixed)
    - Warnings
    - Errors
    """
    infos: List[str] = []
    warns: List[str] = []
    errs: List[str] = []
    for tag, text in lines:
        if tag != 'end':
            continue
        if text.startswith('[INFO]'):
            infos.append(text)
        elif 'WARN' in text:
            warns.append(text)
        elif 'ERROR' in text:
            errs.append(text)
        else:
            infos.append(text)

    out: List[str] = []
    if infos:
        out.append(f"Info:")
        out.extend(f" • {i}" for i in infos)
        out.append('')
    if warns:
        out.append(f"Warnings ({len(warns)}):")
        out += [f" • {w}" for w in warns]
        out.append('')
    if errs:
        out.append(f"Errors ({len(errs)}):")
        out += [f" • {e}" for e in errs]

    text = '\n'.join(out) + '\n'
    if output_path:
        output_path.write_text(text, encoding='utf-8')
    else:
        print(text, end='')


def run(input_path: Path, config_path: Path, output_path: Optional[Path]) -> None:
    """
    Execute the router and write final output.
    """
    try:
        router = StateRouter(config_path)
    except RoutingError as e:
        print(f"Config error: {e}")
        return
    processed = router.run(read_raw(input_path))
    write_output(processed, output_path)

if __name__ == '__main__':
    from cli import app
    app()