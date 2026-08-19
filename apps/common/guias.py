from datetime import datetime, timedelta
import re 

REGEX_NUM_GUIA = {
    'SPCI-SP': [r'DARE\s*(\d+)\s*Emissão', r'Nosso Número\n(\d*)'],
    'SPOJ-SP': [r'\s(\d{17})\s', r'Nosso Número\n(\d*)'],
    'SPCC-SP': [
        r'Pedido\s(\d{16})',
        r'Pedido\s(\d{15})',
        r'Pedido\s(\d{12}\s\d{4})',
        r'Pedido\s(\d{11}\s\d{4})',
        r'Pedido\s(\d{13}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{11})',
        r'Pedido\s(\d{5}\s\d{8}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{10})',
        r'Pedido\s(\d{5}\s\d{6}\s\d{4})',
        r'Pedido\s(\d+\s\d+)',
        r'Nosso Número\n(\d*)'
    ],
    'SPCPE-SP': [
        r'Pedido\s(\d{16})',
        r'Pedido\s(\d{15})',
        r'Pedido\s(\d{12}\s\d{4})',
        r'Pedido\s(\d{11}\s\d{4})',
        r'Pedido\s(\d{13}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{11})',
        r'Pedido\s(\d{5}\s\d{8}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{10})',
        r'Pedido\s(\d{5}\s\d{6}\s\d{4})',
        r'Pedido\s(\d+\s\d+)',
        r'Nosso Número\n(\d*)'
    ],
    'SPDES-SP': [
        r'Pedido\s(\d{16})',
        r'Pedido\s(\d{15})',
        r'Pedido\s(\d{12}\s\d{4})',
        r'Pedido\s(\d{11}\s\d{4})',
        r'Pedido\s(\d{13}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{11})',
        r'Pedido\s(\d{5}\s\d{8}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{10})',
        r'Pedido\s(\d{5}\s\d{6}\s\d{4})',
        r'Pedido\s(\d+\s\d+)',
        r'Nosso Número\n(\d*)'
    ],
    'SPPE-SP': [
        r'Pedido\s(\d{16})',
        r'Pedido\s(\d{15})',
        r'Pedido\s(\d{12}\s\d{4})',
        r'Pedido\s(\d{11}\s\d{4})',
        r'Pedido\s(\d{13}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{11})',
        r'Pedido\s(\d{5}\s\d{8}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{10})',
        r'Pedido\s(\d{5}\s\d{6}\s\d{4})',
        r'Pedido\s(\d+\s\d+)',
        r'Nosso Número\n(\d*)'
    ],
    'CCP-SP': [
        r'Pedido\s(\d{16})',
        r'Pedido\s(\d{15})',
        r'Pedido\s(\d{12}\s\d{4})',
        r'Pedido\s(\d{11}\s\d{4})',
        r'Pedido\s(\d{13}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{11})',
        r'Pedido\s(\d{5}\s\d{8}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{10})',
        r'Pedido\s(\d{5}\s\d{6}\s\d{4})',
        r'Pedido\s(\d+\s\d+)',
        r'Nosso Número\n(\d*)'
    ],
    'SPOC-SP': [
        r'Pedido\s(\d{16})',
        r'Pedido\s(\d{15})',
        r'Pedido\s(\d{12}\s\d{4})',
        r'Pedido\s(\d{11}\s\d{4})',
        r'Pedido\s(\d{13}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{11})',
        r'Pedido\s(\d{5}\s\d{8}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{10})',
        r'Pedido\s(\d{5}\s\d{6}\s\d{4})',
        r'Pedido\s(\d+\s\d+)',
        r'Nosso Número\n(\d*)'
    ],
    'CSF-SP': [
        r'Pedido\s(\d{16})',
        r'Pedido\s(\d{15})',
        r'Pedido\s(\d{12}\s\d{4})',
        r'Pedido\s(\d{11}\s\d{4})',
        r'Pedido\s(\d{13}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{11})',
        r'Pedido\s(\d{5}\s\d{8}\s\d{3})',
        r'Pedido\s(\d{5}\s\d{10})',
        r'Pedido\s(\d{5}\s\d{6}\s\d{4})',
        r'Pedido\s(\d+\s\d+)',
        r'Nosso Número\n(\d*)'
    ],

    'SPCI-RJ': [r'(\d{11}\-\d+)'],
    'SPOJ-RJ': [r'(\d{11}\-\d+)'],
    'SPCC-RJ': [r'(\d{11}\-\d+)'],
    'SPCPE-RJ': [r'(\d{11}\-\d+)'],
    'SPDES-RJ': [r'(\d{11}\-\d+)'],
    'SPPE-RJ': [r'(\d{11}\-\d+)'],
    'CCP-RJ': [r'(\d{11}\-\d+)'],

    'SPCI-MG': [r'(\d{17})'],
    'SPOJ-MG': [r'(\d{17})'],
    'SPCC-MG': [r'(\d{17})'],
    'SPCPE-MG': [r'(\d{17})'],
    'SPDES-MG': [r'(\d{17})'],
    'SPPE-MG': [r'(\d{17})'],
    'CCP-MG': [r'(\d{17})'],
    'CSF-MG': [r'(\d{17})'],
    'SPALV-MG': [r'(\d{17})'],
    'SPCP-MG': [r'(\d{17})'],
    'SPIMP-MG': [r'(\d{17})'],

    'SPCI-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],
    'SPOJ-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],
    'SPCC-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],
    'SPCPE-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],
    'SPDES-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],
    'SPPE-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],
    'CCP-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],
    'SPALV-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],
    'SPCP-BA': [r'Extrajudicial\s*\d{3}\s*(\d{6})\s*CIDADE'],

    'SPCI-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPOJ-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPCC-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPCPE-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPCP-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPDES-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPPE-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'CCP-MA': [r'Guia:\s*(.*?)\nVencimento'],

    'SPCI-MS': [r'\d{2}/\d{2}/\d{4}\s+(\d{11})(?:-(\d))?'],
    'SPOJ-MS': [r'\d{2}/\d{2}/\d{4}\s+(\d{11})(?:-(\d))?'],
    'SPCC-MS': [r'\d{2}/\d{2}/\d{4}\s+(\d{11})(?:-(\d))?'],
    'SPCPE-MS': [r'\d{2}/\d{2}/\d{4}\s+(\d{11})(?:-(\d))?'],
    'SPDES-MS': [r'\d{2}/\d{2}/\d{4}\s+(\d{11})(?:-(\d))?'],
    'SPPE-MS': [r'\d{2}/\d{2}/\d{4}\s+(\d{11})(?:-(\d))?'],
    'CCP-MS': [r'\d{2}/\d{2}/\d{4}\s+(\d{11})(?:-(\d))?'],
    
    'SPCI-CE': [r'\(DAE\)\n(.*?)\n'],
    'SPOJ-CE': [r'\(DAE\)\n(.*?)\n'],
    'SPCC-CE': [r'\(DAE\)\n(.*?)\n'],
    'SPCPE-CE': [r'\(DAE\)\n(.*?)\n'],
    'SPDES-CE': [r'\(DAE\)\n(.*?)\n'],
    'SPPE-CE': [r'\(DAE\)\n(.*?)\n'],
    'CCP-CE': [r'\(DAE\)\n(.*?)\n'],

    'SPCI-PA': [r'Nosso Número\n(\d*)'],
    'SPOJ-PA': [r'Nosso Número\n(\d*)'],
    'SPCC-PA': [r'Nosso Número\n(\d*)'],
    'SPCPE-PA': [r'Nosso Número\n(\d*)'],
    'SPDES-PA': [r'Nosso Número\n(\d*)'],
    'SPPE-PA': [r'Nosso Número\n(\d*)'],
    'CCP-PA': [r'Nosso Número\n(\d*)'],

    'SPCI-AL': [r'\s+(\d{12})\s\n'],
    'SPOJ-AL': [r'\s+(\d{12})\s\n'],
    'SPCC-AL': [r'\s+(\d{12})\s\n'],
    'SPCPE-AL': [r'\s+(\d{12})\s\n'],
    'SPDES-AL': [r'\s+(\d{12})\s\n'],
    'SPPE-AL': [r'\s+(\d{12})\s\n'],
    'CCP-AL': [r'\s+(\d{12})\s\n'],
    'CCP-AL': [r'\s+(\d{12})\s\n'],

    'SPCI-RN': [r'\n(\d+.)\n'],
    'SPOJ-RN': [r'\n(\d+.)\n'],
    'SPCC-RN': [r'\n(\d+.)\n'],
    'SPCPE-RN': [r'\n(\d+.)\n'],
    'SPDES-RN': [r'\n(\d+.)\n'],
    'SPPE-RN': [r'\n(\d+.)\n'],
    'CCP-RN': [r'\n(\d+.)\n'],
    'CCP-RN': [r'\n(\d+.)\n'],

    'SPCI-AM': [r'\d{2}/\d{2}/\d{4}\s+(\d+) \n', r'\d+\n(\d{11})\nR\$'],
    'SPOJ-AM': [r'\d{2}/\d{2}/\d{4}\s+(\d+) \n', r'\d+\n(\d{11})\nR\$'],
    'SPCC-AM': [r'\d{2}/\d{2}/\d{4}\s+(\d+) \n', r'\d+\n(\d{11})\nR\$'],
    'SPCPE-AM': [r'\d{2}/\d{2}/\d{4}\s+(\d+) \n', r'\d+\n(\d{11})\nR\$'],
    'SPDES-AM': [r'\d{2}/\d{2}/\d{4}\s+(\d+) \n', r'\d+\n(\d{11})\nR\$'],
    'SPPE-AM': [r'\d{2}/\d{2}/\d{4}\s+(\d+) \n', r'\d+\n(\d{11})\nR\$'],
    'CCP-AM': [r'\d{2}/\d{2}/\d{4}\s+(\d+) \n', r'\d+\n(\d{11})\nR\$'],

    'SPCI-MT': [r'Nosso Número:\s(\d{17}-\w{1})'],
    'SPOJ-MT': [r'Nosso Número:\s(\d{17}-\w{1})'],
    'SPCC-MT': [r'Nosso Número:\s(\d{17}-\w{1})'],
    'SPCPE-MT': [r'Nosso Número:\s(\d{17}-\w{1})'],
    'SPDES-MT': [r'Nosso Número:\s(\d{17}-\w{1})'],
    'SPPE-MT': [r'Nosso Número:\s(\d{17}-\w{1})'],
    'CCP-MT': [r'Nosso Número:\s(\d{17}-\w{1})'],

    'SPCI-PE': [r'(\d{17})\n'],
    'SPOJ-PE': [r'(\d{17})\n'],
    'SPCC-PE': [r'(\d{17})\n'],
    'SPCPE-PE': [r'(\d{17})\n'],
    'SPDES-PE': [r'(\d{17})\n'],
    'SPPE-PE': [r'(\d{17})\n'],
    'CCP-PE': [r'(\d{17})\n'],

    'SPCI-RR': [r'número\n(\d*)'],
    'SPOJ-RR': [r'número\n(\d*)'],
    'SPCC-RR': [r'número\n(\d*)'],
    'SPCPE-RR': [r'número\n(\d*)'],
    'SPDES-RR': [r'número\n(\d*)'],
    'SPPE-RR': [r'número\n(\d*)'],
    'CCP-RR': [r'número\n(\d*)'],
    
    'SPCI-PB': [r'(\d{3}\.\d{4}\.\d{6})'],
    'SPOJ-PB': [r'(\d{3}\.\d{4}\.\d{6})'],
    'SPCC-PB': [r'(\d{3}\.\d{4}\.\d{6})'],
    'SPCPE-PB': [r'(\d{3}\.\d{4}\.\d{6})'],
    'SPDES-PB': [r'(\d{3}\.\d{4}\.\d{6})'],
    'SPPE-PB': [r'(\d{3}\.\d{4}\.\d{6})'],
    'CCP-PB': [r'(\d{3}\.\d{4}\.\d{6})'],

    'SPCI-PI': [r'(\d{17}-\d)', r'(\d{11})'],
    'SPOJ-PI': [r'(\d{17}-\d)', r'(\d{11})'],
    'SPCC-PI': [r'(\d{17}-\d)', r'(\d{11})'],
    'SPCPE-PI': [r'(\d{17}-\d)', r'(\d{11})'],
    'SPDES-PI': [r'(\d{17}-\d)', r'(\d{11})'],
    'SPPE-PI': [r'(\d{17}-\d)', r'(\d{11})'],
    'CCP-PI': [r'(\d{17}-\d)', r'(\d{11})'],

    'SPCI-AC': [r'(\d{17})'],
    'SPOJ-AC': [r'(\d{17})'],
    'SPCC-AC': [r'(\d{17})'],
    'SPCPE-AC': [r'(\d{17})'],
    'SPDES-AC': [r'(\d{17})'],
    'SPPE-AC': [r'(\d{17})'],
    'CCP-AC': [r'(\d{17})'],

    'SPCI-AP': [r'(\d{17})'],
    'SPOJ-AP': [r'(\d{17})'],
    'SPCC-AP': [r'(\d{17})'],
    'SPCPE-AP': [r'(\d{17})'],
    'SPDES-AP': [r'(\d{17})'],
    'SPPE-AP': [r'(\d{17})'],
    'CCP-AP': [r'(\d{17})'],

    'SPCI-DF': [r'(\d{17})', r'(\d{17})', r'(\d{20})'],
    'SPOJ-DF': [r'(\d{17})', r'(\d{17})', r'(\d{20})'],
    'SPCC-DF': [r'(\d{17})', r'(\d{17})', r'(\d{20})'],
    'SPCPE-DF': [r'(\d{17})', r'(\d{17})', r'(\d{20})'],
    'SPDES-DF': [r'(\d{17})', r'(\d{17})', r'(\d{20})'],
    'SPPE-DF': [r'(\d{17})', r'(\d{17})', r'(\d{20})'],
    'CCP-DF': [r'(\d{17})', r'(\d{17})', r'(\d{20})'],

    'SPCI-ES': [r'(\d{9})'],
    'SPOJ-ES': [r'(\d{9})'],
    'SPCC-ES': [r'(\d{9})'],
    'SPCPE-ES': [r'(\d{9})'],
    'SPDES-ES': [r'(\d{9})'],
    'SPPE-ES': [r'(\d{9})'],
    'CCP-ES': [r'(\d{9})'],

    'SPCI-GO': [r'(\d{3}\/\d{8}\-\d)' , r'(\d{17}\-\d)'],
    'SPOJ-GO': [r'(\d{3}\/\d{8}\-\d)' , r'(\d{17}\-\d)'],
    'SPCC-GO': [r'(\d{3}\/\d{8}\-\d)' , r'(\d{17}\-\d)'],
    'SPCPE-GO': [r'(\d{3}\/\d{8}\-\d)' , r'(\d{17}\-\d)'],
    'SPDES-GO': [r'(\d{3}\/\d{8}\-\d)' , r'(\d{17}\-\d)'],
    'SPPE-GO': [r'(\d{3}\/\d{8}\-\d)' , r'(\d{17}\-\d)'],
    'CCP-GO': [r'(\d{3}\/\d{8}\-\d)' , r'(\d{17}\-\d)'],

    'SPCI-PR': [r'(0000\d+\-\d)\n'],
    'SPOJ-PR': [r'(0000\d+\-\d)\n'],
    'SPCC-PR': [r'(0000\d+\-\d)\n'],
    'SPCPE-PR': [r'(0000\d+\-\d)\n'],
    'SPDES-PR': [r'(0000\d+\-\d)\n'],
    'SPPE-PR': [r'(0000\d+\-\d)\n'],
    'CCP-PR': [r'(0000\d+\-\d)\n'],

    'SPCI-RJ': [r'(\d{11}\-\d+)'],
    'SPOJ-RJ': [r'(\d{11}\-\d+)'],
    'SPCC-RJ': [r'(\d{11}\-\d+)'],
    'SPCPE-RJ': [r'(\d{11}\-\d+)'],
    'SPDES-RJ': [r'(\d{11}\-\d+)'],
    'SPPE-RJ': [r'(\d{11}\-\d+)'],
    'CCP-RJ': [r'(\d{11}\-\d+)'],

    'SPCI-SC': [r'Número\n(\d*)N'],
    'SPOJ-SC': [r'Número\n(\d*)N'],
    'SPCC-SC': [r'Número\n(\d*)N'],
    'SPCPE-SC': [r'Número\n(\d*)N'],
    'SPDES-SC': [r'Número\n(\d*)N'],
    'SPPE-SC': [r'Número\n(\d*)N'],
    'CCP-SC': [r'Número\n(\d*)N'],

    'SPCI-TO': [r'Cedente\n(d{17})'],
    'SPOJ-TO': [r'Cedente\n(d{17})'],
    'SPCC-TO': [r'Cedente\n(d{17})'],
    'SPCPE-TO': [r'Cedente\n(d{17})'],
    'SPDES-TO': [r'Cedente\n(d{17})'],
    'SPPE-TO': [r'Cedente\n(d{17})'],
    'CCP-TO': [r'Cedente\n(d{17})'],
    
    'SPCI-RS': [r'(\d+\.\d+\/\d+\d+)Data', r'(\d+\.\d+\/\d+\d+)\s*Data'],
    'SPOJ-RS': [r'(\d+\.\d+\/\d+\d+)Data', r'(\d+\.\d+\/\d+\d+)\s*Data'],
    'SPCC-RS': [r'(\d+\.\d+\/\d+\d+)Data', r'(\d+\.\d+\/\d+\d+)\s*Data'],
    'SPCPE-RS': [r'(\d+\.\d+\/\d+\d+)Data', r'(\d+\.\d+\/\d+\d+)\s*Data'],
    'SPDES-RS': [r'(\d+\.\d+\/\d+\d+)Data', r'(\d+\.\d+\/\d+\d+)\s*Data'],
    'SPPE-RS': [r'(\d+\.\d+\/\d+\d+)Data', r'(\d+\.\d+\/\d+\d+)\s*Data'],
    'CCP-RS': [r'(\d+\.\d+\/\d+\d+)Data', r'(\d+\.\d+\/\d+\d+)\s*Data'],

    'SPCI-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPOJ-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPCC-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPCPE-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPCP-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPDES-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'SPPE-MA': [r'Guia:\s*(.*?)\nVencimento'],
    'CCP-MA': [r'Guia:\s*(.*?)\nVencimento'],
}

