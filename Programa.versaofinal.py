import re
from datetime import datetime
import mysql.connector
import sys

# Conexão com o banco de dados
def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="jaiminh0Bonit0",
            database="loja_bolos"
        )
        #cursorbd = db.cursor()
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados:", err)
        exit()

conn = conectar()

#Funções
def selecao_produto(conn):
    
    try:
        #cursorbd = db.cursor()
        
        produto_selecao = int(input('Digite o código do produto: '))
    except:
        print('O código deve ser um número inteiro.')
        return

    cursorbd = conn.cursor()

    cursorbd.execute('''SELECT id_produto, qtd_produto FROM tbl_produtos WHERE id_produto = %s''', (produto_selecao,))
        
    resultado_produto = cursorbd.fetchone()
        
    if not resultado_produto:
        print('Produto não encontrado.')
        return None
            
    id_produto, qtd_produto = resultado_produto

    try:
        qtd_selecao = int(input('Digite a quantidade: '))
    except ValueError:
        print('Digite um número inteiro válido.')
        return None

    
    if qtd_selecao <= 0:
        print('Quantidade deve ser maior que zero.')
        return None
            
    if qtd_selecao > qtd_produto:
        print(f'Indisponível. Estoque atual: {qtd_produto}')
        return None

    novo_estoque = qtd_produto - qtd_selecao
    cursorbd.execute('''UPDATE tbl_produtos SET qtd_produto = %s WHERE id_produto = %s''', (novo_estoque, id_produto)) #ATUALIZA A TABELA PRODUTOS
        
    conn.commit()
    print(f'Compra realizada! Novo estoque: {novo_estoque}')
    return id_produto, qtd_selecao


def cadastrar_produto(conn):
    cursorbd = None
    try:
        cod_produto = int(input('Digite o código do produto:'))
        produto_nome = input('Digite o nome do produto: ')
        produto_descricao = input('Digite a descrição do produto: ')
        preco_produto = float(input('Digite o preço do produto: '))
        produto_qtd = int(input('Digite a quantidade do produto: '))
        produto_categoria = input('Digite a categoria do produto: ')
        
        cursorbd = conn.cursor(buffered=True)

        cursorbd.execute('SELECT id_produto FROM tbl_produtos WHERE id_produto = %s', (cod_produto,))

        resultado_cadastro_produto = cursorbd.fetchone()

        if not resultado_cadastro_produto:
            comando = '''INSERT INTO tbl_produtos(id_produto, nome_produto, descricao_produto, preco_produto, qtd_produto, categoria_produto) 
            VALUES (%s, %s, %s, %s, %s, %s)'''
            cursorbd.execute(comando, (cod_produto, produto_nome, produto_descricao, preco_produto, produto_qtd, produto_categoria))
            conn.commit()
            print('Produto', produto_nome, 'inserido com sucesso.')
        else:
            print('Produto já existente.')

    except ValueError:
        print("Erro: Digite valores numéricos válidos para código, preço e quantidade!")
    
    except mysql.connector.Error as erro:
        print(f"Erro no banco de dados: {erro}")
        conn.rollback()

    finally:
        if cursorbd:
            cursorbd.close()
        

#Essa função está funcionando
def deletar_produto(conn):
    cursorbd = None
    try:
        cod_produto = int(input('Digite o código do produto a ser deletado:'))
        
        cursorbd = conn.cursor(buffered=True)

        cursorbd.execute('SELECT id_produto FROM tbl_produtos WHERE id_produto = %s', (cod_produto,))
        
        resultado_delecao = cursorbd.fetchone()

        if not resultado_delecao:
            print('Produto', cod_produto, 'não existe.')
            return
        
        print('Produto localizado.')
        resposta = input('Deseja deletar o produto '+str(cod_produto)+'?. Se sim, digite S').upper()
        if resposta == 'S':
            comando = 'DELETE FROM tbl_produtos WHERE id_produto = %s'
            cursorbd.execute(comando, (cod_produto,))
            conn.commit()
            print('Produto', cod_produto, 'deletado com sucesso.')
        else:
            print('Deleção não processada.')

    except ValueError:
        print("Erro: Digite valores numéricos válidos para código, preço e quantidade!")
    
    except mysql.connector.Error as erro:
        print(f"Erro no banco de dados: {erro}")
        conn.rollback()

    finally:
        if cursorbd:
            cursorbd.close()
        

