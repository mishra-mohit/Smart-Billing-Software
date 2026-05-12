**Smart Billing Software**

A professional desktop-based billing application built with **Python, Tkinter, and MySQL**. This software allows businesses to manage customers, generate dynamic bills, save data to a database, and export professional PDF invoices.

**✨ Features**

**Customer Management:** Input and store customer names, phone numbers, and emails.

**Dynamic Cart:** Add products with real-time price and quantity calculations.

**Database Integration:** Save all billing records securely in a MySQL database.

**Search Functionality:** Quickly find past bills using a unique Bill Number.

**PDF Generation:** Automatically generate and save professional PDF invoices using ReportLab.

**User-Friendly UI:** Clean and intuitive interface designed with Tkinter.

**🚀 Tech Stack**

Language: Python 3.x

GUI Library: Tkinter

Database: MySQL

PDF Engine: ReportLab

Database Connector: mysql-connector-python

**🛠️Installation & Setup**

**Clone the Repository:**

git clone https://github.com/mishra-mohit/Smart-Billing-Software.git

cd Smart-Billing-Software

**Install Dependencies:**

pip install mysql-connector-python reportlab

**Database Configuration:**

Open your MySQL terminal.

**Create a database:** CREATE DATABASE bill_db;

**Create the table:**

CREATE TABLE bills (
    bill_no INT PRIMARY KEY,
    customer_name VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    total_amount DOUBLE
);

**Run the Application:**

python billing_system.py