REGEX_COD_BARRAS = {
    'SPCI-SP': [r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)'],
    'SPOJ-SP': [
        r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)',
        r'\n(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\n'
        ],
    'SPCC-SP': [
        r'Banco(\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+)\s+Corte aqui',
        r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)',
        r'\n(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\n',
        r'(\d*)\s+Local\s+de\s+Pagamento',
        ],
    'SPCPE-SP': [
        r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)',
        r'(\d{11}\s*\d{7}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'\n(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\n'
    ],
    'SPDES-SP': [
        r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)',
        r'\n(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\n'
    ],
    'CCP-SP': [
        r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)'
    ],
    'SPPE-SP': [
        r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)'
    ],
    'SPOC-SP': [
        r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)',
        r'(\d{11}\s*\d{7}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'\n(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\n'
        ],
    'CSF-SP': [
        r'(\d{12}\s*\d{6}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)',
        r'(\d{11}\s*\d{7}\s*\d{6}\s*\d{12}\s*\d{12})',
        r'\n(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\n'
        ],

    'SPCI-RJ': [r'GRERJ\s*(\d*)', r"BRADESCO\s*S?A?\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"PIX\s*\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"(\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*)GRERJ"],
    'SPOJ-RJ': [r'GRERJ\s*(\d*)', r"BRADESCO\s*S?A?\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"PIX\s*\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"(\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*)GRERJ"],
    'SPCC-RJ': [r'GRERJ\s*(\d*)', r"BRADESCO\s*S?A?\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"PIX\s*\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"(\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*)GRERJ"],
    'SPCPE-RJ': [r'GRERJ\s*(\d*)', r"BRADESCO\s*S?A?\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"PIX\s*\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"(\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*)GRERJ"],
    'SPPE-RJ': [r'GRERJ\s*(\d*)', r"BRADESCO\s*S?A?\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"PIX\s*\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"(\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*)GRERJ"],
    'SPDES-RJ': [r'GRERJ\s*(\d*)', r"BRADESCO\s*S?A?\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"PIX\s*\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"(\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*)GRERJ"],
    'CCP-RJ': [r'GRERJ\s*(\d*)', r"BRADESCO\s*S?A?\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"PIX\s*\n\s*(\d*\s*\d*\s*\d*\s*\d*)", r"(\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*\s*\d*)GRERJ"],

    'SPCI-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'SPOJ-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'SPCC-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'SPCPE-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'SPDES-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'SPPE-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'CCP-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'CSF-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'SPALV-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'SPCP-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],
    'SPIMP-MG': [r'(\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d{1}\s*\d{14})'],

    'SPCI-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],
    'SPOJ-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],
    'SPCC-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],
    'SPCPE-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],
    'SPDES-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],
    'SPPE-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],
    'CCP-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],
    'SPALV-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],
    'SPCP-BA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})'],

    'SPCI-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'SPOJ-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'SPCC-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'SPCPE-MA': [
        r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})',
        r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{10}\s*\d{1}\s*\d{1})',
        r'MEC.NICA(.*?)\n',
    ],
    'SPDES-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'CCP-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'SPPE-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'SPDES-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'CCP-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'SPPE-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],
    'SPCP-MA': [r'(\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1}\s*\d{11}\s*\d{1})', r'MEC.NICA(.*?)\n'],

    'SPCI-RS': [r'(\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d)'],
    'SPOJ-RS': [r'(\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d)'],
    'SPCC-RS': [r'(\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d)'],
    'SPCPE-RS': [r'(\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d)'],
    'SPDES-RS': [r'(\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d)'],
    'SPPE-RS': [r'(\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d)'],
    'CCP-RS': [r'(\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d)'],
    'SPCP-RS': [r'(\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d\s\d{11}\-\d)'],

