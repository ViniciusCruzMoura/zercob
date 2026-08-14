def validar_cpf(cpf):
    import re
    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        cpf = colocar_mascara_no_cpf_cpnj(cpf)
        #return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False
    return True

def cpf_adicionar_zero_a_esquerda(cpf):
    return str("{:011d}".format(cpf))

def retirar_mascara_do_rg(texto_rg):
    import re
    return re.compile(r"[^0-9]").sub("", texto_rg)

def retirar_mascara_do_cep(cep):
    import re
    return re.compile(r"[^0-9]").sub("", cep)

def colocar_mascara_no_cep(cep):
    import re
    cep = re.compile(r"[^0-9]").sub("", cep)
    return "{}.{}-{}".format(cep[:2], cep[2:5], cep[5:8])
    
def colocar_mascara_no_cpf_cpnj(cpf_cnpj):
    import re
    cpf_cnpj = re.compile(r"[^0-9]").sub("", cpf_cnpj)
    if len(cpf_cnpj) == 11:
        cpf_cnpj = f'{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}'
    elif len(cpf_cnpj) == 14:
        cpf_cnpj = f'{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}'
    return cpf_cnpj
    
def retirar_mascara_do_cpf_cpnj(cpf_cnpj):
    import re
    return re.compile(r"[^0-9]").sub("", cpf_cnpj)
