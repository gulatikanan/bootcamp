from processor import trim, tagger, Counter, archive, formatter, printer

pipeline_config = {
    "start": {
        "processor": trim,
        "routes": {
            "start": ["tagger"]
        }
    },
    "tagger": {
        "processor": tagger,
        "routes": {
            "error": ["error_counter", "archiver"],
            "warn": ["warn_tally"],
            "general": ["general_formatter"]
        }
    },
    "error_counter": {
        "processor": Counter(),
        "routes": {
            "error": ["printer"]
        }
    },
    "archiver": {
        "processor": archive,
        "routes": {
            "error": ["printer"]
        }
    },
    "warn_tally": {
        "processor": Counter(),
        "routes": {
            "warn": ["printer"]
        }
    },
    "general_formatter": {
        "processor": formatter,
        "routes": {
            "general": ["printer"]
        }
    },
    "printer": {
        "processor": printer,
        "routes": {}
    }
}
