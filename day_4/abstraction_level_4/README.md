# Level 3: Dynamic Config-Driven Pipeline

In this level, we fully decouple pipeline logic from code by allowing users to specify their desired line-processing steps via a configuration file.

## 📝 Task

The code in this directory:

- Uses a YAML configuration file to define processing steps
- Dynamically loads processor functions from their import paths
- Builds a pipeline based on the configuration
- Updates the CLI to accept a config file instead of a mode

## 🧩 Key Concepts

- Dynamic function loading
- Configuration-driven behavior
- Decoupling logic from code
- Extensibility through plugins

## 📋 Structure

\`\`\`
abstraction-level-3/
├── main.py
├── cli.py
├── core.py
├── pipeline.py         # now loads pipeline from YAML
├── types.py
├── processors/
│   ├── upper.py
│   └── snake.py
└── pipeline.yaml
\`\`\`

## 🚀 Usage

\`\`\`bash
python main.py --input input.txt --config pipeline.yaml
\`\`\`

## ✅ Checklist

- [ ] CLI accepts a config file
- [ ] Program dynamically imports processor functions from YAML
- [ ] All processors conform to the str -> str interface
- [ ] Import errors are handled cleanly
- [ ] Configuration file uses full dotted import paths

## 🔄 Next Steps

In the next level, we'll move from line-by-line functions to stream-based processors that allow more complex behaviors like fan-in and fan-out.