'SPCI-GO': [
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{4}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{15})',
],
'SPOJ-GO': [
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{4}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{15})',
],
'SPCC-GO': [
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{4}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{15})',
],
'SPDES-GO': [
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{4}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{15})',
],
'SPCPE-GO': [
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{4}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{15})',
],
'CCP-GO': [
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{4}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{15})',
],
'SPCP-GO': [
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{4}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{15})',
],

'SPCI-MT': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d\s+\d{14})',
],
'SPOJ-MT': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d\s+\d{14})',
],
'SPCC-MT': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d\s+\d{14})',
],
'SPDES-MT': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d\s+\d{14})',
],
'SPCPE-MT': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d\s+\d{14})',
],

'SPCI-MS': [
    r'CAIXA\s+(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s+Beneficiário',
    r'237-2\s*\|\s*(\d*\.\d*\s*\d*\.\d*\s*\d*\.\d*\s*\d*\s*\d*)',
],
'SPOJ-MS': [
    r'CAIXA\s+(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s+Beneficiário',
    r'237-2\s*\|\s*(\d*\.\d*\s*\d*\.\d*\s*\d*\.\d*\s*\d*\s*\d*)',
],
'SPCPE-MS': [
    r'CAIXA\s+(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s+Beneficiário',
    r'237-2\s*\|\s*(\d*\.\d*\s*\d*\.\d*\s*\d*\.\d*\s*\d*\s*\d*)',
],
'SPDES-MS': [
    r'CAIXA\s+(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s+Beneficiário',
    r'237-2\s*\|\s*(\d*\.\d*\s*\d*\.\d*\s*\d*\.\d*\s*\d*\s*\d*)',
],
'SPCC-MS': [
    r'CAIXA\s+(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s+Beneficiário',
    r'237-2\s*\|\s*(\d*\.\d*\s*\d*\.\d*\s*\d*\.\d*\s*\d*\s*\d*)',
],

'SPCI-DF': [r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\s\d{14})', r'(\d*)\s+Local\s+de\s+Pagamento',],
'SPOJ-DF': [r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\s\d{14})', r'(\d*)\s+Local\s+de\s+Pagamento',],
'SPCC-DF': [r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\s\d{14})', r'(\d*)\s+Local\s+de\s+Pagamento',],
'SPDES-DF': [r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\s\d{14})', r'(\d*)\s+Local\s+de\s+Pagamento',],
'SPCPE-DF': [r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\s\d{14})', r'(\d*)\s+Local\s+de\s+Pagamento',],

'SPCI-AL': [r'\s(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s',],
'SPOJ-AL': [r'\s(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s',],
'SPCC-AL': [r'\s(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s',],
'SPDES-AL': [r'\s(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s',],
'SPCPE-AL': [r'\s(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s',],

'SPCI-BA': [r'\n (\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1})',],
'SPOJ-BA': [r'\n (\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1})',],
'SPCC-BA': [r'\n (\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1})',],
'SPDES-BA': [r'\n (\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1})',],
'SPCPE-BA': [r'\n (\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1})',],
'SPALV-BA': [r'\n (\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1})',],

'SPCI-CE': [r'BARRAS\n(.*?)\n',],
'SPOJ-CE': [r'BARRAS\n(.*?)\n',],
'SPCC-CE': [r'BARRAS\n(.*?)\n',],
'SPDES-CE': [r'BARRAS\n(.*?)\n',],
'SPCPE-CE': [r'BARRAS\n(.*?)\n',],

'SPCI-PB': [r'(\d{12}\s\s\s\d{12}\s\s\s\d{12}\s\s\s\d{12})',],
'SPOJ-PB': [r'(\d{12}\s\s\s\d{12}\s\s\s\d{12}\s\s\s\d{12})',],
'SPCC-PB': [r'(\d{12}\s\s\s\d{12}\s\s\s\d{12}\s\s\s\d{12})',],
'SPDES-PB': [r'(\d{12}\s\s\s\d{12}\s\s\s\d{12}\s\s\s\d{12})',],
'SPCPE-PB': [r'(\d{12}\s\s\s\d{12}\s\s\s\d{12}\s\s\s\d{12})',],

'SPDES-PE': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{11}\s.\s\d{11}\s.\s\d{11}\s.\s\d{11}\s.)',
],
'SPCC-PE': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{11}\s.\s\d{11}\s.\s\d{11}\s.\s\d{11}\s.)',
],
'SCOJ-PE': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{11}\s.\s\d{11}\s.\s\d{11}\s.\s\d{11}\s.)',
],
'SPCI-PE': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{11}\s.\s\d{11}\s.\s\d{11}\s.\s\d{11}\s.)',
],
'CCP-PE': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{11}\s.\s\d{11}\s.\s\d{11}\s.\s\d{11}\s.)',
],

'SPCI-PI': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPOJ-PI': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPCC-PI': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPDES-PI': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPCPE-PI': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],

'SPCI-RN': [r'\n(\d+-\d\s+\d+-\d\s+\d+-\d\s+\d+-\d)\nTJRN',],
'SPOJ-RN': [r'\n(\d+-\d\s+\d+-\d\s+\d+-\d\s+\d+-\d)\nTJRN',],
'SPCC-RN': [r'\n(\d+-\d\s+\d+-\d\s+\d+-\d\s+\d+-\d)\nTJRN',],
'SPDES-RN': [r'\n(\d+-\d\s+\d+-\d\s+\d+-\d\s+\d+-\d)\nTJRN',],
'SPCPE-RN': [r'\n(\d+-\d\s+\d+-\d\s+\d+-\d\s+\d+-\d)\nTJRN',],

