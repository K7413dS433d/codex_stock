
import frappe


def remove_stock_entry_for_item(doc, item_code):
    stock_entries = frappe.get_all(
        "Stock Entry",
        filters={"reference_name": doc.name},  # Find Stock Entries linked to this Purchase Receipt
        pluck="name",
    )

    for stock_entry in stock_entries:
        stock_entry_doc = frappe.get_doc("Stock Entry", stock_entry)
        for entry_item in stock_entry_doc.items:
            if entry_item.item_code == item_code:
                stock_entry_doc.cancel()  # Cancel the stock entry containing "ديك حي"
                frappe.delete_doc("Stock Entry", stock_entry, force=1)  # Delete it
                frappe.db.commit()  # Save changes
                print(f"Removed stock entry for: {item_code}")


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

    # Loop through each item in the Purchase Receipt
    for item in doc.items:
        if item.item_code in item_parts:  # Check if the item is in our dictionary
            print(f"Processing item: {item.item_code}")

            stock_entry = frappe.new_doc("Stock Entry")
            stock_entry.stock_entry_type = "Material Receipt"
            stock_entry.to_warehouse = item.warehouse  # Use the warehouse from the Purchase Receipt

            # Add each part with the appropriate quantity multiplied by the received quantity
            for part, qty_per_unit in item_parts[item.item_code].items():
                stock_entry.append(
                    "items",
                    {
                        "item_code": part,
                        "qty": qty_per_unit * item.qty,  # Calculate total quantity for the received item
                        "t_warehouse": item.warehouse,
                    },
                )

            # Submit the Stock Entry to update stock
            stock_entry.insert()
            stock_entry.submit()
            remove_stock_entry_for_item(doc,item.item_code)
