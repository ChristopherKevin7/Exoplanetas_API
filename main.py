#Importando as bibliotecas
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from backend import API_Exoplanetas
import time

#Declarando as cores
co0 = "#FFFFFF"
co1 = "#333333"
co2 = "#3b3b3b"

class interface:
    def __init__(self, screen):
        #Criando a janela    
        self.screen = screen
        self.screen.title('Exoplanetas')
        self.screen.geometry('1280x700')
        self.screen.configure(bg=co2)
        self.screen.columnconfigure(0, weight=1)
        self.screen.columnconfigure(1, weight=1)
        self.screen.columnconfigure(2, weight=1)
        self.screen.columnconfigure(3, weight=1)
        self.screen.columnconfigure(4, weight=1)
        self.screen.rowconfigure(0, weight=1)
        self.screen.rowconfigure(1, weight=1)
        self.screen.rowconfigure(2, weight=1)
        self.screen.rowconfigure(3, weight=1)
        self.screen.rowconfigure(4, weight=1)
        self.screen.rowconfigure(5, weight=1)
        self.screen.rowconfigure(6, weight=1)
        self.screen.rowconfigure(7, weight=1)
        
        titulo = Label(screen, text= "NASA", font=('Ivy 40 bold'), bg= co2, fg= co0)
        titulo.grid(row= 0, column= 2)
        
        btn_exoplanetas = Button(screen, text= "Exoplanetas", command= self.loading)
        btn_exoplanetas.grid(row= 6, column= 2)
        
    def loading(self):
        # Limpar a tela
        for widget in self.screen.winfo_children():
            widget.destroy()
        # Mostrar a janela de carregamento
        loading_window = LoadingWindow(self.screen)
        messagebox.showinfo("Aguarde", "Os exoplanetas estão sendo carregados, aguarde um momento.")
        
        self.exoplanetas(loading_window)
        
    def exoplanetas(self, loading):
        
        # Puxando a classe API_Nasa
        self.API = API_Exoplanetas()
        
        #Receber a lista de exoplanetas
        self.exoplanetas_originais = self.API.obter_nomes_exoplanetas()
        
         # Fechar a janela de carregamento
        loading.fechar()

        messagebox.showinfo("Concluído", "Os exoplanetas foram carregados com sucesso!")
        
        # Criar um LabelFrame para os exoplanetas
        self.frame_exoplanetas = LabelFrame(self.screen, text="Lista de Exoplanetas", bg=co2, fg=co0, font=('Arial', 12, 'bold'))
        self.frame_exoplanetas.grid(row=1, column=1, columnspan=3, rowspan=5, padx=10, pady=10, sticky="nsew")
        
        # Criar a barra de pesquisa
        self.entry_pesquisa = Entry(self.frame_exoplanetas)
        self.entry_pesquisa.pack(side=RIGHT, padx=5, pady=5, fill='x')
        self.entry_pesquisa.bind('<KeyRelease>', self.pesquisar_exoplanetas)
        
        # Criar a lista de exoplanetas dentro do LabelFrame
        self.lista_exoplanetas = Listbox(self.frame_exoplanetas)
        self.lista_exoplanetas.pack(fill=BOTH, expand=True)
        
        # Carregar os exoplanetas na lista
        self.carregar_exoplanetas(self.exoplanetas_originais) 

    def carregar_exoplanetas(self, exoplanetas):
        self.lista_exoplanetas.delete(0, END)
        for nome in exoplanetas:
            self.lista_exoplanetas.insert(tk.END, nome)
        
        # Vinculando um evento de clique à lista de exoplanetas
        self.lista_exoplanetas.bind("<Double-1>", self.exibir_detalhes)
            
    def pesquisar_exoplanetas(self, Event):
        texto_pesquisa = self.entry_pesquisa.get().lower()
        exoplanetas_filtrados = [exoplaneta for exoplaneta in self.exoplanetas_originais if exoplaneta.lower().startswith(texto_pesquisa)]
        self.carregar_exoplanetas(exoplanetas_filtrados)
        
    def exibir_detalhes(self, event):
        print("Na função exibir_exoplaneta")
        # Obtendo o índice do item clicado
        index = self.lista_exoplanetas.curselection()[0]

        # Obtendo o texto do item clicado
        nome_planeta = self.lista_exoplanetas.get(index)
        print(nome_planeta)

        # Chamando uma função para exibir os detalhes do planeta clicado
        self.info = self.API.detalhes_exoplanetas(nome_planeta)
        
        if self.info:
            # Crie uma nova janela para exibir os detalhes
            self.detalhes_window = tk.Toplevel(self.screen)
            self.detalhes_window.title("Detalhes do Exoplaneta")
            self.detalhes_window.geometry("500x600")
            self.detalhes_window.configure(bg='#FFFFFF')

            # Adicione rótulos para cada informação do exoplaneta
            self.text_detalhes = Text(self.detalhes_window, wrap="word")
            self.text_detalhes.pack(expand=True, fill="both")

            self.scrollbar = Scrollbar(self.detalhes_window, orient="vertical", command=self.text_detalhes.yview)
            self.scrollbar.pack(side="right", fill="y")

            self.text_detalhes.config(yscrollcommand=self.scrollbar.set)

            for chave, valor in self.info.items():
                self.text_detalhes.insert("end", f"{chave}: {valor}\n")
            self.text_detalhes.config(state="disabled")

            # Botão para fechar a janela de detalhes
            btn_fechar = Button(self.detalhes_window, text="Fechar", command=self.detalhes_window.destroy)
            btn_fechar.pack(pady=20)
        else:
            # Exiba uma mensagem se os detalhes do exoplaneta não foram encontrados
            messagebox.showwarning("Aviso", f"Detalhes para o exoplaneta '{nome_planeta}' não encontrados.")
    
class LoadingWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Carregando...")
        self.window.configure(bg= co0)
        
         # Configurar a geometria para centralizar a janela
        window_width = 200
        window_height = 100
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        geometry_string = f"{window_width}x{window_height}+{x}+{y}"
        self.window.geometry(geometry_string)
        
        self.window.transient(parent)
        self.window.grab_set()

        self.label = tk.Label(self.window, text="Carregando dados...")
        self.label.pack(pady=20)

    def fechar(self):
        self.window.destroy()

#configurando a janela

if __name__ == "__main__":
    screen = tk.Tk()
    app = interface(screen)
    screen.mainloop()