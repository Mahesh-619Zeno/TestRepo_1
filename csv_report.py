import csv
import os

# Load environment variable for sales file, default to 'sales.csv'
SALES_FILE = os.getenv("SALES_FILE", "sales.csv")

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

def generate_report(sales, report_file="report.txt"):
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

    # Optional: remove the CSV file
    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == "__main__":
    file_path = SALES_FILE
    sales_data = read_sales(file_path)
    generate_report(sales_data)
    input("Press Enter to exit...")
