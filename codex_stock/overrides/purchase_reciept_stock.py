import frappe

def on_submit_purchase_receipt(doc, method):
    # Define parts and their quantities per item type
    item_parts = {
        "ديك حي": {
            "قنصة": 1,
            "كبدة": 1,
            "هيكل": 1,
            "صدور": 2,
            "وراك": 2,
            "دبوس صدر": 2,
            "جناح": 2,
            "رقبة بجلد و رأس": 1,
            "ريش ناعم": 1,
            "ريش سلاح": 1
        },
        "هيكل": {
            "قطع لحم": 1
        },
        "وراك": {
            "شيش": 1,
            "زلموكه": 1,
            "دبوس ورك": 1
        },
        "صدور": {
            "بانيه": 1
        }
    }

    all_items_to_save = []  # New list to store processed items

    # Loop through each item in the Purchase Receipt
    for item in doc.items:
        if item.item_code in item_parts:  # Check if the item is in our dictionary
            print(f"Processing item: {item.item_code}")

            # Add each part with the appropriate quantity
            for part, qty_per_unit in item_parts[item.item_code].items():
                all_items_to_save.append({
                    "item_code": part,
                    "qty": qty_per_unit * item.qty,  # Calculate total quantity
                    "warehouse": item.warehouse,  # Assign warehouse
                })

    # Replace doc.items with the new list
    doc.items = all_items_to_save

    # Save changes to the database
    doc.save()
