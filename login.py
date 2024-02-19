import tkinter as tk
from tkinter import messagebox
import pyodbc
import front

def login():
    # Função para a ação de login
    username = entry_username.get()
    password = entry_password.get()

    # Conecta-se ao banco de dados
    conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=localhost\SQLEXPRESS;'
                          'DATABASE=master;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()

    # Consulta o banco de dados para verificar se o usuário e a senha estão corretos
    cursor.execute("SELECT UserID FROM Usuarios WHERE Username=? AND Password=?", (username, password))
    row = cursor.fetchone()

    if row:
        messagebox.showinfo("Login", "Login bem sucedido!")
        conn.close()  # Fecha a conexão com o banco de dados
        root.withdraw()  # Esconde a janela de login
        front.abrir_janela_filmes()  # Chama a função para abrir 
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")

    conn.close()

def cadastrar():
    # Função para a ação de cadastro
    # Abre uma nova janela para cadastro
    global cadastro_window
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastro de Usuário")

    label_username = tk.Label(cadastro_window, text="Usuário:")
    label_username.grid(row=0, column=0, padx=10, pady=5)
    entry_new_username = tk.Entry(cadastro_window)
    entry_new_username.grid(row=0, column=1, padx=10, pady=5)

    label_password = tk.Label(cadastro_window, text="Senha:")
    label_password.grid(row=1, column=0, padx=10, pady=5)
    entry_new_password = tk.Entry(cadastro_window, show="*")
    entry_new_password.grid(row=1, column=1, padx=10, pady=5)
    

    def salvar_cadastro():
        new_username = entry_new_username.get()
        new_password = entry_new_password.get()

        # Conecta-se ao banco de dados
        conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=localhost\SQLEXPRESS;'
                          'DATABASE=master;'
                          'Trusted_Connection=yes;')

        cursor = conn.cursor()

        # Verifica se o usuário já existe
        cursor.execute("SELECT * FROM Usuarios WHERE Username=?", (new_username,))
        if cursor.fetchone():
            messagebox.showerror("Cadastro", "Este usuário já existe.")
        else:
            # Insere o novo usuário no banco de dados
            cursor.execute("INSERT INTO Usuarios (Username, Password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            cadastro_window.destroy()


        conn.close()

    button_salvar_cadastro = tk.Button(cadastro_window, text="Salvar", command=salvar_cadastro)
    button_salvar_cadastro.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

def alterar_senha():
    # Função para a ação de alterar senha
    # Abre uma nova janela para alterar a senha
    global alterar_senha_window
    alterar_senha_window = tk.Toplevel(root)
    alterar_senha_window.title("Alterar Senha")

    label_username = tk.Label(alterar_senha_window, text="Usuário:")
    label_username.grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(alterar_senha_window)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    label_password = tk.Label(alterar_senha_window, text="Nova Senha:")
    label_password.grid(row=1, column=0, padx=10, pady=5)
    entry_new_password = tk.Entry(alterar_senha_window, show="*")
    entry_new_password.grid(row=1, column=1, padx=10, pady=5)

    def salvar_alteracao_senha():
        username = entry_username.get()
        new_password = entry_new_password.get()

        # Conecta-se ao banco de dados
        conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=localhost\SQLEXPRESS;'
                          'DATABASE=master;'
                          'Trusted_Connection=yes;')

        cursor = conn.cursor()

        # Verifica se o usuário existe
        cursor.execute("SELECT * FROM Usuarios WHERE Username=?", (username,))
        if cursor.fetchone():
            # Atualiza a senha do usuário
            cursor.execute("UPDATE Usuarios SET Password=? WHERE Username=?", (new_password, username))
            conn.commit()
            messagebox.showinfo("Alterar Senha", "Senha alterada com sucesso!")
            alterar_senha_window.destroy()
        else:
            messagebox.showerror("Alterar Senha", "Usuário não encontrado.")

        conn.close()

    button_salvar_alteracao_senha = tk.Button(alterar_senha_window, text="Salvar", command=salvar_alteracao_senha)
    button_salvar_alteracao_senha.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

# Criando a janela principal
root = tk.Tk()
root.title("Sistema de Login")

# Criando os rótulos e campos de entrada para login
label_username = tk.Label(root, text="Usuário:")
label_username.grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=5)

label_password = tk.Label(root, text="Senha:")
label_password.grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

# Definindo os botões para login, cadastro e alterar senha fora das funções
button_login = tk.Button(root, text="Login", command=login)
button_cadastrar = tk.Button(root, text="Cadastrar", command=cadastrar)
button_alterar_senha = tk.Button(root, text="Alterar Senha", command=alterar_senha)

# Posicionando os botões na janela principal
button_login.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="WE")
button_cadastrar.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="WE")
button_alterar_senha.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky="WE")

root.mainloop()
