#!/usr/bin/env python3
"""
Neo4j Data Inspection Script

This script connects to Neo4j and displays stored knowledge graph data.
Usage: python scripts/inspect_neo4j.py
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from neo4j import GraphDatabase
    from neo4j.exceptions import ServiceUnavailable, AuthError
except ImportError:
    print("Error: neo4j library not installed")
    print("Install with: pip install neo4j")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Warning: python-dotenv not installed, using environment variables only")
    load_dotenv = None


def load_environment():
    """Load environment variables from .env file"""
    if load_dotenv:
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)


def get_neo4j_config() -> Dict[str, str]:
    """Get Neo4j connection configuration from environment"""
    return {
        "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.getenv("NEO4J_USER", "neo4j"),
        "password": os.getenv("NEO4J_PASSWORD", "rag123456"),
        "database": os.getenv("NEO4J_DATABASE", "neo4j"),
    }


def format_large_number(num: int) -> str:
    """Format large numbers with thousand separators"""
    return f"{num:,}"


def connect_to_neo4j(config: Dict[str, str]):
    """
    Connect to Neo4j database

    Args:
        config: Neo4j connection configuration

    Returns:
        Neo4j driver instance

    Raises:
        ServiceUnavailable: If Neo4j is not running
        AuthError: If authentication fails
    """
    driver = GraphDatabase.driver(
        config["uri"],
        auth=(config["user"], config["password"])
    )

    # Test connection
    with driver.session(database=config["database"]) as session:
        session.run("RETURN 1").single()

    return driver


def get_node_statistics(driver, database: str) -> List[Dict[str, Any]]:
    """Get node count by label"""
    query = """
    MATCH (n)
    RETURN labels(n) as labels, count(*) as count
    ORDER BY count DESC
    """

    with driver.session(database=database) as session:
        result = session.run(query)
        stats = []
        for record in result:
            labels = record["labels"]
            count = record["count"]
            # Handle nodes with multiple labels
            label_str = ":".join(labels) if labels else "(no label)"
            stats.append({"label": label_str, "count": count})
        return stats


def get_relationship_statistics(driver, database: str) -> List[Dict[str, Any]]:
    """Get relationship count by type"""
    query = """
    MATCH ()-[r]->()
    RETURN type(r) as type, count(*) as count
    ORDER BY count DESC
    """

    with driver.session(database=database) as session:
        result = session.run(query)
        return [{"type": record["type"], "count": record["count"]}
                for record in result]


def get_sample_entities(driver, database: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Get sample entities with properties"""
    query = """
    MATCH (n)
    WHERE labels(n) <> []
    RETURN labels(n) as labels, properties(n) as properties
    LIMIT $limit
    """

    with driver.session(database=database) as session:
        result = session.run(query, limit=limit)
        samples = []
        for record in result:
            labels = record["labels"]
            properties = record["properties"]
            samples.append({
                "labels": labels,
                "properties": properties
            })
        return samples


def get_database_info(driver, database: str) -> Dict[str, Any]:
    """Get overall database information"""
    queries = {
        "total_nodes": "MATCH (n) RETURN count(n) as count",
        "total_relationships": "MATCH ()-[r]->() RETURN count(r) as count",
        "node_labels": "CALL db.labels() YIELD label RETURN collect(label) as labels",
        "relationship_types": "CALL db.relationshipTypes() YIELD relationshipType RETURN collect(relationshipType) as types",
    }

    info = {}
    with driver.session(database=database) as session:
        for key, query in queries.items():
            result = session.run(query).single()
            if key == "total_nodes" or key == "total_relationships":
                info[key] = result["count"]
            elif key == "node_labels":
                info[key] = result["labels"]
            elif key == "relationship_types":
                info[key] = result["types"]

    return info


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_table_row(label: str, value: Any, width: int = 50):
    """Print a formatted table row"""
    label_width = 30
    value_width = width - label_width - 3
    print(f"  {label:<{label_width}} : {str(value):<{value_width}}")


def display_neo4j_data(config: Dict[str, str]):
    """Display Neo4j data in a formatted way"""
    print("\nNeo4j Data Inspection")
    print(f"Connecting to: {config['uri']}")
    print(f"Database: {config['database']}")

    try:
        driver = connect_to_neo4j(config)

        print_section("Database Overview")
        info = get_database_info(driver, config["database"])
        print_table_row("Total Nodes", format_large_number(info["total_nodes"]))
        print_table_row("Total Relationships", format_large_number(info["total_relationships"]))
        print_table_row("Node Labels", len(info["node_labels"]))
        print_table_row("Relationship Types", len(info["relationship_types"]))

        if info["total_nodes"] == 0:
            print("\n[WARNING] Database is empty (no nodes found)")
            print("          Upload documents to populate the knowledge graph")
            driver.close()
            return

        print_section("Node Statistics by Label")
        node_stats = get_node_statistics(driver, config["database"])
        if node_stats:
            print(f"\n  {'Label':<40} {'Count':>15}")
            print(f"  {'-' * 40} {'-' * 15}")
            for stat in node_stats:
                print(f"  {stat['label']:<40} {format_large_number(stat['count']):>15}")
        else:
            print("\n  No nodes found")

        print_section("Relationship Statistics by Type")
        rel_stats = get_relationship_statistics(driver, config["database"])
        if rel_stats:
            print(f"\n  {'Type':<40} {'Count':>15}")
            print(f"  {'-' * 40} {'-' * 15}")
            for stat in rel_stats:
                print(f"  {stat['type']:<40} {format_large_number(stat['count']):>15}")
        else:
            print("\n  No relationships found")

        print_section("Sample Entities")
        samples = get_sample_entities(driver, config["database"], limit=3)
        if samples:
            for i, sample in enumerate(samples, 1):
                print(f"\n  Entity {i}:")
                print(f"    Labels: {', '.join(sample['labels'])}")
                print(f"    Properties:")
                for key, value in sample['properties'].items():
                    value_str = str(value)
                    if len(value_str) > 60:
                        value_str = value_str[:60] + "..."
                    print(f"      {key}: {value_str}")
        else:
            print("\n  No entities found")

        driver.close()
        print("\n" + "=" * 60)
        print("[SUCCESS] Inspection completed successfully")
        print("=" * 60 + "\n")

    except ServiceUnavailable as e:
        print(f"\n[ERROR] Cannot connect to Neo4j at {config['uri']}")
        print(f"        {str(e)}")
        print("\n[SOLUTION]")
        print("   1. Start Neo4j with Docker:")
        print("      docker-compose up -d neo4j")
        print("   2. Or start all services:")
        print("      ./scripts/start.sh")
        print("   3. Verify Neo4j is running:")
        print("      docker ps | grep neo4j")
        sys.exit(1)

    except AuthError as e:
        print(f"\n[ERROR] Authentication failed")
        print(f"        {str(e)}")
        print("\n[SOLUTION]")
        print(f"   Check NEO4J_USER and NEO4J_PASSWORD in .env file")
        print(f"   Current user: {config['user']}")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}")
        print(f"        {str(e)}")
        sys.exit(1)


def main():
    """Main entry point"""
    load_environment()
    config = get_neo4j_config()
    display_neo4j_data(config)


if __name__ == "__main__":
    main()
