import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyodbc
from tkcalendar import DateEntry


class FilmesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Filmes Assistidos")

        # Criando os elementos da interface
        label_nome_filme = tk.Label(root, text="Nome do Filme:")
        label_nome_filme.grid(row=0, column=0, padx=10, pady=(40, 5), sticky="w")
        self.entry_nome_filme = tk.Entry(root)
        self.entry_nome_filme.grid(row=0, column=1, padx=10, pady=(40, 5), sticky="ew")

        label_ano_estreia = tk.Label(root, text="Ano de Estréia:")
        label_ano_estreia.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_ano_estreia = tk.Entry(root)
        self.entry_ano_estreia.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        label_genero = tk.Label(root, text="Gênero:")
        label_genero.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        generos = ["Ação", "Comédia", "Drama", "Romance", "Ficção Científica", "Terror"]
        self.combo_genero = ttk.Combobox(root, values=generos)
        self.combo_genero.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        label_producao_av = tk.Label(root, text="Produção Áudio Visual: ")
        label_producao_av.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tipo_producao = ["Filme", "Série", "Documentário"]
        self.combo_audio_visual = ttk.Combobox(root, values=tipo_producao)
        self.combo_audio_visual.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        label_data_assistido = tk.Label(root, text="Assistido em:")
        label_data_assistido.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.cal_data_assistido = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.cal_data_assistido.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Botão para salvar o filme
        button_salvar = tk.Button(root, text="Salvar Filme", command=self.salvar_filme)
        button_salvar.grid(row=5, column=0, columnspan=2, padx=10, pady=(18, 8), sticky="we")

        # Configurando o redimensionamento dinâmico dos elementos
        root.grid_rowconfigure(5, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def salvar_filme(self):
        nome_filme = self.entry_nome_filme.get()
        ano_estreia = self.entry_ano_estreia.get()
        genero = self.combo_genero.get()
        data_assistido = self.cal_data_assistido.get()
        producao = self.combo_audio_visual.get()

        confirmacao = messagebox.askyesno("Confirmação", f"Por favor, confirme os dados:\n\n"
                                                         f"Nome do Filme: {nome_filme}\n"
                                                         f"Ano de Estréia: {ano_estreia}\n"
                                                         f"Gênero: {genero}\n"
                                                         f"Data Assistido: {data_assistido}\n"
                                                         f"Produção Audio-Visual: {producao}\n\n"
                                                         f"Os dados estão corretos?")
        if confirmacao:
            conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'SERVER=localhost\SQLEXPRESS;;'
                                  'DATABASE=master;'
                                  'Trusted_Connection=yes;')
            cursor = conn.cursor()

        # Insere o registro do filme assistido na tabela correspondente
            cursor.execute("INSERT INTO Filmes (UserID, NomeFilme, AnoEstreia, Genero, DataAssistido, TipoProducao) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, nome_filme, ano_estreia, genero, data_assistido, producao))

            conn.commit()
            conn.close()
            messagebox.showinfo("Filme Assistido", "Filme assistido foi armazenado com sucesso!")
            self.proximo_filme()

    def proximo_filme(self):
        proximo = messagebox.askyesno("Inserir Novo Filme", "Deseja inserir outro filme?")
        if proximo:
            # Limpa os campos para inserção de um novo filme
            self.entry_nome_filme.delete(0, tk.END)
            self.entry_ano_estreia.delete(0, tk.END)
            self.combo_genero.set('')
            self.combo_audio_visual.set('')
            self.cal_data_assistido.set_date(None)
        else:
            self.root.destroy()


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login")

        # Criando os rótulos e campos de entrada para login
        label_username = tk.Label(root, text="Usuário:")
        label_username.grid(row=0, column=0, padx=10, pady=5)
        self.entry_username = tk.Entry(root)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        label_password = tk.Label(root, text="Senha:")
        label_password.grid(row=1, column=0, padx=10, pady=5)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        # Definindo os botões para login, cadastro e alterar senha
        button_login = tk.Button(root, text="Login", command=self.login)
        button_login.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="WE")

        button_cadastrar = tk.Button(root, text="Cadastrar", command=self.cadastrar)
        button_cadastrar.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="WE")

        button_alterar_senha = tk.Button(root, text="Alterar Senha", command=self.alterar_senha)
        button_alterar_senha.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky="WE")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

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
            global user_id
            user_id = row[0]  # Obtém o UserID do resultado da consulta
            messagebox.showinfo("Login", "Login bem sucedido!")
            cursor.close()  # Fecha o cursor
            conn.close()    # Fecha a conexão com o banco de dados
            self.root.withdraw()  # Esconde a janela de login
            self.filmes_app = FilmesApp(tk.Toplevel(self.root))  # Mantém uma referência à instância de FilmesApp

        else:
            messagebox.showerror("Login", "Usuário ou senha incorretos.")

            cursor.close()  # Fecha o cursor
            conn.close()    # Fecha a conexão com o banco de dados

    def cadastrar(self):
        # Abre uma nova janela para cadastro
        cadastro_window = tk.Toplevel(self.root)
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

            cursor.close()  # Fecha o cursor
            conn.close()    # Fecha a conexão com o banco de dados

        button_salvar_cadastro = tk.Button(cadastro_window, text="Salvar", command=salvar_cadastro)
        button_salvar_cadastro.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

    def alterar_senha(self):
        # Abre uma nova janela para alterar a senha
        alterar_senha_window = tk.Toplevel(self.root)
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

            cursor.close()  # Fecha o cursor
            conn.close()    # Fecha a conexão com o banco de dados

        button_salvar_alteracao_senha = tk.Button(alterar_senha_window, text="Salvar", command=salvar_alteracao_senha)
        button_salvar_alteracao_senha.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")


root = tk.Tk()
app = LoginApp(root)
root.mainloop()



