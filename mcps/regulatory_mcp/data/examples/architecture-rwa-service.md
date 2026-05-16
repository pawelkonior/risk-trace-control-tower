# Architecture: RWA Calculation Service

The service ingests exposure files, validates schema and data quality, stores immutable input snapshots, loads approved rule versions from a rule registry, calculates RWA, writes calculation traces, emits audit events, and exports reporting packages with reconciliation evidence.
