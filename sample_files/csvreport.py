import csv
from pathlib import Path
import argparse
from collections import defaultdict


def ensure_sample_file(file_path: Path):
    """Create a sample CSV if it doesn't exist."""
    if not file_path.exists():
        file_path.write_text("product,amount\nSample,10.5\n", encoding="utf-8")


def read_sales(file_path: Path) -> list[dict]:
    """Read sales data from a CSV file and return a list of dicts."""
    ensure_sample_file(file_path)

    sales = []
    with file_path.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                row["amount"] = float(row["amount"])
                sales.append(row)
            except (ValueError, KeyError):
                print(f"Skipping invalid row: {row}")
    return sales


def generate_report(sales: list[dict], report_file: Path, as_csv: bool = False):
    """Generate a sales report, optionally in CSV format."""
    total_sales = sum(s["amount"] for s in sales)

    by_product = defaultdict(float)
    for s in sales:
        by_product[s["product"]] += s["amount"]

    # Print to console
    print(f"\nSales Report")
    print(f"============")
    for product, amount in by_product.items():
        print(f"{product}: ${amount:.2f}")
    print(f"Total Sales: ${total_sales:.2f}\n")

    # Write to report file
    if as_csv:
        with report_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Product", "Amount"])
            for product, amount in by_product.items():
                writer.writerow([product, amount])
            writer.writerow(["Total Sales", total_sales])
    else:
        with report_file.open("w", encoding="utf-8") as f:
            for product, amount in by_product.items():
                f.write(f"{product}: {amount}\n")
            f.write(f"Total Sales: {total_sales}\n")


def main():
    parser = argparse.ArgumentParser(description="Sales report generator.")
    parser.add_argument("--file", type=Path, default=Path("sales.csv"), help="Path to sales CSV")
    parser.add_argument("--report", type=Path, default=Path("report.txt"), help="Path to report file")
    parser.add_argument("--csv", action="store_true", help="Output report as CSV")
    parser.add_argument("--delete-source", action="store_true", help="Delete source CSV after processing")
    args = parser.parse_args()

    sales_data = read_sales(args.file)
    generate_report(sales_data, args.report, args.csv)

    if args.delete_source and args.file.exists():
        args.file.unlink()
        print(f"Deleted source file: {args.file}")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