#Essa função está funcionando
def atualizar_produto(conn):
    cursorbd = None
    try:       
        produto_atualiza = input('Digite o código do produto: ')
        qtd_atualiza = int(input('Digite a nova quantidade: '))

        cursorbd = conn.cursor(buffered = True)
            
        cursorbd.execute('''SELECT id_produto, qtd_produto FROM tbl_produtos WHERE id_produto = %s''', (produto_atualiza,))
            
        resultado_produto = cursorbd.fetchone()
            
        if not resultado_produto:
            print('Produto não encontrado.')
            return  
 
        print('Produto localizado.')

        confirma_atualiza = input('Deseja atualizar o produto '+str(produto_atualiza)+'. Se sim, digite s').upper()
        
        if confirma_atualiza == 'S':
            comando = '''UPDATE tbl_produtos SET qtd_produto = %s WHERE id_produto = %s''' #ATUALIZA A TABELA PRODUTOS

            cursorbd.execute(comando, (qtd_atualiza, produto_atualiza))    
            conn.commit()
            print(f'Estoque atualizado!')
        else:
            print('Alteração não realizada.')
                
    except ValueError:
        print("Digite um número válido para a quantidade!")
    
    except mysql.connector.Error as erro:
        print(f"Erro no banco de dados: {erro}")
        conn.rollback()

    finally:
        if cursorbd:
            cursorbd.close()

# Funções de validação
def validar_login(login):
    return re.match(r'^[a-zA-Z0-9_]{4,20}$', login) is not None

def validar_senha(senha):
    return senha.isdigit() and len(senha) == 6

def validar_nome(nome):
    return len(nome.strip().split()) >= 2

def validar_telefone(telefone):
    padrao = r'^\(\d{2}\)\d{5}-\d{4}$'
    return re.match(padrao, telefone) is not None

def validar_data(data):
    try:
        datetime.strptime(data, '%Y/%m/%d')
        return True
    except ValueError:
        return False


# Cadastro do usuário
def cadastrar_usuario(conn):
    while True:
        usuario_login = input('Digite o seu login de usuário (letras/números, 4-20 caracteres): ')
        if not validar_login(usuario_login):
            print("Login inválido. Use apenas letras, números ou _ (mín. 4 caracteres).")
            continue
        
        cursorbd = conn.cursor()

        cursorbd.execute('SELECT * FROM tbl_usuarios WHERE login_usuario = %s', (usuario_login,))
        if cursorbd.fetchone():
            print('Erro: Este ID de usuário já está em uso.')
            continue
        break

    while True:
        usuario_nome = input('Digite seu nome e sobrenome: ')
        if not validar_nome(usuario_nome):
            print("Por favor, insira nome e sobrenome.")
            continue
        break

    while True:
        usuario_senha = input('Digite uma senha numérica de 6 dígitos: ')
        if not validar_senha(usuario_senha):
            print("Senha inválida. Deve conter exatamente 6 dígitos numéricos.")
            continue
        break

    while True:
        usuario_telefone = input('Digite seu telefone no formato: (DDD) XXXXX-XXXX ')
        if not validar_telefone(usuario_telefone):
            print("Formato de telefone inválido.")
            continue
        break

    comando = '''INSERT INTO tbl_usuarios(nome_usuario, login_usuario, telefone_usuario, senha_usuario)
                 VALUES (%s, %s, %s, %s)'''
    valores = (usuario_nome, usuario_login, usuario_telefone, usuario_senha)

    cursorbd.execute(comando, valores)
    conn.commit()

    return usuario_login


def alterar_dado(conn):
    cursorbd = None
    try:
        cursorbd = conn.cursor(buffered=True)
        id_usuario = input('Digite seu id de usuário: ')
        senha_alterada = input('Digite sua nova senha: ')

        try:
            comando = 'UPDATE tbl_usuarios SET senha_usuario = %s WHERE id_usuario = %s' #ATUALIZA A TABELA USUARIOS
            cursorbd.execute(comando, (senha_alterada, id_usuario))
            conn.commit() #Confirma alteraçao no banco
            print('Senha atualizada com sucesso')

        except mysql.connector.Error as erro:
            print(f'Erro: {erro}')
            conn.rollback()

    finally:
        if cursorbd:
            cursorbd.close()


