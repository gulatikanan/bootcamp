# kanan-hello Architecture

## Component Architecture

\`\`\`mermaid
graph TD
    User[User/Developer]
    CLI[CLI Interface<br>cli.py]
    Main[Core Module<br>main.py]
    Init[Package Initialization<br>__init__.py]
    Rich[Rich Library]
    Typer[Typer Library]
    
    User -->|Uses| CLI
    User -->|Imports| Init
    Init -->|Exports| Main
    CLI -->|Uses| Main
    CLI -->|Uses| Typer
    Main -->|Uses| Rich
    
    classDef core fill:#f9f,stroke:#333,stroke-width:2px;
    classDef external fill:#bbf,stroke:#333,stroke-width:1px;
    classDef user fill:#bfb,stroke:#333,stroke-width:1px;
    
    class Main,Init,CLI core;
    class Rich,Typer external;
    class User user;
\`\`\`

## Data Flow

\`\`\`mermaid
graph LR
    Input[User Input] -->|Name parameter| Process[Process Input]
    Process -->|Format string| Output[Generate Output]
    Output -->|Simple text| Display1[Terminal Output]
    Output -->|Rich formatted| Rich[Rich Formatting]
    Rich -->|Styled text| Display2[Rich Terminal Output]
    
    classDef input fill:#bfb,stroke:#333,stroke-width:1px;
    classDef process fill:#f9f,stroke:#333,stroke-width:2px;
    classDef output fill:#bbf,stroke:#333,stroke-width:1px;
    
    class Input input;
    class Process,Output process;
    class Display1,Display2,Rich output;
\`\`\`

## Package Structure

\`\`\`mermaid
graph TD
    Package[kanan-hello Package]
    Init[__init__.py<br>Exports functions]
    Main[main.py<br>Core functionality]
    CLI[cli.py<br>Command-line interface]
    PyProject[pyproject.toml<br>Package metadata]
    
    Package -->|Contains| Init
    Package -->|Contains| Main
    Package -->|Contains| CLI
    Package -->|Contains| PyProject
    
    classDef package fill:#f96,stroke:#333,stroke-width:2px;
    classDef module fill:#f9f,stroke:#333,stroke-width:1px;
    classDef config fill:#bbf,stroke:#333,stroke-width:1px;
    
    class Package package;
    class Init,Main,CLI module;
    class PyProject config;
\`\`\`