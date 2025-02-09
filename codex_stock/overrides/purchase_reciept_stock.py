# import frappe


# def on_submit_purchase_receipt(doc, method):
#     # Define the 12 components for "ديك"
#     components = [
#         "قطع لحم ديك",
#         "قنصة ديك",
#         "كبدة ديك",
#         "هيكل ديك",
#         "زلموكة ديك",
#         "شيش ديك",
#         "صدور ديك",
#         "وراك ديك",
#         "دبوس ورك ديك",
#         "دبوس صدر ديك",
#         "جناح ديك",
#         "رقبة ديك",
#     ]

#     # Loop through items in the Purchase Receipt
#     for item in doc.items:
#         if item.item_code == "ديك":  # Check if the received item is "ديك"
#             stock_entry = frappe.new_doc("Stock Entry")
#             stock_entry.stock_entry_type = "Material Receipt"
#             stock_entry.to_warehouse = (
#                 item.warehouse
#             )  # Use the warehouse from the Purchase Receipt

#             # Add each component with the same quantity as the "ديك" item
#             for component in components:
#                 stock_entry.append(
#                     "items",
#                     {
#                         "item_code": component,
#                         "qty": item.qty,  # Each "ديك" equals one of each component
#                         "t_warehouse": item.warehouse,
#                     },
#                 )

#             # Submit the Stock Entry to update stock
#             stock_entry.insert()
#             stock_entry.submit()


import frappe

def get_deek_parts():
    """Defines the parts of 'ديك' and their sub-parts (if any)."""
    return {
        "ديك": {  # The whole turkey
            "قنصة ديك": 1,
            "كبدة ديك": 1,
            "هيكل ديك": 1,
            "زلموكة ديك": 1,
            "شيش ديك": 2,
            "صدور ديك": 2,  # Has sub-parts
            "وراك ديك": 2,
            "دبوس ورك ديك": 2,
            "دبوس صدر ديك": 2,
            "جناح ديك": 2,
            "رقبة ديك": 1,
            "قطع لحم ديك": 1,
        },
        "صدور ديك": {  # Breaking "صدور ديك" into smaller parts
            "صدر أيمن ديك": 1,
            "صدر أيسر ديك": 1,
            "فيليه صدر ديك": 1,
        },
        "وراك ديك": {  # If "وراك ديك" has sub-parts
            "ورك أيمن ديك": 1,
            "ورك أيسر ديك": 1,
        },
        "جناح ديك": {  # If "جناح ديك" has sub-parts
            "جناح علوي ديك": 1,
            "جناح سفلي ديك": 1,
        },
    }

def process_parts(stock_entry, part, quantity, warehouse, deek_parts):
    """Recursively processes parts and their sub-parts."""
    
    if part in deek_parts:  # If the part has sub-parts
        for sub_part, qty in deek_parts[part].items():
            process_parts(stock_entry, sub_part, quantity * qty, warehouse, deek_parts)
    else:  # If it's a final part, add it to the stock entry
        stock_entry.append(
            "items",
            {
                "item_code": part,
                "qty": quantity,
                "t_warehouse": warehouse,
            },
        )

def on_submit_purchase_receipt(doc, method):
    """Handles the submission of a Purchase Receipt for 'ديك' by breaking it into parts and sub-parts."""
    
    deek_parts = get_deek_parts()  # Get all part mappings

    for item in doc.items:
        if item.item_code == "ديك":  # If the item is "ديك"
            frappe.logger().info("Processing 'ديك' item in Purchase Receipt.")

            try:
                stock_entry = frappe.new_doc("Stock Entry")
                stock_entry.stock_entry_type = "Material Receipt"
                stock_entry.to_warehouse = item.warehouse

                # Process "ديك" and its sub-parts recursively
                process_parts(stock_entry, "ديك", item.qty, item.warehouse, deek_parts)

                # Insert and submit the stock entry
                stock_entry.insert()
                stock_entry.submit()
                frappe.logger().info(f"Stock Entry created for {item.qty} 'ديك' successfully.")

            except Exception as e:
                frappe.logger().error(f"Error creating Stock Entry for 'ديك': {str(e)}")
