import csv
import os

# Load environment variables
SALES_FILE = os.getenv("SALES_FILE", "sales.csv")
REPORT_FILE = os.getenv("REPORT_FILE", "report.txt")  # new env var for report output file
DELETE_SALES_FILE = os.getenv("DELETE_SALES_FILE", "True").lower() in ("true", "1", "yes")  # optional

def read_sales(file_path):
    sales = []
    # Create file with sample data if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding='utf-8') as f:
            f.write("product,amount\nSample,10.5\n")
    # Read CSV
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['amount'] = float(row['amount'])
            sales.append(row)
    return sales

def generate_report(sales, report_file):
    total = sum(s['amount'] for s in sales)
    print(f"Total Sales: ${total}")

    by_product = {}
    for s in sales:
        by_product[s['product']] = by_product.get(s['product'], 0) + s['amount']

    for product, amount in by_product.items():
        print(f"{product}: ${amount}")

    # Write report to file
    with open(report_file, "w", encoding='utf-8') as f:
        for product, amount in by_product.items():
            f.write(f"{product}: {amount}\n")
        f.write(f"Total Sales: {total}\n")

    # Optional: remove the sales file
    if DELETE_SALES_FILE and os.path.exists(SALES_FILE):
        os.remove(SALES_FILE)
        print(f"Deleted {SALES_FILE}")

if __name__ == "__main__":
    sales_data = read_sales(SALES_FILE)
    generate_report(sales_data, REPORT_FILE)
    input("Press Enter to exit...")
