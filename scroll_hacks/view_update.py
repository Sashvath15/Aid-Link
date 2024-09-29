import pywebio.input as p
import pywebio.output as o
import pymongo
from pywebio import start_server
from datetime import datetime
from pywebio import start_server
from pywebio.session import run_js
import time


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Inventory"]
donations_collection = db["Donations"]
requests_collection = db["Requests"]  # Access the Requests collection

def main():
    # Adding custom styles
    o.put_html("""
    <style>
        body {
            background-color: #f8f8f0; /* Off-white background */
            color: #4e3b31; /* Brown text color */
            text-align: center; /* Center align text */
        }
        h1 {
            color: #4e3b31; /* Brown color for the heading */
            font-size: 24px; /* Increase font size for the heading */
            margin-bottom: 20px; /* Space below the heading */
        }
    </style>
    """)

    def view_inventory():
        inventory = list(donations_collection.aggregate([
            {"$group": {"_id": "$product", "total_qty": {"$sum": "$qty"}}}
        ]))
        o.put_table(
            [["Product", "Total Quantity"]] +
            [[item["_id"], item["total_qty"]] for item in inventory]
        )

    def view_all_requests():
        requests = list(requests_collection.find())
        if requests:
            o.put_text("All Requests:")
            o.put_table(
                [["Name", "Phone", "Product", "Quantity", "Status"]] +
                [[r["name"], r["phone"], r["product"], r["qty"], r["status"]] for r in requests]
            )
        else:
            o.put_text("No requests found.")

    o.put_html('<h1>Inventory Management</h1>')  # Centered heading
    while True:
        choice = p.select("Choose an action", [
            "View Inventory",
            "View All Requests",
            "Exit"
        ])
        
        if choice == "View Inventory":
            view_inventory() 
        elif choice == "View All Requests":
            view_all_requests()
        elif choice == "Exit":
            o.put_text("Thank you for using Inventory Management!")
            time.sleep(3)
            run_js('window.close()')
            break

    o.put_text("Thank you for using Inventory Management!")

if __name__ == '__main__':
    start_server(main, port=8083)
