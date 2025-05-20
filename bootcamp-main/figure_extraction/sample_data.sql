-- Insert sample paper
INSERT INTO papers (id, title, abstract, processed_date, source, status, error_message)
VALUES (
    'PMC6267067',
    'Genetic and epigenetic regulation of human cardiac reprogramming and differentiation in regenerative medicine',
    'Heart disease is the leading cause of death worldwide. The adult human heart has limited regenerative capacity after injury. Cardiac regenerative medicine aims to restore cardiac function by replacing or repairing damaged heart tissue. Advances in stem cell biology and cellular reprogramming have provided new opportunities for cardiac regeneration. This review summarizes recent progress in the genetic and epigenetic regulation of human cardiac reprogramming and differentiation, and discusses the challenges and opportunities for clinical applications in cardiac regenerative medicine.',
    '2023-05-19 14:30:45',
    'PMC',
    'completed',
    NULL
);

-- Insert sample figures
INSERT INTO figures (id, paper_id, figure_number, caption, url)
VALUES (
    'fig_12345',
    'PMC6267067',
    1,
    'Figure 1. Approaches for cardiac regeneration. (A) Cardiac regeneration can be achieved through various approaches, including direct reprogramming of fibroblasts to cardiomyocytes, differentiation of pluripotent stem cells, and activation of endogenous cardiac progenitor cells. (B) Key transcription factors involved in cardiac reprogramming include GATA4, MEF2C, TBX5, and HAND2. These factors work together to activate cardiac gene expression programs while suppressing fibroblast gene signatures.',
    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6267067/bin/fig-1.jpg'
);

INSERT INTO figures (id, paper_id, figure_number, caption, url)
VALUES (
    'fig_12346',
    'PMC6267067',
    2,
    'Figure 2. Cardiac differentiation of human pluripotent stem cells. (A) Schematic representation of cardiac differentiation protocol. Human pluripotent stem cells are sequentially treated with activators and inhibitors of Wnt signaling to induce cardiac mesoderm and subsequent cardiomyocyte differentiation. (B) Immunostaining of cardiac markers TNNT2 (green) and NKX2-5 (red) in differentiated cardiomyocytes. Nuclei are stained with DAPI (blue). Scale bar: 100 μm. (C) Gene expression analysis during cardiac differentiation showing upregulation of cardiac genes (NKX2-5, TNNT2) and downregulation of pluripotency genes (OCT4, NANOG).',
    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6267067/bin/fig-2.jpg'
);

INSERT INTO figures (id, paper_id, figure_number, caption, url)
VALUES (
    'fig_12347',
    'PMC6267067',
    3,
    'Figure 3. Epigenetic regulation of cardiac reprogramming. (A) Heatmap showing changes in histone modifications (H3K4me3, H3K27me3, H3K27ac) at cardiac gene promoters during fibroblast to cardiomyocyte reprogramming. (B) DNA methylation levels at cardiac gene promoters decrease during reprogramming, correlating with increased gene expression. (C) Treatment with the histone deacetylase inhibitor valproic acid (VPA) enhances cardiac reprogramming efficiency by promoting an open chromatin state at cardiac gene loci. (D) The DNA methyltransferase inhibitor 5-azacytidine (5-aza) facilitates cardiac reprogramming by reducing DNA methylation at cardiac gene promoters.',
    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6267067/bin/fig-3.jpg'
);

-- Insert sample entities for Figure 2
INSERT INTO entities (id, figure_id, entity_text, entity_type, start_position, end_position, external_id)
VALUES 
    ('ent_67890', 'fig_12346', 'Cardiac', 'Disease', 8, 15, 'D002311'),
    ('ent_67891', 'fig_12346', 'human', 'Species', 31, 36, '9606'),
    ('ent_67892', 'fig_12346', 'pluripotent stem cells', 'CellLine', 37, 60, 'CL:0002248'),
    ('ent_67893', 'fig_12346', 'Wnt', 'Gene', 211, 214, '7471'),
    ('ent_67894', 'fig_12346', 'cardiac', 'Disease', 237, 244, 'D002311'),
    ('ent_67895', 'fig_12346', 'cardiomyocyte', 'CellLine', 268, 281, 'CL:0000746'),
    ('ent_67896', 'fig_12346', 'TNNT2', 'Gene', 329, 334, '7139'),
    ('ent_67897', 'fig_12346', 'NKX2-5', 'Gene', 348, 354, '1482'),
    ('ent_67898', 'fig_12346', 'cardiomyocytes', 'CellLine', 375, 388, 'CL:0000746'),
    ('ent_67899', 'fig_12346', 'DAPI', 'Chemical', 411, 415, 'C048423'),
    ('ent_67900', 'fig_12346', 'OCT4', 'Gene', 576, 580, '5460'),
    ('ent_67901', 'fig_12346', 'NANOG', 'Gene', 582, 587, '79923');

-- Insert sample job
INSERT INTO jobs (id, job_type, status, created_at, completed_at, paper_ids, total_papers, processed_papers, failed_papers)
VALUES (
    'job_54321',
    'paper_processing',
    'completed',
    '2023-05-19 14:25:30',
    '2023-05-19 14:30:45',
    ARRAY['PMC6267067'],
    1,
    1,
    0
);