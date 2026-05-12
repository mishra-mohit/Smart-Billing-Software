import os
from tkinter import *
from tkinter import messagebox
from turtle import right
import mysql.connector
import random
from reportlab.pdfgen import canvas
import datetime
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# ======= Billing System Class =======
class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Smart Billing Software")
        bg_color = "#f2f2f2"

        # ======= Variables =======
        self.cus_name = StringVar()
        self.cus_phone = StringVar()
        self.cus_email = StringVar()
        self.bill_no = StringVar(value=str(random.randint(101, 9999)))
        self.search_var = StringVar()
        
        self.prod_name = StringVar()
        self.price = DoubleVar()
        self.qty = IntVar(value=1)
        self.total_val = StringVar(value="0.0")

        # ======= UI Layout =======
        title = Label(self.root, text="SMART BILLING SOFTWARE", bd=12, relief=GROOVE, bg="#f2f2f2", fg="red", font=("times new roman", 30, "bold")).pack(fill=X)



        # ======= Customer Frame ======= 
        F1 = LabelFrame(self.root, text="Customer Details", bd=7, relief=GROOVE, font=("arial", 12, "bold"), fg="red")
        F1.place(x=0, y=80, width=500, height=150)
        
        Label(F1, text="Mobile No:").grid(row=0, column=0, padx=20, pady=5)
        Entry(F1, textvariable=self.cus_phone).grid(row=0, column=1)
        
        Label(F1, text="Name:").grid(row=1, column=0, padx=20, pady=5)
        Entry(F1, textvariable=self.cus_name).grid(row=1, column=1)

        Label(F1, text="Email:").grid(row=2, column=0, padx=20, pady=5)
        Entry(F1, textvariable=self.cus_email).grid(row=2, column=1)



        # ======= Product Frame =======
        F2 = LabelFrame(self.root, text="Product Details", bd=7, relief=GROOVE, font=("arial", 12, "bold"), fg="red")
        F2.place(x=0, y=240, width=500, height=200)
        
        Label(F2, text="Product Name:").grid(row=0, column=0, padx=20, pady=10)
        Entry(F2, textvariable=self.prod_name).grid(row=0, column=1)
        
        Label(F2, text="Price:").grid(row=1, column=0, padx=20, pady=10)
        Entry(F2, textvariable=self.price).grid(row=1, column=1)

        Label(F2, text="Qty:").grid(row=2, column=0, padx=20, pady=10)
        Entry(F2, textvariable=self.qty).grid(row=2, column=1)

        Button(F2, text="Add To Cart", command=self.add_to_cart, bg="orange", width=15).grid(row=3, column=1, pady=10)



        # ======= Bill Search Area =======
        search = Frame(self.root, bd=5, relief=GROOVE)
        search.place(x=520, y=80, width=500, height=50)

        Label(search, text="Bill Number:").place(x=10, y=8)
        Entry(search, textvariable=self.search_var).place(x=100, y=8)

        Button(search, text="Search", bg="orange",
               command=self.search_bill).place(x=400, y=7)



        # ======= Bill Area =======
        F3 = Frame(self.root, bd=5, relief=GROOVE)
        F3.place(x=520, y=140, width=500, height=350)

        Label(F3, text="Bill Area", font="arial 15 bold", bd=7, relief=GROOVE).pack(fill=X)
        
        scrollbar = Scrollbar(F3)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.txtarea = Text(F3, yscrollcommand=scrollbar.set)
        self.txtarea.pack(fill=BOTH, expand=1)
        scrollbar.config(command=self.txtarea.yview)

        # ======= Buttons Frame ======= 
        F4 = Frame(self.root, bd=10, relief=GROOVE)
        F4.place(x=0, y=540, width=1350, height=120)
        
        Label(F4, text="Total Amount:", font="arial 12 bold").grid(row=0, column=0, padx=20)
        Entry(F4, textvariable=self.total_val, state='readonly').grid(row=0, column=1)

        Button(F4, text="Save Bill", command=self.save_to_db, bg="orange", width=20, height=2).grid(row=0, column=2, padx=10)
        Button(F4, text="Clear", command=self.clear_data, bg="orange", width=15, height=2).grid(row=0, column=3, padx=10)
        Button(F4, text="Exit", command=self.root.quit, bg="orange", width=15, height=2).grid(row=0, column=4, padx=10)

        self.welcome_bill()
    
    def welcome_bill(self):
        self.txtarea.delete('1.0', END)
        # self.txtarea.insert(END, f" {'='*55}\n")
        self.txtarea.insert(END, "All in One Store".center(60) + "\n")
        self.txtarea.insert(END, "Store Address: XYZ Street".center(60) + "\n")
        self.txtarea.insert(END, "Phone: 9876543210".center(60) + "\n")
        self.txtarea.insert(END, f" {'='*55}\n")
        self.txtarea.insert(END, "Invoice Details".center(60))
        self.txtarea.insert(END, f"\n Bill Number : {self.bill_no.get()}")
        self.txtarea.insert(END, f"\n Customer Name : {self.cus_name.get()}")
        self.txtarea.insert(END, f"\n Phone Number : {self.cus_phone.get()}")
        self.txtarea.insert(END, f"\n Email : {self.cus_email.get()}")
        self.txtarea.insert(END, f"\n {'='*55}")
        self.txtarea.insert(END, f"\n {'Product':<15}{'QTY':<8}{'Price':<10}{'Total':<10}")
        self.txtarea.insert(END, f"\n {'='*55}")
        
    # ======= Add Product to Cart =======
    def add_to_cart(self):
        if self.prod_name.get() == "" or self.price.get() == 0:
            messagebox.showerror("Error", "Product details are must!")
        else:
            if float(self.total_val.get()) == 0.0:
                self.welcome_bill()
            p = self.price.get()
            q = self.qty.get()
            total = p * q
            self.txtarea.insert(END, f"\n {self.prod_name.get():<15}{q:<8}{p:<10}{total:<10}")
            current_total = float(self.total_val.get()) + total
            self.total_val.set(str(current_total))
            self.prod_name.set("")
            self.price.set(0.0)
            self.qty.set(1)

    # ======= Search Bill from Database =======
    def search_bill(self):
        bill_no = self.search_var.get().strip()
        if bill_no == "":
            messagebox.showwarning("Warning", "Please enter a bill number to search.")
            return
        
        try:
            conn = get_db_connection()
            curr = conn.cursor()
            curr.execute("SELECT customer_name, phone, email, total_amount FROM bills WHERE bill_no = %s", (bill_no,))
            result = curr.fetchone()
            conn.close()
            
            if result:
                cus_name, phone, email, total = result
                # Display in bill area
                self.txtarea.delete('1.0', END)
                self.txtarea.insert(END, f" {'='*55}\n")
                self.txtarea.insert(END, "SMART BILLING SOFTWARE".center(60) + "\n")
                self.txtarea.insert(END, "Store Address: XYZ Street".center(60) + "\n")
                self.txtarea.insert(END, "Phone: 9876543210".center(60) + "\n")
                self.txtarea.insert(END, f" {'='*55}\n")
                self.txtarea.insert(END, "Invoice Details".center(60) + "\n")
                self.txtarea.insert(END, f"\n Bill Number : {bill_no}")
                self.txtarea.insert(END, f"\n Customer Name : {cus_name}")
                self.txtarea.insert(END, f"\n Phone Number : {phone}")
                self.txtarea.insert(END, f"\n Email : {email}")
                self.txtarea.insert(END, f"\n {'='*55}")
                self.txtarea.insert(END, f"\n Total Amount: Rs. {total}")
                self.txtarea.insert(END, f"\n {'='*55}")
            else:
                messagebox.showinfo("Not Found", f"Bill {bill_no} was not found.")
        except Exception as es:
            messagebox.showerror("Database Error", f"Error: {str(es)}")

    # ======= Save Bill to Database =======
    def save_to_db(self):
        self.txtarea.insert(END, f"\n Total Amount: Rs. {self.total_val.get()}")
        self.txtarea.insert(END, f"\n {'='*55}\n")
        self.txtarea.insert(END, "Thank you for shopping with us!".center(60) + "\n")
        self.txtarea.insert(END, "Please visit again!".center(60) + "\n")
        self.txtarea.insert(END, f" {'='*55}\n")
        
        try:
            conn = get_db_connection()
            curr = conn.cursor()
            
            query = "INSERT INTO bills (bill_no, customer_name, phone, email, total_amount) VALUES (%s, %s, %s, %s, %s)"
            values = (self.bill_no.get(), self.cus_name.get(), self.cus_phone.get(), self.cus_email.get(), self.total_val.get())
            
            curr.execute(query, values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Bill {self.bill_no.get()} saved to Database!")
            self.print_bill()
        except Exception as es:
            messagebox.showerror("Database Error", f"Error: {str(es)}")

    # ======= Print Bill to PDF =======
    def print_bill(self):
        filename = f"Bill_{self.bill_no.get()}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(filename)
        c.setFont("Helvetica", 12)
        lines = [
            f" {'='*55}",
            "All in One Store".center(60),
            "Store Address: XYZ Street".center(60),
            "Phone: 9876543210".center(60),
            f" {'='*55}",
            f" Invoice Details".center(60),
            f" Bill Number : {self.bill_no.get()}",
            f" Customer Name : {self.cus_name.get()}",
            f" Phone Number : {self.cus_phone.get()}",
            f" Email : {self.cus_email.get()}",
            f" {'='*55}",
        ]
        bill_text = self.txtarea.get(1.0, END)
        all_lines = bill_text.split('\n')

        # ======= Append product and footer lines from the current bill area, ======= 
        # ======= skipping the existing header section in the text area. ======= 
        append = False
        for line in all_lines:
            if append:
                if line.strip():
                    lines.append(line)
            elif 'Product' in line:
                append = True
                lines.append(line)

        y = 800
        for line in lines:
            if line.strip():
                c.drawString(50, y, line)
                y -= 18
                if y < 50:
                    c.showPage()
                    y = 800

        c.save()
        messagebox.showinfo("Bill Printed", f"Bill saved as PDF: {filename}")

    # ======= Clear Data for New Bill =======
    def clear_data(self):
        self.cus_name.set("")
        self.cus_phone.set("")
        self.cus_email.set("")
        self.prod_name.set("")
        self.price.set(0.0)
        self.qty.set(1)
        self.total_val.set("0.0")
        self.search_var.set("")
        self.bill_no.set(str(random.randint(101, 9999)))
        self.welcome_bill()

if __name__ == "__main__":
    root = Tk()
    obj = BillingSystem(root)
    root.mainloop()