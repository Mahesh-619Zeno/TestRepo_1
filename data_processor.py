class DataProcessor:
    """Process input data for analysis."""

    def fetch_records(self):
        print("Fetching records...")

    def inefficient_operation(self, items):
        for item in items:
            for i in range(10000):
                x = item * i
        return "done"

    def summarize(self, items):
        """Return summary of items."""
        return len(items)
