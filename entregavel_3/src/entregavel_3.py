import json
import pandas as pd 

def readFile():

    """
        Funcao que faz a leitura dos dados disponivelem arquivo data.json.
    """
    
    # leitura do arquivo salvo no diretorio
    with open("../files/data.json") as data_json:
        data = json.load(data_json)
    
    # Retorno
    return data

def dataProcessing(data_json):

    """
        Funcao que faz o tratamento dos dados:
        - Carrega os dados em um dicionario.
        - Faz a normalizacao dos dados direto do dicionario criado com os dados.
        - Gera dataframe com dados normalizado, concatena para fazer o incremento dos dados.
    """
    
    # criar dicionario vazio
    dict_json = {}
    dict_raw = {}

    # dataframes
    df = pd.DataFrame()
    df_temp01 = pd.DataFrame()
    df_temp02 = pd.DataFrame()

    # gera dicionario com os dados
    for data in data_json:

        # retorno de chave e valor
        for chave,valor in data.items():

            dict_json[chave] = valor

        # incrementa dicionario temporario
        dict_raw["CreateDate"] = dict_json["CreateDate"]
        dict_raw["EmissionDate"] = dict_json["EmissionDate"]
        dict_raw["Discount"] = dict_json["Discount"]
        dict_raw["NFeNumber"] = dict_json["NFeNumber"]
        dict_raw["NFeID"] = dict_json["NFeID"]

        # gerar lista do dicionario de ItemList
        lista_ProductName = []
        lista_Value = []
        lista_Quantity = []

        # append na lista - normaliza os dados
        for x in range(0, len(dict_json["ItemList"])):
            lista_ProductName.append(dict_json["ItemList"][x]["ProductName"])
            lista_Value.append(dict_json["ItemList"][x]["Value"])
            lista_Quantity.append(dict_json["ItemList"][x]["Quantity"])
        
        # adiciona lista ao dicionario
        dict_raw["ProductName"] = lista_ProductName
        dict_raw["Value"] = lista_Value
        dict_raw["Quantity"] = lista_Quantity

        # gerar dataframe incremental
        if (df_temp01.empty):
            df_temp01 = pd.DataFrame(dict_raw)
            df = df_temp01
        else:
            df_temp02 = pd.DataFrame(dict_raw)
            df = pd.concat([df, df_temp02], ignore_index = True)

    # gerar arquivo .csv
    df.to_csv("../files/data_json_full_normalizado.csv")

def dataProcessing_2(data_json):

    """
        Funcao que o tratamento dos dados:
        - Gera um dicionario com os dados.
        - Usando a funcao do .json_normalize() do pandas faz a normalizacao dos dados.
        - Gera dois dataframe, um sem a normalizacao dos dados, e outro com a normalizacao dos dados.
        - Faz o concat() para incrementar os dados.
    """

    # dicionario vazio
    dict_json = {}

    # dataframes
    df_temp01 = pd.DataFrame()
    df_temp03 = pd.DataFrame()

    # gerar dicionario
    for data in data_json:
        dict_json = data
        
        # dataframe nao normalizado incremental
        if (df_temp01.empty):
            df_temp01 = pd.DataFrame(dict_json)
            df = df_temp01
        else:
            df_temp02 = pd.DataFrame(dict_json)
            df = pd.concat([df, df_temp02], ignore_index = True)

        # datafrae normalizado incremental
        if (df_temp03.empty):
            df_temp03 = pd.json_normalize(dict_json, record_path=["ItemList"],
                                meta=["NFeNumber","NFeID"])
            df_new = df_temp03
        else:
            df_temp04 = pd.json_normalize(dict_json, record_path=["ItemList"],
                                meta=["NFeNumber","NFeID"])
            df_new = pd.concat([df_new, df_temp04], ignore_index = True)

    # dataframe com dados "nao" normalizado
    df.to_csv("../files/data_json_nao_normalizado.csv")

    # datafrae com dados noralizado
    df_new.to_csv("../files/data_json_normalizado.csv")

##------------------------------------------------------##

if __name__ == "__main__":

    # funcao para ler dados do .json
    data = readFile()

    # processamento dos dados
    dataProcessing(data)

    # processamento dos dados - formato mais simples
    dataProcessing_2(data)

