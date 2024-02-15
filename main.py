#Importando as bibliotecas
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from backend import API_Exoplanetas
from backend import API_Missoes

#Declarando as cores
co0 = "#FFFFFF"
co1 = "#333333"
co2 = "#3b3b3b"

class interface:
    def __init__(self, screen):
        #Criando a janela    
        self.screen = screen
        self.screen.title('Nasa')
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
        
        btn_missoes = Button(screen, text= "Missões", font=('Ivy 16 bold'), command= self.loading_miss)
        btn_missoes.grid(row= 5, column= 2, padx=30, pady=40, sticky="nsew")
        
        btn_exoplanetas = Button(screen, text= "Exoplanetas", font=('Ivy 16 bold'), command= self.loading_exo)
        btn_exoplanetas.grid(row= 6, column= 2, padx=30, pady=40, sticky="nsew")
        
    def loading_miss(self):
        # Limpar a tela
        for widget in self.screen.winfo_children():
            widget.destroy()
        # Mostrar a janela de carregamento
        loading_window = LoadingWindow(self.screen)
        messagebox.showinfo("Aguarde", "As missões estão sendo carregadas, aguarde um momento.")
        
        self.missoes(loading_window)
        
    def missoes(self,loading):
        
        #Puxando a classe API_Missoes
        self.API_miss = API_Missoes()
        self._missoes = self.API_miss.obter_missoes()
        
         # Fechar a janela de carregamento
        loading.fechar()

        messagebox.showinfo("Concluído", "As missões foram carregadas com sucesso!")
        
         # Adicionar botão para retornar ao menu principal
        btn_menu_principal = Button(screen, text="Menu Principal", command=self.voltar_menu_principal)
        btn_menu_principal.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        # Criar um LabelFrame para os missoes
        self.frame_missoes = LabelFrame(self.screen, text="Lista de missões", bg=co2, fg=co0, font=('Arial', 12, 'bold'))
        self.frame_missoes.grid(row=1, column=1, columnspan=3, rowspan=5, padx=10, pady=10, sticky="nsew")
        
        # Criar a barra de pesquisa
        self.entry_pesquisa = Entry(self.frame_missoes)
        self.entry_pesquisa.pack(side=RIGHT, padx=5, pady=5, fill='x')
        self.entry_pesquisa.bind('<KeyRelease>', self.pesquisar_missoes)
        
        # Criar a lista de missoes dentro do LabelFrame
        self.lista_missoes = Listbox(self.frame_missoes)
        self.lista_missoes.pack(fill=BOTH, expand=True)
        
        # Carregar os exoplanetas na lista
        self.carregar_missoes(self._missoes) 
        
        
    def carregar_missoes(self, missoes):
        self.lista_missoes.delete(0, END)
        for nome in missoes:
            self.lista_missoes.insert(tk.END, nome)
        
        # Vinculando um evento de clique à lista de exoplanetas
        self.lista_missoes.bind("<Double-1>", self.exibir_detalhes_miss)
        
    def pesquisar_missoes(self, event):
        texto_pesquisa = self.entry_pesquisa.get().lower()
        missoes_filtradas = [missoes for missoes in self._missoes if missoes.lower().startswith(texto_pesquisa)]
        self.carregar_missoes(missoes_filtradas)

    def exibir_detalhes_miss(self, event):
        # Obtendo o índice do item clicado
        index = self.lista_missoes.curselection()[0]

        # Obtendo o texto do item clicado
        missao = self.lista_missoes.get(index)

        # Chamando uma função para exibir os detalhes do planeta clicado
        self.info = self.API_miss.detalhes_missao(missao)
        
        if self.info:
            # Crie uma nova janela para exibir os detalhes
            self.detalhes_window = tk.Toplevel(self.screen)
            self.detalhes_window.title("Detalhes da Missão")
            self.detalhes_window.geometry("500x600")
            self.detalhes_window.configure(bg='#FFFFFF')

            # Adicione rótulos para cada informação do exoplaneta
            self.text_detalhes = Text(self.detalhes_window, wrap="word")
            self.text_detalhes.pack(expand=True, fill="both")

            self.scrollbar = Scrollbar(self.detalhes_window, orient="vertical", command=self.text_detalhes.yview)
            self.scrollbar.pack(side="right", fill="y")

            self.text_detalhes.config(yscrollcommand=self.scrollbar.set)

            for chave, valor in self.info.items():
                # Verifica se a chave é 'Pessoas'
                if chave == 'Pessoas':
                    self.text_detalhes.insert("end", f"{chave}:\n")
                    # Itera sobre a lista de pessoas e exibe suas informações
                    for pessoa in valor:
                        pessoa_nome = pessoa.get("Nome")
                        pessoa_papel = pessoa.get("Função")
                        pessoa_instituicao = pessoa.get("Instituição")
                        pessoa_email = pessoa.get("Email")
                        pessoa_telefone = pessoa.get("Telefone")
                        self.text_detalhes.insert("end", f"    Nome: {pessoa_nome}\n")
                        self.text_detalhes.insert("end", f"    Função: {pessoa_papel}\n")
                        self.text_detalhes.insert("end", f"    Instituição: {pessoa_instituicao}\n")
                        self.text_detalhes.insert("end", f"    Email: {pessoa_email}\n")
                        self.text_detalhes.insert("end", f"    Telefone: {pessoa_telefone}\n\n")
                else:
                    # Insere as outras informações da missão
                    self.text_detalhes.insert("end", f"{chave}: {valor}\n")

            self.text_detalhes.config(state="disabled")

            # Botão para fechar a janela de detalhes
            btn_fechar = Button(self.detalhes_window, text="Fechar", command=self.detalhes_window.destroy)
            btn_fechar.pack(side= "left", pady=20, padx=15)
            
            #Botão para saber mais sobre o veiculo utilizado na missão
            nome_veiculo = self.info.get("Veiculo")  
            btn_veiculo = Button(self.detalhes_window, text="Veiculo", command=lambda: self.Veiculo(nome_veiculo))
            btn_veiculo.pack(side= "right", pady=20, padx=15)
        else:
            # Exiba uma mensagem se os detalhes do exoplaneta não foram encontrados
            messagebox.showwarning("Aviso", f"Detalhes para a missão '{missao}' não encontrados.")
            
    def Veiculo(self, nome_veiculo):
        if nome_veiculo == "Informação sobre o veículo não disponível":
            messagebox.showwarning("Aviso", "Não existem informações a respeito deste veiculo.")
            
        else:
            self.info_veiculo = self.API_miss.detalhes_veiculos(nome_veiculo)
            
            if self.info_veiculo:
                # Crie uma nova janela para exibir os detalhes
                self.detalhes_window = tk.Toplevel(self.screen)
                self.detalhes_window.title("Detalhes do " + nome_veiculo)
                self.detalhes_window.geometry("500x600")
                self.detalhes_window.configure(bg='#FFFFFF')

                # Adicione rótulos para cada informação do exoplaneta
                self.text_detalhes = Text(self.detalhes_window, wrap="word")
                self.text_detalhes.pack(expand=True, fill="both")

                self.scrollbar = Scrollbar(self.detalhes_window, orient="vertical", command=self.text_detalhes.yview)
                self.scrollbar.pack(side="right", fill="y")

                self.text_detalhes.config(yscrollcommand=self.scrollbar.set)

                for chave, valor in self.info_veiculo.items():
                     # Verifica se a chave é 'Arquivos'
                    if chave == 'Arquivos':
                        if valor != "Sem mais informações a respeito do veículo":
                            self.text_detalhes.insert("end", f"{chave}:\n")
                            # Itera sobre a lista de Arquivos e exibe suas informações
                            for veiculo in valor:
                                veiculo_id = veiculo.get("id")
                                arquivo_completo = veiculo.get("Arquivo Completo")
                                subcategoria = veiculo.get("Subcategoria")
                                descricao = veiculo.get("Descrição")
                                categoria = veiculo.get("Categoria")
                                self.text_detalhes.insert("end", f"    ID: {veiculo_id}\n")
                                self.text_detalhes.insert("end", f"    Arquivo completo: {arquivo_completo}\n")
                                self.text_detalhes.insert("end", f"    Subcategoria: {subcategoria}\n")
                                self.text_detalhes.insert("end", f"    Descrição: {descricao}\n")
                                self.text_detalhes.insert("end", f"    Categoria: {categoria}\n\n")
                        else:
                            self.text_detalhes.insert("end", f"Arquivos: {valor}")
                    else:
                        # Insere as outras informações da missão
                        self.text_detalhes.insert("end", f"{chave}: {valor}\n")
                        
                self.text_detalhes.config(state="disabled")

                # Botão para fechar a janela de detalhes
                btn_fechar = Button(self.detalhes_window, text="Fechar", command=self.detalhes_window.destroy)
                btn_fechar.pack(pady=20)
            else:
                # Exiba uma mensagem se os detalhes do exoplaneta não foram encontrados
                messagebox.showwarning("Aviso", f"Detalhes para o veiculo '{nome_veiculo}' não encontrados.")
            

    def loading_exo(self):
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
        
         # Adicionar botão para retornar ao menu principal
        btn_menu_principal = Button(screen, text="Menu Principal", command=self.voltar_menu_principal)
        btn_menu_principal.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
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
        self.lista_exoplanetas.bind("<Double-1>", self.exibir_detalhes_exo)
            
    def pesquisar_exoplanetas(self, Event):
        texto_pesquisa = self.entry_pesquisa.get().lower()
        exoplanetas_filtrados = [exoplaneta for exoplaneta in self.exoplanetas_originais if exoplaneta.lower().startswith(texto_pesquisa)]
        self.carregar_exoplanetas(exoplanetas_filtrados)
        
    def exibir_detalhes_exo(self, event):
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
            
    def voltar_menu_principal(self):
        # Limpar a tela e recriar os elementos do menu principal
        for widget in self.screen.winfo_children():
            widget.destroy()
        self.__init__(self.screen)
    
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