'SPCI-SE': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'Mecânica(\d+\s+\d+\s+\d+\s+\d+)',
    r'(\d{12})\s{2}(\d{12})\s{2}(\d{12})\s{2}(\d{12})',
    r'(\d{5}.\d{5}\s\d{5}.\d{6}\s\d{5}.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d{1}\s\d{14})',
],
'SPCI-AC': [
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\s\d{14})',
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\d\s\s\d{8}\s\d{6})',
    r'Cola\n(.*?)\n.*?Código',
],
'SPCI-AP': [
    r'(\d{5}\.\d{5}\t\d{5}\.\d{6}\t\d{5}\.\d{6}\t\d\t\d{14})',
    r'(\d{5}\.\d{5}\t\d{5}\.\d{6}\t\d{5}\.\d{6}\t\d\n\d{14})',
],
'SPCPE-AP': [
    r'(\d{5}\.\d{5}\t\d{5}\.\d{6}\t\d{5}\.\d{6}\t\d\t\d{14})',
    r'(\d{5}\.\d{5}\t\d{5}\.\d{6}\t\d{5}\.\d{6}\t\d\n\d{14})',
],
'SPOJ-AP': [
    r'(\d{5}\.\d{5}\t\d{5}\.\d{6}\t\d{5}\.\d{6}\t\d\t\d{14})',
    r'(\d{5}\.\d{5}\t\d{5}\.\d{6}\t\d{5}\.\d{6}\t\d\n\d{14})',
],
'CCP-AP': [
    r'(\d{5}\.\d{5}\t\d{5}\.\d{6}\t\d{5}\.\d{6}\t\d\t\d{14})',
    r'(\d{5}\.\d{5}\t\d{5}\.\d{6}\t\d{5}\.\d{6}\t\d\n\d{14})',
],
'SPCI-AM': [
    r'Compensação\s+(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s*',
    r'-\d{2}\n(.*?)\n\d{5}',
],
'SPCPE-AM': [
    r'Compensação\s+(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s*',
    r'-\d{2}\n(.*?)\n\d{5}',
],

'SPCI-PA': [r'nica\n037\s*-\s*0(.*?)\nLocal', r'\nREAL(\d{47})Referente',],
'SPOJ-PA': [r'nica\n037\s*-\s*0(.*?)\nLocal', r'\nREAL(\d{47})Referente',],
'SPCC-PA': [r'nica\n037\s*-\s*0(.*?)\nLocal', r'\nREAL(\d{47})Referente',],
'SPDES-PA': [r'nica\n037\s*-\s*0(.*?)\nLocal', r'\nREAL(\d{47})Referente',],
'SPCPE-PA': [r'nica\n037\s*-\s*0(.*?)\nLocal', r'\nREAL(\d{47})Referente',],

'SPCI-RO': [r'Documento(.*?)\n',],
'SPOJ-RO': [r'Documento(.*?)\n',],
'SPCC-RO': [r'Documento(.*?)\n',],
'SPDES-RO': [r'Documento(.*?)\n',],
'SPCPE-RO': [r'Documento(.*?)\n',],

'SPCI-RR': [
    r'(\d{11}-\d\s\s\d{11}\-\d\s\s\d{11}\-\d\s\s\d{11}\-\d)',
    r'digitável\n(\d*\.\d+\s\d+\.\d+\s\d+\.\d+\s\d\s\d+)',
],
'SPCI-TO': [
    r'(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\s+Local\s+de\s+Pagamento',
    r'Valor\n(.*?)\n',
    r'CNPJ:CEP:(.*?)\n\d',
],
'SPCI-ES': [
    r'(\d{11}\xa0\d\xa0\d{11}\xa0\d\xa0\d{11}\xa0\d\xa0\d{11})',
    r'(\d{11}\s\d\s\d{11}\s\d\s\d{11}\s\d\s\d{11})',
],

'SPCI-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPOJ-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPCDP-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPTJ-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPCC-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPCPE-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPDES-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'SPPE-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],
'CCP-PR': [r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',],

'SPCI-SC': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\d{14})',
],
'SPOJ-SC': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\d{14})',
],
'SPCC-SC': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\d{14})',
],
'SPDES-SC': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\d{14})',
],
'SPCPE-SC': [
    r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',
    r'(\d{5}\.\d{5}\s\s\d{5}\.\d{6}\s\s\d{5}\.\d{6}\s\s\d\s\d{14})',
],

}

REGEX_COMPROVANTES = [
    r'Pagamento de Boleto\n-*\n(\d*)\n',
    r'CODIGO DE BARRAS\s*(\d*-?\d*\s*\d*-?\d*\n?\s*\d*-?\d*\s*\d*-?\d*)',
    r'NOME DA COBRANCA:\s*GRERJ\s*(\d*)\n?',
    r'Banco\s*destinatário:\s*(\d{5}\s\d{5}\s\d{5}\s\d{6}\s\d{5}\s\d{6}\s\d\s\d{14})\s*Código de barras',
    r'Órgão:\s*(\d{11}-\d{1}\s\d{11}-\d{1}\s\d{11}\-\d{1}\s\d{11}-\d)\s*Código de barras',
    r'Linha Digitável:\s+(\d{44,48})', #r'Código de barras:\s+(\d{44,48})',
    r'Linha Digitável:\s*(\d{5}.?\s*\d{5}.?\s*\d{5}.?\s*\d{6}.?\s*\d{5}.?\s*\d{6}.?\s*\d{1}.?\s*\d{14})',
    r'Linha Digitável:\s*(\d+.?-?\d+.?-?\d+.?-?\d+)\s+Número do Boleto',
    r'Banco destinatário:\s?(\d{5}\s+\d{5}\s+\d{5}\s+\d{6}\s+\d{5}\s+\d{6}\s+\d{1}\s+\d{14})\sCódigo de barras',
]

REGEX_DATA_VENCIMENTO = {
'AC': [
r'Vencimento\s\s\:\s\s(\d{2}\/\d{2}\/\d{4})',
r'Vencimento\s*em:\s*(\d{2}/\d{2}/\d{4})',
],
'AL': [r'Vencimento  :  (\d{2}/\d{2}/\d{4}) \n',],
'AM': [
r'Vencimento\s*?:\s*?(\d{2}\/\d{2}\/\d{4})',
r'(\d{2}\/\d{2}\/\d{4})',
],
'AP': [
r'Vencimento\n(\d{2}\/\d{2}\/\d{4})',
],
'BA': [
r'(\d{2}/\d{2}/\d{4})\n',
],
'CE': [
r'(?:Vencimento|VENCIMENTO)\n(\d{2}\/\d{2}\/\d{4})\n',
],
'DF': [
r'(\d{2}\/\d{2}\/\d{4})',
r'(\d{2}/\d{2}/\d{4})',
r'(\d{2}\/\d{2}\/\d{4})',
],
'ES': [

],
'GO': [
r'LIMITE\s(\d{2}\/\d{2}\/\d{4})',
r'Sacado\n(\d{2}\/\d{2}\/\d{4})',
r'Vencimento(\d{2}\/\d{2}\/\d{4})',
],
'MA': [
r'(\d{2}/\d{2}/\d{4})\nData',
],
'MG': [
r'vencimento\s\-\s(\d{2}\/\d{2}\/\d{4})',
],
'MS': [

],
'MT': [
r'(\d{2}/\d{2}/\d{4})',
],
'PA': [
r'Vencimento\n(\d{2}\/\d{2}\/\d{4})',
r'VENCIMENTO -(\d{2}/\d{2}/\d{4})\n',
r'Vencimento\n(\d{2}\/\d{2}\/\d{4})',
],
'PB': [
r'Total:(\d{2}\/\d{2}\/\d{4})',
],
'PE': [
r'\n(\d{2}/\d{2}/\d{4})\n',
],
'PI': [
r'(\d{2}\/\d{2}\/\d{4})',
],
'PR': [
r'\n\s(\d{2}\/\d{2}\/\d{4})', #'Bairro:\s*(\d{2}\/\d{2}\/\d{4})\\n'
],
'RJ': [
r'(\d{2}\/\d{2}\/\d{4})VALIDADE',
],
'RN': [
r'\n(\d{2}/\d{2}/\d{4})',
],
'RO': [
r'Cobrado\n(\d{2}/\d{2}/\d{4}) ',
],
'RR': [
r'(\d{2}\/\d{2}\/\d{4})',
r'[vV]encimento\n(\d{2}\/\d{2}\/\d{4})',
],
'SC': [
r'\n(\d{2}\/\d{2}\/\d{4})\n',
],
'SE': [
r'Vencimento\s(\d{2}\/\d{2}\/\d{4})',
r'Vencimento\s:\s(\d{2}\/\d{2}\/\d{4})',
r'Válida\s(\d{2}\/\d{2}\/\d{4})',
r'(\d{2}/\d{2}/\d{4})',
r'Vencimento\s*(\d{2}/\d{2}/\d{4})',
r'Vencimento\s\:\s(\d{2}\/\d{2}\/\d{4})',
],
'SP': [
r'Vencimento\n(\d{2}\/\d{2}\/\d{4})',
r'\s+(\d{2}/\d{2}/\d{4})\n',
],
'TO': [
r'Vencimento\n(\d{2}/\d{2}/\d{4})',
r'TOCANTINS(\d{2}/\d{2}/\d{4})',
],
}

