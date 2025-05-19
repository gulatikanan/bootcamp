-- Create papers table
CREATE TABLE papers (
    id VARCHAR PRIMARY KEY,
    title TEXT,
    abstract TEXT,
    processed_date TIMESTAMP,
    source VARCHAR,
    status VARCHAR,
    error_message TEXT
);

-- Create figures table
CREATE TABLE figures (
    id VARCHAR PRIMARY KEY,
    paper_id VARCHAR REFERENCES papers(id),
    figure_number INTEGER,
    caption TEXT,
    url VARCHAR
);

-- Create entities table
CREATE TABLE entities (
    id VARCHAR PRIMARY KEY,
    figure_id VARCHAR REFERENCES figures(id),
    entity_text VARCHAR,
    entity_type VARCHAR,
    start_position INTEGER,
    end_position INTEGER,
    external_id VARCHAR
);

-- Create jobs table
CREATE TABLE jobs (
    id VARCHAR PRIMARY KEY,
    job_type VARCHAR,
    status VARCHAR,
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    paper_ids VARCHAR[], -- Array of paper IDs
    total_papers INTEGER,
    processed_papers INTEGER,
    failed_papers INTEGER
);

-- Create indexes for frequently queried columns
CREATE INDEX idx_papers_title ON papers (title);
CREATE INDEX idx_papers_status ON papers (status);
CREATE INDEX idx_figures_paper_id ON figures (paper_id);
CREATE INDEX idx_figures_caption ON figures (caption);
CREATE INDEX idx_entities_figure_id ON entities (figure_id);
CREATE INDEX idx_entities_entity_type ON entities (entity_type);
CREATE INDEX idx_entities_entity_text ON entities (entity_text);
CREATE INDEX idx_jobs_status ON jobs (status);
CREATE INDEX idx_jobs_created_at ON jobs (created_at);