import Prestamos_DeFi as DeFi
from web3 import Web3
import json
from random import choice

def menu() -> int:
    '''Funcion encargada de mostrar el menu de opciones al usuario
    y tomar la opcion seleccionada por este'''
    
    print('\033[0;36m 1>> Seleccionar para dar\033[0;m' + '\033[3;32m ALTA a PRESTAMISTAS\033[0;m')
    print('\033[0;36m 2>> Seleccionar para dar\033[0;m' + '\033[3;32m ALTA a CLIENTES\033[0;m')
    print('\033[0;36m 3>> Seleccionar para\033[0;m' + '\033[3;32m DEPOSITAR GARANTIA\033[0;m')
    print('\033[0;36m 4>> Seleccionar para\033[0;m' + '\033[3;32m SOLICITAR PRESTAMO\033[0;m')
    print('\033[0;36m 5>> Seleccionar para\033[0;m' + '\033[3;32m APROBAR PRESTAMO\033[0;m')
    print('\033[0;36m 6>> Seleccionar para\033[0;m' + '\033[3;32m REEMBOLSAR PRESTAMO\033[0;m')
    print('\033[0;36m 7>> Seleccionar para\033[0;m' + '\033[3;32m LIQUIDAR GARANTIA\033[0;m')
    print('\033[0;36m 8>> Seleccionar para obtener\033[0;m' + '\033[3;32m PRESTAMOS por PRESTATARIO\033[0;m')
    print('\033[0;36m 9>> Seleccionar para obtener\033[0;m' + '\033[3;32m DETALLES de PRESTAMO\033[0;m')
    print('\033[0;36m 10>> Seleccionar para obtener\033[0;m' + '\033[3;32m LISTADO de PRESTAMISTAS\033[0;m')
    print('\033[0;36m 11>> Seleccionar para obtener\033[0;m' + '\033[3;32m LISTADO de CLIENTES\033[0;m')
    print('\033[0;36m 0>>\033[0;m' + '\033[0;31m Salir\033[0;m')
    try:
        opcion = int(input('Seleccione opcion >> '))
    except ValueError:
        print('Error: debe introducir un numero entero')
    else:
        return opcion


def cargar_contrato(ruta: str) -> dict:
    '''Funcion encargada de obtener los datos necesarios del contrato para poder
    desplegarlo en la blockchain a partir de su archivo json y devuelve un diccionario
    con los datos del abi y el bytecode'''
    
    data_contract = dict()
    try:
        archivo_json = open('DeFi-Python-Web3\PrestamoDeFi.json')
    except FileNotFoundError:
        return data_contract
    else:
        abi = json.load(archivo_json)['abi']
        archivo_json.close()
        archivo_json = open(ruta)
        bytecode = '0x' + json.load(archivo_json)['data']['bytecode']['object']
        data_contract['abi'] = abi
        data_contract['bytecode'] = bytecode
    finally:
        archivo_json.close()
    return data_contract


def encriptar_clave_privada(clave_privada: str) -> str:
    caracteres = 'a,e,i,o,u,A,Ä,á,B,C,D,E,Ë,é,F,G,H,I,Ï,í,J,K,L,M,O,Ö,ó,P,Q,R,S,T,U,Ü,ú,X,Y,Z,0,1,2,3,4,5,6,7,8,9,<,>,?,/,[,],{,},&,^,%,$,#,@,!,*,-,+,(,),_'.split(',')
    longitud = len(caracteres)
    caracteres_random = list()

    print(longitud)
    print(caracteres,'\n')
    for i in range(longitud):
        letra = choice(caracteres)
        indice = caracteres.index(letra)
        caracteres_random.append(caracteres.pop(indice))
        
    print(caracteres,'\n')
    print(caracteres_random)
    
    
def desencriptar_clave_privada():
    pass


def mostrar_cuentas(cuentas):
    for i in range(len(cuentas)):
            print(f'{i}>> {cuentas[i]}')
    print(f'{i + 1}>> Insertar manualmente')


def seleccionar_cuenta(cuentas) -> str:
    '''Funcion encargada de mostrar y seleccionar una cuenta de la blockchain'''
    cuenta = ''
    mostrar_cuentas(cuentas)
    try:
        indice = int(input('>>>> '))
    except ValueError:
        print()
        print(f'!!ERROR!! Introduce un numero entero del 0 al {len(cuentas)}')
        return ''
    else:
        if indice == len(cuentas):
                cuenta = input('>>>> ')
        else:
            try:
                cuenta = cuentas[indice] 
            except IndexError:
                print()
                print('!!ERROR!! Ha seleccionado un numero para una cuenta incorrecto')
                return ''
            
    return cuenta


