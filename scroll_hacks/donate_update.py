import pywebio.input as p
import pywebio.output as o
import pymongo
from pywebio import start_server

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Inventory"]
donations_collection = db["Donations"]

def main():
    def add_donation():
        # Get user input
        donor_name = p.input("Enter your name", css_style='color: #8c5c47')
        phone = p.input("Enter Phone no")
        address = p.input("Enter address")
        product = p.radio("Choose the product you are willing to donate:", options=["Bread packet", "Water Bottle", "Blanket", "Biscuit Packet"])
        qty = int(p.input("Enter quantity"))
        
        # Create donation dictionary
        donation = {
            "donor_name": donor_name,
            "phone": phone,
            "address": address,
            "product": product,
            "qty": qty,
        }
        
        # Insert donation into MongoDB
        try:
            donations_collection.insert_one(donation)
            o.put_text("Thank you for your contribution and support!")
            
            # Create a styled and centered table
            table_html = """
            <div style="display: flex; justify-content: center; margin: 20px 0;">
                <table style="width: 50%; border-collapse: collapse; margin: auto;">
                    <tr style="background-color: #8c5c47; color: white;">
                        <th style="padding: 8px; border: 1px solid #ddd;">Field</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Value</th>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Donor Name</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Product</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Quantity</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{}</td>
                    </tr>
                </table>
            </div>
            """.format(donor_name, product, qty)

            o.put_html(table_html)
        except Exception as e:
            o.put_text(f"An error occurred: {e}")

    # Display the form and button
    o.put_html("""
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8efe0;
            color: black; /* Change the text color to black */
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #4CAF50;
        }
        .pywebio_button {
            background-color: #d9534f; /* Change to your desired button color */
            color: white; /* Change text color */
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        .pywebio_button:hover {
            background-color: #c9302c; /* Change hover color */
        }
        /* Style for placeholder text */
        input::placeholder {
            color: brown; /* Change this to the desired color */
        }
    </style>
    """)

    o.put_html('<div style="color: brown; font-family: \'Times New Roman\'; font-size: 24px;">ADD DONATIONS</div>')
    o.put_buttons(["Donate"], [add_donation])
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
    start_server(main, port=8081)
