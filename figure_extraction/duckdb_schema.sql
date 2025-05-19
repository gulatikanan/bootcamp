-- DuckDB Schema for Scientific Publication Data Extraction System
-- Used for analytical queries and data exports

-- Papers dimension table
CREATE TABLE papers (
    paper_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    abstract VARCHAR,
    processed_date TIMESTAMP,
    source VARCHAR,
    status VARCHAR
);

-- Figures dimension table
CREATE TABLE figures (
    figure_id VARCHAR PRIMARY KEY,
    paper_id VARCHAR,
    figure_number INTEGER,
    caption VARCHAR,
    url VARCHAR
);

-- Entities dimension table
CREATE TABLE entities (
    entity_id VARCHAR PRIMARY KEY,
    entity_text VARCHAR,
    entity_type VARCHAR,
    external_id VARCHAR
);

-- Figure-entity fact table
CREATE TABLE figure_entities (
    figure_id VARCHAR,
    entity_id VARCHAR,
    start_position INTEGER,
    end_position INTEGER,
    PRIMARY KEY (figure_id, entity_id, start_position)
);

-- Entity co-occurrence fact table
CREATE TABLE entity_cooccurrences (
    figure_id VARCHAR,
    entity_id1 VARCHAR,
    entity_id2 VARCHAR,
    entity_type1 VARCHAR,
    entity_type2 VARCHAR,
    distance INTEGER,
    PRIMARY KEY (figure_id, entity_id1, entity_id2)
);

-- Paper-entity relationship table
CREATE TABLE paper_entities (
    paper_id VARCHAR,
    entity_id VARCHAR,
    occurrence_count INTEGER,
    PRIMARY KEY (paper_id, entity_id)
);

-- Entity statistics table
CREATE TABLE entity_statistics (
    entity_type VARCHAR PRIMARY KEY,
    entity_count INTEGER,
    figure_count INTEGER,
    paper_count INTEGER,
    top_entities VARCHAR  -- JSON array of top entities
);

-- Create indexes for performance
CREATE INDEX idx_figures_paper_id ON figures (paper_id);
CREATE INDEX idx_figure_entities_entity_id ON figure_entities (entity_id);
CREATE INDEX idx_entities_type ON entities (entity_type);
CREATE INDEX idx_paper_entities_entity_id ON paper_entities (entity_id);