class ExtratorGuias:
    def __init__(self):
        pass

    def formatar_valor(self, valor: str) -> str:
        """Realiza a formatação do valor para o formato XX,XX.

        Args:
            valor (str): Valor da guia a ser formatado.

        Returns:
            str: Valor formatado.
        """
        parte_inteira = valor[:-2]
        parte_decimal = valor[-2:]
        saida = parte_inteira + "," + parte_decimal
        return saida


    def validar_regex(self, regex_list, indicador, texto = '') -> str:
        """Faz a validação do regex na lista de regex;.

        Args:
            regex_list (list): Lista de regex a serem validados.
            indicador (str): Variável a ser preenchida com o resultado do regex.
            texto (str, optional): Texto a ser validado. Defaults to ''.

        Returns:
            str: Indicador preenchido com o resultado do regex.
        """
        for regex_pattern in regex_list:
            try:
                indicador = re.search(regex_pattern, texto).group(1)
                if indicador:
                    break
            except AttributeError:
                continue

        indicador = indicador.replace(" ", "").replace("-", "").replace(".", "").replace("/", "").replace(",", "")
        return indicador


    def extrair_dados(self, texto, estado, tipo_custas, banco_do_brasil) -> list:
        match estado:
            case "AC":
                return GuiasAC().extrair_dados(texto)
            case "AL":
                return GuiasAL().extrair_dados(texto)
            case "AM":
                if "TRIBUNAL DE JUSTIÇA DO ESTADO DO AMAZONAS" in texto:
                    return GuiasAM2().extrair_dados(texto)
                return GuiasAM().extrair_dados(texto)
            case "AP":
                return GuiasAP().extrair_dados(texto)
            case "BA":
                return GuiasBA().extrair_dados(texto, banco_do_brasil)
            case "CE":
                return GuiasCE().extrair_dados(texto)
            case "DF":
                if tipo_custas and "CCP" in str(tipo_custas).upper():
                    return GuiasComplementarDF().extrair_dados(texto)
                elif tipo_custas and "SPOJ" in str(tipo_custas).upper():
                    return GuiasOjDF().extrair_dados(texto)
                return GuiasInicialDF().extrair_dados(texto)
            case "ES":
                return GuiasES().extrair_dados(texto)
            case "GO":
                if "Estado de Goiás" in texto or "Tribunal de Justiça do Estado de Goiás" in texto:
                    return GuiasItauGO().extrair_dados(texto)
                return GuiasCaixaGO().extrair_dados(texto)
            case "MA":
                return GuiasMA().extrair_dados(texto, banco_do_brasil)
            case "MG":
                return GuiasMG().extrair_dados(texto, banco_do_brasil)
            case "MS":
                return GuiasMS().extrair_dados(texto)
            case "MT":
                return GuiasMT().extrair_dados(texto)
            case "PA":
                if tipo_custas and "SPOJ" in str(tipo_custas).upper():
                    return GuiasOjPA().extrair_dados(texto)
                return GuiasIniciaisPA().extrair_dados(texto)
            case "PB":
                return GuiasPB().extrair_dados(texto)
            case "PE":
                if tipo_custas and "SPCPE" in str(tipo_custas).upper():
                    return GuiasPesquisaPE().extrair_dados(texto)
                return GuiasPE().extrair_dados(texto)
            case "PI":
                return GuiasPI().extrair_dados(texto)
            case "PR":
                return GuiasPR().extrair_dados(texto)
            case "RJ":
                return GuiasRJ().extrair_dados(texto, banco_do_brasil)
            case "RN":
                return GuiasRN().extrair_dados(texto)
            case "RO":
                return GuiasRO().extrair_dados(texto)
            case "RR":
                if tipo_custas and "SPCI" in str(tipo_custas).upper():
                    return GuiasIniciaisRR().extrair_dados(texto)
                return GuiasRR().extrair_dados(texto)
            case "RS":
                return GuiasRS().extrair_dados(texto)
            case "SC":
                return GuiasSC().extrair_dados(texto)
            case "SE":
                if "SERGIPE" in texto:
                    return GuiasPixSE().extrair_dados(texto)
                elif tipo_custas and "SPCC" in str(tipo_custas).upper():
                    return GuiasCitacaoSE().extrair_dados(texto)
                return GuiasSE().extrair_dados(texto)
            case "SP":
                v = None
                p = [GuiasBBLSP(), GuiasEPROCSP(), GuiasCitacaoSP(), GuiasComplementarSP(), GuiasOjSP(), GuiasIniciaisSP()]
                for _p in p:
                    try:
                        v = _p.extrair_dados(texto, banco_do_brasil)
                        if v and v[0]: break
                    except AttributeError:
                        pass
                return v
            case "TO":
                if tipo_custas and "SPOJ" in str(tipo_custas).upper():
                    return GuiasOjTO().extrair_dados(texto)
                return GuiasTO().extrair_dados(texto)

        if "PESQUISA" in texto:
            return GuiasRenajud().extrair_dados(texto)
        elif "DESBLOQUEIO" in texto or "Operador Nacional do Registro" in texto or "CERTIDOES" in texto or "CARTÓRIOS" in texto or "PARCELA" in texto or "PARCELA EXPRESS" in texto or "Cartório" in texto or "ASSOCIACAO DOS NOTARIOS" in texto or "ANOREG" in texto:
            return GuiasPesquisa().extrair_dados(texto)
        elif "COMPLEMENTAR" in texto or "CITAÇÃO" in texto:
            return GuiasComplementar().extrair_dados(texto)

        return None


class GuiasAC(ExtratorGuias):
    # ACRE
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'BANCO\s\sR\$\s(\d+\.\d+\.\d+)',
            r'BANCO\s\sR\$\s(\d+\.\d+\,\d+)',
            r'BANCO\s\sR\$\s(\d+,\d+)',
            r'BANCO\s\sR\$\s(\d+.\d+)',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasAL(ExtratorGuias):
    # ALAGOAS
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r"BANCO  R\$\s(.*)\s+R\$", texto).group(1).replace(".", "").replace(",", "").strip()
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasAM(ExtratorGuias):
    # AMAZONAS
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r"Cobrado \n (.*?) \n Nome", texto).group(1).strip().replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasAM2(ExtratorGuias):
    # AMAZONAS 2
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r"\nR\$\s*(.*?)\n\d{2}\/\d{2}\/\d{4}", texto).group(1).strip().replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasAP(ExtratorGuias):
    # AMAPÁ
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = None
            regex_valor_guia = [
                r'\tR\$\t(\d+\.\d+\,\d+)\;',
                r'\tDocumento\n(\d+,\d+)',
            ]

            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasBA(ExtratorGuias):
    # BAHIA
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        try:
            valor_guia = re.search(r"\nR\$\s(.*)\(esta", texto).group(1).replace(".", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None

        nome_tribunal = ""
        cnpj_tribunal = ""
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE CONVENIO (OUTROS)"

        if banco_do_brasil:
            try:
                nome_tribunal = re.search(r'PAGAR([\w\s]+)\n', texto).group(1)
            except:
                nome_tribunal = ''
            try:
                cnpj_tribunal = re.search(r'DE(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})', texto).group(1).replace(".", "").replace("/", "").replace("-", "")
            except:
                cnpj_tribunal = ""
            try:
                codigo_barras = re.search(r'\n (\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1}\s\d{11}\s\d{1})', texto).group(1).replace(" ", "")
            except:
                codigo_barras = ""
            try:
                indicador = re.search(r'Emissor\s*\d{3}(\d{1})', texto).group(1)
            except:
                indicador = ""
            try:
                numero_guia = indicador + re.search(r'(\d{3}\n\d+)\nCIDADE', texto).group(1).replace("\n", "")
            except:
                numero_guia = ""

        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasCE(ExtratorGuias):
    # CEARÁ
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'TOTAL A RECOLHER\nR\$\s+(\d+,\d{2})\n1ª\s', texto).group(1).replace(".", "").replace(",", "").replace("ESTADO DO CEARÁ", "")
        except:
            try:
                valor_guia = re.search(r'RECOLHER\nR\$\s+(.*?)\n', texto).group(1).replace(".", "").replace(",", "").replace("ESTADO DO CEARÁ", "")
            except:
                valor_guia = None

        valor_guia = self.formatar_valor(valor_guia)
        valor_guia = re.sub('\D', '', valor_guia)
        return [valor_guia]