def verificar_login(conn):
    while True:
        digite_login = input('Digite seu login de usuário: ')
        with conn.cursor(buffered=True) as cursorbd:
            cursorbd.execute('SELECT * FROM tbl_usuarios WHERE login_usuario = %s', (digite_login,))
            resultado_login = cursorbd.fetchone()

            if resultado_login is None:
                print('Usuário', digite_login, 'não localizado.')
            else:
                print('Usuário', digite_login, 'localizado.')
                break  # Sai do loop quando o login é encontrado

    while True:
        digite_senha = input('Digite sua senha: ')
        with conn.cursor(buffered=True) as cursorbd_senha:
            # Verifica se a senha corresponde ao login específico
            cursorbd_senha.execute(
                'SELECT * FROM tbl_usuarios WHERE login_usuario = %s AND senha_usuario = %s',
                (digite_login, digite_senha)
            )
            resultado_senha = cursorbd_senha.fetchone()

            if resultado_senha:
                print('Senha correta.')
                return digite_login  # Retorna o login após validação completa
            else:
                print('Senha incorreta.')
                altera_senha = input('Deseja alterar sua senha? (S/N): ').upper()
                if altera_senha == 'S':
                    alterar_dado(conn)
                else:
                    print('Login não realizado.')
                    return None 
        

def menu_produtos(conn):
    cursorbd = None
    try:
        cursorbd = conn.cursor(buffered = True)
        cursorbd.execute("SELECT id_produto, nome_produto, descricao_produto, preco_produto FROM tbl_produtos;") #SELECIONA A TABELA PRODUTOS
        resultados_produtos = cursorbd.fetchall()

        print("\nID | Nome do Produto                 | Descrição                                                    | Preço")
        print("-" * 111)

        for resultado_produto in resultados_produtos:
            id_produto, nome_produto, descricao_produto, preco_produto = resultado_produto

                #Converte decimal para float
            preco_formatado = float(preco_produto)
                
            print(f"{id_produto:2} | {nome_produto:31} | {descricao_produto:60} | R${preco_formatado:>7.2f}") 

    except mysql.connector.Error as e:
        print(f"Erro ao acessar produtos: {e}")
    finally:
        if cursorbd:
            cursorbd.close()


#Programa
check_admin = input('Olá! Seja bem-vindo(a) ao site Cake Tech. Você é um administrador? Digite S ou N.').upper()

login_verificado = False
estoque_verificado = False
usuario_logado = None

while True:
    if check_admin == 'S':
        if not login_verificado:           
            usuario_logado = verificar_login(conn)
            login_verificado = True

            while True:
                resposta_adm = input('Deseja fazer alterações no estoque? Digite S ou N.').upper()
                
                if resposta_adm == 'S':
                    menu = menu_produtos(conn) 
                    try:
                        selecao_alteracao = int(input('Digite uma das opções: 1 - Cadastrar produto, 2 - Deletar produto, 3 - Atualizar produto '))
                        if selecao_alteracao == 1:
                            produto_cadastro = cadastrar_produto(conn)
                            menu = menu_produtos(conn) 
                        elif selecao_alteracao == 2:
                            delecao_produto = deletar_produto(conn)
                            menu = menu_produtos(conn) 
                        elif selecao_alteracao == 3:
                            atualiza_produto = atualizar_produto(conn)
                            menu = menu_produtos(conn) 
                        else:
                            print('Opção não localizada.')
                            #break
                    except:
                        print('A opção escolhida deve ser um numéro inteiro.')
                else:
                    print('Ok, saindo do estoque.')
                    sys.exit()        

    else:
        print('Ok. Saindo do estoque. ')
        break


check_cadastro = input('Você já tem cadastro? Digite S ou N.').upper()

if check_cadastro == 'N':
    resposta_usuario = input('Deseja fazer o seu cadastro agora? Digite S ou N.').upper()
    if resposta_usuario == 'S':
        usuario_logado = cadastrar_usuario(conn)
        print('Usuario cadastrado com sucesso. Confira nossos produtos.')
    else:
        print('Ok, talvez na próxima.')
else:
    usuario_logado = verificar_login(conn)


#Mostrar produtos e preço

usuario_validar = input('Deseja ver nossa lista de produtos? Digite S ou N.').upper()
menu_produtos(conn) 

# Carrinho de compras
carrinho = []

produto_usuario = input('Deseja adicionar produtos? S/N: ').upper()

while produto_usuario == 'S':
    produto_selecao = selecao_produto(conn)

    if produto_selecao: 
        id_produto, qtd_selecionada = produto_selecao
        carrinho.append({'Produto': id_produto, 'Quantidade': qtd_selecionada})
    
    produto_usuario = input('Deseja adicionar mais produtos? S/N: ').upper()

