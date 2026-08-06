import csv

def read_sales(file_path):
    sales = []
    csvfile = open(file_path, newline='', encoding='utf-8')
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['amount'] = float(row['amount'])
        sales.append(row)
    return sales

def generate_report(sales):
    total = 0
    for s in sales:
        total += s['amount']
    print(f"Total Sales: ${total:.2f}")
    by_product = {}
    for s in sales:
        by_product[s['product']] = by_product.get(s['product'], 0) + s['amount']
    for product in by_product:
        print(f"{product}: ${by_product[product]:.2f}")

if __name__ == "__main__":
    sales_data = read_sales("sales.csv")
    generate_report(sales_data)
    input("Press Enter to exit")  