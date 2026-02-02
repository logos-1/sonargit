from collections import defaultdict

d1 = defaultdict(default_factory=int) # Noncompliant: this creates a dictionary with a single key-value pair.
