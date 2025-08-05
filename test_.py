from outros import obtemTextoQuebrado,obtem_tags_a_partir_do_produto

nomes = obtemTextoQuebrado(nome = "MICRO-ONDAS LG EASY CLEAN 30 LITROS BRANCO")
print(nomes.get("primeiro_nome"))


print("teste 2")
print(obtem_tags_a_partir_do_produto("inverno"))
print(obtem_tags_a_partir_do_produto("guarda-roupa"))
print(obtem_tags_a_partir_do_produto("guarda roupa"))
