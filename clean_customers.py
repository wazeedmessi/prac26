import csv
from pathlib import Path
from statistics import median


def _clean_name(value):
    return (value or "").strip()


def _clean_email(value, customer_id):
    email = (value or "").strip()
    if not email:
        return f"user{customer_id}@example.com"
    return email.replace("#", "@")


def _clean_city(value):
    city = (value or "").strip()
    return city or "Unknown"


def _clean_amount(value, name, amount_by_name):
    if value is None or str(value).strip() == "":
        if name and amount_by_name.get(name):
            return str(int(median(amount_by_name[name])))
        return ""
    cleaned = str(value).strip()
    if cleaned == "":
        if name and amount_by_name.get(name):
            return str(int(median(amount_by_name[name])))
        return ""
    return str(int(float(cleaned)))


def clean_customers(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)

    with input_path.open(newline="") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    amount_by_name = {}
    for row in rows:
        name = _clean_name(row.get("name"))
        if not name:
            continue
        amount = (row.get("amount") or "").strip()
        if amount:
            amount_by_name.setdefault(name, []).append(int(float(amount)))

    cleaned_rows = []
    for row in rows:
        cleaned = {}
        for field in fieldnames:
            value = row.get(field, "")
            if field == "name":
                cleaned[field] = _clean_name(value)
            elif field == "email":
                customer_id = (row.get("customer_id") or "").strip()
                cleaned[field] = _clean_email(value, customer_id)
            elif field == "city":
                cleaned[field] = _clean_city(value)
            elif field == "amount":
                name = _clean_name(row.get("name"))
                cleaned[field] = _clean_amount(value, name, amount_by_name)
            else:
                cleaned[field] = (value or "").strip()
        cleaned_rows.append(cleaned)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    return output_path


if __name__ == "__main__":
    clean_customers("customers.csv", "cleaned_customers.csv")
