#!/usr/bin/env python3
"""
Qdrant Data Inspection Script

This script connects to Qdrant and displays stored vector data.
Usage: python scripts/inspect_qdrant.py
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http.exceptions import UnexpectedResponse
    from qdrant_client.http.models import Distance
except ImportError:
    print("Error: qdrant-client library not installed")
    print("Install with: pip install qdrant-client")
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


def get_qdrant_config() -> Dict[str, str]:
    """Get Qdrant connection configuration from environment"""
    return {
        "url": os.getenv("QDRANT_URL", "http://localhost:6333"),
        "collection_name": os.getenv("QDRANT_COLLECTION_NAME", "rag_collection"),
    }


def format_large_number(num: int) -> str:
    """Format large numbers with thousand separators"""
    return f"{num:,}"


def format_bytes(bytes_size: int) -> str:
    """Format bytes to human-readable format"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def distance_to_string(distance: Distance) -> str:
    """Convert Distance enum to readable string"""
    distance_map = {
        Distance.COSINE: "Cosine",
        Distance.EUCLID: "Euclidean",
        Distance.DOT: "Dot Product",
        Distance.MANHATTAN: "Manhattan",
    }
    return distance_map.get(distance, str(distance))


def connect_to_qdrant(config: Dict[str, str]) -> QdrantClient:
    """
    Connect to Qdrant database

    Args:
        config: Qdrant connection configuration

    Returns:
        QdrantClient instance

    Raises:
        ConnectionError: If Qdrant is not running or not accessible
    """
    client = QdrantClient(
        url=config["url"],
        timeout=10.0,
        prefer_grpc=False,
        https=False,
    )

    # Test connection
    try:
        client.get_collections()
    except Exception as e:
        raise ConnectionError(f"Cannot connect to Qdrant: {e}")

    return client


def get_collection_info(client: QdrantClient, collection_name: str) -> Optional[Dict[str, Any]]:
    """Get detailed information about a collection"""
    try:
        info = client.get_collection(collection_name=collection_name)
        return info
    except UnexpectedResponse:
        return None


def get_sample_points(client: QdrantClient, collection_name: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Get sample points from collection"""
    try:
        # Scroll through collection to get samples
        points, _ = client.scroll(
            collection_name=collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )
        return [{"id": point.id, "payload": point.payload} for point in points]
    except UnexpectedResponse:
        return []


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


def display_collection_details(client: QdrantClient, collection_name: str):
    """Display detailed information about a specific collection"""
    print_section(f"Collection: {collection_name}")

    info = get_collection_info(client, collection_name)
    if not info:
        print(f"\n  [WARNING] Collection '{collection_name}' not found")
        return

    config = info.config
    status = info.status
    points_count = info.points_count
    vectors_count = info.vectors_count

    print("\n  Configuration:")
    print_table_row("  Vector Size", config.params.vectors.size)
    print_table_row("  Distance Metric", distance_to_string(config.params.vectors.distance))
    print_table_row("  On-Disk Payload", config.params.on_disk_payload)

    print("\n  Statistics:")
    print_table_row("  Status", status)
    print_table_row("  Points Count", format_large_number(points_count) if points_count else 0)
    print_table_row("  Vectors Count", format_large_number(vectors_count) if vectors_count else 0)

    if points_count and points_count > 0:
        print_section("Sample Points")
        samples = get_sample_points(client, collection_name, limit=3)

        if samples:
            for i, sample in enumerate(samples, 1):
                print(f"\n  Point {i}:")
                print(f"    ID: {sample['id']}")
                print(f"    Payload:")
                if sample['payload']:
                    for key, value in sample['payload'].items():
                        value_str = str(value)
                        if len(value_str) > 60:
                            value_str = value_str[:60] + "..."
                        print(f"      {key}: {value_str}")
                else:
                    print("      (empty)")
        else:
            print("\n  No sample points available")
    else:
        print("\n  [WARNING] Collection is empty (no points found)")
        print("            Upload documents to populate the vector database")


def display_qdrant_data(config: Dict[str, str]):
    """Display Qdrant data in a formatted way"""
    print("\nQdrant Data Inspection")
    print(f"Connecting to: {config['url']}")

    try:
        client = connect_to_qdrant(config)

        print_section("Qdrant Overview")

        # List all collections
        collections_response = client.get_collections()
        collections = collections_response.collections

        if not collections:
            print("\n  [WARNING] No collections found")
            print("            Upload documents to create collections")
            return

        print_table_row("Total Collections", len(collections))

        print_section("All Collections")
        print(f"\n  {'Collection Name':<40} {'Points':>15}")
        print(f"  {'-' * 40} {'-' * 15}")

        total_points = 0
        for collection in collections:
            info = get_collection_info(client, collection.name)
            points = info.points_count if info and info.points_count else 0
            total_points += points
            print(f"  {collection.name:<40} {format_large_number(points):>15}")

        print(f"  {'-' * 40} {'-' * 15}")
        print(f"  {'Total':<40} {format_large_number(total_points):>15}")

        # Display detailed info for main collection if it exists
        main_collection = config["collection_name"]
        if any(c.name == main_collection for c in collections):
            display_collection_details(client, main_collection)
        elif collections:
            display_collection_details(client, collections[0].name)

        print("\n" + "=" * 60)
        print("[SUCCESS] Inspection completed successfully")
        print("=" * 60 + "\n")

    except ConnectionError as e:
        print(f"\n[ERROR] {str(e)}")
        print("\n[SOLUTION]")
        print("   1. Start Qdrant with Docker:")
        print("      docker-compose up -d qdrant")
        print("   2. Or start all services:")
        print("      ./scripts/start.sh")
        print("   3. Verify Qdrant is running:")
        print("      docker ps | grep qdrant")
        print(f"   4. Check if Qdrant is accessible:")
        print(f"      curl {config['url']}/healthz")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}")
        print(f"        {str(e)}")
        sys.exit(1)


def main():
    """Main entry point"""
    load_environment()
    config = get_qdrant_config()
    display_qdrant_data(config)


if __name__ == "__main__":
    main()
