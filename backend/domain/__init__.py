"""
Domain Layer - Clean Architecture

This layer contains the core business logic and entities.
It has NO dependencies on external frameworks, databases, or UI.

Structure:
- entities/: Core business objects (User, Story, Message, Snippet)
- value_objects/: Immutable objects defined by their attributes
- services/: Domain services for complex business logic
- exceptions.py: Domain-specific exceptions
"""
