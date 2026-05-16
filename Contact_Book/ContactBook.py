import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# =============== COLORS ===============
bg_color = "#111827"
sidebar_color = "#1E2533"
card_color = "#202838"
button_color = "#1F4D3A"
entry_color = "#0F172A"
text_color = "#F3F4F6"
secondary_text = "#9CA3AF"
border_color = "#3B4252"
hover_color = "#2D3748"
danger_color = "#C95C54"
danger_hover = "#A94740"
favourite_color = "#D6A85F"
favourite_hover = "#B98E4B"

class ContactBookApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Contact Book v1.0")
        self.geometry("1100x650")
        self.resizable(False, False)
        self.configure(fg_color=bg_color)

        # =============== DATA ===============
        self.contacts = [
            {
                "name": "Rahul",
                "phone": "9876543210",
                "email": "rahul@gmail.com",
                "favorite": True
            },
            {
                "name": "Priya",
                "phone": "9123456780",
                "email": "priya@gmail.com",
                "favorite": False
            }
        ]

        self.selected_contact = None

        # =============== MAIN LAYOUT ===============
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =============== LEFT SIDEBAR ===============
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color=sidebar_color)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # =============== SEARCH BOX ===============
        self.search_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Search contacts...",
            width=250,
            height=45,
            corner_radius=25,
            font=("Arial", 15),

            fg_color=entry_color,
            border_color=border_color,
            text_color=text_color,
            placeholder_text_color=secondary_text
        )
        self.search_entry.pack(pady=(20, 10), padx=20)
        self.search_entry.bind("<KeyRelease>", self.search_contacts)

        # Scrollable Contact List
        self.contact_list_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            width=260,
            height=470,
            fg_color=sidebar_color
        )
        self.contact_list_frame.pack(padx=10, pady=10)

        # Add Contact Button
        self.add_button = ctk.CTkButton(
            self.sidebar,
            text="+  Add New Contact",
            height=50,
            corner_radius=18,
            font=("Arial", 18, "bold"),
            fg_color=button_color,
            hover_color="#355C4A",
            text_color=text_color,
            command=self.open_add_window
        )
        self.add_button.pack(padx=20, pady=15, fill="x")

        # =============== RIGHT PANEL ===============
        self.details_frame = ctk.CTkFrame(self, fg_color=bg_color)
        self.details_frame.grid(row=0, column=1, sticky="nsew")

        # Top Icons
        self.top_frame = ctk.CTkFrame(self.details_frame, fg_color=entry_color, height=50)
        self.top_frame.pack(fill="x")

        # Profile Area
        self.profile_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        self.profile_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Profile image
        self.profile_pic = ctk.CTkLabel(
            self.profile_frame,
            text="👩",
            font=("Arial", 80)
        )
        self.profile_pic.grid(row=0, column=0, rowspan=2, padx=20)

        # =============== NAME ===============
        self.name_value = ctk.CTkEntry(
            self.profile_frame,
            width=400,
            height=55,
            font=("Arial", 30, "bold"),
            fg_color=entry_color,
            border_color=border_color,
            text_color=text_color,
            state="disabled"
        )
        self.name_value.grid(row=0, column=1, sticky="w", pady=(20, 0))
        self.name_value.configure(state="normal")
        self.name_value.insert(0, "Select a Contact")
        self.name_value.configure(state="disabled")

        self.role_label = ctk.CTkLabel(
            self.profile_frame,
            text="Contact Information",
            font=("Arial", 20),
            text_color=secondary_text
        )
        self.role_label.grid(row=1, column=1, sticky="w")

        # =============== PHONE ===============
        self.phone_title = ctk.CTkLabel(
            self.profile_frame,
            text="Phone:",
            font=("Arial", 22, "bold")
        )
        self.phone_title.grid(row=3, column=0, sticky="w", pady=(40, 10))

        self.phone_value = ctk.CTkEntry(
            self.profile_frame,
            width=400,
            height=45,
            font=("Arial", 18),
            fg_color=entry_color,
            border_color=border_color,
            text_color=text_color,
            state="disabled"
        )
        self.phone_value.grid(row=3, column=1, sticky="w", pady=(40, 10))

        # =============== EMAIL ===============
        self.email_title = ctk.CTkLabel(
            self.profile_frame,
            text="Email:",
            font=("Arial", 22, "bold")
        )
        self.email_title.grid(row=4, column=0, sticky="w", pady=10)

        self.email_value = ctk.CTkEntry(
            self.profile_frame,
            width=400,
            height=40,
            font=("Arial", 18),
            fg_color=entry_color,
            border_color=border_color,
            text_color=text_color,
            state="disabled"
        )
        self.email_value.grid(row=4, column=1, sticky="w", pady=10)

        # =============== BUTTONS ===============
        self.button_frame = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=40)

        self.edit_button = ctk.CTkButton(
            self.button_frame,
            text="Edit Contact",
            width=170,
            height=45,
            corner_radius=15,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            border_width=2,
            border_color=border_color,
            font=("Arial", 18, "bold"),
            state="disabled",
            command=self.edit_contact
        )
        self.edit_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(
            self.button_frame,
            text="Delete Contact",
            width=170,
            height=45,
            corner_radius=15,
            fg_color=danger_color,
            hover_color=danger_hover,
            text_color=text_color,
            font=("Arial", 18, "bold"),
            state="disabled",
            command=self.delete_contact
        )
        self.delete_button.pack(side="left", padx=10)

        self.favorite_button = ctk.CTkButton(
            self.button_frame,
            text="Favorite ☆",
            width=170,
            height=45,
            corner_radius=15,
            fg_color=favourite_color,
            hover_color=favourite_hover,
            text_color=text_color,
            font=("Arial", 18, "bold"),
            state="disabled",
            command=self.toggle_favorite
        )
        self.favorite_button.pack(side="left", padx=10)

        # Load contacts
        self.display_contacts(self.contacts)

    # =============== DISPLAY CONTACTS ===============
    def display_contacts(self, contacts):

        for widget in self.contact_list_frame.winfo_children():
            widget.destroy()

        for contact in contacts:

            display_name = contact["name"]

            if contact["favorite"]:
                display_name = "★ " + display_name

            button = ctk.CTkButton(
                self.contact_list_frame,
                text=display_name,
                anchor="w",
                height=60,
                corner_radius=18,
                font=("Arial", 20),
                fg_color=card_color,
                hover_color=hover_color,
                text_color=text_color,
                command=lambda c=contact: self.show_contact(c)
            )
            button.pack(fill="x", padx=5, pady=5)

    # =============== SHOW CONTACT ===============
    def show_contact(self, contact):

        self.selected_contact = contact

        # Enable fields
        self.name_value.configure(state="normal")
        self.phone_value.configure(state="normal")
        self.email_value.configure(state="normal")

        # Enable buttons
        self.edit_button.configure(state="normal")
        self.delete_button.configure(state="normal")
        self.favorite_button.configure(state="normal")

        self.name_value.delete(0, "end")
        self.name_value.insert(0, contact["name"])

        self.phone_value.delete(0, "end")
        self.phone_value.insert(0, contact["phone"])

        self.email_value.delete(0, "end")
        self.email_value.insert(0, contact["email"])

        if contact["favorite"]:
            self.favorite_button.configure(text="Favorite ★")
        else:
            self.favorite_button.configure(text="Favorite ☆")

    # =============== SEARCH ===============
    def search_contacts(self, event=None):

        query = self.search_entry.get().lower()

        filtered = []

        for contact in self.contacts:
            if query in contact["name"].lower():
                filtered.append(contact)

        self.display_contacts(filtered)

    # =============== ADD WINDOW ===============
    def open_add_window(self):

        window = ctk.CTkToplevel(self)
        window.title("Add Contact")
        window.geometry("400x350")
        window.resizable(False, False)

        title = ctk.CTkLabel(
            window,
            text="Add New Contact",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        name_entry = ctk.CTkEntry(window, placeholder_text="Name", width=300, height=40)
        name_entry.pack(pady=10)

        phone_entry = ctk.CTkEntry(window, placeholder_text="Phone", width=300, height=40)
        phone_entry.pack(pady=10)

        email_entry = ctk.CTkEntry(window, placeholder_text="Email", width=300, height=40)
        email_entry.pack(pady=10)

        def save_contact():

            name = name_entry.get().title()
            phone = phone_entry.get()
            email = email_entry.get()

            # Empty field validation
            if name.strip() == "" or phone.strip() == "" or email.strip() == "":
                messagebox.showerror("Error", "All fields are required")
                return

            # Phone number validation
            if not phone.isdigit():
                messagebox.showerror("Error", "Phone number must contain only digits")
                return

            # Phone length validation
            if len(phone) != 10:
                messagebox.showerror("Error", "Phone number must be exactly 10 digits")
                return

            # Email validation
            if "@" not in email or "." not in email:
                messagebox.showerror("Error", "Please enter a valid email address")
                return

            new_contact = {
                "name": name,
                "phone": phone,
                "email": email,
                "favorite": False
            }

            self.contacts.append(new_contact)

            self.display_contacts(self.contacts)

            messagebox.showinfo("Success", "Contact Added Successfully")

            window.destroy()

        save_button = ctk.CTkButton(
            window,
            text="Save Contact",
            width=300,
            height=45,
            font=("Arial", 18, "bold"),
            command=save_contact
        )
        save_button.pack(pady=30)

    # =============== EDIT CONTACT ===============
    def edit_contact(self):

        if not self.selected_contact:
            messagebox.showwarning("Warning", "Please select a contact")
            return

        self.selected_contact["name"] = self.name_value.get()
        self.selected_contact["phone"] = self.phone_value.get()
        self.selected_contact["email"] = self.email_value.get()

        self.display_contacts(self.contacts)

        messagebox.showinfo("Updated", "Contact Updated Successfully")

    # =============== DELETE CONTACT ===============
    def delete_contact(self):

        if not self.selected_contact:
            messagebox.showwarning("Warning", "Please select a contact")
            return

        confirm = messagebox.askyesno(
            "Delete",
            "Are you sure you want to delete this contact?"
        )

        if confirm:
            self.contacts.remove(self.selected_contact)
            self.selected_contact = None

            self.display_contacts(self.contacts)

            # Temporarily enable fields
            self.name_value.configure(state="normal")
            self.phone_value.configure(state="normal")
            self.email_value.configure(state="normal")

            # Clear fields
            self.name_value.delete(0, "end")
            self.name_value.insert(0, "Select a Contact")

            self.phone_value.delete(0, "end")
            self.email_value.delete(0, "end")
            self.favorite_button.configure(text="Favorite ☆")

            # Disable fields
            self.name_value.configure(state="disabled")
            self.phone_value.configure(state="disabled")
            self.email_value.configure(state="disabled")

            # Disable buttons
            self.edit_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")
            self.favorite_button.configure(state="disabled")

            messagebox.showinfo("Deleted", "Contact Deleted Successfully")

    # =============== FAVORITE ===============
    def toggle_favorite(self):

        if not self.selected_contact:
            messagebox.showwarning("Warning", "Please select a contact")
            return

        self.selected_contact["favorite"] = not self.selected_contact["favorite"]

        self.display_contacts(self.contacts)

        self.show_contact(self.selected_contact)


# =============== RUN APP ===============
app = ContactBookApp()
app.mainloop()