from minio import Minio
from minio.error import S3Error
from time import sleep

# Connexion au cluster MinIO via Nginx
def con():
    client = Minio(
        "localhost:19000",  # Adresse Nginx
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    return client

def create_bucket(client):
    # Créer un bucket s'il n'existe pas
    bucket_name = "my-bucket"
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' créé.")
    else:
        print(f"Bucket '{bucket_name}' existe déjà.")
    return bucket_name

# Charger un fichier
def upload_file(client, objets, bucket_name):
    try:
        for item in objets:
            # Créer un fichier temporaire pour l'exemple
            with open(item, "w") as f:
                f.write("Minio, fichier")  # Exemple de contenu dans le fichier

            # Télécharger le fichier
            client.fput_object(bucket_name, item, item)
            print(f"Fichier '{item}' téléchargé dans le bucket '{bucket_name}'.")
    except S3Error as e:
        print(f"Erreur lors du chargement de l'objet {item}: {e}")

# Télécharger un fichier
def download_file(client, bucket_name, object_name, file_path):
    try:
        client.fget_object(bucket_name, object_name, file_path)
        print(f"Objet {object_name} téléchargé avec succès dans {file_path}.")
    except S3Error as e:
        print(f"Erreur lors du téléchargement de l'objet {object_name}: {e}")

# Lister les fichiers dans le bucket
def file_list(client, bucket_name):
    print("Fichiers dans le bucket :")
    for obj in client.list_objects(bucket_name):
        print(obj.object_name)

# Suppression fichier
def delete_file(client, bucket_name, object_name):
    try:
        client.remove_object(bucket_name, object_name)
        print(f"Objet {object_name} supprimé avec succès.")
    except S3Error as e:
        print(f"Erreur lors de la suppression de l'objet {object_name}: {e}")

if __name__ == "__main__":
    client = con()
    objets = ['texte.txt']  # Liste des fichiers à télécharger
    bucket_name = create_bucket(client)
    upload_file(client, objets, bucket_name)
    file_list(client, bucket_name)
    sleep(3)
    download_file(client, bucket_name='my-bucket', object_name='texte.txt', file_path='image/texte.txt')
    sleep(3)
    delete_file(client, bucket_name='my-bucket', object_name='text.txt')
