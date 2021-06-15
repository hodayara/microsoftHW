import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

try:
    print("Azure Blob Storage v" + __version__ )


    #-------Storage accounts 1 storagehodayahw1------

    #connect to Storage accounts 1 storagehodayahw1 with the connection string key
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = str(uuid.uuid4())

    # Create the container
    container_client = blob_service_client.create_container(container_name)
    # A local directory to hold blob data
    local_path = "./data"


     #-------Storage accounts 2 storagehodayahw2------

    #connect to Storage accounts 2 storagehodayahw2 with the connection string key
    connect_str2 = os.getenv('AZURE_STORAGE_CONNECTION_STRING2')

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client2 = BlobServiceClient.from_connection_string(connect_str2)

    # Create a name for the container
    container_name2 = "copy-from-a "+ str(uuid.uuid4())

    # Create the container
    container_client2 = blob_service_client2.create_container(container_name2)


    #------the copy code-------
    
    for i in range(100):
        # Create a file in the local data directory to upload and download
        local_file_name = str(uuid.uuid4()) + ".txt"
        upload_file_path = os.path.join(local_path, local_file_name)

        # Write text to the file
        file = open(upload_file_path, 'w')
        file.write("Hello, World! A")
        file.close()

        # Create a blob client using the local file name as the name for the blob - for Storage accounts 1 
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file to Storage accounts 1
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
        
        # Download the blob to a local file from Storage accounts 1
        # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
        download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
        print("\nDownloading blob to \n\t" + download_file_path)

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
    

        
        # Create a blob client using the local file name as the name for the blob - for Storage accounts 2
        local_download_file_path = str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt')
        blob_client2 = blob_service_client2.get_blob_client(container=container_name2, blob=local_download_file_path)


        # Upload the file to Storage accounts 2
        with open(download_file_path, "rb") as data:
            blob_client2.upload_blob(data)
           
except Exception as ex:
    print('Exception:')
    print(ex)