def gestionar_clave_privada(cuenta_publica: str, web3: Web3) -> str:
        private_key = input('Clave Privada >>> ')
        direcc_publica = web3.eth.account.from_key(private_key)
        #print(direcc_publica.key.hex())
        #print(direcc_publica.address)
        try:
            assert(cuenta_publica == direcc_publica.address)
        except AssertionError:
            print('!!ERROR!! Su clave privada no coincide con la cuenta seleccionada')
            return ''
        else:
            return direcc_publica.key.hex()
            
            
def mostrar_prestamistas(listado_prestamistas: list):
    for i in range(len(listado_prestamistas)):
        print(f'{i} - > {listado_prestamistas[i]}')
        
        
def mostrar_clientes(listado_clientes: list):
    for i in range(len(listado_clientes)):
        print(f'{i} - > {listado_clientes[i]}')


def mostrar_id_prestamos(listado_prestamos: list):
    for i in range(len(listado_prestamos)):
            print(f'ID: {listado_prestamos[i]}')
            
    
def main():
    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    
    # Comprobar conexion con la blockchain Ganache
    if not web3.is_connected():
        print('\033[0;31m FALLO DE CONEXION\033[0;m')
        exit()   
    print('\033[0;32m CONEXION EXITOSA A GANACHE\033[0;m\n\n')
    
    # Cargar abi y bytecode del contrato 
    data_contract = cargar_contrato('DeFi-Python-Web3\PrestamoDeFi.json')
    if len(data_contract) != 2:
        print('\033[0;31mError al cargar los datos del contrato\033[0;m')
        exit()
    
    print('\033[0;32m DATOS DEL CONTRATO CARGADOS EXITOSAMENTE\033[0;m\n\n')
    
    cuentas = web3.eth.accounts # tupla de cuentas de Ganache
    
    while(True):
        print('***Selecciona la cuenta del administrador a utilizar***')
        admin = seleccionar_cuenta(cuentas)
        if admin != '':
            try:
                assert(admin in cuentas)
            except AssertionError:
                print('!!Error!! La cuenta introducida no esta registrada en la blockchain')
            else:
                break
        
    print('\033[0;31m!!!!Tenga en cuenta que debe introducir la clave privada de la cuenta seleccionada')
    print('!!!! la cual previamente sera encriptada y almacenada para mayor seguridad\033[0;m')
        
    while(True):
        private_key = gestionar_clave_privada(admin, web3)
        if private_key != '':
            break
        print('Inserte su clave privada')    
            
    # Desplegar el contrato
    PrestamoDeFi = web3.eth.contract(abi=data_contract['abi'], bytecode=data_contract['bytecode'])
    tx = PrestamoDeFi.constructor().build_transaction({
        'from': admin,
        'nonce': web3.eth.get_transaction_count(admin)
    })
    # Firmar la transaccion
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    # Enviar la transaccion a la blockchain Ganache
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Esperar a que se mine la transaccion y recibir el comprobante o recibo de la transaccion que contiene datos de la transaccion
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
    # Instanciar el contrato
    direccion_contrato = web3.to_checksum_address(tx_receipt.contractAddress)
    contract_DeFi = web3.eth.contract(address=direccion_contrato, abi=data_contract['abi'])
        
    # Interactuar con el contrato
    listado_prestamistas = list() # Listado de cuentas que son de alta como prestamistas
    listado_prestamistas.append(admin)
    prestamistas_claves = dict() # Diccionario de cuentas y sus respectivas claves privadas de prestamistas
    prestamistas_claves[admin] = private_key
    listado_clientes = list() # Listado de cuentas que son de alta como clientes
    clientes_claves = dict() # Diccionario de cuentas y sus respectivas claves privadas de clientes
    prestamos_por_clientes = dict() # Diccionario de cuentas de clientes y su listado de prestamos solicitados
    # Menu de opciones
    while(True):
        opcion = menu()
        if opcion == 1: # Dar de alta a prestamistas
            # Seleccionar al administrador
            while(True):
                print('\033[0;36mSelecciona la direccion del administrador\033[0;m')
                print(f'0>> {admin}')
                print('1>> Insertar manualmente')
                try:
                    opcion = int(input('>>>> '))
                except ValueError:
                    print('!!ERROR!! Introduce un numero entero entre 0 y 1')
                else:
                    if opcion != 0:
                        print('Inserte la cuenta administrativa manualmente')
                        aux_admin = input('>>>> ')
                    else:
                        aux_admin = admin
                        print(f'Administrador: {aux_admin}')
                    break
            try:
                assert(aux_admin == admin)
                assert(aux_admin in cuentas)
            except AssertionError:
                if aux_admin != admin:
                    message = '!!Error!! Esta utilizando una cuenta que no es la del administrador'
                else:
                    message = 'La cuenta introducida no esta registrada en la blockchain'
                print(f'!!Error!! {message}')
                continue
            
            # Seleccionar al prestamista
            while(True):
                print('\033[0;36mSelecciona la direccion para el prestamista\033[0;m')
                aux_prestamista = seleccionar_cuenta(cuentas)
                if aux_prestamista != '':
                    break
            try:
                assert(aux_admin != aux_prestamista)
                assert(aux_prestamista not in listado_prestamistas)
                assert(aux_prestamista in cuentas)
            except AssertionError:
                if aux_admin == aux_prestamista:
                    message = 'La cuenta a dar de alta no debe ser la misma que la cuenta del socio principal'
                elif aux_prestamista in listado_prestamistas:
                    message = 'La cuenta ya fue dada de alta como prestamista con anterioridad'
                else:
                    message = 'La cuenta introducida no esta registrada en la blockchain'
                print(f'!!ERROR!! {message}')
            else:
                print(aux_prestamista)
                clave_admin = prestamistas_claves[aux_admin]
                print(clave_admin)
                if DeFi.alta_prestamista(web3, contract_DeFi, aux_admin, clave_admin, aux_prestamista):
                    listado_prestamistas.append(aux_prestamista)
                
        elif opcion == 2: # Dar de alta a clientes
            # Seleccionar al prestamista
            while(True):
                print('\033[0;36mSelecciona la direccion para el prestamista\033[0;m')
                aux_prestamista = seleccionar_cuenta(listado_prestamistas)
                if aux_prestamista != '':
                    break
            try:
                assert(aux_prestamista in listado_prestamistas) 
            except AssertionError:
                print('!!Error!! Esta utilizando una cuenta que no se ha dado de alta como prestamista')
                continue
                
            print('\033[0;31m!!!!Tenga en cuenta que debe introducir la clave privada de la cuenta seleccionada')
            print('!!!! la cual previamente sera encriptada y almacenada para mayor seguridad\033[0;m')
        
            while(True):
                private_key = gestionar_clave_privada(aux_prestamista, web3)
                if private_key != '':
                    break
                print('Inserte su clave privada')
            
            # Guardar la clave del prestamista en el diccionario
            if aux_prestamista not in prestamistas_claves:
                prestamistas_claves[aux_prestamista] = private_key
            
            # Seleccionar al cliente que se dara de alta
            while(True):
                print('\033[0;36mSelecciona la direccion para el cliente\033[0;m')
                aux_cliente = seleccionar_cuenta(cuentas)
                if aux_cliente != '':
                    break  
            try:
                assert(aux_cliente not in listado_clientes)
                assert(aux_cliente in cuentas)
                assert(aux_cliente not in listado_prestamistas)
            except AssertionError:
                if aux_cliente in listado_clientes:
                    message = 'La cuenta ya fue dada de alta como cliente con anterioridad' 
                elif aux_cliente not in cuentas:
                    message = 'La cuenta introducida no esta registrada en la blockchain'
                else:
                    message = 'No se puede dar de alta a una cuenta cliente que sea una cuenta de prestamista'
                print(f'!!ERROR!! {message}')
            else:
                clave_prestamista = prestamistas_claves[aux_prestamista]
                if DeFi.alta_cliente(web3, contract_DeFi, aux_prestamista, clave_prestamista, aux_cliente):
                    listado_clientes.append(aux_cliente)
                
        elif opcion == 3: # Depositar Garantia
            # Seleccionar al cliente
            if len(listado_clientes) == 0:
                print('!!Warning!! No hay existencia de clientes dados de alta')
                continue
            while(True):
                print('\033[0;36mSelecciona la direccion para el cliente\033[0;m')
                aux_cliente = seleccionar_cuenta(listado_clientes)
                if aux_cliente != '':
                    break
            try:
                assert(aux_cliente in listado_clientes)
            except AssertionError:
                print('!!Error!! Esta utilizando una cuenta que no se ha dado de alta como cliente')
                continue
                
            print('\033[0;31m!!!!Tenga en cuenta que debe introducir la clave privada de la cuenta seleccionada')
            print('!!!! la cual previamente sera encriptada y almacenada para mayor seguridad\033[0;m')
            
            while(True):
                private_key = gestionar_clave_privada(aux_cliente, web3)
                if private_key != '':
                    break
                print('Inserte su clave privada')
            
            # Guardar la clave del cliente en el diccionario
            if aux_cliente not in clientes_claves:
                clientes_claves[aux_cliente] = private_key
                
            # Solicitar el monto de la garantia a depositar
            while(True):
                try:
                    monto_garantia = int(input('\033[0;36mIntroduce el monto de la garantia en\033[0;m' + '\033[3;36m ETHER>> \033[0;m'))
                    assert(monto_garantia > 0)
                except ValueError:
                    print('!!Error!! Valor incorrecto introduczca un numero entero')
                except AssertionError:
                    print('!!Error!! Introduce un monto mayor que 0')
                else:
                    break
                
            clave_cliente = clientes_claves[aux_cliente]
            DeFi.depositar_garantia(web3, contract_DeFi, aux_cliente, clave_cliente, monto_garantia)
            
        elif opcion == 4: # Solicitar Prestamo
            # Seleccionar al cliente
            if len(listado_clientes) == 0:
                print('!!Warning!! No hay existencia de clientes dados de alta')
                continue
            while(True):
                print('\033[0;36mSelecciona la direccion para el cliente\033[0;m')
                aux_cliente = seleccionar_cuenta(listado_clientes)
                if aux_cliente != '':
                    break
            try:
                assert(aux_cliente in listado_clientes)
            except AssertionError:
                print('!!Error!! Esta utilizando una cuenta que no se ha dado de alta como cliente')
                continue
                
            print('\033[0;31m!!!!Tenga en cuenta que debe introducir la clave privada de la cuenta seleccionada')
            print('!!!! la cual previamente sera encriptada y almacenada para mayor seguridad\033[0;m')
            
            while(True):
                private_key = gestionar_clave_privada(aux_cliente, web3)
                if private_key != '':
                    break
                print('Inserte su clave privada')
            
            # Guardar la clave del cliente en el diccionario
            if aux_cliente not in clientes_claves:
                clientes_claves[aux_cliente] = private_key
            
            print('\033[0;31m!!!!La cuenta seleccionada tenga en cuenta que debe haber depositado un monto de garantia')
            print('!!!! con anterioridad para poder solicitar prestamo o pueden ocasionarse errores en la aplicacion\033[0;m')
            
            confirmacion = input('¿Deseas continuar con el proceso? (y/n): ')
            if confirmacion.lower() != 'y':
                continue
                
            # Solicitar el monto y plazo del prestamo
            while(True):
                try:
                    monto = int(input('\033[0;36mIntroduce el monto a solicitar en \033[0;m' + '\033[3;36m ETHER>> \033[0;m'))
                    plazo = int(input('\033[0;36mIntroduce el plazo de tiempo en minutos para reembolsar el prestamo>> \033[0;m'))
                    assert (monto > 0 and plazo > 0) 
                except ValueError:
                    print('!!Error!! Introduce valores de entrada que sean numeros enteros')
                except AssertionError:
                    print('!Error! El monto y el plazo no pueden ser 0')
                else:
                    break
                
            clave_cliente = clientes_claves[aux_cliente]
            if DeFi.solicitar_prestamo(web3, contract_DeFi, aux_cliente, clave_cliente, monto, plazo):
                # Actualizar diccionario de listado de prestamos por clientes
                aux_lista_prestamos = prestamos_por_clientes.get(aux_cliente, [])
                aux_lista_prestamos.append(len(aux_lista_prestamos) + 1)
                prestamos_por_clientes[aux_cliente] = aux_lista_prestamos
            
        elif opcion == 5: # Aprobar prestamo
            # Seleccionar al prestamista
            while(True):
                print('\033[0;36mSelecciona la direccion para el prestamista\033[0;m')
                aux_prestamista = seleccionar_cuenta(listado_prestamistas)
                if aux_prestamista != '':
                    break
            try:
                assert(aux_prestamista in listado_prestamistas) 
            except AssertionError:
                print('!!Error!! Esta utilizando una cuenta que no se ha dado de alta como prestamista')
                continue
                
            print('\033[0;31m!!!!Tenga en cuenta que debe introducir la clave privada de la cuenta seleccionada')
            print('!!!! la cual previamente sera encriptada y almacenada para mayor seguridad\033[0;m')
        
            while(True):
                private_key = gestionar_clave_privada(aux_prestamista, web3)
                if private_key != '':
                    break
                print('Inserte su clave privada')
                
            # Guardar la clave del prestamista en el diccionario
            if aux_prestamista not in prestamistas_claves:
                prestamistas_claves[aux_prestamista] = private_key
            
            # Seleccionar al cliente que se le aprobara el prestamo
            if len(listado_clientes) == 0:
                print('!!Warning!! No hay existencia de clientes dados de alta')
                continue
            while(True):
                print('\033[0;36mSelecciona la direccion para el cliente\033[0;m')
                aux_cliente = seleccionar_cuenta(listado_clientes)
                if aux_cliente != '':
                    break
            try:
                assert(aux_cliente in listado_clientes)
                assert(len(prestamos_por_clientes.get(aux_cliente, [])) > 0)
            except AssertionError:
                if aux_cliente not in listado_clientes:
                    message = 'Esta utilizando una cuenta que no se ha dado de alta como cliente'
                else:
                    message = 'El cliente seleccionado no ha solicitado prestamos todavia'
                print(f'!!Error!! {message}')
                continue
            
            # Solicitar ID de prestamo para aprobar
            while(True):
                aux_lista_prestamos = prestamos_por_clientes[aux_cliente]
                print(f'Listado de ID de prestamos del cliente: {aux_cliente}')
                mostrar_id_prestamos(aux_lista_prestamos)
                try:
                    id_prestamo = int(input('\033[0;36mIntroduce el ID de prestamo que se va a aprobar>> \033[0;m'))
                    assert (id_prestamo > 0 and id_prestamo <= len(aux_lista_prestamos))
                except ValueError:        
                    print(f'!!ERROR!! Introduce un ID de entrada que sean un numero entero')
                except AssertionError:
                    print(f'!!Warning!! Un ID 0 o mayor que {len(aux_lista_prestamos)} no existe, esto puede ocasionar errores en la aplicacion')
                    confirmacion = input('¿Deseas continuar con su eleccion? (y/n): ')
                    if confirmacion.lower() == 'y':
                        break
                else:
                    break
                    
            clave_prestamista = prestamistas_claves[aux_prestamista]
            DeFi.aprobar_prestamo(web3, contract_DeFi, aux_prestamista, clave_prestamista, aux_cliente, id_prestamo)
                     
        elif opcion == 6: # Reembolsar prestamo
            # Seleccionar al cliente que se le aprobara el prestamo
            if len(listado_clientes) == 0:
                print('!!Warning!! No hay existencia de clientes dados de alta')
                continue
            while(True):
                print('\033[0;36mSelecciona la direccion para el cliente\033[0;m')
                aux_cliente = seleccionar_cuenta(listado_clientes)
                if aux_cliente != '':
                    break
            try:
                assert(aux_cliente in listado_clientes)
                assert(len(prestamos_por_clientes.get(aux_cliente, [])) > 0)
            except AssertionError:
                if aux_cliente not in listado_clientes:
                    message = 'Esta utilizando una cuenta que no se ha dado de alta como cliente'
                else:
                    message = 'El cliente seleccionado no ha solicitado prestamos todavia'
                print(f'!!Error!! {message}')
                continue
            
            print('\033[0;31m!!!!Tenga en cuenta que debe introducir la clave privada de la cuenta seleccionada')
            print('!!!! la cual previamente sera encriptada y almacenada para mayor seguridad\033[0;m')
            
            while(True):
                private_key = gestionar_clave_privada(aux_cliente, web3)
                if private_key != '':
                    break
                print('Inserte su clave privada')
            
            # Solicitar ID de prestamo para reembolsar
            while(True):
                aux_lista_prestamos = prestamos_por_clientes[aux_cliente]
                print(f'Listado de ID de prestamos del cliente: {aux_cliente}')
                mostrar_id_prestamos(aux_lista_prestamos)
                try:
                    id_prestamo = int(input('\033[0;36mIntroduce el ID de prestamo que se va a reembolsar>> \033[0;m'))
                    assert (id_prestamo > 0 and id_prestamo <= len(aux_lista_prestamos))
                except ValueError:        
                    print(f'!!ERROR!! Introduce un ID de entrada que sean un numero entero')
                except AssertionError:
                    print(f'!!Warning!! Un ID 0 o mayor que {len(aux_lista_prestamos)} no existe, esto puede ocasionar errores en la aplicacion')
                    confirmacion = input('¿Deseas continuar con su eleccion? (y/n): ')
                    if confirmacion.lower() == 'y':
                        break
                else:
                    break
            
            clave_cliente = clientes_claves[aux_cliente] 
            DeFi.reembolsar_prestamo(web3, contract_DeFi, aux_cliente, clave_cliente, id_prestamo) 

        elif opcion == 7: # Liquidar garantia
            # Seleccionar al prestamista
            while(True):
                print('\033[0;36mSelecciona la direccion para el prestamista\033[0;m')
                aux_prestamista = seleccionar_cuenta(listado_prestamistas)
                if aux_prestamista != '':
                    break
            try:
                assert(aux_prestamista in listado_prestamistas) 
            except AssertionError:
                print('!!Error!! Esta utilizando una cuenta que no se ha dado de alta como prestamista')
                continue
                
            print('\033[0;31m!!!!Tenga en cuenta que debe introducir la clave privada de la cuenta seleccionada')
            print('!!!! la cual previamente sera encriptada y almacenada para mayor seguridad\033[0;m')
        
            while(True):
                private_key = gestionar_clave_privada(aux_prestamista, web3)
                if private_key != '':
                    break
                print('Inserte su clave privada')
                
            # Guardar la clave del prestamista en el diccionario
            if aux_prestamista not in prestamistas_claves:
                prestamistas_claves[aux_prestamista] = private_key
            
            # Seleccionar al cliente que se le retirara la garantia
            if len(listado_clientes) == 0:
                print('!!Warning!! No hay existencia de clientes dados de alta')
                continue
            while(True):
                print('\033[0;36mSelecciona la direccion para el cliente\033[0;m')
                aux_cliente = seleccionar_cuenta(listado_clientes)
                if aux_cliente != '':
                    break
            try:
                assert(aux_cliente in listado_clientes)
                assert(len(prestamos_por_clientes.get(aux_cliente, [])) > 0)
            except AssertionError:
                if aux_cliente not in listado_clientes:
                    message = 'Esta utilizando una cuenta que no se ha dado de alta como cliente'
                else:
                    message = 'El cliente seleccionado no ha solicitado prestamos todavia'
                print(f'!!Error!! {message}')
                continue
            
            # Solicitar ID de prestamo para liquidar
            while(True):
                aux_lista_prestamos = prestamos_por_clientes[aux_cliente]
                print(f'Listado de ID de prestamos del cliente: {aux_cliente}')
                mostrar_id_prestamos(aux_lista_prestamos)
                try:
                    id_prestamo = int(input('\033[0;36mIntroduce el ID de prestamo que se va a liquidar la garantia>> \033[0;m'))
                    assert (id_prestamo > 0 and id_prestamo <= len(aux_lista_prestamos))
                except ValueError:        
                    print(f'!!ERROR!! Introduce un ID de entrada que sean un numero entero')
                except AssertionError:
                    print(f'!!Warning!! Un ID 0 o mayor que {len(aux_lista_prestamos)} no existe, esto puede ocasionar errores en la aplicacion')
                    confirmacion = input('¿Deseas continuar con su eleccion? (y/n): ')
                    if confirmacion.lower() == 'y':
                        break
                else:
                    break
            
            clave_prestamista = prestamistas_claves[aux_prestamista]
            DeFi.liquidar_garantia(web3, contract_DeFi, aux_prestamista, clave_prestamista, aux_cliente, id_prestamo)
        
        elif opcion == 8:
            pass
        
        elif opcion == 9:
            pass
        
        elif opcion == 10:
            print('Listado de prestamistas')
            mostrar_prestamistas(listado_prestamistas)
        elif opcion == 11:
            print('Listado de cliente0s')
            mostrar_clientes(listado_clientes)
        elif opcion == 0:
            print('!!!!Ha decidido salir de la aplicacion')
            break
        else:
            print('Opcion incorrecta, intente de nuevo')

   
if __name__ == '__main__':
    main()