from sqlalchemy import text
from db import get_db_connection_myzonego
from utils import JSONEncoder
import json

def get_all_customers():
    engine = get_db_connection_myzonego()
    
    with engine.connect() as connection:
        # Utilizar la conexión para realizar consultas y operaciones en la base de datos
        result = connection.execute(text("SELECT id, name, url_portal FROM customers"))
        customers_list = []
        for row in result:
            item = {
                "id": row[0],
                "name": row[1],
                "url_portal": row[2]
            }
            customers_list.append(item)

        customers = json.loads(JSONEncoder().encode(customers_list))
        return customers

def get_client_by_id(id):
    engine = get_db_connection_myzonego()
    
    with engine.connect() as connection:
        # Utilizar la conexión para realizar consultas y operaciones en la base de datos
        query = text("SELECT * FROM customers WHERE id = :id")
        result = connection.execute(query, {"id": id})
        customer_result = []
        for row in result:
            item = {
                "id": row[0],
                "name": row[1],
                "url_portal": row[2]
            }
            customer_result.append(item)
        customer = json.loads(JSONEncoder().encode(customer_result))
        return customer

def get_clubs_by_id_customer(id):
    engine = get_db_connection_myzonego()
    
    with engine.connect() as connection:
        # Utilizar la conexión para realizar consultas y operaciones en la base de datos
        query = text("SELECT id, name from clubs WHERE client_id = :id")
        result = connection.execute(query, {"id": id})

        clubs_list = []
        for row in result:
            item = {
                "id": row[0],
                "club": row[1],
            }
            clubs_list.append(item)
        # Acceder a los resultados
        print(type(clubs_list))
        print(clubs_list)
        clubs = json.loads(JSONEncoder().encode(clubs_list))

        return clubs

def get_contents_type_video_by_id_club( id_club):
    id_content_video = 2 # Id de los contenidos de videos en la zona privada
    engine = get_db_connection_myzonego()
    
    with engine.connect() as connection:
        # Utilizar la conexión para realizar consultas y operaciones en la base de datos
        query = text("SELECT id, content_type_id, club_id from contents WHERE content_type_id = 2 AND club_id = :id_club")
        result = connection.execute(query, {"id_club": id_club})

        content_type_video_list = []
        for row in result:
            item = {
                "id": row[0],
                "content_type": row[1],
                "club_id": row[2],
            }
            content_type_video_list.append(item)
        # Acceder a los resultados
        print(type(content_type_video_list))
        print(content_type_video_list)
        video_list = json.loads(JSONEncoder().encode(content_type_video_list))

        return video_list

def get_url_content_video(id_content):
    print(id_content)
    engine = get_db_connection_myzonego()
    
    with engine.connect() as connection:
        # Utilizar la conexión para realizar consultas y operaciones en la base de datos
        query_image_id = text("SELECT image_id from content_images WHERE content_id = :id_content")
        result_query_image_id = connection.execute(query_image_id, {"id_content": id_content})
        id_image = result_query_image_id.fetchone()[0]
        print(id_image)

        # obtener el image_id como avriable y pasarla
        query_url_video = text("SELECT * from images WHERE id = :id_image")
        result_query_url_video = connection.execute(query_url_video , {"id_image": id_image})

        # result = result_query_url_video.fetchall()

        url_list = []
        for row in result_query_url_video:
            item = {
                # "id": row[0],
                "url": row[1],
            }
            url_list.append(item)
        print(result_query_url_video)

        url_video_list = json.loads(JSONEncoder().encode(url_list))
        print(url_video_list)
        return url_video_list

def get_urls_video_by_customer(customer_id):
    engine = get_db_connection_myzonego()

    with engine.connect() as connection:
        # Obtener la informacion del cliente
        query_customer = text("SELECT id, name, url_portal FROM customers WHERE id=:customer_id")
        result_customer = connection.execute(query_customer, {"customer_id": customer_id})
        customer = result_customer.fetchone()
        client_id = customer[0]
        customer_name = customer[1]
        customer_url_portal = customer[2]

        print(customer_name, customer_url_portal)
        
        # Obtener los clubs del cliente
        query_clubs = text("SELECT id, name FROM clubs WHERE client_id = :customer_id")
        result_clubs = connection.execute(query_clubs, {"customer_id": customer_id})
        
        video_urls = []
        urls = []

        for club_row in result_clubs:
            club_id = club_row[0]
            club_name = club_row[1]

            # Obtener los contenidos de video para el club
            query_contents = text("SELECT id FROM contents WHERE content_type_id = 2 AND club_id = :club_id")
            result_contents = connection.execute(query_contents, {"club_id": club_id})

            for content_row in result_contents:
                content_id = content_row[0]
                # print(content_id)

                # Obtener el image_id para cada contenido
                query_image_id = text("SELECT image_id FROM content_images WHERE content_id = :content_id")
                result_image_id = connection.execute(query_image_id, {"content_id": content_id})
                image_id_row = result_image_id.fetchone()

                if image_id_row:
                    image_id = image_id_row[0]

                # Obtener la URL del video para cada image_id
                query_url_video = text("SELECT name FROM images WHERE id = :image_id")
                result_url_video = connection.execute(query_url_video, {"image_id": image_id})
                url = result_url_video.fetchone()
                if url:
                    url_video = url[0]
                name_video = url_video.split('/')[-1]
                
                # video_urls.append(name_video)
                video_urls.append({
                    "url": customer_url_portal,
                    "zona": customer_name,
                    "club": club_name,
                    "content_id": f"content{content_id}",
                    "video": name_video
                })
                # se agregan las urls de los videos del client
                urls.append({
                    "client_id" : client_id,
                    "club_id" : club_id,
                    "club": f"{club_name.split('_')[0]}",
                    "content_id": content_id,
                    "url_video": f"https://{customer_url_portal}/storage/{customer_name}/{club_name}/content{content_id}/image/{name_video}",
                })
        return urls