class GuiasComplementar(ExtratorGuias):
    # COMPLEMENTAR
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'Valor\s*(\d+,\d{2})', texto).group(1).replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasComplementarDF(ExtratorGuias):
    # COMPLEMENTAR DISTRITO FEDERAL
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'(\d+\.\d+\,\d+)',
            r'(\d+,\d+)',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasInicialDF(ExtratorGuias):
    # INICIAL DISTRITO FEDERAL
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
                r'(\d+,\d+)',
                r'(\d+\.\d+\,\d+)',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasOjDF(ExtratorGuias):
    # OJ DISTRITO FEDERAL
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'documento\nR\$\s(\d+\.\d+\,\d+)',
            r'documento\nR\$\s(\d+,\d+)',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto).replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasES(ExtratorGuias):
    # ESPÍRITO SANTO
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'RECEITA\n(\d+\.\d+\,\d+)',
            r'RECEITA\n(\d+,\d+)',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasCaixaGO(ExtratorGuias):
    # CAIXA GOIÁS
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'R\$\s(\d+\.\d+\,\d{2})',
            r'R\$\s(\d+,\d{2})',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasItauGO(ExtratorGuias):
    # ITAÚ GOIÁS
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'Guia\sR\$\s(\d{1,3}(?:\.\d{3})*,\d{2})',
            r'Documento\sR\$\s(\d{1,3}(?:\.\d{3})*,\d{2})',
            r'Documento\sR\$\s(\d+,\d{2})',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto).replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasMA(ExtratorGuias):
    # MARANHÃO
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        try:
            valor_guia = re.search(r'x\s+(.*?)\s*TOTAL', texto).group(1).strip().replace(".", "").replace(",", "").replace(" ","").replace("E", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None

        nome_tribunal = ""
        cnpj_tribunal = ""
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE CONVENIO (OUTROS)"

        if banco_do_brasil:
            try:
                nome_tribunal = re.search(r'Cedente\sCNPJ\n(.*?)\d', texto).group(1)
            except:
                nome_tribunal = ""
            try:
                cnpj_tribunal = re.search(r'FERJ\s?(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})', texto).group(1).replace(".", "").replace("/", "").replace("-", "")
            except:
                cnpj_tribunal = ""
            try:
                codigo_barras = re.search(r'MEC.NICA(.*?)\n', texto).group(1).replace(" ","").strip()
            except:
                codigo_barras = ""
            try:
                numero_guia = re.search(r'Guia:\s*(.*?)\nVencimento', texto).group(1).replace("\n", "").replace('.','').replace('-','').replace(" ",'')
            except:
                numero_guia = ""
        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasMG(ExtratorGuias):
    # MINAS GERAIS
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'Documento\nR\$\s(\d+\.\d+\,\d{2})',
            r'Documento\nR\$\s(\d+,\d{2})',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto).replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None

        nome_tribunal = ""
        cnpj_tribunal = ""
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE TITULO/BOLETO"

        if banco_do_brasil:
            try:
                nome_tribunal = re.search(r'Beneficiário:\s*([^\\\n]+)', texto).group(1)
            except:
                nome_tribunal = ""
            try:
                cnpj_tribunal = re.search(r'(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})', texto).group(1).replace(".", "").replace("/", "").replace("-", "")
            except:
                cnpj_tribunal = ""
            try:
                codigo_barras = re.search(r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})',texto).group(1).strip().replace(" ", "").replace(".", "")
            except:
                codigo_barras = ""
            try:
                numero_guia = re.search(r'(\d{17})', texto).group(1).replace("/", "").replace("-", "")
            except:
                numero_guia = ""

        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasMS(ExtratorGuias):
    # MATO GROSSO DO SUL
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r"Cobrado \n (.*?) \n Pagador", texto).group(1).strip().replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasMT(ExtratorGuias):
    # MATO GROSSO
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
                r'Valor\s+a\s+Recolher\nR\$(\d{1,3}(?:\.\d{3})*,\d{2})',
                r'Diligência\sR\$\s(\d+\.\d+\,\d+)',
                r'Diligência\sR\$(\d+,\d+)',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto).replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasIniciaisPA(ExtratorGuias):
    # INICIAIS PARÁ
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r"Documento\n(\d+.\d+,\d{2}|\d+,\d{2})", texto).group(1).replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasOjPA(ExtratorGuias):
    # OJ PARÁ
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'R\$(.*?,\d{2})', texto).group(1).strip().replace(".", "").replace(",", "").replace(" ","")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            try:
                valor_guia = re.search(r"o\s*\n\s*((\d{1,3}(?:\.\d{3})|\d+),\s\d{2})\s*\n", texto).group(1).replace(".", "").replace(" ", "")
                valor_guia = re.sub('\D', '', valor_guia)
            except:
                valor_guia = None

        return [valor_guia]


class GuiasPB(ExtratorGuias):
    # PARAÍBA
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'\n\sR\$\s\s(\d+\.\d+\,\d{2})',
            r'\n\sR\$\s\s(\d+,\d{2})',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasPE(ExtratorGuias):
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'Total\s*R\$\s*(\d+\,\d+)\nTari',
            r'Total\s*R\$\s*(\d+\.\d+\,\d+)\nTari',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasPesquisaPE(ExtratorGuias):
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'OTAL\n*R\$\s*(\d+\.\d+\,\d+)',
            r'OTAL\n*R\$\s*(\d+\,\d+)',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasPesquisa(ExtratorGuias):
    # PESQUISA ELETRÔNICA
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'(\d.\d+,\d{2})', texto).group(1).replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            try:
                valor_guia = re.search(r'(\d+,\d{2})', texto).group(1).replace(",", "")
                valor_guia = self.formatar_valor(valor_guia)
                valor_guia = re.sub('\D', '', valor_guia)
            except:
                valor_guia = None

        return [valor_guia]


class GuiasPI(ExtratorGuias):
    # PIAUÍ
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'TOTAL\s(\d+\.\d+\,\d{2})',
            r'TOTAL\s(\d+,\d{2})',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasPR(ExtratorGuias):
    # PARANÁ
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'VRC\)\sR\$\s(\d+\.\d+\,\d{2})',
            r'VRC\)\sR\$\s(\d+,\d{2})',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasRenajud(ExtratorGuias):
    # RENAJUD
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'Total\n(\d+\.\d+\,\d+)',
            r'Total\n(\d+\,\d+)',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasRJ(ExtratorGuias):
    # RIO DE JANEIRO
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        try:
            valor_guia = re.search(r'(\d*,\d*|\d*\.\d*,\d*)VALOR', texto).group(1).replace(".","").replace(" ", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None

        nome_tribunal = "TRIBUNAL DE JUSTICA DO ESTADO DO RIO DE JANEIRO"
        cnpj_tribunal = "28538734000148"
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PIX"

        if banco_do_brasil:
            try:
                codigo_barras = re.search(r"PIX\s*\n\s*(\d*\s*\d*\s*\d*\s*\d*)",texto).group(1).replace(' ','')
            except:
                try:
                    codigo_barras = re.search(r"BRADESCO\s*S?A?\n\s*(\d*\s*\d*\s*\d*\s*\d*)", texto).group(1).replace(' ','')
                except:
                    codigo_barras = ""
            try:
                numero_guia = re.search(r'(\d*-\d*)NÚMERO', texto).group(1).replace("-", "").replace(" ", "")
            except:
                numero_guia = ""
        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasRN(ExtratorGuias):
    # RIO GRANDE DO NORTE
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'\nR\$\s(\d+\.\d+\,\d+)', texto).group(1).replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            try:
                valor_guia = re.search(r'\nR\$\s(\d+\,\d+)', texto).group(1).replace(",", "")
                valor_guia = self.formatar_valor(valor_guia)
                valor_guia = re.sub('\D', '', valor_guia)
            except:
                valor_guia = None
        return [valor_guia]


