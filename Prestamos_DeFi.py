def alta_prestamista(web3, contrato, administrador: str, clave: str, nuevo_prestamista:str) -> bool:
    costo_gas = contrato.functions.altaPrestamista(nuevo_prestamista).estimate_gas({'from':administrador})
    costo_eth = web3.from_wei(costo_gas * web3.eth.gas_price, 'ether')
    print(f'Gas estimado para uso de la funcion: {costo_gas}')
    print(f'Costo estimado de gas para la transacción: {costo_eth} ETH')
    confirmacion = input('¿Deseas continuar y dar de alta al prestamista? (y/n): ')
    if confirmacion.lower() != 'y':
        return False
    
    # Contruir la transaccion
    tx = contrato.functions.altaPrestamista(nuevo_prestamista).build_transaction({
        'from': administrador,
        'nonce': web3.eth.get_transaction_count(administrador)
    })
    # Firmar la transaccion
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=clave)
    # Enviar la transaccion a la blockchain Ganache
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Esperar a que se mine la transaccion y recibir el comprobante o recibo de la transaccion que contiene datos de la transaccion
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    try:
        assert(tx_receipt['status'] == 1)
        assert(administrador == tx_receipt['from'])
    except AssertionError:
        if tx_receipt['status'] == 0:
            print('!!Error! Transaccion invalida')
        else:
            print('!!Error!! Existe problemas con la identidad del remitente')
        return False
    else:
        print(f'Transaccion realizada: {web3.to_hex(tx_hash)}')
        return True
    

def alta_cliente(web3, contrato, prestamista: str, clave: str, nuevo_cliente:str) -> bool:
    costo_gas = contrato.functions.altaCliente(nuevo_cliente).estimate_gas({'from':prestamista})
    costo_eth = web3.from_wei(costo_gas * web3.eth.gas_price, 'ether')
    print(f'Gas estimado para uso de la funcion: {costo_gas}')
    print(f'Costo estimado de gas para la transacción: {costo_eth} ETH')
    confirmacion = input('¿Deseas continuar y dar de alta al cliente? (y/n): ')
    if confirmacion.lower() != 'y':
        return False
    
    # Contruir la transaccion
    tx = contrato.functions.altaCliente(nuevo_cliente).build_transaction({
        'from': prestamista,
        'nonce': web3.eth.get_transaction_count(prestamista)
    })
    # Firmar la transaccion
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=clave)
    # Enviar la transaccion a la blockchain Ganache
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Esperar a que se mine la transaccion y recibir el comprobante o recibo de la transaccion que contiene datos de la transaccion
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    try:
        assert(tx_receipt['status'] == 1)
        assert(prestamista == tx_receipt['from'])
    except AssertionError:
        if tx_receipt['status'] == 0:
            print('!!Error! Transaccion invalida')
        else:
            print('!!Error!! Existe problemas con la identidad del remitente')
        return False
    else:
        print(f'Transaccion realizada: {web3.to_hex(tx_hash)}')
        return True
    

def depositar_garantia(web3, contrato, cliente: str, clave: str, monto_garantia: int):
    costo_gas = contrato.functions.depositarGarantia().estimate_gas({'from':cliente, 'value': web3.to_wei(monto_garantia, 'ether')})
    costo_eth = web3.from_wei(costo_gas * web3.eth.gas_price, 'ether')
    print(f'Gas estimado para uso de la funcion: {costo_gas}')
    print(f'Costo estimado de gas para la transacción: {costo_eth} ETH')
    confirmacion = input('¿Deseas continuar y depositar la garantia? (y/n): ')
    if confirmacion.lower() != 'y':
        return
    
    # Contruir la transaccion
    tx = contrato.functions.depositarGarantia().build_transaction({
        'from': cliente,
        'nonce': web3.eth.get_transaction_count(cliente),
        'value': web3.to_wei(monto_garantia, 'ether')
    })
    # Firmar la transaccion
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=clave)
    # Enviar la transaccion a la blockchain Ganache
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Esperar a que se mine la transaccion y recibir el comprobante o recibo de la transaccion que contiene datos de la transaccion
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    try:
        assert(tx_receipt['status'] == 1)
        assert(cliente == tx_receipt['from'])
    except AssertionError:
        if tx_receipt['status'] == 0:
            print('!!Error! Transaccion invalida')
        else:
            print('!!Error!! Existe problemas con la identidad del remitente')
    else:
        print(f'Transaccion realizada: {web3.to_hex(tx_hash)}')
        

