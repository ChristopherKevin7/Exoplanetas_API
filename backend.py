#Importando as bibliotecas
import json
import urllib.request

class API_Exoplanetas:
    def __init__(self):
        #Recebendo a API da NASA de exoplanetas
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+pscomppars&format=json"
        response = urllib.request.urlopen(url)
        self.result = json.loads(response.read())
        
    def obter_nomes_exoplanetas(self):
        nomes = [exoplaneta['pl_name'] for exoplaneta in self.result]
        return nomes
    
    def detalhes_exoplanetas(self, nome):
        self.nome_pl = nome
        for exoplaneta_info in self.result:
            if exoplaneta_info['pl_name'] == self.nome_pl:
                info_pl = {
                    "Nome planeta": exoplaneta_info.get('pl_name'),
                    "Nome de anfitrião": exoplaneta_info.get('hostname'),
                    "Carta do planeta": exoplaneta_info.get('pl_letter'),
                    "Nome da estrela (Catalogo Henry Draper)": exoplaneta_info.get('hd_name'),
                    "Nome da estrela (Catalogo Hipparcos)": exoplaneta_info.get('hip_name'),
                    "Nome da estrela (Catalogo TESS)": exoplaneta_info.get('tic_id'),
                    "Nome da estrela (Catalogo GAIA)": exoplaneta_info.get('gaia_id'),
                    "Numero de estrelas": exoplaneta_info.get('sy_snum'),
                    "Numero de planetas no sistema planetario": exoplaneta_info.get('sy_pnum'),
                    "numero de luas": exoplaneta_info.get('e_mnum'),
                    "Sistema binario": exoplaneta_info.get('cb_flag'),
                    "Metodo de descoberta": exoplaneta_info.get('discoverymethod'),
                    "Ano de descoberta": exoplaneta_info.get('disc_year'),
                    "Data de publicação da descoberta": exoplaneta_info.get('disc_pubdate'),
                    "Local de descoberta": exoplaneta_info.get('disc_locale'),
                    "Instalação de descoberta": exoplaneta_info.get('disc_facility'),
                    "Telescopio de descoberta": exoplaneta_info.get('disc_telescope'),
                    "Periodo de orbita (Dias)": exoplaneta_info.get('pl_orbper'),
                    "Raio do planeta (Unidade de raio da Terra)": exoplaneta_info.get('pl_rade'),
                    "Massa do planeta (Unidade de massa da Terra)": exoplaneta_info.get('pl_masse'),
                    "Densidade do planeta (g/cm³)": exoplaneta_info.get('pl_dens'),
                    "Temperatura de equlibrio (K)": exoplaneta_info.get('pl_eqt'),
                    "Temperatura efetiva estelar (K)": exoplaneta_info.get('st_teff'),
                    "Latitude Galatica": exoplaneta_info.get('glat'),
                    "Longitude Galatica": exoplaneta_info.get('glon'),
                    "Latitude Ecliptica": exoplaneta_info.get('elat'),
                    "Longitude Ecliptica": exoplaneta_info.get('elon'),
                    "Brilho da estrela hospedeira (Magnitude B)": exoplaneta_info.get('e_bmag'),
                    "Ultima atualização": exoplaneta_info.get('rowupdate'),
                    "Publicação dos parametros": exoplaneta_info.get('pl_pubdate'),
                    "Data de divulgação pelo Arquivo de Exoplanetas da NASA": exoplaneta_info.get('releasedate'),
                }
                
                return info_pl
        return None
    
class API_Missoes:
    def __init__(self):
        #Recebendo a API da NASA de missôes
        url = "https://osdr.nasa.gov/geode-py/ws/api/missions"
        response = urllib.request.urlopen(url)
        self.result = json.loads(response.read())
        
    def obter_missoes(self):
        #Recebe a url de cada missão e seleciona apenas o nome da missão ao final
        nomes_missoes = [missoes['mission'].split('/')[-1] for missoes in self.result['data']]
        return nomes_missoes
    
    def detalhes_missao(self, missao):
        url_missao = f"https://osdr.nasa.gov/geode-py/ws/api/mission/{missao}"
        response_missao = urllib.request.urlopen(url_missao)
        self.result_missao = json.loads(response_missao.read())
        
        # Extrair o nome do veículo da URL
        if 'vehicle' in self.result_missao and isinstance(self.result_missao['vehicle'], dict):
            veiculo_url = self.result_missao['vehicle'].get('vehicle', '')
            if veiculo_url:
                nome_veiculo = veiculo_url.split('/')[-1]
            else:
                nome_veiculo = "Informação sobre o veículo não disponível"
        else:
            nome_veiculo = "Informação sobre o veículo não disponível"
        
        # Criar uma lista para armazenar os detalhes de cada pessoa
        pessoas = []
        for pessoa in self.result_missao["people"]:
            pessoa_info = pessoa.get('person', {})
            if pessoa_info:
                detalhes_pessoa = {
                    "Instituição": pessoa.get("institution", "Informação não disponível"),
                    "Função": ', '.join(pessoa.get("roles", [])),
                    "Nome": f"{pessoa_info.get('firstName', '')} {pessoa_info.get('middleName', '')} {pessoa_info.get('lastName', '')}",
                    "Email": pessoa_info.get("emailAddress", "Informação não disponível"),
                    "Telefone": pessoa_info.get("phone", "Informação não disponível"),
                }
                pessoas.append(detalhes_pessoa)
            else:
                print("Informações da pessoa não encontradas para este item.")

        detalhes_missao = {
            "id": self.result_missao["id"],
            "identificador": self.result_missao["identifier"],
            "Aliases": self.result_missao["aliases"],
            "Data de inicio": self.result_missao["startDate"],
            "Data de término": self.result_missao["endDate"],
            "Arquivos": self.result_missao["files"],
            "Veiculo": nome_veiculo,
            "Pessoas": pessoas,
            
        }
        
        return detalhes_missao
    
    def detalhes_veiculos(self, nome_veiculo):
        url_veiculo = f" https://osdr.nasa.gov/geode-py/ws/api/vehicle/{nome_veiculo}"
        response_veiculo = urllib.request.urlopen(url_veiculo)
        self.detalhes = json.loads(response_veiculo.read())
        
        arquivos = []

        # Verificar se a lista de arquivos está vazia
        if self.detalhes["files"]:
            for arquivo in self.detalhes["files"]:
                detalhes_arquivo = {
                    "id": arquivo.get("id", "Informação não disponível"),
                    "Arquivo completo": arquivo.get("fullPath", "Informação não disponível"),
                    "Subcategoria": arquivo.get("subcategory", "Informação não disponível"),
                    "Descrição": arquivo.get("description", "Informação não disponível"),
                    "Categoria": arquivo.get("category", "Informação não disponível")
                }
                arquivos.append(detalhes_arquivo)
        else:
            arquivos = "Sem mais informações a respeito do veículo"

        
        detalhes_veiculo = {
            "id": self.detalhes["id"],
            "identificador": self.detalhes["identifier"],
            "esID": self.detalhes["esID"],
            "Arquivos": arquivos,
            
        }
        
        return detalhes_veiculo