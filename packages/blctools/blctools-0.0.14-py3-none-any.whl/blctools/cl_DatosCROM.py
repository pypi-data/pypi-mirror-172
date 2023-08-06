import gc
import numpy as np
import pandas as pd
import datetime as dt
from pathlib import Path

from sympy import ff

from . import eo
from . import dirs
from . import fechas

from .cl_TablasVC import *


__all__ = ['DatosCROM']

class DatosCROM(TablasVC):
    
    def __init__(
        self,
        fecha_i = None,
        fecha_f = None,
        periodo = None,
        parques = [],
        clientes = [],
        solo_CROM=False,
        dir_salida = None,
        cargar_incidencias=False,
        cargar_datos_segundales=False,
        forzar_reprocesamiento=False,
        reporte_consolidado=False,
        mensajes=True,
        mensajes_procesamiento = 1
        ):
        
        
        if reporte_consolidado:
            cargar_incidencias = True
            cargar_datos_segundales = True
        
        super().__init__(
            cargar_incidencias=cargar_incidencias,
            parques = parques,
            clientes = clientes,
            solo_CROM=solo_CROM,
            mensajes=mensajes
            )
        
        self.__dir_salida = dirs.raiz if dir_salida == None else dir_salida 
        
        self.__parques_excluidos = []
        self.__parques = [parque for parque in parques if not parque in self.__parques_excluidos]
        
        self.__forzar_reprocesamiento = forzar_reprocesamiento
        
        self.__archivos_necesarios = None
        self.__archivos_encontrados = None
        self.__archivos_faltantes = None
        self.__archivos_disponibles = None
        
        self.__fecha_i = fechas.ayer() if fecha_i is None else fechas.validar_fecha(fecha_i)
        self.__fecha_f = fechas.ayer() if fecha_f is None else fechas.validar_fecha(fecha_f)
        self.__periodo = None
        
        if periodo is None: 
            self.fecha_i = self.__fecha_i
            self.fecha_f = self.__fecha_f
        else:
            try:
                self.periodo = periodo
            except:
                print("No se pudo procesar el parámetro periodo correctamente.")
                
                self.fecha_i = self.__fecha_i
                self.fecha_f = self.__fecha_f
                
                print(f"Fecha de inicio {self.fecha_i}")
                print(f"Fecha de fin {self.fecha_f}")
        
        self.__incidencias= None
        self.__incidencias_redux = None
        self.__incidencias_explotadas = None

        self.__rpt_iec61400_minutal = None
        self.__rpt_iec61400_incidencias = None
        
        self.__rpt_consolidado_status = False
        self.__rpt_consolidado = None
        
        self.__rpt_curvas_de_potencia = None
        
        self.__mensajes_procesamiento = None
        
        self._datos_s = None
        if cargar_incidencias:
            self.__actualizar_incidencias()
        
        if mensajes_procesamiento not in [0,1,2]:
            print(f"Se esperaban valores [0,1,2] para 'mensajes_procesamiento' pero se recibió {mensajes_procesamiento}")
            print(f"Se procederá con mensajes_procesamiento=0 (apagado)")
            self.__mensajes_procesamiento = 0
        else:
            self.__mensajes_procesamiento = mensajes_procesamiento
            
        if cargar_datos_segundales and len(parques)>0:
            self.cargar_segundales(mensajes_procesamiento=mensajes_procesamiento)
            
        if reporte_consolidado and len(parques)>0:
            self.consolidar_todo(mensajes=(mensajes_procesamiento>1))

    #
    # Propiedades. Getters y Setters
    #
    @property
    def fecha_i(self):
        return self.__fecha_i
    
    @fecha_i.setter
    def fecha_i(self,val):
        '''Ingresar una fecha para usar como fecha inicial del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        fi = fechas.validar_fecha(val)
        self.__fecha_i = fi
        if self.__fecha_i <= self.__fecha_f:
            self.__actualizar_archivos()
            self.__actualizar_incidencias()

    @property
    def fecha_f(self):
        return self.__fecha_f

    @fecha_f.setter
    def fecha_f(self,val):
        '''Ingresar una fecha para usar como fecha final del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        ff = fechas.validar_fecha(val)
        self.__fecha_f = ff
        if self.__fecha_i <= self.__fecha_f:
            self.__actualizar_archivos()
            self.__actualizar_incidencias()

    @property
    def incidencias(self):
        self.__actualizar_incidencias()
        return self.__incidencias
    
    @incidencias.setter
    def incidencias(self,val):
        raise AttributeError('La propiedad "incidencias" es de sólo lectura.')

    @property
    def incidencias_redux(self):
        self.__actualizar_incidencias()
        return self.__incidencias_redux
    
    @incidencias_redux.setter
    def incidencias_redux(self,val):
        raise AttributeError('La propiedad "incidencias_redux" es de sólo lectura.')

    @property
    def incidencias_explotadas(self):
        return self.__incidencias_explotadas
    
    @incidencias_explotadas.setter
    def incidencias_explotadas(self,val):
        raise AttributeError('La propiedad "incidencias_explotadas" es de sólo lectura.')
       
    @property
    def incidencias_iec61400(self):
        return self.__rpt_iec61400_incidencias
    
    @incidencias_iec61400.setter
    def incidencias_iec61400(self,val):
        raise AttributeError('La propiedad "incidencias_iec61400" es de sólo lectura.') 
       
    @property
    def incidencias_iec61400_minutal(self):
        return self.__rpt_iec61400_minutal
       
    @incidencias_iec61400_minutal.setter
    def incidencias_iec61400_minutal(self,val):
        raise AttributeError('La propiedad "incidencias_iec61400_minutal" es de sólo lectura.')

    @property
    def datos_seg(self):
        return self._datos_s
    
    @datos_seg.setter
    def datos_seg(self,val):
        self._datos_s = val
    
    @property
    def archivos_necesarios(self):
        '''Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self.__archivos_necesarios

    @property
    def archivos_encontrados(self):
        '''Lista de objetos pathlib.Path con los archivos reales encontrados'''
        return self.__archivos_encontrados

    @property
    def archivos_faltantes(self):
        '''Archivos necesarios pero no encontrados
        Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self.__archivos_faltantes

    @property
    def archivos_disponibles(self):
        '''Combinación de archivos necesarios y encontrados
        Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self.__archivos_disponibles
        
    @archivos_necesarios.setter
    def archivos_necesarios(self,val):
        self.__archivos_necesarios = val
    
    @archivos_encontrados.setter
    def archivos_encontrados(self,val):
        self.__archivos_encontrados = val
    
    @archivos_faltantes.setter
    def archivos_faltantes(self,val):
        self.__archivos_faltantes = val
    
    @archivos_disponibles.setter
    def archivos_disponibles(self,val):
        self.__archivos_disponibles = val

    @property
    def dir_salida(self):
        return self.__dir_salida

    @dir_salida.setter
    def dir_salida(self,val):
        '''Toma una ruta a una carpeta en formato string o como objeto pathlib.Path'''
        self.__dir_salida = dirs.check_dir(val)
    
    @property
    def periodo(self):
        return self.__periodo
    
    @periodo.setter
    def periodo(self,val):
        if not (val is None):
            fi,ff = fechas.obtener_periodo(val)
            self.fecha_f = ff
            self.fecha_i = fi
            self.fecha_f = ff
            self.__periodo = val

    @property
    def rpt_consolidado(self):
        return self.__rpt_consolidado
    
    @rpt_consolidado.setter
    def rpt_consolidado(self,val):
        raise AttributeError('La propiedad "rpt_consolidado" es de sólo lectura.')

    @property
    def rpt_curvas_de_potencia(self):
        return self.__rpt_curvas_de_potencia
    
    @rpt_curvas_de_potencia.setter
    def rpt_curvas_de_potencia(self,val):
        raise AttributeError('La propiedad "rpt_curvas_de_potencia" es de sólo lectura.')

    #
    # Conjunto de funciones destinadas a procesar archivos de datos 10-segundales que se exportan automáticamente
    # desde la base de datos del Vision CROM y quedan en el OneDrive
    #
    def __actualizar_incidencias(self):
        
        if self.__fecha_i > self.fecha_f:
            print(f'Imposible actualizar incidencias. fecha_i {self.fecha_i} es mayor que fecha_f: {self.fecha_f}')
        else:
            if self.incidencias_todas is None:
                self.__incidencias= None
                
            elif not isinstance(self.incidencias_todas,pd.DataFrame):
                raise TypeError('El atributo "incidencias_todas" debe ser del tipo pandas.DataFrame o None')
            else:
                if self.incidencias_todas.empty:
                    self.__incidencias= None
                else:
                    
                    fi = self.fecha_i.replace(hour=0,minute=0,second=0)
                    ff = self.fecha_f.replace(hour=23,minute=59,second=59)
                    
                    flt_ff = self.incidencias_todas['Start'] <= ff
                    flt_fi = self.incidencias_todas['End'] >= fi
                    flt_nd = self.incidencias_todas['Status'].str.upper() != 'DESCARTADA'
                    
                    flt_activa = flt_fi & flt_ff & flt_nd
                    
                    seleccion_valida = not(self.parques == [] and self.clientes == [])
                    
                    if seleccion_valida:
                        if self.parques != []:
                            flt_ucs = self.incidencias_todas['UC'].isin(self.parques) 
                            flt_nemos = self.incidencias_todas['Nemo'].isin(self.parques) 
                            flt_pq = flt_ucs | flt_nemos
                            flt = flt_activa & flt_pq
                        else:
                            flt_cl = self.incidencias_todas['Owner'].isin(self.clientes) 
                            flt = flt_activa & flt_cl

                        self.__incidencias= self.incidencias_todas.loc[flt,:].copy(deep=True).reset_index(drop=True)
                        
                    if not self.__incidencias.empty:
                        cols_redux = ['ID','Owner','Nemo','Equipo','Pnom','Start','End','Hours','ENS','SolvedBy','Reason','Origin','Code','Pteo','SP_P','BLC_Description']

                        self.__incidencias_redux = self.__incidencias.loc[:,cols_redux]

    def __actualizar_archivos(self):
        if self.__fecha_i > self.fecha_f:
            print(f'Imposible actualizar listados de archivos. fecha_i {self.fecha_i} es mayor que fecha_f: {self.fecha_f}')
        else:
            self.archivos_encontrados = self.__obtener_archivos_encontrados()
            self.archivos_necesarios = self.__obtener_archivos_necesarios()
            
            nombres_encontrados = [archivo.stem for archivo in self.archivos_encontrados]
            existe = lambda x: x.stem in nombres_encontrados
            no_existe = lambda x: not x.exists()

            self.archivos_faltantes = list(filter(no_existe,self.archivos_necesarios))
            self.archivos_disponibles = list(filter(existe,self.archivos_necesarios))
        
    def __obtener_archivos_encontrados(self):

        archivos_totales = self.__buscar_archivos_10s_ct_rango()
        parques_vacio = self.parques == [] or self.parques == None or len(self.parques)==0
        
        pertenece_a_parques_seleccionados = lambda archivo: any(parque in archivo.name for parque in self.parques)
        
        if parques_vacio:
            return archivos_totales
        else:
            return list(filter(pertenece_a_parques_seleccionados,archivos_totales))

    def __obtener_archivos_necesarios(self):
        
        iterable = fechas.iterar_entre_timestamps_diario(self.fecha_i,self.fecha_f)
        get_carpeta = lambda x : Path(dirs.get_dc_10s_fecha(x))
        
        carpetas = [get_carpeta(fi) for fi,_ in iterable]
        
        parques_vacio = self.parques == [] or self.parques == None or len(self.parques)==0
        parques = self.nemos if parques_vacio else self.parques

        if parques != []:
            archivos_necesarios = []
            for carpeta in carpetas:
                for parque in parques:
                    if parque in self.__parques_excluidos:
                        continue

                    fecha_archivo = carpeta.stem.replace('-','.')
                    
                    archivo = f'{carpeta}\\{fecha_archivo} {parque}'
                    archivo_pickle = Path(archivo + '.pickle')
                    archivo_xlsx = Path(archivo + '.xlsx')
                    
                    if archivo_pickle.exists() and not self.__forzar_reprocesamiento:
                        archivos_necesarios.append(archivo_pickle)
                    else:
                        archivos_necesarios.append(archivo_xlsx)
                        
            return archivos_necesarios
        else:
            return []

    def __buscar_archivos_10s_ct_rango(self):
        
        iterable = fechas.iterar_entre_timestamps_diario(self.fecha_i,self.fecha_f)
        
        lista_de_listas = [self.__buscar_archivos10s_diarios(fi) for fi,_ in iterable]
        lista_unificada = [archivo for lista_archivos in lista_de_listas for archivo in lista_archivos]
        return lista_unificada

    def __buscar_archivos10s_diarios(self,fecha):
        '''Para un día determinado, busca los archivos .xlsx de la central elegida.
        Importante: la fecha debe proveerse como objeto datetime'''
        
        dir_tmp = Path(dirs.get_dc_10s_fecha(fecha))
        if dir_tmp.exists():
        
            iterable = dir_tmp.iterdir()
            
            archivos_xlsx = dirs.filtra_archivos(iterable,'.xlsx')
            archivos_pickle = dirs.filtra_archivos(iterable,'.pickle')
            
            nombres_archivos_pickle = (archivo.stem for archivo in archivos_pickle)
            
            archivos_xlsx_no_procesados = [archivo for archivo in archivos_xlsx if not (archivo.stem in nombres_archivos_pickle)]
            
            return archivos_pickle + archivos_xlsx_no_procesados

        else:
            return []

    def __renombrar_lvl0(self,texto,prefijo_generador='WTG'):
        texto = texto.replace('Datos del parque','PLANT')
        
        if 'Unnamed: 0_level_0' in texto:
            texto = ''
        
        #La cantidad de 0s delante del número del ezuipo (.zfill)
        #debería ser dinámica, de acuerdo a la cantidad de equipos en la planta
        #el mínimo de dígitos es 2
        if 'Datos del equipo' in texto:
            generador = texto.split(' ')[-1].zfill(2)
            texto = ''.join([prefijo_generador,generador])

        return texto

    def __renombrar_lvl1(self,texto):
        v = texto
        v = v.replace('Wind Dir','Wind_dir')
        v = v.replace('Wind Speed','Wind')
        v = v.replace('P Disponible','Ppos')
        v = v.replace('FB Consigna P Equipo','SP_P')
        v = v.replace('Q Equipo','Q')
        v = v.replace('P Equipo','P')
        v = v.replace('Estado','op_state')
        v = v.replace('Consigna P','SP_P')
        v = v.replace('Consigna Q','SP_Q')
        v = v.replace('Consigna V','SP_V')
        v = v.replace('FB ','FB_')
        
        return v

    def __obtener_id_central(self,nemo_parque):
        mapeo_nemo_idcentral = self._crear_dict(self.central,'nemoCammesa','idcentral')
        return mapeo_nemo_idcentral[nemo_parque]
        
    def __obtener_prefijo_equipos(self,nemo_parque):
        
        id_central = self.__obtener_id_central(nemo_parque)
        
        #Chequear otro método de obtener el prefijo, que no sea reposando sobre el "not null"
        equipos = self.tipoequipo\
                    .query(f'id_central == {id_central} & fabricante.notnull()')\
                    .loc[:,'equipo']\
                    .to_list()
                    
        #Con esto alcanza para eólicos
        remover_numeros = lambda s: ''.join([c for c in s if not c.isdigit()])
        
        #Pensar cómo resolver para solares que tienen nombres tipo
        #INV1_25
        prefijo = set(map(remover_numeros,equipos))
        if len(prefijo) != 1:
            raise ValueError(f'Se han encontrado más de un prefijo de equipos para el parque {nemo_parque}.\n A saber: {prefijo}')
        else:
            return prefijo.pop()

    def __renombrar_cols(self,cols,nemo_parque):
        
        prefijo = self.__obtener_prefijo_equipos(nemo_parque)
        nuevas_cols = []
        for col in cols:
            lvl0 = self.__renombrar_lvl0(texto=col[0],prefijo_generador=prefijo)
            lvl1 = self.__renombrar_lvl1(col[1])
            nuevas_cols.append((nemo_parque,lvl0,lvl1))
        
        nuevas_cols[0] = ('t_stamp','t_stamp','t_stamp')
        return nuevas_cols

    def __preprocesar_un_xlsx(self,archivo,mensajes_shallow=False,mensajes_deep=False):
        
        nemo_parque = archivo.stem.split(' ')[-1]
        
        if archivo.exists():
            df = pd.read_excel(archivo,skiprows=1,header=[0,1])
            
            #Devuelve una lista de tuples con formato (p,e,v)
            # p = parque, e = equipo (WTG), v = variable
            nuevas_columnas = self.__renombrar_cols(cols=df.columns,nemo_parque=nemo_parque)
            
            df.columns = pd.MultiIndex.from_tuples(nuevas_columnas,names=['Parque','Equipo','Variable'])

            df.set_index(keys=('t_stamp','t_stamp','t_stamp'),drop=True,inplace=True)
            df.index.name = 't_stamp'
            
            self.datos_seg = df.copy(deep=True)
            self.__procesar_d10s(mensajes_shallow=mensajes_shallow,mensajes_deep=mensajes_deep)
            
            nuevo_archivo = str(archivo.parent) + '\\' + archivo.stem + '.pickle'
            self.datos_seg.to_pickle(nuevo_archivo)
            self.datos_seg = None
            del df
            gc.collect()
        else:
            # Esto debería haber quedado solucionado con la lógica de archivos disponibles vs necesarios.
            # ¿Qué pasó?
            print(f'El archivo "{archivo.name}" no existe.')

    def __procesar_d10s(self,mensajes_shallow=True,mensajes_deep=True):
        '''Toma los datos 10 segundales pre-procesados y
        sobre ellos se realiza data cleaning/formating, feauture engineering'''

        # Procesamientos generales de aeros
        # sin importar el parque al que pertenecen.
        if mensajes_shallow: print("\tProcesando datos 10 segundales: Iteración 1")
        self.__procesar_d10s_1i(mensajes=mensajes_deep)

        # Procesamientos específicos por parque 
        # Calcula potencias, energías, vientos promedios, direcciones, etc.
        # Por parque, agrupamiento(s) y agrega potencias nominales de equipos.
        if mensajes_shallow: print("\tProcesando datos 10 segundales: Iteración 2")
        self.__procesar_d10s_2i(mensajes=mensajes_deep)
        
        # Procesamientos por parque de todos los equipos
        # Magnitudes unitarias, coeficientes (FC, PI)
        if mensajes_shallow: print("\tProcesando datos 10 segundales: Iteración 3")
        self.__procesar_d10s_3i(mensajes=mensajes_deep)
        
        # Dedicada a procesar la Pposible y sus eventuales huecos
        if mensajes_shallow: print("\tProcesando datos 10 segundales: Iteración 4")
        self.__procesar_d10s_4i(mensajes=mensajes_deep)
        
        #Reordenar las columnas del dataframe
        levels = self.datos_seg.columns.names
        self.datos_seg.sort_index(
            axis=1,
            level=levels,
            ascending=[1 for l in levels],
            inplace=True
            )
        
    def __procesar_d10s_1i(self,mensajes=True):
        #Esta función toma unos pocos segundos ejecutarse
        
        get_equipos = lambda x: self.consultar_equipos_parque_no_agrupamientos(nemo_parque=x)
        
        #Identificar parques y aerogeneradores a procesar
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))

        #Procesar sólo algunas variables de los Aerogeneradores
        viento_vel_bins, viento_vel_labels = eo.crear_bins_viento_vel(lower_val=0,upper_val=40,step=0.5)
        viento_dir_bins, viento_dir_labels = eo.crear_bins_viento_dir()
        for p in parques_con_datos:

            # Cambio de unidades de las variables de planta
            if mensajes: print(f"Cambiando unidades de {p}'PLANT'")
            seleccion = (p,'PLANT',['P','SP_P','Q'])
            self.datos_seg.loc[:,seleccion] = self.datos_seg.loc[:,seleccion] * 1000    # de MW a kW
            
            equipos = get_equipos(p) 
            i = 0
            k = len(equipos)
            for e in equipos:
                i+=1

                if mensajes: print(f"Procesando {i} de {k} {p} {e}: Discriminando entre potencia generada de consumida")
                flt_p_gen = self.datos_seg.loc[:,(p,e,'P')] >= 0
                flt_p_con = self.datos_seg.loc[:,(p,e,'P')] <= 0

                self.datos_seg.loc[:,(p,e,'Pgen')] = self.datos_seg.loc[:,(p,e,'P')] * flt_p_gen
                self.datos_seg.loc[:,(p,e,'Pcon')] = self.datos_seg.loc[:,(p,e,'P')] * flt_p_con
            
                if mensajes: print(f"Procesando {i} de {k} {p} {e}: Calculando energías")
                self.datos_seg.loc[:,(p,e,'Egen')] = self.datos_seg.loc[:,(p,e,'Pgen')] * (10/3600)
                self.datos_seg.loc[:,(p,e,'Econ')] = self.datos_seg.loc[:,(p,e,'Pcon')] * (10/3600)
                self.datos_seg.loc[:,(p,e,'Epos')] = self.datos_seg.loc[:,(p,e,'Ppos')] * (10/3600)

                if mensajes: print(f"Procesando {i} de {k} {p} {e}: Wind_dir_r")
                self.datos_seg.loc[:,(p,e,'Wind_dir_r')] = pd.cut(
                                                        self.datos_seg.loc[:,(p,e,'Wind_dir')],
                                                        bins=viento_dir_bins,
                                                        labels=viento_dir_labels,
                                                        ordered=False,
                                                        include_lowest=True
                                                        )
                
                if mensajes: print(f"Procesando {i} de {k} {p} {e}: Wind_bin")
                self.datos_seg.loc[:,(p,e,'Wind_bin')] = pd.cut(
                                                        self.datos_seg.loc[:,(p,e,'Wind')],
                                                        bins=viento_vel_bins,
                                                        labels=viento_vel_labels,
                                                        ordered=True,
                                                        include_lowest=True
                                                        )
                
            self.datos_seg = self.datos_seg.copy(deep=True)
            gc.collect()

    def __procesar_d10s_2i(self,mensajes=True):
        #Esta función toma 1 minuto por mes, aprox
        
        get_agrupamientos = lambda x: self.consultar_agrupamientos_parque(nemo_parque=x)
        get_equipos = lambda x: self.consultar_equipos_parque_no_agrupamientos(nemo_parque=x)
        get_equipos_agr = lambda parque,agrupamiento: self.consultar_equipos_por_agrupamiento(nemo_parque=parque)[agrupamiento]

        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        viento_vel_bins, viento_vel_labels = eo.crear_bins_viento_vel(lower_val=0,upper_val=40,step=0.5)
        viento_dir_bins, viento_dir_labels = eo.crear_bins_viento_dir()
        vars_suma_circ = ['P', 'Q', 'SP_P']
        vars_suma = ['Pgen','Pcon','Egen','Econ']
        vars_prom = ['Wind','Wind_dir',]
        
        for p in parques_con_datos:
            # Diccionario equipos y su potencia en MW
            ep = self.consultar_equipos_parque(nemo_parque=p,potencia=True) # {'PLANT':80,'CIRCUITO n': 14, 'WTGnn':3.6}
            ep = {k:v*1000 for k,v in ep.items()}                           # Convertir de NW a kW
            
            #Procesar agrupamientos de aerogeneradores
            parque_agrupamientos = get_agrupamientos(p)
            for a in parque_agrupamientos:
                equipos_agrup = get_equipos_agr(p,a)
                pot_a = ep[a]
                
                for var in vars_suma_circ + vars_suma:
                    if mensajes: print(f"Procesando {p} {a}: {var}")
                    self.datos_seg.loc[:,(p,a,var)] = self.datos_seg.loc[:,(p,equipos_agrup,var)].sum(axis=1)
                    
                for var in vars_prom:
                    if mensajes: print(f"Procesando {p} {a}: {var}")
                    self.datos_seg.loc[:,(p,a,var)] = self.datos_seg.loc[:,(p,equipos_agrup,var)].mean(axis=1).fillna(0)
                                
                if mensajes: print(f"Procesando {p} {a}: Pnom")
                self.datos_seg.loc[:,(p,a,'Pnom')] = pot_a

                if mensajes: print(f"Procesando {p} {a}: Wind_dir_r")
                self.datos_seg.loc[:,(p,a,'Wind_dir_r')] = pd.cut(
                                                        self.datos_seg.loc[:,(p,a,'Wind_dir')],
                                                        bins=viento_dir_bins,
                                                        labels=viento_dir_labels,
                                                        ordered=False,
                                                        include_lowest=True
                                                        )
                
                if mensajes: print(f"Procesando {p} {a}: Wind_bin")
                self.datos_seg.loc[:,(p,a,'Wind_bin')] = pd.cut(
                                                        self.datos_seg.loc[:,(p,a,'Wind')],
                                                        bins=viento_vel_bins,
                                                        labels=viento_vel_labels,
                                                        ordered=True,
                                                        include_lowest=True
                                                        )

            #Procesar aerogeneradores, individualizados por parque
            parque_equipos = get_equipos(p)
            for e in parque_equipos:
                pot_e = ep[e]
                if mensajes: print(f"Procesando {p} {e}: Pnom")
                self.datos_seg.loc[:,(p,e,'Pnom')] = pot_e

            #Procesar variables de todo el parque ('PLANT')
            pot_p = ep['PLANT']
            if mensajes: print(f"Procesando {p}: Pnom")
            self.datos_seg.loc[:,(p,'PLANT','Pnom')] = pot_p
            
            for var in vars_suma:
                if mensajes: print(f"Procesando {p} 'PLANT': {var}")
                self.datos_seg.loc[:,(p,'PLANT',var)] = self.datos_seg.loc[:,(p,equipos_agrup,var)].sum(axis=1)
                
            for var in vars_prom:
                if mensajes: print(f"Procesando {p} 'PLANT': {var}")
                self.datos_seg.loc[:,(p,'PLANT',var)] = self.datos_seg.loc[:,(p,parque_equipos,var)].mean(axis=1)

            if mensajes: print(f"Procesando {p} 'PLANT': Wind_dir_r")
            self.datos_seg.loc[:,(p,'PLANT','Wind_dir_r')] = pd.cut(
                                                    self.datos_seg.loc[:,(p,'PLANT','Wind_dir')],
                                                    bins=viento_dir_bins,
                                                    labels=viento_dir_labels,
                                                    ordered=False,
                                                    include_lowest=True
                                                    )
            if mensajes: print(f"Procesando {p} 'PLANT': Wind_bin")
            self.datos_seg.loc[:,(p,'PLANT','Wind_bin')] = pd.cut(
                                                    self.datos_seg.loc[:,(p,'PLANT','Wind')],
                                                    bins=viento_vel_bins,
                                                    labels=viento_vel_labels,
                                                    ordered=True,
                                                    include_lowest=True
                                                    )
            
        self.datos_seg = self.datos_seg.copy(deep=True)
        gc.collect()

    def __procesar_d10s_3i(self,mensajes=True):
        # Esta función toma aprox 9 minutos para un mes, por parque
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        
        vars_unitarias = ['Pgen','Pcon','Egen','Econ',]
               
        for p in parques_con_datos:
            # ep = Equipos del Parque 
            # ['PLANT','CIRCUITO 1',..,'CIRCUITO n','WTG01',...,'WTGnn]
            ep = self.consultar_equipos_parque(nemo_parque=p)

            for e in ep:
                    pnom = (p,e,'Pnom')   # Tuple que se utiliza para ubicar la columna en el MultiIndex del DataFrame
                    for v in vars_unitarias:
                        old = (p,e,v)         # Tuple que se utiliza para ubicar la columna en el MultiIndex del DataFrame
                        new = (p,e,v+'_U')    # Tuple que se utiliza para CREAR la nueva columna en el DataFrame
                        if mensajes: print(f"Procesando {p} {e} {v}_U")
                        self.datos_seg.loc[:,new] = self.datos_seg.loc[:,old] / self.datos_seg.loc[:,pnom]
                    
                    #Preconfigurar algunas selecciones de columna
                    # Tuples que se utilizan para ubicar la respectiva variable en el MultiIndex del DataFrame
                    fc = (p,e,'FC'); pgenu = (p,e,'Pgen_U')
                    
                    if mensajes: print(f"Procesando {p} {e} FC") #Sí, es igual a Pgen_U, pero psicológicamente impacta si no está. 
                    self.datos_seg.loc[:,fc] = self.datos_seg.loc[:,pgenu]

        self.datos_seg = self.datos_seg.copy(deep=True)
        gc.collect()

    def __procesar_d10s_4i(self,mensajes=True):
        
        get_agrupamientos = lambda x: self.consultar_agrupamientos_parque(nemo_parque=x)
        get_equipos = lambda x: self.consultar_equipos_parque_no_agrupamientos(nemo_parque=x)
        get_equipos_agr = lambda parque,agrupamiento: self.consultar_equipos_por_agrupamiento(nemo_parque=parque)[agrupamiento]

        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        for p in parques_con_datos:
            
            equipos = get_equipos(p)
            for e in equipos:
                eq = e
                ppos = (p,eq,'Ppos') ; pposu = (p,eq,'Ppos_U') ; pnom = (p,eq,'Pnom')
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos_U")
                self.datos_seg.loc[:,pposu] = self.datos_seg.loc[:,ppos].div(self.datos_seg.loc[:,pnom])
                
            #Completar Ppos_U, Ppos y PI a nivel planta
            eq = 'PLANT'
            ppos = (p,eq,'Ppos') ; pposu = (p,eq,'Ppos_U') ; pnom = (p,eq,'Pnom') ; pi = (p,eq,'PI') ; pgen = (p,eq,'Pgen')
            epos = (p,eq, 'Epos') ; eposu = (p,eq, 'Epos_U')
            
            if mensajes: print(f"Procesando {p} {eq}: Ppos_U")
            self.datos_seg.loc[:,pposu] = self.datos_seg.loc[:,(p,equipos,'Ppos_U')].mean(axis=1)
            
            if mensajes: print(f"Procesando {p} {eq}: Ppos")
            self.datos_seg.loc[:,ppos] = self.datos_seg.loc[:,pposu] * self.datos_seg.loc[:,pnom]
            
            if mensajes: print(f"Procesando {p} {eq}: PI")
            self.datos_seg.loc[:,pi] = self.datos_seg.loc[:,pgen] * self.datos_seg.loc[:,ppos]

            if mensajes: print(f"Procesando {p} {eq}: Epos")
            self.datos_seg.loc[:,epos] = self.datos_seg.loc[:,ppos] * (10/3600)
            
            if mensajes: print(f"Procesando {p} {eq}: Epos_U")
            self.datos_seg.loc[:,eposu] = self.datos_seg.loc[:,pposu] * (10/3600)
            
            # Rellenar huecos de Ppos(_U) en generadores
            # Con el promedio de los que sí tienen Ppos(_U)
            for e in equipos:
                eq = e
                ppos = (p,eq,'Ppos') ; pposu = (p,eq,'Ppos_U') ; pnom = (p,eq,'Pnom') ; pi = (p,eq,'PI') ; pgen = (p,eq,'Pgen')
                epos = (p,eq, 'Epos') ; eposu = (p,eq, 'Epos_U')
                
                #Detectar huecos de Ppos (Es lo mismo que los huecos de Ppos_U)
                hay_hueco = self.datos_seg.loc[:,ppos].isna()
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos_U (rellenando huecos)")
                self.datos_seg.loc[hay_hueco,pposu] =  self.datos_seg.loc[hay_hueco,(p,'PLANT','Ppos_U')]
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos (rellenando huecos)")
                self.datos_seg.loc[hay_hueco,ppos]  = self.datos_seg.loc[hay_hueco,pposu] * self.datos_seg.loc[hay_hueco,pnom] 
                
                if mensajes: print(f"Procesando {p} {eq}: PI")
                self.datos_seg.loc[:,pi] = self.datos_seg.loc[:,pgen] * self.datos_seg.loc[:,ppos]

                if mensajes: print(f"Procesando {p} {eq}: Epos")
                self.datos_seg.loc[:,epos] = self.datos_seg.loc[:,ppos] * (10/3600)
                
                if mensajes: print(f"Procesando {p} {eq}: Epos_U")
                self.datos_seg.loc[:,eposu] = self.datos_seg.loc[:,pposu] * (10/3600)
            
            # Calcular Ppos_U y Ppos para los agrupamientos
            agrupamientos = get_agrupamientos(p)
            for a in agrupamientos:
                eq = a
                ppos = (p,eq,'Ppos') ; pposu = (p,eq,'Ppos_U') ; pnom = (p,eq,'Pnom') ; pi = (p,eq,'PI') ; pgen = (p,eq,'Pgen')
                epos = (p,eq, 'Epos') ; eposu = (p,eq, 'Epos_U')
                
                equipos_agr = get_equipos_agr(p,a)
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos_U")
                self.datos_seg.loc[:,pposu] = self.datos_seg.loc[:,(p,equipos_agr,'Ppos_U')].mean(axis=1)
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos")
                self.datos_seg.loc[:,ppos] = self.datos_seg.loc[:,pposu] * self.datos_seg.loc[:,pnom] 
                
                if mensajes: print(f"Procesando {p} {eq}: PI")
                self.datos_seg.loc[:,pi] = self.datos_seg.loc[:,pgen] * self.datos_seg.loc[:,ppos] 

                if mensajes: print(f"Procesando {p} {eq}: Epos")
                self.datos_seg.loc[:,epos] = self.datos_seg.loc[:,ppos] * (10/3600)
                
                if mensajes: print(f"Procesando {p} {eq}: Epos_U")
                self.datos_seg.loc[:,eposu] = self.datos_seg.loc[:,pposu] * (10/3600)

        self.datos_seg = self.datos_seg.copy(deep=True)
        gc.collect()

    def preprocesar_archivos_disponibles(self,mensajes_procesamiento=0):
        
        mensajes_shallow = False if mensajes_procesamiento == 0 else True,
        mensajes_deep = False if mensajes_procesamiento < 2 else True
        
        ahora = dt.datetime.now()
        
        #Lista de objetos Path con la ruta completa hacia los archivos .xlsx o .pickle
        a_pre_procesar = [archivo for archivo in self.archivos_disponibles if archivo.name.lower().endswith('.xlsx')]
        
        
        
        if a_pre_procesar:
            
            #Elijo el primer archivo, 
            # obtengo su nombre sin la extensión (stem), parto el nombre en dos (split(' ')) y me quedo con el último pedazo [-1]
            parque = a_pre_procesar[0].stem.split(' ')[-1]
            equipos_totales = len(self.consultar_equipos_parque(nemo_parque=parque))
                                  
            n_archivos = len(a_pre_procesar)

            k = equipos_totales * n_archivos  # Archivos x cantidad de equipos en el parque
            
            ritmo_slow = 2.95  # Archivos * Equipo / segundo
            ritmo_fast = 2.35  # Archivos * Equipo / segundo
            
            tiempo_slow = ritmo_slow * k * (1/60)  # Conversión a minutos
            tiempo_fast = ritmo_fast * k * (1/60)  # Conversión a minutos
            
            min_slow = int(tiempo_slow) ; min_fast = int(tiempo_fast)
            sec_slow = round(((tiempo_slow) - min_slow)*60)
            sec_fast = round(((tiempo_fast) - min_fast)*60)
            
            if mensajes_shallow: print(f'Se pre-procesarán {n_archivos} archivos Excel. Paciencia...')
            if mensajes_shallow: print(f'Tiempo estimado: entre {min_fast}min {sec_fast}seg y {min_slow}min {sec_slow}seg.')
            
            for archivo in a_pre_procesar:
                if mensajes_shallow: print(f'Pre-procesando: {archivo.name}')
                self.__preprocesar_un_xlsx(archivo,mensajes_shallow=mensajes_shallow,mensajes_deep=mensajes_deep)
            # Deshabilitar el fuerce de carga de archivos. Inevitablemente ya se re-procesó a esta altura.
            self.__forzar_reprocesamiento = False
            self.__actualizar_archivos()
            
            duracion = (dt.datetime.now() - ahora).total_seconds() 
            ritmo = duracion / len(a_pre_procesar)
            
            if mensajes_shallow: print(f'Pre-procesamiento finalizado. Duración: {round(duracion)}seg a razón de {round(ritmo)} seg/archivo.')

    def cargar_segundales(self,fecha_i=None,fecha_f=None,mensajes_procesamiento=0):
        if not fecha_i is None:
            self.fecha_i = fecha_i
        
        if not fecha_f is None:
            self.fecha_f = fecha_f
        
        self.preprocesar_archivos_disponibles(mensajes_procesamiento=mensajes_procesamiento)
        
        if len(self.archivos_disponibles) >0:
            if mensajes_procesamiento: print(f'Cargando {len(self.archivos_disponibles)} archivos en la memoria...')
            
            lista_dfs_ancha = []
            for p in self.parques:
                lista_dfs_larga = []
                for archivo in self.__archivos_disponibles:
                    if p in archivo.name:
                        if mensajes_procesamiento: print(f'Cargando {archivo.name}...')
                        lista_dfs_larga.append(pd.read_pickle(archivo)) 
                
                lista_dfs_ancha.append(pd.concat(lista_dfs_larga,ignore_index=False))
            
            df_left = None
            for df_right in lista_dfs_ancha:
                
                if df_left is None:
                    df_left = df_right.copy(deep=True)
                else:
                    df_left = df_left.join(df_right,how='outer')
            
            self.datos_seg = df_left.copy(deep=True)
            
            self.datos_seg.sort_index(
                axis=0,
                ascending=True,
                inplace=True
                )
            
            del df_left, df_right, lista_dfs_ancha, lista_dfs_larga
            gc.collect()
        else:
            raise Exception(f'No hay archivos con datos 10 segundales disponibles para cargar de los parques {self.parques}')

    #
    # Conjunto de funciones destinadas a procesar las incidencias "crudas" (según las devuelve TablasVC())
    #
    def __check_jerarquia_equipos_iterable(self,iterable):
        
        valores_posibles = ['WTG','BOP','GRID']
        
        if len(iterable) != 3:
            raise Exception('El iterable con la jerarquía de priorización de incidencias, debe tener exactamente 3 elementos: "WTG","BOP" y "GRID" en algún orden.')
        
        for x in iterable:
            if not isinstance(x,str):
                raise ValueError(f'Error al procesar el valor {x}. El iterable con la jerarquía de priorización de incidencias, debe tener exactamente 3 elementos: "WTG","BOP" y "GRID" en algún orden.')
            
            if not x.upper() in valores_posibles:
                raise ValueError(f'Error al procesar el valor {x}. El iterable con la jerarquía de priorización de incidencias, debe tener exactamente 3 elementos: "WTG","BOP" y "GRID" en algún orden.')

        user_values = [x.upper() for x in iterable]
        k = len(user_values)
        return {v:(k-i) for i,v in enumerate(user_values)}

    def __check_jerarquia_equipos(self,jerarquia_equipos='WTG',mensajes=False):
        defaults = {
            'WTG'  : {'WTG': 3, 'BOP': 2, 'GRID': 1},
            'BOP'  : {'BOP': 3, 'WTG': 2, 'GRID': 1},
            'GRID' : {'GRID': 3, 'BOP': 2, 'WTG': 1}
        }
        
        if isinstance(jerarquia_equipos,str):
            if jerarquia_equipos.upper() in defaults.keys():
                return defaults[jerarquia_equipos]
            else:
                raise ValueError('El parámetro "método" debe ser "WTG", "BOP", "GRID", o una lista/tupla jerarquizando dichos grupos, de más importante a menos importante')
        elif isinstance(jerarquia_equipos,(list,tuple)):
            return self.__check_jerarquia_equipos_iterable(jerarquia_equipos)
        else:
            print(f"El valor recibido de jerarquia_equipos es: {jerarquia_equipos}. Tipo {type(jerarquia_equipos)}")
            raise TypeError('El parámetro "método" debe ser "WTG", "BOP", "GRID", o una lista/tupla jerarquizando dichos grupos, de más importante a menos importante')

    def __iec61400_crear_indice_fechas(self,mensajes=False):
        #Obtener extremos de fecha del dataframe de incidencias
        fi = self.incidencias.Start.min()
        ff = max(self.incidencias.Start.max(),self.incidencias.End.max())
        
        #Iterar minutalmente entre ambos extremos, para construir una lista de fechas, cada 1 minuto
        td = dt.timedelta(minutes=1)
        iterable = fechas.iterar_entre_timestamps(fi,ff,td)
        lista_fechas = [x[0] for x in iterable]

        return pd.Index(lista_fechas)

    def __iec61400_crear_columnas_pev(self,i,mensajes=False):
        #pev = (Parque, Equipo, Variable)
        
        get_equipos_parque = lambda x: self.consultar_equipos_parque(nemo_parque=x)
        get_pot_pe = lambda p,e: self.consultar_equipos_parque(nemo_parque=p,potencia=True)[e]*1000

        # Inicializar arrays de numpy
        # Crea un array vacío de 1 dimensión y largo n
        # Asigna np.nan a todos los valores del array
        n = len(i)
        nans   = np.empty(n); nans[:] = np.nan     
        trues  = np.empty(n); trues[:] = True 
        falses = np.empty(n); falses[:] = False
        zeros  = np.zeros(n)

        #Crea una instancia de cada tipo de serie en la memoria, de largo n
        s_bool_t = pd.Series(data=trues,index=i,dtype=bool)
        s_bool_f = pd.Series(data=falses,index=i,dtype=bool)
        s_f64 = pd.Series(data=zeros,index=i,dtype='float64')
        s_i64 = pd.Series(data=zeros,index=i,dtype='Int64')
        s_str = pd.Series(data=nans,index=i,dtype=str)

        cols_dtypes =  {
                'ID':s_i64, 
                'SolverAgent':s_str,'Reason':s_str,'Origin':s_str,'Priority_IEC':s_i64,  
                'Pnom':None,'PotDis':s_f64,
                'FullPerf':s_bool_t,
                'Lim':s_bool_f,'LimExt':s_bool_f,'LimInt':s_bool_f,
                'Ind':s_bool_f,'IndExt':s_bool_f,'IndInt':s_bool_f,
                'ENS':s_f64,
                'ENS_Lim':s_f64,'ENS_LimExt':s_f64,'ENS_LimInt':s_f64,
                'ENS_Ind':s_f64,'ENS_IndExt':s_f64,'ENS_IndInt':s_f64,
        }

        #p = Parque, e = equipo, v = variable, t = DataType
        parques_con_datos = set(self.incidencias.Nemo)

        columnas = {}
        for p in parques_con_datos:
            for e in get_equipos_parque(p):
                for v,t in cols_dtypes.items():
                    if v == 'Pnom':
                        pot = np.empty(n) 
                        pot[:] = get_pot_pe(p,e)
                        columnas[(p,e,v)] = pd.Series(data=pot,index=i,dtype='float64')
                    else:
                        columnas[(p,e,v)] = t   
        return columnas
    
    def __iec61400_preparar_df_vacio_minutal(self,mensajes=False):
        # A partir del DataFrame de incidencias contenido en el objeto DatosCROM().incidencias
        # se crea un dataframe vacío con índice de fechas minutal, con:
        #   inicio en la fecha Start de la incidencia más antigua
        #   finalización en la fecha End de la incidencia más reciente
        #   Columnas Multi Índice del tipo (Parque, Elemento, Variable). Elementos pueden ser = 'PLANT', 'CIRCUITO 1', 'WTG01', etc.
        
        i = self.__iec61400_crear_indice_fechas()
        c = self.__iec61400_crear_columnas_pev(i)
        
        self.__rpt_iec61400_minutal = pd.DataFrame(c,index=i)

    def __iec61400_explotar_minutalmente_incidencias(self,jerarquia_equipos='WTG',mensajes=False):
        
        # Crear una versión reducida del dataframe de incidencias del CROM
        cols = ['ID','Nemo','Start','End','Equipo','Pnom','Hours','ENS','SolverAgent','Reason','Origin','Priority_IEC']

        flt_ok = self.incidencias.Status != 'DESCARTADA'
        df_inc = self.incidencias.loc[flt_ok,cols].copy(deep=True)
        
        df_inc['ENS'] = df_inc['ENS'] *1000 / (60*df_inc['Hours'])  # Conversión a ENS Minutal
        df_inc['Pnom'] = df_inc['Pnom'] *1000                   # Conversión de MW a kW
        df_inc.drop(columns=['Hours'],inplace=True)                 # Ya no va a hacer falta la columna de duración

        # Con este paso, se convierte la columna Solver Agent a un número del 1 al 3, representando la
        # prioridad de desempate, en caso de haber incidencias solapadas con igual nivel de prioridad IEC
        rn = {'GENERATOR':'WTG','BOP_CONTRACTOR':'BOP','GRID_OPERATOR':'GRID'}
        rj = self.__check_jerarquia_equipos(jerarquia_equipos=jerarquia_equipos,mensajes=mensajes)
        rf = {k:rj[v] for k,v in rn.items()}
        
        df_inc.loc[:,'SolverAgent'] = df_inc.loc[:,'SolverAgent'].replace(rf).astype('Int64')

        # DF minutal vacío, con espacio para todas las variables de las incidencias
        df = self.__rpt_iec61400_minutal
        
        #Inicia el ciclo para poblar el df vacío
        vars_a_asignar=['ID','Pnom','SolverAgent','Reason','Origin', 'Priority_IEC']
        for _ , incidencia in df_inc.iterrows():
            
            ini = incidencia['Start']
            fin = incidencia['End'] - dt.timedelta(minutes=1) #El minuto final no va incluido
            i = incidencia['ID']
            r = incidencia['Reason']        #Motivo de la incidencia
            o = incidencia['Origin']        #Origen (Interno / Externo : Int/Ext)
            p = incidencia['Nemo']          #Parque
            e = incidencia['Equipo']        #Equipo
            ens = incidencia['ENS']         #Energía No Suministrada

            # Compartimentación de los tiempos y energía perdidos
            col_tba1 = ('Lim' if r == 'LIMITATION' else 'Ind')
            col_tba2 = col_tba1 + o.title()
            col_ens1 = 'ENS_' + col_tba1
            col_ens2 = 'ENS_' + col_tba2
                
            #Asignación de valores
            df.loc[ini:fin,(p,e,'FullPerf')] = False
            df.loc[ini:fin,(p,e,col_tba1)] = True
            df.loc[ini:fin,(p,e,col_tba2)] = True
            
            # Esta forma de sumar energía, es resistente a solapamiento de incidencias para un mismo equipo
            # Realmente no debería suceder, pero si fuera el caso, que por lo menos no se pierda la ENS
            df.loc[ini:fin,(p,e,'ENS')] = df.loc[ini:fin,(p,e,'ENS')].add(ens,fill_value=0)
            df.loc[ini:fin,(p,e,col_ens1)] = df.loc[ini:fin,(p,e,col_ens1)].add(ens,fill_value=0)
            df.loc[ini:fin,(p,e,col_ens2)] = df.loc[ini:fin,(p,e,col_ens2)].add(ens,fill_value=0)
            
            for v in vars_a_asignar:
                df.loc[ini:fin,(p,e,v)] = incidencia[v]
        
        self.__rpt_iec61400_minutal = df.copy(deep=True)

    def __iec61400_calcular_pot_dis(self,mensajes=False):
        
        #Crea un df populado con las incidencias en DatosCROM.incidencias
        
        df = self.__rpt_iec61400_minutal
        
        #Calcular la variable "Potencia Disponible" (PotDis) para todos los elementos del parque
        # en base a la Potencia Nominal (Pnom) y el estado del elemento (Indisponible (Ind) : True/False) 
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            
            #Potencia Disponible de Generadores
            equipos = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=p)
            for e in equipos:
                pdis = (p,e,'PotDis') ; pnom = (p,e,'Pnom') ; ind = (p,e,'Ind')

                df.loc[:,pdis] = ((~df.loc[:,ind]) * df.loc[:,pnom]).astype('float64')
                
            #Potencia Disponible de Agrupamientos
            # ¿Qué pasa si no hay agrupamientos? Caso PEGARCIG
            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=p)
            for a in agrupamientos.keys():
                pdis = (p,a,'PotDis') ; pnom = (p,a,'Pnom') ; ind = (p,a,'Ind')
                pdisa = (p,a,'PotDis_Asociada') ; pdise = (p,agrupamientos[a],'PotDis')
                
                df.loc[:,pdis] = ((~df.loc[:,ind]) * df.loc[:,pnom]).astype('float64')
                df.loc[:,pdisa] = df.loc[:,pdise].sum(axis=1)

            #Potencia Disponible de la Planta
            pl = 'PLANT'
            pdis = (p,pl,'PotDis') ; pnom = (p,pl,'Pnom') ; ind = (p,pl,'Ind')
            pdisa = (p,pl,'PotDis_Asociada') ; pdise = (p,equipos,'PotDis')
            
            df.loc[:,pdis] = ((~df.loc[:,ind]) * df.loc[:,pnom]).astype('float64')
            df.loc[:,pdisa] = df.loc[:,pdise].sum(axis=1)
            
        self.__rpt_iec61400_minutal = df.copy(deep=True)

    def __iec61400_propagar_ens(self,mensajes=False):
        
        #Crea un df populado con las incidencias en DatosCROM.incidencias y le calcula la potencia disponible a cada elemento
        
        df = self.__rpt_iec61400_minutal
        
        vars_ens = [
            'ENS_Lim','ENS_LimExt','ENS_LimInt',
            'ENS_Ind','ENS_IndExt','ENS_IndInt',
        ]
        # A partir de acá se propone propagar la ENS desde los elementos 'más grandes' (PLANT) hacia los más pequeños (WTG)
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            
            #¿Qué pasa si no hay agrupamientos? Caso PEGARCIG
            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=p)
            for a in agrupamientos.keys():
                for v in vars_ens:
                    for e in agrupamientos[a]:
                        proporcion = df.loc[:,(p,e,'PotDis')].div(df.loc[:,(p,a,'PotDis_Asociada')],fill_value=0)
                        ens_rolldown = df.loc[:,(p,a,v)].mul(proporcion,fill_value=0)
                        df.loc[:,(p,e,v)] = df.loc[:,(p,e,v)].add(ens_rolldown,fill_value=0)

            pl = 'PLANT'
            equipos = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=p)
            for v in vars_ens:
                for e in equipos:
                    proporcion =  df.loc[:,(p,e,'PotDis')].div(df.loc[:,(p,pl,'PotDis_Asociada')],fill_value=0)
                    ens_rolldown = df.loc[:,(p,pl,v)].mul(proporcion,fill_value=0)
                    df.loc[:,(p,e,v)] = df.loc[:,(p,e,v)].add(ens_rolldown,fill_value=0)

            for e in equipos:
                #Esto se hace en un ciclo aparte porque no todos los parques tienen agrupamientos
                df.loc[:,(p,e,'ENS_Lim')] = df.loc[:,(p,e,'ENS_LimExt')].add(df.loc[:,(p,e,'ENS_LimInt')],fill_value=0)
                df.loc[:,(p,e,'ENS_Ind')] = df.loc[:,(p,e,'ENS_IndExt')].add(df.loc[:,(p,e,'ENS_IndInt')],fill_value=0)
                df.loc[:,(p,e,'ENS')] = df.loc[:,(p,e,'ENS_Lim')].add(df.loc[:,(p,e,'ENS_Ind')],fill_value=0)
        
        self.__rpt_iec61400_minutal = df.copy(deep=True)

    def __iec61400_propagar_tba(self,mensajes=False):
        '''Esta función puede tomar el df antes o después de haber sido populado, da igual.
        Por cuestiones de eficiencia, entiendo que sería mejor ejecutarlo luego de propagar la ENS'''
        
        #Crea un df populado de incidencias, con PotDis y ENS ya calculados/propagados
        
        df = self.__rpt_iec61400_minutal
        vars_a_copiar = [
            'ID',
            'SolverAgent','Reason','Origin','Priority_IEC',
            'LimExt','LimInt',
            'IndExt','IndInt',
        ]
        
        pl = 'PLANT'
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            # Para facilitar lectura, se preparan las variables que se utilizarán para seleccionar columnas en el multi índice
            # Formato: (parque, elemento, variable)
            # notar la diferencia entre pl, a, y e para las próximas asignaciones. pl = planta, a = agrupamiento y e = equipo
            plsa = (p,pl,'SolverAgent')     # Número identificando la prioridad del SolverAgent (3, 2 ó 1) para (WTG, BOP y/o GRID) según ordene el usuario 
            pliec = (p,pl,'Priority_IEC')   # Número identificando la prioridad del evento según la norma IEC61400
                                            
            # Asumimos que BOP = Agrupamiento, para todos los parques del CROM
            flt_hay_incidencia_pl = df.loc[:,pliec] > 0
            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=p)
            if agrupamientos != []:
                
                # Si hay agrupamientos, propagar primero PLANT -> CIRCUITO a
                for a in agrupamientos:
                    asa = (p,a,'SolverAgent') ; aiec = (p,a,'Priority_IEC')

                    flt_pl_pisa_a_iec = df.loc[:,pliec] > df.loc[:,aiec]
                    flt_pl_pisa_a_jer = df.loc[:,plsa] > df.loc[:,asa]
                    flt_iec_igual = df.loc[:,pliec] == df.loc[:,aiec]
                    
                    migra_pl_a = flt_hay_incidencia_pl & (flt_pl_pisa_a_iec | (flt_iec_igual & flt_pl_pisa_a_jer) )
                    
                    # Transferir registros marcardos desde la planta hacia el el agrupamiento
                    for v in vars_a_copiar:
                        df.loc[migra_pl_a,(p,a,v)] = df.loc[migra_pl_a,(p,pl,v)]

                    # Recalcular variables de disponibilidad
                    df.loc[migra_pl_a,(p,a,'Lim')] = df.loc[migra_pl_a,(p,a,'LimExt')] | df.loc[migra_pl_a,(p,a,'LimInt')]
                    df.loc[migra_pl_a,(p,a,'Ind')] = df.loc[migra_pl_a,(p,a,'IndExt')] | df.loc[migra_pl_a,(p,a,'LimInt')]
                    df.loc[migra_pl_a,(p,a,'FullPerf')] = ~(df.loc[migra_pl_a,(p,a,'Lim')] | df.loc[migra_pl_a,(p,a,'Ind')])
                    
                    #Una vez propagadas las incidencias sobre los circuitos, se procede a propagar CIRCUITO a -> WTG e
                    flt_hay_incidencia_a = df.loc[:,aiec] > 0
                    equipos = agrupamientos[a]
                    for e in equipos:
                        esa = (p,e,'SolverAgent') ; eiec = (p,e,'Priority_IEC')
                        
                        flt_a_pisa_e_iec = df.loc[:,aiec] > df.loc[:,eiec]
                        flt_a_pisa_e_jer = df.loc[:,asa] > df.loc[:,esa]
                        flt_iec_igual = df.loc[:,aiec] == df.loc[:,eiec]
                        
                        migra_a_wtg = flt_hay_incidencia_a & (flt_a_pisa_e_iec | (flt_iec_igual & flt_a_pisa_e_jer) )

                        # Transferir registros marcardos desde el agrupamiento hacia la WTG
                        for v in vars_a_copiar:
                            df.loc[migra_a_wtg,(p,e,v)] = df.loc[migra_a_wtg,(p,a,v)]
                            
                        df.loc[migra_a_wtg,(p,e,'Lim')] = df.loc[migra_a_wtg,(p,e,'LimExt')] | df.loc[migra_a_wtg,(p,e,'LimInt')]
                        df.loc[migra_a_wtg,(p,e,'Ind')] = df.loc[migra_a_wtg,(p,e,'IndExt')] | df.loc[migra_a_wtg,(p,e,'LimInt')]
                        df.loc[migra_a_wtg,(p,e,'FullPerf')] = ~(df.loc[migra_a_wtg,(p,e,'Lim')] | df.loc[migra_a_wtg,(p,e,'Ind')])
                        
                        pdis = (p,e,'PotDis') ; pnom = (p,e,'Pnom') ; ind = (p,e,'Ind')
                        df.loc[migra_a_wtg,pdis] = ((~df.loc[migra_a_wtg,ind]) * df.loc[migra_a_wtg,pnom]).astype('float64')
                        
                    # El elemento "CIRCUITO a" ya fue procesado, por lo tanto lo podemos descartar.
                    cols = df.loc[:,(p,a,slice(None))].columns
                    df.drop(columns=cols,inplace=True)
                # El elemento PLANT ya fue procesado, por lo tanto lo podemos descartar.
                cols = df.loc[:,(p,pl,slice(None))].columns
                df.drop(columns=cols,inplace=True)
            else:       
                # En caso de que no haya circuitos (que no haya "BOP"), 
                # se procede directamente a propagar las incidencias desde la planta (PLANT) hacia las WTG 
                equipos = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=p)
                for e in equipos:
                    esa = (p,e,'SolverAgent') ; eiec = (p,e,'Priority_IEC')
                    
                    flt_pl_pisa_e_iec = df.loc[:,pliec] > df.loc[:,eiec]
                    flt_pl_pisa_e_jer = df.loc[:,plsa] > df.loc[:,esa]
                    flt_iec_igual = df.loc[:,pliec] == df.loc[:,eiec]
                    
                    migra_pl_wtg = flt_hay_incidencia_pl & (flt_pl_pisa_e_iec | (flt_iec_igual & flt_pl_pisa_e_jer) )
                    
                    # Transferir registros marcardos desde la planta hacia la WTG
                    for v in vars_a_copiar:
                        df.loc[migra_pl_wtg,(p,e,v)] = df.loc[migra_pl_wtg,(p,pl,v)]
                    df.loc[migra_pl_wtg,(p,e,'Lim')] = df.loc[migra_pl_wtg,(p,e,'LimExt')] | df.loc[migra_pl_wtg,(p,e,'LimInt')]
                    df.loc[migra_pl_wtg,(p,e,'Ind')] = df.loc[migra_pl_wtg,(p,e,'IndExt')] | df.loc[migra_pl_wtg,(p,e,'LimInt')]
                    df.loc[migra_pl_wtg,(p,e,'FullPerf')] = ~(df.loc[migra_pl_wtg,(p,e,'Lim')] | df.loc[migra_pl_wtg,(p,e,'Ind')])
                    
                    pdis = (p,e,'PotDis') ; pnom = (p,e,'Pnom') ; ind = (p,e,'Ind')
                    df.loc[migra_pl_wtg,pdis] = ((~df.loc[migra_pl_wtg,ind]) * df.loc[migra_pl_wtg,pnom]).astype('float64')
                    
                # El elemento PLANT ya fue procesado, por lo tanto lo podemos descartar.
                cols = df.loc[:,(p,pl,slice(None))].columns
                df.drop(columns=cols,inplace=True)
                
        self.__rpt_iec61400_minutal = df.copy(deep=True)

    def __iec61400_colapsar_nuevamente_a_incidencias(self,mensajes=False):
        
        df = self.__rpt_iec61400_minutal
        
        get_pot_pe = lambda p,e: self.consultar_equipos_parque(nemo_parque=p,potencia=True)[e]*1000

        lista_dfs = []
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            equipos = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=p)
            for e in equipos:

                # Identificar principios y fines de las incidencias serializadas
                    # De una serie de elementos, 
                    #   el primero es distinto al elemento anterior, y es igual al siguiente
                    #   el último es igual al anterior y distinto al siguiente
                    #   Son distintos de 0
                    #   No son Null
                # Los elementos únicos (un solo registro)
                    #   es distinto del elemento anterior
                    #   es distinto del elemento siguiente
                    #   es distinto de 0
                    #   No es Null
                v = 'ID'
                distinto_cero = df.loc[:,(p,e,v)] != 0
                distinto_nan = ~df.loc[:,(p,e,v)].isna()
                es_valido = distinto_cero & distinto_nan

                distinto_anterior = (df.loc[:,(p,e,v)] != df.loc[:,(p,e,v)].shift(1)).fillna(True)
                distinto_siguiente = (df.loc[:,(p,e,v)] != df.loc[:,(p,e,v)].shift(-1)).fillna(True)
                igual_anterior = (df.loc[:,(p,e,v)] == df.loc[:,(p,e,v)].shift(1)).fillna(True)
                igual_siguiente = (df.loc[:,(p,e,v)] == df.loc[:,(p,e,v)].shift(-1)).fillna(True)

                serie_pri = distinto_anterior & igual_siguiente & es_valido
                serie_ult = igual_anterior & distinto_siguiente & es_valido
                unicos = distinto_anterior & distinto_siguiente & es_valido

                #Creamos dos series, una para detectar las fechas de inicio de las nuevas incidencias y otra para las fechas de fin de dichas incidencias
                flt_fechas_ini = serie_pri | unicos
                flt_fechas_fin = serie_ult | unicos

                # Obtener fechas exactas de inicios y fines de incidencia
                fechas_ini = df.index[flt_fechas_ini].values
                fechas_fin = df.index[flt_fechas_fin].values

                # A partir de las fechas obtenidas, rellenar el resto de los valores de las incidencias
                n = len(fechas_ini)
                if n > 0:
                    pnom = get_pot_pe(p,e)
                    ids = df.loc[fechas_ini,(p,e,v)].values
                    origenes = df.loc[fechas_ini,(p,e,'Origin')].values
                    razones = df.loc[fechas_ini,(p,e,'Reason')].values
        
                    data = {
                        'Nemo':np.full(n,dtype=object,fill_value=p),
                        'Equipo':np.full(n,dtype=object,fill_value=e),
                        'ID':ids,
                        'Start':fechas_ini,
                        'End':fechas_fin,
                        'Hours':np.zeros(n),
                        'ENS':np.zeros(n),
                        'Reason':razones,
                        'Origin':origenes,
                        'Pnom':np.full(n,fill_value=pnom)
                    }

                    #Crear un dataframe temporal con los resultados
                    df_tmp = pd.DataFrame(data)
                    df_tmp['Hours'] = (df_tmp['End'] - df_tmp['Start']).dt.total_seconds()/3600
                    lista_dfs.append(df_tmp.copy(deep=True))
            
        df_short = pd.concat(lista_dfs,axis=0,ignore_index=True)
        for i,row in df_short.iterrows():
            p = row['Nemo']
            e = row['Equipo']
            v = 'ENS'
            fi = row['Start']
            ff = row['End']
            df_short.loc[i,'ENS'] = df.loc[fi:ff,(p,e,v)].sum()/1000
        
        self.__rpt_iec61400_minutal = df
        self.__rpt_iec61400_incidencias = df_short.copy(deep=True)

    def __iec61400_ajustes_finales(self,mensajes=False,guardar_minutal=False):
        
        df_long = self.__rpt_iec61400_minutal
        df_short = self.__rpt_iec61400_incidencias
        
        vars_a_recuperar = [
            'ID',
            'Status', 'UC',  'Owner', 'SolvedBy',
            'ID_PT11', 'Code',
            'BLC_Description', 'BLC_Comments',
            'Owner_Description', 'Owner_AffectedEquipment', 'Owner_ActionsTaken',
            'Owner_Results', 'Owner_NextSteps', 'Owner_Comments', 
            'IEC_lvl1','IEC_lvl2', 'IEC_lvl3', 'IEC_lvl4', 'IEC_Label','Priority_IEC'
        ]

        cols_ordenadas = [
        'Owner', 'Nemo', 'UC', 'Equipo', 'Equipo_Orig', 
        'ID', 'Start', 'End', 'Hours', 'ENS', 'Pnom', 'Reason', 'Origin', 'SolvedBy', 'Status', 'Code','ID_PT11',
        'IEC_lvl1', 'IEC_lvl2', 'IEC_lvl3','IEC_lvl4', 'IEC_Label', 'Priority_IEC',
        'BLC_Description', 'BLC_Comments', 'Owner_Description',
        'Owner_AffectedEquipment', 'Owner_ActionsTaken', 'Owner_Results','Owner_NextSteps', 'Owner_Comments', 
        
        ]

        #Recuperar variables que no dependen del equipo o del tipo de equipo
        df_short = pd.merge(left=df_short,right=self.incidencias.loc[:,vars_a_recuperar],on='ID',how='left')
        
        #Recuperar el equipo original del cual proviene la incidencia
        get_equipo_original = lambda id: self.incidencias.query(f'ID == {id}').loc[:,'Equipo'].values[0]
        df_short.loc[:,'Equipo_Orig'] = df_short['ID'].map(get_equipo_original)
        
        # Colocar nuevamente la variable de potencia nominal por fila
        df_short.loc[:,'Pnom'] = 0
        get_pot_equipo = lambda p,e: self.consultar_equipos_parque(nemo_parque=p,potencia=True)[e]
        for i , row in df_short.iterrows():
            p = row['Nemo']
            e  = row['Equipo']
            df_short.loc[i,'Pnom'] = get_pot_equipo(p,e)
        
        #Reordenar dataframe
        df_short = df_short.loc[:,cols_ordenadas]

        if guardar_minutal:
            self.__rpt_iec61400_minutal = df_long.copy(deep=True)  
        else:
            self.__rpt_iec61400_minutal = None

        gc.collect()
        self.__rpt_iec61400_incidencias = df_short.copy(deep=True)

    def incidencias_interpretar_bajo_iec61400(self,jerarquia_equipos='WTG',mensajes=False,guardar_minutal=False): 
        if self.incidencias is None: 
            self.consultar_incidencias(mensajes=True)
        
        # Crea DF vacío sobre el cual se colocarán los datos de las incidencias,
        # Pero equipo por equipo (columnas), en paralelo, sobre un mismo eje de tiempo (filas)
        self.__iec61400_preparar_df_vacio_minutal(mensajes=mensajes)
        
        #Popular el df vacío minutal, con datos de las incidencias
        self.__iec61400_explotar_minutalmente_incidencias(jerarquia_equipos=jerarquia_equipos,mensajes=mensajes)
        
        #Agregar el dato de potencia disponible minutal por equipo, basado en el tipo de incidencia
        self.__iec61400_calcular_pot_dis(mensajes=mensajes)
        
        # Propagar las proporciones de ENS correspondientes, desde arriba ('PLANT') hacia abajo ('WTG's)
        # pasando por los circuitos en caso de haberlos.
        self.__iec61400_propagar_ens(mensajes=mensajes)
        
        # Priorización de motivo de incidencias, bajo norma IEC61400, 
        # sólo se tocan las columnas booleanas de disponibilidad//limitación
        # y se trasladan los motivos de incidencias desde arriba ('plant' / 'circuito x') hacia abajo ('wtg's)
        # IMPORTANTE: Aquí se eliminan todas las columnas PLANT y CIRCUITO a, ya que dejan de ser útiles
        self.__iec61400_propagar_tba(mensajes=mensajes)
        
        #Convertir el DataFrame minutal resultante, a un Dataframe con registros que tenga fecha desde-hasta (tipo incidencias)
        self.__iec61400_colapsar_nuevamente_a_incidencias(mensajes=mensajes)
        
        # Incorpora las variables faltantes de las incidencias originales, a partir de las cuales se trabajó
        # ejemplo: Equipo original del cual proviene la incidencia, ordenar columnas, reconvertir unidades, etc.
        self.__iec61400_ajustes_finales(guardar_minutal=guardar_minutal,mensajes=mensajes)

    def incidencias_identificar_solapamientos(self,df):
        ''' Esta función toma un dataframe de incidencias formateado por el objeto blctools.DatosCROM() o blctools.TablasVC()
        y lo analiza iterativamente, en búsqueda de incidencias que se solapen para un mismo equipo y período en el tiempo.'''
        
        # #Recorrer todas las incidencias y buscar incidencias solapadas
        conflictos = []
        for _, incidencia in df.iterrows():
            
            id = incidencia['ID']
            fi = incidencia['Start']
            ff = incidencia['End']
            e = incidencia['Equipo']
            p = incidencia['Nemo']
            
            flt_id = df.ID != id
            flt_e = df.Equipo == e
            flt_p = df.Nemo == p
            flt_fi = df.Start < ff
            flt_ff = df.End > fi
            
            if 'Status' in incidencia.index:
                s = incidencia['Status']
                flt_s = df.Status != 'DESCARTADA'
                #Un filtro que cumple con todas las condiciones en simultáneo, incluyendo Status
                flt = flt_id & flt_p & flt_e & flt_fi & flt_fi & flt_ff & flt_s
            else:
                #Un filtro que cumple con todas las condiciones en simultáneo
                flt = flt_id & flt_p & flt_e & flt_fi & flt_fi & flt_ff
            
            if not df[flt].empty:
                valores = df.loc[flt,'ID'].to_list()
                conflictos.append({id:valores})

        # Convertir conflictos a DataFrame largo
        conflictos = pd.DataFrame(conflictos)\
                        .melt(var_name='ID',value_name='IDs_solapados')\
                        .dropna()\
                        .reset_index(drop=True)
        
        # Crear una lista de sets (no tiene elementos repetidos) de la incidencia analizada vs sus solapamientos
        valores = []
        for i, r in conflictos.iterrows():
            b = set(r['IDs_solapados'])
            a = set((r['ID'],))
            
            valores.append(a.union(b))
            
        #Convertir dicha lista en una serie de pandas
        conflictos['IDs_con_solapamiento'] = pd.Series(valores)

        # Eliminar elementos duplicados (a,b) == (b,a)
        duped = ~ conflictos['IDs_con_solapamiento'].duplicated()
        serie_limpia = conflictos[duped]\
                        .loc[:,['IDs_con_solapamiento']]\
                        .reset_index(drop=True)
        
        return serie_limpia

    #
    # Conjunto de funciones destinadas a explotar las incidencias.
    # Se puede seleccionar entre incidencias crudas, o IEC61400.
    #
    def __check_granularidad(self,granularidad,intervalos):
        
        if isinstance(granularidad,str):
            granularidad = granularidad.lower()
            if granularidad not in intervalos.keys():
                raise ValueError(f'La granularidad indicada no es un objeto datetime.timedelta ni está entre {list(intervalos.keys())}')
            else:
                return intervalos[granularidad]

        elif not isinstance(granularidad,dt.timedelta):
            raise TypeError('El parámetro "granularidad" debe ser del tipo string o datetime.timedelta.')
        else:
            return granularidad

    def __explotar_incidencia(self,incidencia,col_start='Start',col_end='End',granularidad='1dia'):

        intervalos = {
            '10seg':dt.timedelta(seconds=10),
            '1min':dt.timedelta(minutes=1),
            '5min':dt.timedelta(minutes=5),
            '10min':dt.timedelta(minutes=10),
            '15min':dt.timedelta(minutes=15),
            '1hora':dt.timedelta(hours=1),
            '1dia':dt.timedelta(days=1)
            }
        
        intervalo = self.__check_granularidad(granularidad,intervalos)

        fecha_ini_real = incidencia[col_start]
        fecha_fin_real = incidencia[col_end]
        fecha_ini_iter = fecha_ini_real.replace(hour=0,minute=0,second=0,microsecond=0)
        fecha_fin_iter = fecha_fin_real.replace(hour=23,minute=59,second=59,microsecond=0)

        iterable = fechas.iterar_entre_timestamps(fecha_ini_iter,fecha_fin_iter,intervalo)

        data = {
            col_start:[],
            col_end:[],
            'Activa':[],
        }

        for fecha_i, fecha_f in iterable:
            activa = (fecha_ini_real < fecha_f) and (fecha_fin_real >= fecha_i)
            
            data[col_start].append(fecha_i)
            data[col_end].append(fecha_f)
            data['Activa'].append(activa)

        if len(data['Activa']) == 1:
            data = incidencia.to_dict()
            return pd.DataFrame(data,index=[0])

        #Continuamos con incidencias de duración mayor a un registro
        df = pd.DataFrame(data)
        df = df[df['Activa']].copy(deep=True).reset_index(drop=True)
        try:
            df.iloc[0,0] = fecha_ini_real   #Columna 'Start', primera fila
            df.iloc[-1,1] = fecha_fin_real  #Columna 'End', última fila
            
            #Colocando el tiempo y la energía perdidos
            df['Hours'] = (df[col_end] - df[col_start]).dt.total_seconds()/3600
            df['ENS'] = incidencia['ENS'] * (df['Hours'] / incidencia['Hours'])
            
            #eliminar columna auxiliar
            df.drop(columns='Activa',inplace=True)
            
            for col in incidencia.index:
                if col not in df.columns:
                    df[col] = incidencia[col]
            
            return df.loc[:,incidencia.index]
            
        except:
            print(f'Error al procesar la incidencia {incidencia["ID"]}')
                    
    def explotar_incidencias(
        self,
        df=None,
        iec61400=False,
        col_start='Start',
        col_end='End',
        cols_seleccion=None,
        granularidad='1dia'
        ):
        
        if df is None:
            if iec61400:
                if self.__rpt_iec61400_incidencias is None:
                    self.incidencias_interpretar_bajo_iec61400()
                df = self.__rpt_iec61400_incidencias
            else:
                df = self.incidencias
        
        if cols_seleccion is None:
            cols_seleccion = df.columns.to_list()
                 
        iterador = df.loc[:,cols_seleccion].iterrows()
        f = lambda x: self.__explotar_incidencia(x,col_start=col_start,col_end=col_end,granularidad=granularidad)
        
        lista_dfs = [f(incidencia) for _ , incidencia in iterador]
        
        self.__incidencias_explotadas = pd.concat(lista_dfs,ignore_index=True)

    #
    # Conjunto de funciones destinadas a consolidar en los datos 10segundales
    # junto con el resultado de procesar las incidencias bajo IEC61400
    #
    def __rpt_consolidado_preparar_df_10s(self,mensajes=False):
        # Preparar las columnas necesarias para poder descargar la info de las incidencias IEC61400, al DF de mediciones 10 segundales.
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        
        n = len(self.datos_seg.index)
        
        trues = np.full(n,fill_value=True)
        falses = np.full(n,fill_value=False)
        zeros = np.zeros(n)
        
        for p in parques_con_datos:
            equipos_todos = self.consultar_equipos_parque(nemo_parque=p)
            for e in equipos_todos:
                if mensajes: print(f"Preparando {p} {e} para descargar datos de incidencias")
                self.datos_seg.loc[:,(p,e,'FullPerf')] = pd.Series(trues,name=(p,e,'FullPerf'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'Ind')] = pd.Series(falses,name=(p,e,'Ind'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'Lim')] = pd.Series(falses,name=(p,e,'Lim'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'ENS')] = pd.Series(zeros,name=(p,e,'ENS'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'ENS_U')] = pd.Series(zeros,name=(p,e,'ENS_U'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'PBA')] = pd.Series(zeros,name=(p,e,'PBA'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'TBA')] = pd.Series(zeros,name=(p,e,'TBA'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'Pteo')] = pd.Series(zeros,name=(p,e,'Pteo'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'Pteo_U')] = pd.Series(zeros,name=(p,e,'Pteo_U'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'Eteo')] = pd.Series(zeros,name=(p,e,'Eteo'),index=self.datos_seg.index)
                self.datos_seg.loc[:,(p,e,'Eteo_U')] = pd.Series(zeros,name=(p,e,'Eteo_U'),index=self.datos_seg.index)
                
        self.datos_seg = self.datos_seg.copy(deep=True)

    def __rpt_consolidado_descargar_incidencias(self,mensajes=False):
        
        # Va leyendo las incidencias que correspondan, y las descargue en el df 10 segundal consolidado
        for _ , incidencia in self.incidencias_iec61400.iterrows():
            
            fi = incidencia['Start']
            ff = incidencia['End']
            p = incidencia['Nemo']
            e = incidencia['Equipo']
            id = incidencia['ID']
            ens = incidencia['ENS'] *1000       # Conversión de MWh a kWh
            h = incidencia['Hours']
            pnom = incidencia['Pnom']
            
            if h:
                ens_10 = (ens/h) * (10/3600)    #Convertir de valor unitario horario, a diezsegundal
                ens_u = ens_10 / pnom           #Convertir a un valor unitario, sirve para reponer datos en caso de faltantes
            else:
                ens_10 = 0
                ens_u = 0
            
            if mensajes: print(f"Procesando incidencia {p} {e} {id}")
            
            es_lim = incidencia['Reason'] == 'LIMITATION'
            es_ind = not es_lim
            
            self.datos_seg.loc[fi:ff,(p,e,'FullPerf')] = False
            self.datos_seg.loc[fi:ff,(p,e,'Ind')] = es_ind
            self.datos_seg.loc[fi:ff,(p,e,'Lim')] = es_lim
            self.datos_seg.loc[fi:ff,(p,e,'ENS')] = ens_10
            self.datos_seg.loc[fi:ff,(p,e,'ENS_U')] = ens_u

    def __rpt_consolidado_roll_up(self,mensajes=False):
        
        # Hacer un roll up de los estados lógicos FullPerf, Ind y Lim, desde las WTG hacia el parque y los circuitos
        
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        for p in parques_con_datos:
            
            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=p)
            for a,equipos in agrupamientos.items():
                if mensajes: print(f"Haciendo Roll-up de FullPerf/Ind/Lim de {p} {a}")
                self.datos_seg.loc[:,(p,a,'Ind')] = self.datos_seg.loc[:,(p,equipos,'Ind')].any(axis=1)
                self.datos_seg.loc[:,(p,a,'Lim')] = self.datos_seg.loc[:,(p,equipos,'Lim')].any(axis=1)
                self.datos_seg.loc[:,(p,a,'FullPerf')] = ~(self.datos_seg.loc[:,(p,a,'Ind')] | self.datos_seg.loc[:,(p,a,'Lim')])
                self.datos_seg.loc[:,(p,a,'ENS')] = self.datos_seg.loc[:,(p,equipos,'ENS')].sum(axis=1)
                self.datos_seg.loc[:,(p,a,'ENS_U')] = self.datos_seg.loc[:,(p,equipos,'ENS_U')].sum(axis=1)

            a = 'PLANT'
            equipos = list(agrupamientos.keys())
            if mensajes: print(f"Haciendo Roll-up de FullPerf/Ind/Lim de {p} {a}")
            self.datos_seg.loc[:,(p,a,'Ind')] = self.datos_seg.loc[:,(p,equipos,'Ind')].any(axis=1)
            self.datos_seg.loc[:,(p,a,'Lim')] = self.datos_seg.loc[:,(p,equipos,'Lim')].any(axis=1)
            self.datos_seg.loc[:,(p,a,'FullPerf')] = ~(self.datos_seg.loc[:,(p,a,'Ind')] | self.datos_seg.loc[:,(p,a,'Lim')])
            self.datos_seg.loc[:,(p,a,'ENS')] = self.datos_seg.loc[:,(p,equipos,'ENS')].sum(axis=1)
            self.datos_seg.loc[:,(p,a,'ENS_U')] = self.datos_seg.loc[:,(p,equipos,'ENS_U')].sum(axis=1)
            
            # Calcular variables dependientes de las variables recientemente calculadas, para todos los equipos del parque
            equipos_todos = self.consultar_equipos_parque(nemo_parque=p)
            for e in equipos_todos:
                if mensajes: print(f"Haciendo Roll-Up de TBA/PBA/Pteo {p} {e}")
                self.datos_seg.loc[:,(p,e,'TBA')] = 1 - self.datos_seg.loc[:,(p,e,'Ind')]
                self.datos_seg.loc[:,(p,e,'Eteo')] = self.datos_seg.loc[:,(p,e,'Egen')] + self.datos_seg.loc[:,(p,e,'ENS')]
                self.datos_seg.loc[:,(p,e,'Pteo')] = self.datos_seg.loc[:,(p,e,'Eteo')] / (10/3600)
                self.datos_seg.loc[:,(p,e,'Eteo_U')] = self.datos_seg.loc[:,(p,e,'Eteo')].div(self.datos_seg.loc[:,(p,e,'Pnom')])
                self.datos_seg.loc[:,(p,e,'Pteo_U')] = self.datos_seg.loc[:,(p,e,'Pteo')].div(self.datos_seg.loc[:,(p,e,'Pnom')])
                
                flt = self.datos_seg.loc[:,(p,e,'Pteo')] == 0

                self.datos_seg.loc[ flt,(p,e,'PBA')] = 1
                self.datos_seg.loc[~flt,(p,e,'PBA')] = self.datos_seg.loc[:,(p,e,'P')].div(self.datos_seg.loc[:,(p,e,'Pteo')])
    
    def __rpt_consolidado_ajustes_finales(self,mensajes=False):
        
        #Forzar un reordenamiento de todas las columnas
        columnas_ordenadas = []
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        for p in parques_con_datos:

            cols = self.datos_seg.loc[:,(p,'PLANT',slice(None))].columns.to_list()
            columnas_ordenadas += cols
            agrupamientos = self.consultar_agrupamientos_parque(nemo_parque=p)
            for a in agrupamientos:
                cols = self.datos_seg.loc[:,(p,a,slice(None))].columns.to_list()
                columnas_ordenadas += cols
            
            equipos = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=p)
            for e in equipos:
                cols = self.datos_seg.loc[:,(p,e,slice(None))].columns.to_list()
                columnas_ordenadas += cols
            
        self.datos_seg = self.datos_seg.loc[:,columnas_ordenadas].copy(deep=True)
    
    def consolidar_todo(self,mensajes=False):
        if self.__rpt_iec61400_incidencias is None:
            self.incidencias_interpretar_bajo_iec61400()
        
        self.__rpt_consolidado_preparar_df_10s(mensajes=mensajes)       #Crear columnas vacías con datatype booleano, para luego manipular sus datos
                                                                        # Dichas columnas son: FullPerf, Ind y Lim
        self.__rpt_consolidado_descargar_incidencias(mensajes=mensajes) #Descargar datos de las incidencias IEC61400 sobre las columnas booleanas
        self.__rpt_consolidado_roll_up(mensajes=mensajes)               #Afectar los circuitos y la planta toda, con operaciones lógicas
        self.__rpt_consolidado_ajustes_finales(mensajes=mensajes)       #Ajustes finales, ordenar columnas, básicamente
        self.__rpt_consolidado_status = True                            #Indicar que ya se consolidó la información

    def __reporte_consolidado(self,granularidad):
        
        #Obtener listado total de equipos
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        get_equipos= lambda p: self.consultar_equipos_parque_no_agrupamientos(nemo_parque=p)
        equipos = {e for p in parques_con_datos for e in get_equipos(p)}      
        equipos = list(equipos)                  

        # equipos contiene todos los aerogeneradores, que no sean 'PLANT' ni 'CUIRCUITO a'. Sólo generadores
        t = slice(None)     # slice(None) se usa en los MultiIndex para seleccionar "Todo" por eso la t.
        vars_prom = ['TBA','Lim']                   #Variables que hay que hacer promedios al consolidarlas
        vars_suma = ['Egen','Eteo','Epos','ENS']    #Variables que hay que sumarlas al consolidarlas    
    
        #Aquí haremos uso de la función "resample"
        df_suma = self.datos_seg\
                    .loc[:,(t,equipos,t)]\
                    .loc[:,(t,t,vars_suma)]\
                    .resample(granularidad)\
                    .sum()\
                    .div(1000)\
                    .melt(ignore_index=False)\
                    .reset_index(drop=False)\
                    .rename(columns={'t_stamp':'Fecha'})\
                    .pivot(index=['Parque','Fecha','Equipo'],columns='Variable')
                    
        df_prom = self.datos_seg\
                    .loc[:,(t,equipos,t)]\
                    .loc[:,(t,t,vars_prom)]\
                    .resample(granularidad)\
                    .mean()\
                    .melt(ignore_index=False)\
                    .reset_index(drop=False)\
                    .rename(columns={'t_stamp':'Fecha'})\
                    .pivot(index=['Parque','Fecha','Equipo'],columns='Variable')
                        
        df_merged = pd.merge(left=df_prom,right=df_suma,left_index=True,right_index=True)
        df_merged.columns = df_merged.columns.droplevel(0)
        df_merged = df_merged.rename_axis(None,axis='columns')

        df_merged['PBA'] = df_merged['Egen'] / df_merged['Epos']
        df_merged['PI'] = df_merged['Egen'] / df_merged['Eteo']

        cols_ordenadas = ['TBA','Lim','PBA','PI','Egen','Epos','Eteo','ENS']
        return  df_merged\
                        .loc[:,cols_ordenadas]\
                        .dropna(axis=0,how='all')\
                        .reset_index(drop=False)\
                        .copy(deep=True)

    def reporte_consolidado(self,granularidad='1D',mensajes=False,exportar=False,ruta=None,nombre=None):
        
        if not self.__rpt_consolidado_status:
            self.consolidar_todo(mensajes=mensajes)
        
        get_rpt = lambda g: self.__reporte_consolidado(granularidad=g)
        
        if isinstance(granularidad,str):
            self.__rpt_consolidado = get_rpt(granularidad)
        elif isinstance(granularidad,(list,tuple)):
            self.__rpt_consolidado = {g:get_rpt(g) for g in granularidad}
        
        #Exportar reporte consolidado
        if exportar:
            #Configurar nombre del archivo
            if not nombre:
                fecha_str = dt.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
                fecha_i_str = self.fecha_i.strftime("%Y-%m-%d")
                fecha_f_str = self.fecha_f.strftime("%Y-%m-%d")
                fechas = f'{fecha_i_str} a {fecha_f_str} {fecha_str}'
                
                encabezado = 'Reporte Consolidado IEC61400'
                
                if len(self.parques) > 1:
                    nombre_rpt = f'{encabezado} {fechas}.xlsx'
                else:
                    nombre_rpt = f'{encabezado} {fechas} {self.parques[0]}.xlsx'
            
            #Configurar ruta de salida
            if not ruta:
                ruta = self.dir_salida
            else:
                ruta = dirs.check_dir(ruta)
            
            archivo = Path(ruta + '\\' + nombre_rpt)
            
            #Rutina de exportación
            if isinstance(self.__rpt_consolidado,pd.DataFrame):
                self.rpt_consolidado.to_excel(archivo,index=False)
            else:
                with pd.ExcelWriter(archivo) as writer:
                    for granularidad,df in self.rpt_consolidado.items():
                        df.to_excel(writer,sheet_name=granularidad,index=False)

    #
    # Conjunto de funciones destinadas a crear las curvas de potencia
    # a partir de los reportes consolidados entre 
    # datos 10segundales e incidencias IEC61400
    #
    def __curvas_de_potencia(self,
                              variables_medicion=['Pgen',],
                              variable_categorica='Wind_bin',
                              variable_filtro='FullPerf',
                              aggfunc=np.mean
                              ):
        
        # Cambio de nombre de variables para reducir el código
        vf = variable_filtro
        vm = variables_medicion
        vc = variable_categorica
        f = aggfunc
        
        # Esta función toma tres parámetros, p, e y v
        # p = parque, e = equipo y vf = variable para filtrar (serie booleana de pandas) todas del tipo string
        fp = lambda p,e,vf : self.datos_seg.loc[:,(p,e,vf)]

        # Esta función toma los siguientes parámetros
        # p = parque, e= equipo, vf = variable para filtrar (serie booleana de pandas). Datatype str
        # vc = variable categórica, para categorizar mediciones. Datatype str
        # vm = variable(s)  de medición. Datatype list, con objetos str adentro
        get_curva_vc = lambda p,e,vf,vc,vm,f: self.datos_seg\
                                            .loc[fp(p,e,vf),(p,e,vm+[vc])]\
                                            .melt(id_vars=[(p,e,vc)],value_vars=[(p,e,v) for v in vm],ignore_index=False)\
                                            .reset_index(drop=True)\
                                            .rename(columns={(p,e,vc):vc})\
                                            .pivot_table(columns=['Parque','Equipo','Variable'],index=vc,aggfunc=f)\
                                            .droplevel(level=0,axis='columns')

        get_equipos = lambda p: self.consultar_equipos_parque_no_agrupamientos(nemo_parque=p)       # Toma de parámetro el Nemo de un parque y devuelve un listado de generadores (no agrupamientos)
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))                         # Listado de Nemotécnicos presentes en el dataframe de mediciones consolidadas
        
        # Listado de dataframes, con las mediciones vm ya categorizadas según vc
        lista_dfs = [get_curva_vc(p,e,vf,vc,vm,f) for p in parques_con_datos for e in get_equipos(p)] 
        
        # Concatenar todos los dataframes de izquierda a derecha, basado en el nuevo índice categórico
        dfm = None
        for df in lista_dfs:
            if dfm is None:
                dfm = df.copy(deep=True)
            else:
                dfm = pd.merge(left=dfm,right=df,left_index=True,right_index=True,how='outer')
                
        # Reordenar niveles del DataFrame para que queden las variables agrupadas.   
        dfm = dfm.reorder_levels(axis='columns',order=['Parque','Variable','Equipo']).sort_index(axis='columns')
        return dfm.copy(deep=True)
    
    def reporte_curvas_de_potencia(self,
                               variables_medicion=['Pgen','Pteo','Wind',],
                               variables_categoricas=['Wind_bin','Wind_dir_r'],
                               variable_filtro='FullPerf',
                               aggfunc=np.mean,
                               ruta=None,
                               nombre=None,
                               exportar=False,
                               ):
        
        vm = variables_medicion         # Conjunto de variables de medición, las cuales se quiere categorizar
        vc = variables_categoricas      # Vcs = Variables categóricas. Por cada variable categórica, se creará un dataframe con todas las variables de medición
        vf = variable_filtro            # Variable (Serie booleana) por la cual se filtrarán los datos crudos, previo a categorizar
        f = aggfunc                     # Variable de agregación, sobre las varaibles de medicion (suma, promedio, etc.)
        
        dict_dfs = {v:self.__curvas_de_potencia(vm,v,vf,f) for v in vc}

        if len(dict_dfs) == 1:
            k = list(dict_dfs.keys())[0]
            self.__rpt_curvas_de_potencia = dict_dfs[k]
        elif len(dict_dfs) > 1:
            self.__rpt_curvas_de_potencia = dict_dfs
            
        #Exportar reporte consolidado
        if exportar:
            #Configurar nombre del archivo
            if not nombre:
                fecha_str = dt.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
                fecha_i_str = self.fecha_i.strftime("%Y-%m-%d")
                fecha_f_str = self.fecha_f.strftime("%Y-%m-%d")
                fechas = f'{fecha_i_str} a {fecha_f_str} {fecha_str}'
                
                encabezado = 'Curvas de Potencia'
                
                if len(self.parques) > 1:
                    nombre_rpt = f'{encabezado} {fechas}.xlsx'
                else:
                    nombre_rpt = f'{encabezado} {fechas} {self.parques[0]}.xlsx'
            
            #Configurar ruta de salida
            if not ruta:
                ruta = self.dir_salida
            else:
                ruta = dirs.check_dir(ruta)
            
            archivo = Path(ruta + '\\' + nombre_rpt)
            
            #Rutina de exportación
            if isinstance(self.__rpt_curvas_de_potencia,pd.DataFrame):
                self.rpt_consolidado.to_excel(archivo,index=False)
            else:
                with pd.ExcelWriter(archivo) as writer:
                    for variable_categorica,df in self.__rpt_curvas_de_potencia.items():
                        df.to_excel(writer,sheet_name=variable_categorica,index=False)
