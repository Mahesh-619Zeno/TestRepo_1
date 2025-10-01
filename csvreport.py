import csv

def read_sales(file_path):
    sales = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['amount'] = float(row['amount'])
            sales.append(row)
    return sales

def generate_report(sales):
    total = sum(s['amount'] for s in sales)
    print(f"Total Sales: ${total:.2f}")
    by_product = {}
    for s in sales:
        by_product[s['product']] = by_product.get(s['product'], 0) + s['amount']
    for product, amount in by_product.items():
        print(f"{product}: ${amount:.2f}")

if __name__ == "__main__":
    sales_data = read_sales("sales.csv")
    generate_report(sales_data)
