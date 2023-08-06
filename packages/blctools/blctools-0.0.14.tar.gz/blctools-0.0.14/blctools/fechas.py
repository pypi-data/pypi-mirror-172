import datetime as __dt

__formatos_default_fecha = [
    '%Y-%m-%d',
    '%d/%m/%y',
    '%d/%m/%Y',
    '%d-%m-%y',
    '%d-%m-%Y',
    '%d.%m.%y',
    '%d.%m.%Y',
    '%d%m%y',
    '%d%m%Y',
    '%y-%m-%d',
    ]

__formatos_default_periodo = [
    '%Y-%m',
    '%y-%m',
    '%Y.%m',
    '%y.%m',
    '%Y%m',
    '%y%m',
    '%Y-%m-%d',
    '%d/%m/%y',
    '%d/%m/%Y',
    '%d-%m-%y',
    '%d-%m-%Y',
    '%d.%m.%y',
    '%d.%m.%Y',
    '%d%m%y',
    '%d%m%Y',
    '%y-%m-%d'
    ] 

def hora_op(fecha):
    fecha = validar_fecha(fecha)
    if fecha.minute == 0:
        if fecha.hour == 0:
            hora_op = 24
        else:
            hora_op = fecha.hour
    else:
        hora_op = fecha.hour + 1
    
    return hora_op

def fecha_op(fecha):  
    fecha = validar_fecha(fecha)
    if hora_op(fecha) == 24 :
        if fecha.hour == 0:
            return (fecha.date() + __dt.timedelta(days=-1))
        else:
            return fecha.date()
    else:
        return fecha.date()

def sumar_mes(fecha):
    fecha = validar_fecha(fecha)
    if fecha.month == 12:
        return fecha.replace(year=fecha.year +1, month=1)
    else:
        return fecha.replace(month=fecha.month +1)
    
def restar_mes(fecha):
    fecha = validar_fecha(fecha)
    if fecha.month == 1:
        return fecha.replace(year=fecha.year -1, month=12)
    else:
        return fecha.replace(month=fecha.month -1)

def hoy():
    return __dt.datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)

def ayer():
    return __dt.datetime.today().replace(hour=0,minute=0,second=0,microsecond=0) - __dt.timedelta(days=1)

def mes_dia_1(fecha,formatos=__formatos_default_fecha,prevenir_futuro=True):
    fecha = validar_fecha(fecha,formatos=formatos,prevenir_futuro=prevenir_futuro)
    fecha = fecha.replace(day=1)
    return fecha

def mes_ult_dia(fecha,formatos=__formatos_default_fecha,prevenir_futuro=True):
    fecha = validar_fecha(fecha,formatos=formatos,prevenir_futuro=prevenir_futuro)
    fecha = sumar_mes(mes_dia_1(fecha)) - __dt.timedelta(days=1)
    return fecha

def mes_periodo(fecha,formatos=__formatos_default_periodo,prevenir_futuro=True):
    fecha_ini = mes_dia_1(fecha,formatos=formatos,prevenir_futuro=prevenir_futuro)
    fecha_fin = mes_ult_dia(fecha,formatos=formatos,prevenir_futuro=prevenir_futuro)
    fecha_ini, fecha_fin = validar_fechas(fecha_ini,fecha_fin,formatos=formatos,prevenir_futuro=prevenir_futuro)
    return fecha_ini, fecha_fin

def obtener_periodo(fecha,formatos=__formatos_default_periodo,prevenir_futuro=True):
    '''Toma una fecha y devuelve el día 1 del mes correspondiente y el último día de dicho mes.'''
    
    if isinstance(fecha,__dt.datetime):
        fi, ff = mes_periodo(fecha)
        
    elif not isinstance(fecha,str):
        raise TypeError('El valor de "período" debe ser datetime.datetime o string')
    
    elif fecha.lower() == 'mes_actual':
        fi, ff = mes_act_periodo()
        
    elif fecha.lower() == 'mes_anterior':
        fi, ff = mes_ant_periodo()
    
    else:
        fi, ff = mes_periodo(fecha)
        
    return fi,ff

def mes_act_dia_1():
    return mes_dia_1(hoy())

def mes_act_ult_dia():
    return min(hoy(),mes_ult_dia(hoy()))

def mes_act_periodo():
    return mes_periodo(mes_act_dia_1())

def mes_ant_dia_1():
    return restar_mes(mes_act_dia_1())

def mes_ant_ult_dia():
    return mes_ult_dia(mes_ant_dia_1())
    
def mes_ant_periodo():
    return mes_periodo(mes_ant_dia_1())