def solicitar_prestamo(web3, contrato, cliente: str, clave: str, monto: int, plazo: int) -> bool:
    costo_gas = contrato.functions.solicitarPrestamo(monto, plazo).estimate_gas({'from':cliente})
    costo_eth = web3.from_wei(costo_gas * web3.eth.gas_price, 'ether')
    print(f'Gas estimado para uso de la funcion: {costo_gas}')
    print(f'Costo estimado de gas para la transacción: {costo_eth} ETH')
    confirmacion = input('¿Deseas continuar y solicitar el prestamo? (y/n): ')
    if confirmacion.lower() != 'y':
        return False
    
    # Contruir la transaccion
    tx = contrato.functions.solicitarPrestamo(monto, plazo).build_transaction({
        'from': cliente,
        'nonce': web3.eth.get_transaction_count(cliente),
    })
    # Firmar la transaccion
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=clave)
    # Enviar la transaccion a la blockchain Ganache
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Esperar a que se mine la transaccion y recibir el comprobante o recibo de la transaccion que contiene datos de la transaccion
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    try:
        assert(tx_receipt['status'] == 1)
        assert(cliente == tx_receipt['from'])
    except AssertionError:
        if tx_receipt['status'] == 0:
            print('!!Error! Transaccion invalida')
        else:
            print('!!Error!! Existe problemas con la identidad del remitente')
        return False
    else:
        print(f'Transaccion realizada: {web3.to_hex(tx_hash)}')
        return True


def aprobar_prestamo(web3, contrato, prestamista: str, clave: str, cliente: str, id_prestamo:int):
    costo_gas = contrato.functions.aprobarPrestamo(cliente, id_prestamo).estimate_gas({'from':prestamista})
    costo_eth = web3.from_wei(costo_gas * web3.eth.gas_price, 'ether')
    print(f'Gas estimado para uso de la funcion: {costo_gas}')
    print(f'Costo estimado de gas para la transacción: {costo_eth} ETH')
    confirmacion = input('¿Deseas continuar y aprobar el prestamo? (y/n): ')
    if confirmacion.lower() != 'y':
        return
    
    # Contruir la transaccion
    tx = contrato.functions.aprobarPrestamo(cliente, id_prestamo).build_transaction({
        'from': prestamista,
        'nonce': web3.eth.get_transaction_count(prestamista),
    })
    # Firmar la transaccion
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=clave)
    # Enviar la transaccion a la blockchain Ganache
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Esperar a que se mine la transaccion y recibir el comprobante o recibo de la transaccion que contiene datos de la transaccion
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    try:
        assert(tx_receipt['status'] == 1)
        assert(prestamista == tx_receipt['from'])
    except AssertionError:
        if tx_receipt['status'] == 0:
            print('!!Error! Transaccion invalida')
        else:
            print('!!Error!! Existe problemas con la identidad del remitente')
    else:
        print(f'Transaccion realizada: {web3.to_hex(tx_hash)}')
        

def reembolsar_prestamo(web3, contrato, cliente: str, clave: str, id_prestamo:int):
    costo_gas = contrato.functions.reembolsarPrestamo(id_prestamo).estimate_gas({'from':cliente})
    costo_eth = web3.from_wei(costo_gas * web3.eth.gas_price, 'ether')
    print(f'Gas estimado para uso de la funcion: {costo_gas}')
    print(f'Costo estimado de gas para la transacción: {costo_eth} ETH')
    confirmacion = input('¿Deseas continuar y reembolsar el prestamo? (y/n): ')
    if confirmacion.lower() != 'y':
        return
    
    # Contruir la transaccion
    tx = contrato.functions.reembolsarPrestamo(id_prestamo).build_transaction({
        'from': cliente,
        'nonce': web3.eth.get_transaction_count(cliente),
    })
    # Firmar la transaccion
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=clave)
    # Enviar la transaccion a la blockchain Ganache
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Esperar a que se mine la transaccion y recibir el comprobante o recibo de la transaccion que contiene datos de la transaccion
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    try:
        assert(tx_receipt['status'] == 1)
        assert(cliente == tx_receipt['from'])
    except AssertionError:
        if tx_receipt['status'] == 0:
            print('!!Error! Transaccion invalida')
        else:
            print('!!Error!! Existe problemas con la identidad del remitente')
    else:
        print(f'Transaccion realizada: {web3.to_hex(tx_hash)}')
        

def liquidar_garantia(web3, contrato, prestamista: str, clave: str, cliente: str, id_prestamo: int):
    costo_gas = contrato.functions.liquidarGarantia(cliente, id_prestamo).estimate_gas({'from':prestamista})
    costo_eth = web3.from_wei(costo_gas * web3.eth.gas_price, 'ether')
    print(f'Gas estimado para uso de la funcion: {costo_gas}')
    print(f'Costo estimado de gas para la transacción: {costo_eth} ETH')
    confirmacion = input('¿Deseas continuar y liquidar la garantia? (y/n): ')
    if confirmacion.lower() != 'y':
        return
    
    # Contruir la transaccion
    tx = contrato.functions.liquidarGarantia(cliente, id_prestamo).build_transaction({
        'from': prestamista,
        'nonce': web3.eth.get_transaction_count(prestamista),
    })
    # Firmar la transaccion
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=clave)
    # Enviar la transaccion a la blockchain Ganache
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Esperar a que se mine la transaccion y recibir el comprobante o recibo de la transaccion que contiene datos de la transaccion
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    try:
        assert(tx_receipt['status'] == 1)
        assert(prestamista == tx_receipt['from'])
    except AssertionError:
        if tx_receipt['status'] == 0:
            print('!!Error! Transaccion invalida')
        else:
            print('!!Error!! Existe problemas con la identidad del remitente')
    else:
        print(f'Transaccion realizada: {web3.to_hex(tx_hash)}')