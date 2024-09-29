import pywebio.input as p
import pywebio.output as o
import pymongo
from pywebio import start_server

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Inventory"]
requests_collection = db["Requests"]
donations_collection = db["Donations"]

def main():
    # Adding custom styles
    o.put_html("""
    <style>
        body {
            background-color: #f8f8f0; /* Off-white background */
            color: #4e3b31; /* Brown text color */
            display: flex;
            flex-direction: column;
            align-items: center; /* Center align items horizontally */
            justify-content: center; /* Center align items vertically */
            height: 100vh; /* Full height of the viewport */
            margin: 0; /* Remove default margin */
        }
        h1, h2, h3, h4, h5, h6 {
            color: #4e3b31; /* Brown for headings */
        }
        input, button {
            background-color: #ffffff; /* White for input and buttons */
            width: 300px; /* Set input width */
            padding: 10px; /* Add padding for better appearance */
            border: 1px solid #4e3b31; /* Brown border for inputs */
            border-radius: 5px; /* Rounded corners */
        }
        table {
            margin-left: auto;
            margin-right: auto;
            border-collapse: collapse; /* Ensures borders are merged */
        }
        table, th, td {
            border: 1px solid #4e3b31; /* Brown border for the table */
            padding: 8px;
        }
        th, td {
            text-align: left; /* Align text to the left */
        }
        .center-text {
            text-align: center;
            color: #4e3b31; /* Brown color for the text */
            font-weight: bold; /* Make it bold */
            font-size: 24px; /* Increase font size */
            margin-bottom: 20px; /* Space below the title */
            margin-top: 40px; /* Add margin to bring it lower */
        }
    </style>
    """)

    def add_document():
        name = p.input("Enter your name", required=True)
        phone = p.input("Enter Phone no", required=True)
        address = p.input("Enter address", required=True)
        product = p.radio("Choose the product you are willing to donate:", options=["Bread packet", "Water Bottle", "Blanket", "Biscuit Packet"],required=True)
        qty = int(p.input("Enter quantity", required=True))

        # Check availability in Donations table
        donation = donations_collection.find_one({"product": product, "qty": {"$gte": qty}})

        if donation and donation.get("qty") > qty:
            o.put_text(f"Product '{product}' is available!")
            o.put_table([
                ["Field", "Value"],
                ["Product", donation.get("product", "N/A")],
                ["Available Quantity", donation.get("qty", "N/A")],
                ["Donor Name", donation.get("donor_name", donation.get("name", "N/A"))],
            ])
           
            requests_collection.insert_one({
                "name": name,
                "phone": phone,
                "address": address,
                "product": product,
                "qty": qty,
                "status": "Available"
            })
            o.put_text("Your request has been recorded. We'll contact you soon.")
        else:
            o.put_text(f"Sorry, the requested product '{product}' is not available in the required quantity.")
            requests_collection.insert_one({
                "name": name,
                "phone": phone,
                "address": address,
                "product": product,
                "qty": qty,
                "status": "Unavailable"
            })
            o.put_text("Your request has been recorded. We'll notify you when the product becomes available.")

    o.put_html('<div class="center-text">REQUEST</div>')
    o.put_buttons(["Add Request"], [add_document])  # Button should be centered
    o.put_html("""
    <button onclick="window.close();">Close Tab</button>
    <script>
        // Ensure that the button can close the tab in some browsers
        window.onbeforeunload = function() {
            return 'Are you sure you want to close the tab?';
        };
    </script>
    """)

if __name__ == '__main__':
    start_server(main, port=8082)
