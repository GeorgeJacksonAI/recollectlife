"""
Infrastructure Layer - Clean Architecture

This layer contains implementations of interfaces defined in the application layer.
It handles external concerns: databases, external APIs, file systems, etc.

Structure:
- persistence/: Database repositories (SQLAlchemy implementations)
- services/: External service implementations (AI, Auth)
- mappers/: Entity <-> ORM model mappers
"""
