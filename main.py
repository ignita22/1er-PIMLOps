from fastapi import FastAPI
import pandas as pd
import numpy as np

app = FastAPI()

@app.get('/userdata/{user_id}')
def userdata(user_id):
    df_user_items_id = df_user_items_final[df_user_items_final['user_id']==user_id]['item_id']
    respuesta = ''

    items = df_user_items_id.values
    precios =  []
    for i in items:
        precio = df_steam_games[df_steam_games['id']== i]['price2']
        if not precio.empty:
            precios.append(precio.values[0])

    df_user_reviews_id = df_user_reviews_final[df_user_reviews_final['user_id']==user_id]['recommend']

    j = 0
    for i in df_user_reviews_id.values:
        if(i == True):
            j = j + 1

    recomendacion = j/len(df_user_reviews_id.values)*100

    suma = 0

    for precio in precios:
        suma += precio

    item_count = df_user_items_final[df_user_items_final['user_id']=='js41637']['items_count'].iloc[0]

    respuesta = {'recomendación:': recomendacion,
                'Cantidad de dinero:' : suma,
                'Cantidad de items': item_count}

    return respuesta

@app.get('/count_reviews/{fecha1}')

def count_reviews(fecha1, fecha2):
    df_user_fechas=df_user_reviews_final[['user_id']][df_user_reviews_final['fecha']
                                                  .between(fecha1, fecha2)].value_counts()

    primeros_valores = df_user_fechas.index.get_level_values('user_id').tolist()

    recomendaciones = []
    for i in primeros_valores:
        recomendacion = (userdata(i)[list(userdata(i).keys())[0]])
        recomendaciones.append(recomendacion)

    respuesta = {'usuario': primeros_valores, 'recomendación':recomendaciones}

    df = pd.DataFrame(respuesta)

    respuesta = df.to_dict(orient='records')

    return respuesta

# AQUÍ VA LA 3° FUNCIÓN 


@app.get('/genre/{genero}')

def genre(genero):
    try:
        df = pd.read_csv('rankgenres.csv')
        rank = df[df['genero'] == genero]['Rank'].values[0]
    except:
        rank = 'Genero no existe'
    return rank

@app.get('/user_for_genre/{genero}')

def user_for_genre(genero):
  """
  Devuelve una lista de los 5 usuarios principales para el género especificado.

  Args:
    genero: El género.

  Returns:
    Una lista de los 5 usuarios principales para el género especificado.
  """

  # Obtiene los juegos del género especificado.
  df_steam_games_generos = df_steam_games[df_steam_games['genres'].apply(lambda generos: genero in generos)]
  juegos = df_steam_games_generos['id'].values

  # Obtiene los usuarios que han jugado los juegos del género especificado.
  df_user_items_final_genres = df_user_items_final[df_user_items_final['item_id'].isin(juegos)]

  # Agrupa los usuarios por ID y suma su tiempo de juego total para cada juego.
  df_top_users = df_user_items_final_genres[['user_id', 'user_url', 'playtime_forever']].groupby(['user_id', 'user_url']).sum('playtime_forever')

  # Obtiene los 5 usuarios principales ordenados por tiempo de juego total.
  df_top_users = df_top_users.sort_values('playtime_forever', ascending=False).head(5)

  # Convierte el DataFrame a una lista de diccionarios.
  respuesta = df_top_users.to_dict(orient='records')

  return respuesta

@app.get('/free_cont/{fila}')

def free_cont(fila):
    if(fila['total gratis']==0.0):
        return 0.0
    else:
        return round((fila['total gratis']/fila['total'])*100,2)