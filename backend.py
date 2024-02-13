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
        print("Na função exibir_detalhes_exoplaneta")
        self.nome_pl = nome
        print(self.nome_pl)
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