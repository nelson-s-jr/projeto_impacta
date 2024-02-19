import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry

def salvar_filme():
    nome_filme = entry_nome_filme.get()
    ano_estreia = entry_ano_estreia.get()
    genero = combo_genero.get()
    data_assistido = cal_data_assistido.get()
    producao = combo_audio_visual.get()

    # Verificar se o gênero selecionado está na lista de gêneros válidos
    if genero not in generos:
        messagebox.showerror("Erro", "Por favor, selecione um gênero válido.")
        return
    
    if producao not in tipo_producao:
        messagebox.showerror("Erro", "Por favor, selecione um gênero válido.")
        return

    confirmacao = messagebox.askyesno("Confirmação", f"Por favor, confirme os dados:\n\n"
                                                     f"Nome do Filme: {nome_filme}\n"
                                                     f"Ano de Estréia: {ano_estreia}\n"
                                                     f"Gênero: {genero}\n"
                                                     f"Data Assistido: {data_assistido}\n\n"
                                                     f"Os dados estão corretos?")
    if confirmacao:
        filmes.append((nome_filme, ano_estreia, genero, data_assistido))
        proximo_filme()



def proximo_filme():
    proximo = messagebox.askyesno("Inserir Novo Filme", "Deseja inserir outro filme?")
    if proximo:
        # Limpa os campos para inserção de um novo filme
        entry_nome_filme.delete(0, tk.END)
        entry_ano_estreia.delete(0, tk.END)
        combo_genero.set('')
        cal_data_assistido.set_date(None)
    else:
        escrever_arquivo()
        root.destroy()

def escrever_arquivo():
    with open("filmes.txt", "w") as f:
        for filme in filmes:
            f.write(f"Nome do Filme: {filme[0]}\n")
            f.write(f"Ano de Estréia: {filme[1]}\n")
            f.write(f"Gênero: {filme[2]}\n")
            f.write(f"Data Assistido: {filme[3]}\n\n")

# Lista para armazenar os filmes inseridos
filmes = []

def abrir_janela_filmes():
    root = tk.Toplevel()
    root.title("Registro de Filmes Assistidos")

    # Ajustando o tamanho da janela
    root.geometry("400x300")

    # Criando os rótulos e campos de entrada
    label_nome_filme = tk.Label(root, text="Nome do Filme:")
    label_nome_filme.grid(row=0, column=0, padx=10, pady=(40, 5), sticky="w")
    entry_nome_filme = tk.Entry(root)
    entry_nome_filme.grid(row=0, column=1, padx=10, pady=(40, 5), sticky="ew")

    label_ano_estreia = tk.Label(root, text="Ano de Estréia:")
    label_ano_estreia.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_ano_estreia = tk.Entry(root)
    entry_ano_estreia.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    label_genero = tk.Label(root, text="Gênero:")
    label_genero.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    generos = ["Ação", "Comédia", "Drama", "Romance", "Ficção Científica", "Terror"]
    combo_genero = ttk.Combobox(root, values=generos)
    combo_genero.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    label_producao_av = tk.Label(root, text="Produção Áudio Visual: ")
    label_producao_av.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tipo_producao = ["Filme", "Série", "Documentário"]
    combo_audio_visual = ttk.Combobox(root, values=tipo_producao)
    combo_audio_visual.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    label_data_assistido = tk.Label(root, text="Assistido em:")
    label_data_assistido.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    cal_data_assistido = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
    cal_data_assistido.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # Botão para salvar o filme
    button_salvar = tk.Button(root, text="Salvar Filme", command=salvar_filme)
    button_salvar.grid(row=5, column=0, columnspan=2, padx=10, pady=(18, 8), sticky="we")

    # Configurando o redimensionamento dinâmico dos elementos
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Iniciando o loop principal
    root.mainloop()
