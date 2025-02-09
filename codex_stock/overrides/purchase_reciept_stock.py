
import frappe

def on_submit_purchase_receipt(doc, method):
    # Define parts and their quantities per item type
    item_parts = {
        "ديك": {
            "قنصة ديك": 1,
            "كبدة ديك": 1,
            "هيكل ديك": 1,
            "صدور ديك": 2,
            "وراك ديك": 2,
            "دبوس صدر ديك": 2,
            "جناح ديك": 2,
            "رقبة ديك": 1,
            "ريش ناعم": 1,
            "ريش سلاح": 1
        },
        "هيكل": {
            "قطع لحم": 1
        },
        "ورك": {
            "شيش ديك": 1
            "زلموكه ديك": 1
            "دبوس ورك": 1
        },
        "صدر": {
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
