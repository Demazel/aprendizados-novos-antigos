while True:

    import pandas as pd

    df_modelos = pd.read_csv('modelos\modelos.csvn', sep=';')

    print(df_modelos)

    add_modelo = input('deseja adicionar um novo modelo? (s/n)')
    
    print(add_modelo)


    if add_modelo == 's':
        id = input('informe o id')
        modelo = input('inform o modelo')
        companhia = input('informe a companhia')
        capacidade = input('informe a capacidade')
        ano_fabricacao = input('informe o ano de frabricao')

        novo_modelo1 = {
            'id':id,
            'modelo':modelo,
            'companhia':companhia,
            'capacidade':capacidade,
            'ano_fabricacao':ano_fabricacao
        }

        df_modelos = pd.concat([df_modelos, pd.DataFrame([novo_modelo1])], ignore_index= True)

        df_modelos.to_csv('modelos.csv', sep = ';', index = False)
    
    else:
        print('saindo do sistema...')
        break