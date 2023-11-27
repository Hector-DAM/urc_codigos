from pymongo import MongoClient
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd

# MongoDB connection information
uri = "mongodb+srv://hadaya:24enero98@basedatos1.gamnobr.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Database and collection names
db_name = "BaseDatos1"
collection_name = "DatosPP"

# Access the specified database and collection
db = client[db_name]
collection = db[collection_name]

# Fetch all documents from the collection
cursor = collection.find()

# Convert MongoDB cursor to DataFrame
result_df = pd.DataFrame(list(cursor))

ventana = Tk()
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()
margin = 5

window_width = screen_width - margin
window_height = screen_height - margin

ventana.geometry(f"{window_width}x{window_height}+{margin//2}+{margin//2}")
ventana.title("Demo \nVoto Electrónico")
ventana.geometry("1360x720")
ventana.config(bg="#FCF8EC") 
zoom = 0.6
image = Image.open("logo_urc.png")  # Use a relative path for the image
pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])

foto = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))

# Global variables
user_info_label = None
end_login_button = None
vote_button = None

def open_login_window():
    global entry_email, entry_password, user_info_label, end_login_button

    login_window = Toplevel(ventana)
    login_window.title("Login")
    
    label_email = Label(login_window, text="Email:")
    label_email.grid(row=0, column=0, padx=10, pady=10)
    entry_email = Entry(login_window)
    entry_email.grid(row=0, column=1, padx=10, pady=10)

    label_password = Label(login_window, text="Contraseña:")
    label_password.grid(row=1, column=0, padx=10, pady=10)
    entry_password = Entry(login_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    login_button = Button(login_window, text="Acceso", command=lambda: handle_login(login_window))
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

def handle_login(login_window):
    email = entry_email.get()
    password = entry_password.get()

    user = result_df[(result_df['email'] == email) & (result_df['password'] == password)]

    if not user.empty:
        messagebox.showinfo("Acceso", "Se ha logrado el acceso.")
        login_window.destroy()
        
        # Update the main window to display user information
        show_user_info(user)
        show_end_login_button()
    else:
        messagebox.showerror("Error", "Correo o contraseña erroneos.")

def show_user_info(user):
    global user_info_label

    # Remove the login button
    login_button.place_forget()

    # Select the columns you want to display
    columns_to_display = ["nombre1", "nombre2", "apellido1", "apellido2", "genero", "edad"]

    # Create a string with the selected columns and their values
    user_info_str = "\n".join([f"{column}: {user.iloc[0][column]}" for column in columns_to_display])

    # Check if the user has already voted
    has_voted = user.iloc[0]["voto"]

    if has_voted == "":
        user_info_str += "\nAún no has votado."
        # Add the voting button if the user hasn't voted
        vote_button = Button(ventana, text="Votar", command=lambda: open_vote_window(user))
        vote_button.place(width=150, x=500, y=500)
    else:
        user_info_str += f"\nYa has votado. Voto registrado: {str(has_voted)}"  # Assuming 'voto' is an integer

    # Display user information
    user_info_label = Label(ventana, text=f"Información:\n{user_info_str}")
    user_info_label.place(x=300, y=400)  # Adjust the position as needed

def open_vote_window(user):
    global vote_button

    # Check if the user has already voted
    has_voted = user.iloc[0]["voto"]

    if has_voted != "":
        # Inform the user that they have already voted
        messagebox.showinfo("Voto Registrado", "Ya has votado. No puedes votar nuevamente.")
    else:
        # Create a new window for vote selection
        vote_window = Toplevel(ventana)
        vote_window.title("Selección de Voto")

        # Add options for voting (modify as needed)
        vote_options = ["Opción 1", "Opción 2", "Opción 3"]
        selected_option = StringVar(value=vote_options[0])

        # Create radio buttons for each option
        for option in vote_options:
            Radiobutton(vote_window, text=option, variable=selected_option, value=option).pack()

        # Create a button to submit the vote
        submit_button = Button(vote_window, text="Votar", command=lambda: handle_vote_submission(user, selected_option.get(), vote_window))
        submit_button.pack()

        # Position for buttons in the vote window
        submit_button.place(width=150, x=500, y=500)

        # Assign the "Votar" button to the global variable
        vote_button = submit_button


def handle_vote_submission(user, selected_option, vote_window):
    # Update the DataFrame with the vote
    result_df.loc[result_df['id'] == user.iloc[0]['id'], 'voto'] = selected_option

    # Inform the user that the vote was successful
    messagebox.showinfo("Voto Exitoso", f"¡Tu voto por {selected_option} ha sido registrado!")

    # Close the vote window
    vote_window.destroy()

    # Update the interface
    reset_interface()

    # Save the updated DataFrame to the MongoDB collection
    for _, row in result_df.iterrows():
        collection.replace_one({'id': row['id']}, row.to_dict(), upsert=True)

def show_end_login_button():
    global end_login_button

    # Create the "End Login" button
    end_login_button = Button(ventana, text="Salir Sistema", command=reset_interface)
    end_login_button.grid(row=3, column=0, columnspan=2, pady=10)

def reset_interface():
    # Destroy user information label and "End Login" button
    if user_info_label:
        user_info_label.destroy()
    if end_login_button:
        end_login_button.destroy()

    # Show the login button again
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Main window setup...
etq_imagen = Label(ventana, image=foto, bg="#FCF8EC")
etq_imagen.image = foto
etq_imagen.place(x=0, y=0)
nombre = Label(ventana, text="Voto Electrónico", bg="#FCF8EC", fg="gray26")
nombre.configure(font=("Arial", 34))

nombre.place(width=500, x=400, y=200)
login_button = Button(ventana, text="Entrar Sistema", command=open_login_window)
login_button.place(width=150, x=500, y=500)

# ...

# Main loop
ventana.mainloop()
