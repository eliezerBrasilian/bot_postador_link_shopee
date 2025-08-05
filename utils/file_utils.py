import os
async def salvar_arquivo(file_obj):
    pasta = "comprovantes"
    os.makedirs(pasta, exist_ok=True)

    # se for documento (PDF ou outro)
    if hasattr(file_obj, "file_name") and file_obj.file_name:
        nome_arquivo = file_obj.file_name
    else:
        # padrão: imagem ou sem nome → salva com .jpg
        nome_arquivo = f"{file_obj.file_unique_id}.jpg"

    caminho = os.path.join(pasta, nome_arquivo)

    novo_arquivo = await file_obj.get_file()
    await novo_arquivo.download_to_drive(caminho)
    return caminho