class GuiasRO(ExtratorGuias):
    # RONDONIA
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'\d{2}/\d{2}/\d{4}\s+(.*?)\n', texto).group(1).strip().replace(".", "").replace(",", "").replace(" ","")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasRR(ExtratorGuias):
    # RORAIMA
    def extrair_dados(self, texto) -> list:
        regex = r'R\$\s*\d{1,3}(?:\.\d{3})*,\d{2}'
        try:
            resultado = re.findall(regex, texto)
            resultado = [re.sub(r'R\$', '', valor.replace(',', '').replace('.', '')) for valor in resultado]

            if resultado:
                valor_guia = resultado[2]

            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasIniciaisRR(ExtratorGuias):
    # RORAIMA INICIAIS
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'documento\nR\$\s*(\d*,\d*|\d*\.\d*,\d*)', texto).group(1).replace(".","").replace(" ", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasRS(ExtratorGuias):
    # RIO GRANDE DO SUL
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'TOTAL:\s(\d+\.\d+\,\d{2})',
            r'TOTAL:\s(\d+,\d{2})'
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasSC(ExtratorGuias):
    # SANTA CATARINA
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'Documento\n(\d+\.\d+\,\d{2})',
            r'Documento\n(\d+,\d{2})'
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasSE(ExtratorGuias):
    # SERGIPE
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'alor\sdo\sDocumento\n(\d+\.\d+\,\d{2})',
            r'alor\sdo\sDocumento\n(\d+,\d{2})',
            r'TOTAL\s(\d+\.\d+\,\d{2})',
            r'TOTAL\s(\d+,\d{2})',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasPixSE(ExtratorGuias):
    # PIX SERGIPE
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'(\d+\.\d+\,\d+)',
            r'(\d+,\d+)',
        ]
        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasCitacaoSE(ExtratorGuias):
    # CITAÇÃO SERGIPE
    def extrair_dados(self, texto) -> list:
        valor_guia = None
        regex_valor_guia = [
            r'Valor\sdo\sDocumento\n(\d+\.\d+\,\d{2})',
            r'Valor\sdo\sDocumento\n(\d+,\d{2})',
            r'(\d{1,3}(?:,\d{2}))',
        ]

        try:
            valor_guia = self.validar_regex(regex_valor_guia, valor_guia, texto)
            valor_guia = self.formatar_lor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasBBLSP(ExtratorGuias):
    # BBL SÃO PAULO
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        try:
            valor_guia = re.search(r'Valor\s*(\d+,\d{2})', texto).group(1).replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            try:
                valor_guia = re.search(r'Valor\s*(\d{1,3}(?:\.\d{3})*\,\d{2})', texto).group(1).replace(".", "").replace(",", "")
                valor_guia = self.formatar_valor(valor_guia)
                valor_guia = re.sub('\D', '', valor_guia)
            except:
                valor_guia = None

        nome_tribunal = "TRIBUNAL DE JUSTICA DO ESTADO DE SAO PAULO"
        cnpj_tribunal = "51174001000193"
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE TITULO/BOLETO"

        if banco_do_brasil:
            codigo_barras = None
            numero_guia = None
            regex_codigo_de_barras = [
                r'(\d{12}\s\d{6}\s\d{6}\s\d{12}\s\d{6}\s\d{4}\s\d{2})',
                r'(\d{11}\s\d{7}\s\d{6}\s\d{12}\s\d{6}\s\d{4}\s\d{2})',
                r'(\d{9}\s\d{3}\s\d{6}\s\d{6}\s\d{5}\s\d{7}\s\d{12})',
                r'(\d{9}\s\d{3}\s\d{6}\s\d{6}\s\d{12}\s\d{6}\s\d{6})',
                r'(\d{12}\s\d{6}\s\d{6}\s\d{5}\s\d{7}\s\d{11}\s\d)',
                r'(\d{12}\s\d{6}\s\d{6}\s\d{12}\s\d{6}\s\d{5}\s\d)',
                r'(\d{12}\s\d{6}\s\d{6}\s\d{5}\s\d{7}\s\d{12})',
                r'(\d{11}\s\d{7}\s\d{6}\s\d{5}\s\d{7}\s\d{12})',
                r'(\d{12}\s\d{6}\s\d{6}\s\d{12}\s\d{6}\s\d{6})',
                r'(\d{11}\s\d{7}\s\d{6}\s\d{12}\s\d{6}\s\d{6})',
                r'(\d{11}\s\d{6}\s\d{6}\s\d{12}\s\d{9}\s\d{3})',
                r'(\d{9}\s\d{3}\s\d{6}\s\d{6}\s\d{12}\s\d{12})',
                r'(\d{12}\s\d{6}\s\d{6}\s\d{12}\s\d{11}\s\d)',
                r'(\d{11}\s\d{7}\s\d{6}\s\d{12}\s\d{12})',
                r'(\d{12}\s\d{6}\s\d{6}\s\d{12}\s\d{12})',
            ]
            regex_nosso_numero = [
                r'Pedido\s(\d{5}\s\d{6}\s\d{4})',
                r'Pedido\s(\d{5}\s\d{8}\s\d{3})',
                r'Pedido\s*(\d{5}\s*\d{11})',
                r'Pedido\s(\d{12}\s\d{4})',
                r'Pedido\s(\d{11}\s\d{4})',
                r'Pedido\s(\d{13}\s\d{3})',
                r'Pedido\s(\d{5}\s\d{11})',
                r'Pedido\s(\d{5}\s\d{10})',
                r'Pedido\s(\d+\s\d+)',
                r'Pedido\s(\d{16})',
                r'Pedido\s(\d{15})',
            ]
            try:
                codigo_barras = self.validar_regex(regex_codigo_de_barras, codigo_barras)
            except:
                codigo_barras = ""
            try:
                numero_guia = self.validar_regex(regex_nosso_numero, numero_guia)
            except:
                numero_guia = ""

        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasCitacaoSP(ExtratorGuias):
    # CITAÇÃO SÃO PAULO
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        valor_guia = re.search(r"Total\s*\n\s*(\d{1,3}(?:\.\d{3})*,\d{2})", texto).group(1).strip()
        valor_guia = self.formatar_valor(valor_guia.replace(".", "").replace(",", ""))
        valor_guia = re.sub('\D', '', valor_guia)

        nome_tribunal = ""
        cnpj_tribunal = ""
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE TITULO/BOLETO"

        if banco_do_brasil:
            codigo_barras = re.search(r'Banco\n(.*?)\nCorte', texto).group(1).replace(" ", "")
            numero_guia = re.search(r'[Número|Pedido]\n?\s*(\d+)\n*', texto).group(1)

        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasComplementarSP(ExtratorGuias):
    # COMPLEMENTAR SÃO PAULO
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        try:
            valor_guia = re.search(r"Dep\n(.*)\nB", texto).group(1).strip().replace(".", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            try:
                valor_guia = re.search(r"R\$\s(\d+\,\d+)", texto).group(1).strip().replace(".", "")
                valor_guia = self.formatar_valor(valor_guia)
                valor_guia = re.sub('\D', '', valor_guia)
            except:
                valor_guia = None

        nome_tribunal = "TRIBUNAL DE JUSTICA DO ESTADO DE SAO PAULO"
        cnpj_tribunal = "51174001000193"
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE TITULO/BOLETO"

        if banco_do_brasil:
            try:
                codigo_barras = re.search(r'\n(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\n', texto).group(1).replace(" ", "").replace(".", "").replace("-", "").replace("/", "")
            except:
                codigo_barras = ""
            try:
                numero_guia = re.search(r'[Número|Pedido]\n?\s*(\d+)\n*', texto).group(1)
            except:
                numero_guia = ""

        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasEPROCSP(ExtratorGuias):
    # EPROC SÃO PAULO
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        try:
            valor_guia = re.search(r"Documento\n(\d+\,\d{2})", texto).group(1).replace(".", "").replace(",", "")
            valor_ia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = re.search(r"Documento\n(\d+\.\d+\,\d{2})", texto).group(1).replace(".", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)

        nome_tribunal = ""
        cnpj_tribunal = ""
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE TITULO/BOLETO"

        if banco_do_brasil:
            try:
                nome_tribunal = re.search(r'rio\/CPF\/CNPJ\n(\D*)(?=\sCPF\/CNPJ:)', texto).group(1)
            except:
                nome_tribunal = ""
            try:
                cnpj_tribunal = re.search(r'CNPJ:\s(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})Ag', texto).group(1).replace(".", "").replace("/", "").replace("-", "")
            except:
                cnpj_tribunal = ""
            try:
                codigo_barras = re.search(r'(\|\s\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\s\d\s\d+)', texto).group(1).replace(" ", "").replace("|", "").replace(".", "").replace("-", "")
            except:
                codigo_barras = ""
            try:
                numero_guia = re.search(r'Número\n(\d+)', texto).group(1)
            except:
                numero_guia = ""

        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasIniciaisSP(ExtratorGuias):
    # INICIAL SÃO PAULO
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        try:
            valor_guia = re.search(r"R\$\s*(.*?)\n*\s*06 - Observações", texto).group(1).replace(".", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            try:
                valor_guia = re.search(r"\n(\d+,\d{2})", texto).group(1).replace(".", "")
                valor_guia = self.formatar_valor(valor_guia)
                valor_guia = re.sub('\D', '', valor_guia)
            except:
                valor_guia = None

        nome_tribunal = "TRIBUNAL DE JUSTICA DO ESTADO DE SAO PAULO"
        cnpj_tribunal = "51174001000193"
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE TITULO/BOLETO"

        if banco_do_brasil:
            try:
                codigo_barras = None
                regex_codigo_barras = [
                    r'r"Estaduais\s+(\d{11}-\d{1}\s+\d{11}-\d{1}\s+\d{11}-\d{1}\s+\d{11}-\d{1})\s+Documento"',
                    r'\n(\d{11}-\d{1}\s*\d{11}-\d{1}\s*\d{11}-\d{1}\s+\d{11}-\d{1})\s*\n?',
                    r'(\d{5}.\d{5}\s+\d{5}.\d{6}\s+\d{5}.\d{6}\s+\d{1}\s+\d{14})',
                ]
                codigo_barras = self.validar_regex(regex_codigo_barras, codigo_barras)
            except:
                codigo_barras = ""

        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasOjSP(ExtratorGuias):
    def extrair_dados(self, texto, banco_do_brasil) -> list:
        try:
            valor_guia = re.search(r"(\d+\,\d+)".format(None),texto).group(1).replace(".", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            try:
                valor_guia = re.search(r"(\d+\,\d+)".format(None), texto).group(1).replace(".", "")
                valor_guia = self.formatar_valor(valor_guia)
                valor_guia = re.sub('\D', '', valor_guia)
            except:
                valor_guia = None

        nome_tribunal = ""
        cnpj_tribunal = ""
        numero_guia = ""
        codigo_barras = ""
        texto_final = "PAGAMENTO DE TITULO/BOLETO"

        if banco_do_brasil:
            try:
                nome_tribunal = re.search(r'\d{5}\n(\D+)\s\d{4}-\w', texto).group(1)
            except:
                nome_tribunal = ""
            try:
                cnpj_tribunal = re.search(r'\s(\d+\/\d+-\d{2})\n', texto).group(1).replace(".", "").replace("/", "").replace("-", "")
            except:
                cnpj_tribunal = ""
            try:
                codigo_barras = re.search(r'\n(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d{1}\s+\d{14})\n', texto).group(1)
            except:
                codigo_barras = ""

        return [valor_guia, nome_tribunal, cnpj_tribunal, numero_guia, codigo_barras, texto_final]


class GuiasTO(ExtratorGuias):
    # TOCANTINS
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'Documento\nR\$\s?(\d+,\d{2}|\d+.\d+,\d{2})', texto).group(1).replace(".","").replace(" ", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]


class GuiasOjTO(ExtratorGuias):
    # OJ TOCANTINS
    def extrair_dados(self, texto) -> list:
        try:
            valor_guia = re.search(r'\nCR\s?(\d+,\d{2}|\d+.\d{3},\d{2})', texto).group(1).replace(".","").replace(" ", "").replace(",", "")
            valor_guia = self.formatar_valor(valor_guia)
            valor_guia = re.sub('\D', '', valor_guia)
        except:
            valor_guia = None
        return [valor_guia]

def guias_has_numero_guia_regex(tipo_custa, uf_sigla):
    try:
        regex_guia = REGEX_NUM_GUIA[f'{tipo_custa}-{uf_sigla}']
        return True
    except:
        pass
    return False

def guias_has_cod_barras_regex(tipo_custa, uf_sigla):
    try:
        regex_guia = REGEX_COD_BARRAS[f'{tipo_custa}-{uf_sigla}']
        return True
    except:
        pass
    return False

def guias_has_data_de_vencimento_regex(tipo_custa, uf_sigla):
    try:
        regex_guia = REGEX_DATA_VENCIMENTO[f'{uf_sigla}']
        return True
    except:
        pass
    return False

def guias_extrair_numero_da_guia(tipo_custa, uf_sigla, texto):
    if not guias_has_numero_guia_regex(tipo_custa, uf_sigla):
        # TODO 202608041231 esta logica de buscar guias gerais 
        # esta adicionando muita lentidão, e isso resulta em SIGKILL
        return guias_extrair_numero_da_guia_geral(uf_sigla, texto)
    numero_guia = ""
    regex_guia = REGEX_NUM_GUIA[f'{tipo_custa}-{uf_sigla}']
    for regex_pattern in regex_guia: 
        try:
            num_guia = re.search(regex_pattern, texto).group(1)
            numero_guia = re.sub(r'\D+', '', num_guia)
            if numero_guia:
                break
        except AttributeError:
            continue
    if not numero_guia:
        numero_guia = guias_extrair_numero_da_guia_geral(uf_sigla, texto)
        if not numero_guia:
            print(tipo_custa, uf_sigla, texto, regex_guia)
    return numero_guia

def guias_extrair_codigo_de_barra(tipo_custa, uf_sigla, texto):
    if not guias_has_cod_barras_regex(tipo_custa, uf_sigla):
        return guias_extrair_codigo_de_barra_geral(uf_sigla, texto)
    codigo_barras = ""
    regex_codbarras = REGEX_COD_BARRAS[f'{tipo_custa}-{uf_sigla}']
    for regex_pattern in regex_codbarras:
        try:
            cod_barras = re.search(regex_pattern, texto).group(1)
            codigo_barras = re.sub(r'\D+', '', cod_barras)
            if codigo_barras:
                break
        except AttributeError:
            continue
    if not codigo_barras:
        codigo_barras = guias_extrair_codigo_de_barra_geral(uf_sigla, texto)
        if not codigo_barras:
            print(tipo_custa, uf_sigla, texto, regex_codbarras)
    if not codigo_barras or len(codigo_barras) < 13 or len(codigo_barras) > 48:
        print("FATAL ERROR", tipo_custa, uf_sigla, texto, regex_codbarras)
        return None
    return codigo_barras

def comprovantes_extrair_codigo_de_barra(texto):
    comprovante_cod_barras = ""
    for regex_pattern in REGEX_COMPROVANTES:
        try:
            comprovante_cod_barras = re.search(regex_pattern, texto).group(1)
            comprovante_cod_barras = re.sub(r'\D+', '', comprovante_cod_barras)
            if comprovante_cod_barras:
                break
        except AttributeError:
            continue
    return comprovante_cod_barras

TIPO_CUSTA_POSSIBILIDADES = {
    "SPCI": {
        "contains": [
            "Custas iniciais",
            "Custas Intermediarias",
            "I - DAS CAUSAS EM GERAL E PROCESSOS DE COMPETÊNCIA",
            "AçãO DE EXECUçãO",
            "AçãO MONITóRIA",
            "Tipo de Guia: Guia de Recolhimento Judicial",
        ],
        "not_contains": [
            "Citação E Penhora E Avaliação",
            "CARTA PRECATÓRIA CÍVEL",
        ]
    },
    "SPOC": {
        "contains": [
            "Complementação de custas de impressão",
        ],
        "not_contains": [
        ]
    },
    "SPOJ": {
        "contains": [
            "CITAçãO, INTIMAçãO OU NOTIFICAçãO",
            "Atos de Oficiais",
            "PENHORA E AVALIAçãO",
            "Depósito Oficiais de Justiça",
            "VII - CITAÇÃO, INTIMAÇÃO, NOTIFICAÇÃO E ENTREGA DE",
            "PENHORA, ARRESTO, SEQUESTRO E OUTROS",
            "IX - AUTO DE PENHORA (INCLUÍDA A AVALIAÇÃO)",
        ],
        "not_contains": [
            "Complemento de Atos de Oficiais",
            "Despesas Postais",
        ]
    },
    "SPCPE": {
        "contains": [
            "PESQUISA ELETRÔNICA",
            "PESQUISA ELETRÓNICA",
            "CONSULTA NOS SISTEMAS - BANCEJUD",
            "Atos ocasionais",
            "XIII - PESQUISA E/OU EFETIVAÇÃO DE RESTRIÇÕES NOS",
        ],
        "not_contains": [
        ]
    },
    "SPCC": {
        "contains": [
            "XIX - CITAÇÕES E INTIMAÇÕES/NOTIFICAÇÕES POR VIA",
            "CITAÇÃO POSTAL",
            "Atos de Oficiais / Despesas Postais / e-Carta",
        ],
        "not_contains": [
        ]
    },
    "SPCP": {
        "contains": [
            "CARTA PRECATóRIA",
            "Custas iniciais",
            "III - CARTA PRECATÓRIA, DE ORDEM E ROGATÓRIA, INCLUÍDO",
            "CARTA PRECATÓRIA CÍVEL",
        ],
        "not_contains": [
        ]
    },
    "CCP": {
        "contains": [
            "Complemento de Atos de Oficiais",
        ],
        "not_contains": [
        ]
    },
    "SPDES": {
        "contains": [
            "DESARQUIVAMENTO",
            "Desarquivamento",
        ],
        "not_contains": [
        ]
    },
    "SPCDP": {
        "contains": [
            "DESARQUIVAMENTO",
            "Desarquivamento",
        ],
        "not_contains": [
        ]
    },
    "SPPE": {
        "contains": [
            "XX - PUBLICAÇÕES DE EDITAIS NO DIÁRIO DA JUSTIÇA",
            "PUBLICAÇÃO EDITAL",
        ],
        "not_contains": [
        ]
    },
    "CSF": {
        "contains": [
            "Pré-Calculada - Cumprimento de Sentença - Final",
        ],
        "not_contains": [
        ]
    },
    "SPALV": {
        "contains": [
            "XVIII - EXPEDIÇÃO DE ALVARÁ, CARTAS DE SENTENÇA",
        ],
        "not_contains": [
        ]
    },
}

def guias_extrair_tipo_de_custa(texto):
    for p in TIPO_CUSTA_POSSIBILIDADES.keys():
        for c in TIPO_CUSTA_POSSIBILIDADES[p].get("contains"):
            if TIPO_CUSTA_POSSIBILIDADES[p].get("not_contains"):
                _nc = False
                for nc in TIPO_CUSTA_POSSIBILIDADES[p].get("not_contains"):
                    if c in texto and not nc in texto:
                        _nc = True
                    else:
                        _nc = False
                if _nc:
                    return p
            else:
                if c in texto:
                    return p
    return None

def guias_extrair_valor_da_guia(uf_sigla, tipo_custa, grupo_carteira_tipo, texto):
    obj = ExtratorGuias()
    v = obj.extrair_dados(texto, uf_sigla, tipo_custa, grupo_carteira_tipo == "BB")
    return v[0]

def guias_extrair_data_de_vencimento(tipo_custa, uf_sigla, texto):
    has_fix_data_vencimento = (uf_sigla in ["MS", "RS", "ES"]) \
        or (uf_sigla == "SP" and tipo_custa in ["SPCPE", "SPDES", "SPCC"])

    if has_fix_data_vencimento:
        data = datetime.now()
        dias_uteis = 0
        dias = 5
        while dias > 0:
            data += timedelta(days=1)
            if data.weekday() < 5:
                dias_uteis += 1
                dias -= 1
        return data.strftime("%Y-%m-%d")

    if not guias_has_data_de_vencimento_regex(tipo_custa, uf_sigla):
        return None
    data_vencimento = ""
    regex_data_vencimento = REGEX_DATA_VENCIMENTO[f'{uf_sigla}']
    for regex_pattern in regex_data_vencimento:
        try:
            d = re.search(regex_pattern, texto).group(1)
            data_vencimento = re.sub(r'\D+', '', d)
            if data_vencimento:
                break
        except AttributeError:
            continue
    if data_vencimento:
        date_obj = datetime.strptime(data_vencimento, "%d%m%Y")
        data_vencimento = date_obj.strftime("%Y-%m-%d")
    return data_vencimento

def comprovantes_extrair_numero_da_guia(tipo_custa, uf_sigla, texto):
    return guias_extrair_codigo_de_barra(tipo_custa, uf_sigla, texto)

def guias_tem_apenas_pix(uf_sigla, tipo_custa=None, carteira_tipo=None, cod_barras=None):
    if cod_barras:
        return False
    if carteira_tipo and carteira_tipo in ["BB"] and uf_sigla.upper() in ["RJ"]:
        return True
    if tipo_custa and tipo_custa == "SPCI" and uf_sigla == "DF":
        return True
    if uf_sigla.upper() in ["SE", "DF"]:
        return True
    return False

def guias_extrair_codigo_de_barra_geral(_uf, _text):
    v = None
    _regex_t = REGEX_COD_BARRAS
    for k in _regex_t.keys():
        if f"-{_uf}" in k:
            for r in _regex_t[k]:
                try:
                    d = re.search(r, _text).group(1)
                    v = re.sub(r'\D+', '', d)
                    if v:
                        return v
                except AttributeError:
                    continue
    return v

def guias_extrair_numero_da_guia_geral(_uf, _text):
    v = None
    _regex_t = REGEX_NUM_GUIA
    for k in _regex_t.keys():
        if f"-{_uf}" in k:
            for r in _regex_t[k]:
                try:
                    d = re.search(r, _text).group(1)
                    v = re.sub(r'\D+', '', d)
                    if v:
                        return v
                except AttributeError:
                    continue
    return v

def guias_formatar_valor(valor_guia):
    if valor_guia is None or valor_guia == "":
        return None
    v = "R$ {:,.2f}".format(valor_guia/100)
    v = v.replace('.', 'X').replace(',', '.').replace('X', ',')
    return v 

def comprovantes_extrair_spf(texto):
    spf = re.search(r'Observação:\s*(\d{6})', texto)
    if spf:
        return spf.group(1)
    return None
