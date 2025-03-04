import os
import subprocess

git_objects_path = "/home/YOUR-USER/path-to-file/.git/objects"

if not os.path.exists(git_objects_path):
    print("[-] Caminho inválido! Verifique se está dentro do repositório Git.")
    exit()

pastas = [p for p in os.listdir(git_objects_path) if len(p) == 2 and os.path.isdir(os.path.join(git_objects_path, p))]

objetos_encontrados = set()
trees_encontradas = []

print("[*] Encontradas {} pastas de objetos Git!\n".format(len(pastas)))

for pasta in pastas:
    pasta_path = os.path.join(git_objects_path, pasta)
    arquivos = os.listdir(pasta_path)

    for arquivo in arquivos:
        hash_completo = "{}{}".format(pasta, arquivo)

        if hash_completo in objetos_encontrados:
            continue

        objetos_encontrados.add(hash_completo)

        try:
            resultado_tipo = subprocess.run(
                ["git", "cat-file", "-t", hash_completo],
                capture_output=True, text=True, timeout=3
            )
            tipo_objeto = resultado_tipo.stdout.strip()

            if resultado_tipo.stderr:
                print("[-] Erro no hash {}: {}".format(hash_completo, resultado_tipo.stderr.strip()))
                continue

        except Exception as e:
            print("[-] Erro ao processar {}: {}".format(hash_completo, e))
            continue

        print("[+] {} ({})".format(hash_completo, tipo_objeto))

        if tipo_objeto == "tree":
            trees_encontradas.append(hash_completo)

        if tipo_objeto == "blob":
            try:
                resultado_conteudo = subprocess.run(
                    ["git", "cat-file", "-p", hash_completo],
                    capture_output=True, text=True, timeout=3
                )
                conteudo = resultado_conteudo.stdout.strip()

                if conteudo:
                    print("--- Conteúdo do {} ---".format(hash_completo))
                    print(conteudo[:500])
                    print("---------------------------------------\n")

            except Exception as e:
                print("[-] Erro ao processar {}: {}".format(hash_completo, e))

print("\n[ + ] - LISTANDO OS TREE")
for tree_hash in trees_encontradas:
    print("[ + ] - LISTANDO TREE - {}".format(tree_hash))

    try:
        resultado_tree = subprocess.run(
            ["git", "ls-tree", "-r", tree_hash],
            capture_output=True, text=True, timeout=5
        )
        tree_conteudo = resultado_tree.stdout.strip()

        if tree_conteudo:
            print(tree_conteudo)
            print("---------------------------------------\n")

    except Exception as e:
        print("[-] Erro ao listar tree {}: {}".format(tree_hash, e))
