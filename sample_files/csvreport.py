import csv

def read_sales(file_path):
    sales = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                row['amount'] = float(row['amount'])
                sales.append(row)
            except (ValueError, TypeError) as e:
                print(f"Warning: Skipping row with invalid amount. Row: {row}, Error: {e}")
                continue
    return sales

def generate_report(sales):
    total = sum(sale['amount'] for sale in sales)
    print(f"Total Sales: ${total:.2f}")

    by_product = {}
    for sale in sales:
        by_product[sale['product']] = by_product.get(sale['product'], 0) + sale['amount']

    for product, amount in by_product.items():
        print(f"{product}: ${amount:.2f}")

if __name__ == "__main__":
    try:
        sales_data = read_sales("sales.csv")
        generate_report(sales_data)
    except FileNotFoundError:
        print("Error: 'sales.csv' not found.")
    input("Press Enter to exit")