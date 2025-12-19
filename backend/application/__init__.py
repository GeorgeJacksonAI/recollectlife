"""
Application Layer - Clean Architecture

This layer contains use cases (application business rules) and interfaces.
It orchestrates domain entities and depends only on the domain layer.

Structure:
- interfaces/: Abstract interfaces (repositories, services)
- use_cases/: Application-specific business rules
- dto/: Data Transfer Objects for input/output
"""