def iterar_entre_timestamps(ts_ini,ts_fin,timedelta,formatos=__formatos_default_fecha,prevenir_futuro=False):
    '''Itera entre dos objetos datetime. 
    El intervalo de iteración está dado por el objeto timedelta.
    
    Importante: incluye el valor final'''
    
    ts_ini, ts_fin = validar_fechas(ts_ini,ts_fin,formatos=formatos,prevenir_futuro=prevenir_futuro)
    
    td = timedelta
    ts_loop = ts_ini
    ts_loop_end = ts_fin
    
    while ts_loop <= ts_loop_end:
        
        if ts_loop == ts_ini:
            ts_cur_ini = ts_ini
            ts_cur_end = ts_ini + td

        elif ts_loop == ts_loop_end:
            ts_cur_ini = ts_loop_end
            ts_cur_end = ts_fin
            
        else:
            ts_cur_ini = ts_loop
            ts_cur_end = ts_loop + td

        yield ts_cur_ini,ts_cur_end
        
        ts_loop += td
        
def iterar_entre_timestamps_diario(ts_ini,ts_fin,formatos=__formatos_default_fecha,prevenir_futuro=False):
    '''Devuelve un iterador diario entre dos objetos datetime. 
    
    Importante: incluye el valor final'''
    
    td_obj = __dt.timedelta(days=1)
    
    return iterar_entre_timestamps(
        ts_ini,
        ts_fin,
        td_obj,
        formatos=formatos,
        prevenir_futuro=prevenir_futuro
        )

def iterar_mensual(ts_ini,ts_fin,formatos=__formatos_default_fecha,prevenir_futuro=False):
    '''Itera entre dos objetos datetime, mensualmente.
    Descarta los valores diarios y horarios que tengan las fechas ingresadas.
    Sólo tomará los valores de año y mes.
    
    Importante: incluye el valor final'''
    
    ts_ini, ts_fin = validar_fechas(ts_ini,ts_fin,formatos=formatos,prevenir_futuro=prevenir_futuro)
    
    ts_ini = ts_ini.replace(day=1)
    ts_fin = ts_fin.replace(day=1)
    
    ts_loop = ts_ini

    while ts_loop <= ts_fin:

        if ts_loop == ts_ini:
            ts_cur_ini = ts_ini
            ts_cur_end = sumar_mes(ts_ini)

        else:
            ts_cur_ini = ts_loop
            ts_cur_end = sumar_mes(ts_loop)

        yield ts_cur_ini,ts_cur_end
        
        ts_loop = sumar_mes(ts_loop)

def _procesar_formato(fecha,formato):
    try:
        return __dt.datetime.strptime(fecha,formato)
    except ValueError:
        return None

def _procesar_formatos(fecha,formatos):

    for formato in formatos:
        fecha_formateada = _procesar_formato(fecha,formato)
        if fecha_formateada != None:
            return fecha_formateada
        
    raise ValueError('Formato de fecha no reconocido.')

def input_fecha(nombre='',formatos=__formatos_default_fecha,prevenir_futuro=False):
    '''Se prueban distintas combinaciones para reconocer el formato de fecha ingresado en el input.
    Devuelve un objeto datetime.datetime'''

    if not isinstance(nombre,str):
        raise ValueError('La variable "nombre" debe ser del tipo string')

    fecha = input(f'- Ingresar fecha {nombre}: \n')

    # Procesar usando los formatos_default cargados en este archivo .py
    # El usuario podría confeccionar la lista de formatos que quisiera.
    fecha = validar_fecha(fecha,formatos=formatos,prevenir_futuro=prevenir_futuro)
    
    return fecha
    
def input_fechas(*args,formatos=__formatos_default_fecha,prevenir_futuro=False):
    '''Toma un conjunto de strings para solicitar fechas al usuario.
    Los valores deberían ser indicativos del tipo de fecha que se espera, ejemplos:
    
    ["Inicial", "Final", etc.] '''
    
    fechas = []
    for v in args:
        if not (isinstance(v,str)):
            raise ValueError(f'La variable {v} debe ser del tipo string')
        else:
            fechas.append(input_fecha(v,formatos=formatos,prevenir_futuro=prevenir_futuro))

    return fechas

def validar_fecha(fecha,formatos=__formatos_default_fecha,prevenir_futuro=True):
    '''Compara la fecha ingresada vs la fecha actual del sistema.
    Elije el valor más pequeño entre ambas. Es decir, no permite fechas futuras por defecto.'''
    if isinstance(fecha,str):
        fecha = _procesar_formatos(fecha,formatos)
        
    elif isinstance(fecha,__dt.datetime):
        pass
    
    else:
        raise ValueError('La variable "fecha" debe ser del tipo String o datetime.datetime')
    
    if prevenir_futuro:
        return min(hoy(),fecha)
    else:
        return fecha

def validar_fechas(fecha_ini,fecha_fin,formatos=__formatos_default_fecha,prevenir_futuro=True):
    '''
    Toma dos fechas, las valida usando la función validar_fecha y las ordena de más antigua a más reciente.
    '''
    fecha_ini = validar_fecha(fecha_ini,formatos=formatos,prevenir_futuro=prevenir_futuro)
    fecha_fin = validar_fecha(fecha_fin,formatos=formatos,prevenir_futuro=prevenir_futuro)
    
    fecha_ini, fecha_fin = sorted([fecha_ini,fecha_fin])
    
    return fecha_ini, fecha_fin