print('Carrinho final:', carrinho)

# Finalização do pedido
if not carrinho:
    print("Nenhum item no carrinho. Pedido não realizado.")
else:
    if usuario_logado:
        cursorbd = conn.cursor(buffered=True)
        try:
            # Parte 1: Processamento do pedido e atualização de estoque
            cursorbd.execute('SELECT id_usuario FROM tbl_usuarios WHERE login_usuario = %s', (usuario_logado,))
            resultado_usuario = cursorbd.fetchone()

            if not resultado_usuario:
                print("Erro: usuário não encontrado.")
            else:
                id_usuario = resultado_usuario[0]
                valor_total = 0
                qtd_total = 0

                # Processar cada item do carrinho
                for item in carrinho:
                    id_produto = item['Produto']
                    qtd = item['Quantidade']
                    qtd_total += qtd

                    # Verificar estoque e preço
                    cursorbd.execute('SELECT preco_produto, qtd_produto FROM tbl_produtos WHERE id_produto = %s', (id_produto,))
                    produto_info = cursorbd.fetchone()

                    if not produto_info:
                        print(f"Produto {id_produto} não encontrado.")
                        continue

                    preco_unitario, estoque_atual = produto_info

                    if qtd > estoque_atual:
                        print(f"Quantidade solicitada de {id_produto} excede o estoque.")
                        continue

                    # Atualizar cálculos e estoque
                    valor_total += preco_unitario * qtd
                    novo_estoque = estoque_atual - qtd
                    cursorbd.execute('UPDATE tbl_produtos SET qtd_produto = %s WHERE id_produto = %s', 
                                    (novo_estoque, id_produto))

                # Inserir o pedido principal
                data_atual = datetime.now().strftime('%Y-%m-%d')
                cursorbd.execute(
                    '''INSERT INTO tbl_pedidos 
                    (data_pedido, valor_total, qtd_pedido, fk_tbl_usuarios_id_usuario) 
                    VALUES (%s, %s, %s, %s)''', 
                    (data_atual, valor_total, qtd_total, id_usuario)
                )
                id_pedido = cursorbd.lastrowid

                # Parte 2: Inserção na tabela de relacionamento (DENTRO DO BLOCO ELSE!)
                cursorbd_pedido = conn.cursor(buffered=True)
                try:
                    for item in carrinho:
                        id_produto = item['Produto']
                        cursorbd_pedido.execute(
                            '''INSERT INTO Relacionamento_3 
                            (fk_tbl_produtos_id_produto, fk_tbl_pedidos_id_pedido) 
                            VALUES (%s, %s)''',
                            (id_produto, id_pedido)
                        )
                finally:
                    cursorbd_pedido.close()

                # Commit único para todas as operações
                conn.commit()

                print(f"\nPedido #{id_pedido} realizado com sucesso! Valor total: R$ {valor_total:.2f}")

            print("\nEscolha a forma de pagamento:")
            print("1 - Cartão de Crédito")
            print("2 - Pix")
            print("3 - Boleto Bancário")

            while True:
                metodo_pagamento = input("Digite o número correspondente à forma de pagamento: ")

                if metodo_pagamento == "1":
                    print("Pagamento por cartão selecionado.")
                    print("Processando pagamento...")
                    print("\u2705 Pagamento aprovado com sucesso!")
                    break
                elif metodo_pagamento == "2":
                    print("Pagamento por Pix selecionado.")
                    print("Chave Pix: pagamentos@sitex.com.br")
                    input("Pressione Enter após efetuar o pagamento.")
                    print("\u2705 Pagamento confirmado!")
                    break
                elif metodo_pagamento == "3":
                    print("Pagamento por boleto selecionado.")
                    print("Gerando boleto...")
                    print("Seu boleto foi gerado com vencimento em 3 dias úteis.")
                    print("\u2705 Aguarde a confirmação após o pagamento.")
                    break
                else:
                    print("Opção inválida. Tente novamente.")

            print("\n✅ Compra finalizada com sucesso! Agradecemos pela preferência.")
        
        except mysql.connector.Error as e:
            print(f"Erro ao processar pedido: {e}")
            conn.rollback()  # Rollback de TODAS as operações em caso de erro
        finally:
            if cursorbd:
                cursorbd.close() 
    else:
        print("Erro: Usuário não está logado.")

if conn.is_connected():
    conn.close()
    print("Conexão ao MySQL encerrada")

