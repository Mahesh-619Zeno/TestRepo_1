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
    for sale in sales:
      total += sale['amount']
    print(f"Total Sales: ${total:.2f}")
    by_product = {}
    for sale in sales:
      by_product[sale['product']] = by_product.get(sale['product'], 0) + sale['amount']
    for product in by_product:
        print(f"{product}: ${by_product[product]:.2f}")

if __name__ == "__main__":
    sales_data = read_sales("sales.csv")
    generate_report(sales_data)
    input("Press Enter to exit")