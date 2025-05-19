#!/usr/bin/env python3
"""
Example script for querying the DuckDB analytics database
Scientific Publication Data Extraction System
"""

import duckdb
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def connect_to_db(db_path):
    """Connect to DuckDB database."""
    return duckdb.connect(db_path)


def get_entity_distribution(conn):
    """Get distribution of entities by type."""
    query = """
    SELECT 
        entity_type, 
        COUNT(*) as count 
    FROM entities 
    GROUP BY entity_type 
    ORDER BY count DESC
    """
    return conn.execute(query).fetchdf()


def get_top_entities_by_type(conn, entity_type, limit=10):
    """Get top entities of a specific type."""
    query = f"""
    SELECT 
        e.entity_text, 
        COUNT(DISTINCT fe.figure_id) as figure_count,
        COUNT(DISTINCT f.paper_id) as paper_count
    FROM entities e
    JOIN figure_entities fe ON e.entity_id = fe.entity_id
    JOIN figures f ON fe.figure_id = f.figure_id
    WHERE e.entity_type = '{entity_type}'
    GROUP BY e.entity_text
    ORDER BY figure_count DESC
    LIMIT {limit}
    """
    return conn.execute(query).fetchdf()


def get_entity_cooccurrences(conn, entity_text, limit=10):
    """Get entities that co-occur with a specific entity."""
    query = f"""
    WITH target_entity AS (
        SELECT entity_id FROM entities WHERE entity_text = '{entity_text}'
    )
    SELECT 
        e2.entity_text, 
        e2.entity_type,
        COUNT(*) as cooccurrence_count,
        AVG(ec.distance) as avg_distance
    FROM entity_cooccurrences ec
    JOIN entities e1 ON ec.entity_id1 = e1.entity_id
    JOIN entities e2 ON ec.entity_id2 = e2.entity_id
    JOIN target_entity te ON e1.entity_id = te.entity_id
    GROUP BY e2.entity_text, e2.entity_type
    ORDER BY cooccurrence_count DESC
    LIMIT {limit}
    """
    return conn.execute(query).fetchdf()


def get_figures_with_entities(conn, entity_types, limit=20):
    """Get figures containing specific entity types."""
    entity_types_str = "', '".join(entity_types)
    query = f"""
    SELECT 
        f.figure_id,
        f.paper_id,
        p.title as paper_title,
        f.figure_number,
        f.caption,
        COUNT(DISTINCT fe.entity_id) as entity_count,
        GROUP_CONCAT(DISTINCT e.entity_text) as entities
    FROM figures f
    JOIN figure_entities fe ON f.figure_id = fe.figure_id
    JOIN entities e ON fe.entity_id = e.entity_id
    JOIN papers p ON f.paper_id = p.paper_id
    WHERE e.entity_type IN ('{entity_types_str}')
    GROUP BY f.figure_id, f.paper_id, p.title, f.figure_number, f.caption
    HAVING COUNT(DISTINCT e.entity_type) = {len(entity_types)}
    ORDER BY entity_count DESC
    LIMIT {limit}
    """
    return conn.execute(query).fetchdf()


def get_entity_statistics(conn):
    """Get statistics for all entity types."""
    return conn.execute("SELECT * FROM entity_statistics").fetchdf()


def plot_entity_distribution(df):
    """Plot distribution of entities by type."""
    plt.figure(figsize=(10, 6))
    plt.bar(df['entity_type'], df['count'])
    plt.xlabel('Entity Type')
    plt.ylabel('Count')
    plt.title('Distribution of Entities by Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('entity_distribution.png')
    plt.close()


def export_figures_with_entities_to_json(df, output_file):
    """Export figures with entities to JSON file."""
    result = df.to_dict(orient='records')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)


def export_figures_with_entities_to_csv(df, output_file):
    """Export figures with entities to CSV file."""
    df.to_csv(output_file, index=False)


def main():
    """Main function."""
    # Connect to database
    db_path = "tests/mocks/analytics.duckdb"
    conn = connect_to_db(db_path)
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Get entity distribution
    entity_distribution = get_entity_distribution(conn)
    print("Entity Distribution:")
    print(entity_distribution)
    plot_entity_distribution(entity_distribution)
    
    # Get top genes
    top_genes = get_top_entities_by_type(conn, "Gene", limit=5)
    print("\nTop Genes:")
    print(top_genes)
    
    # Get co-occurrences with GATA4
    gata4_cooccurrences = get_entity_cooccurrences(conn, "GATA4", limit=5)
    print("\nEntities co-occurring with GATA4:")
    print(gata4_cooccurrences)
    
    # Get figures with both Gene and Disease entities
    figures_with_gene_disease = get_figures_with_entities(conn, ["Gene", "Disease"], limit=10)
    print("\nFigures with both Gene and Disease entities:")
    print(figures_with_gene_disease)
    
    # Export results
    export_figures_with_entities_to_json(figures_with_gene_disease, output_dir / "figures_with_entities.json")
    export_figures_with_entities_to_csv(figures_with_gene_disease, output_dir / "figures_with_entities.csv")
    
    # Get entity statistics
    entity_stats = get_entity_statistics(conn)
    print("\nEntity Statistics:")
    print(entity_stats)
    
    # Export entity statistics
    with open(output_dir / "entity_statistics.json", 'w') as f:
        json.dump(entity_stats.to_dict(orient='records'), f, indent=2)
    
    # Close connection
    conn.close()
    
    print(f"\nResults exported to {output_dir}")


if __name__ == "__main__":
    main()