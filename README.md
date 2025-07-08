# Key Architecture Elements:

🏛️ **Domain Layer** (Business Logic)

- Pure Python objects
- No external dependencies
- Core business rules

🔌 **Ports Layer** (Interfaces)

- Abstract base classes or protocols
- Define contracts between layers
- Technology-agnostic

🎯 **Services Layer** (Use Cases)

- Application logic
- Orchestrates domain objects
- Uses ports, not adapters directly

🔧 **Adapters Layer** (External Integrations)

- Implement port interfaces
- Handle external dependencies (aiohttp, Streamlit)
- Contain all I/O operations