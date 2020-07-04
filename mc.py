import lib as l

class Rocket:
    
    def __init__(self,name,file_path,engine_path):
        self.name = name
        self.file_path = file_path
        self.engine_path = engine_path

    def to_xml(self):
        l.unzip_rocket(self.file_path)
        return l.ET.parse(l.os.path.dirname(self.file_path) + '/rocket.ork')

    def to_ork(self,xml):
        xml.write(self.name,'utf-8')



class Simulation:
    def __init__(self,name,elev,windv,winddir,launchrod,turbulency):
        self.name = name
        self.elevation = elev
        self.wind_velocity = windv
        self.wind_direction = winddir
        self.location = ""
        self.launch_rod = launchrod
        self.turbulency = turbulency
        self.simu_path = ""

    def add_simulation(self,rocket):
        self.rocket = rocket
        rocket_run = rocket.to_xml()
        root_before = rocket_run.getroot()
        simulations = root_before.find('simulations')

        #Atributo da simulação
        simulation = l.ET.SubElement(simulations, 'simulation')
        simulation.attrib['status'] = 'cantrun'

        #Nome da simulação
        name = l.ET.SubElement(simulation,'name')
        #name.text = '{}° de elevação, sob ventos de {} m/s {}°'.format(elev, wind,winddir*180/math.pi)
        name.text = self.name

        #Método de resolução
        simulator = l.ET.SubElement(simulation,'simulator')
        simulator.text = 'RK4Simulator'

        #Método de cálculo
        calculator = l.ET.SubElement(simulation,'calculator')
        calculator.text = 'BarrowmanCalculator'

        #cria o ramo de simulações
        conditions = l.ET.SubElement(simulation, 'conditions')

        #Motor CRT
        configid = l.ET.SubElement(conditions,'configid')
        configid.text = '193878ee-d8af-46eb-9af4-e67f7149b232'

        #Tamanho do Trilho de Lançamento
        launchrodlength = l.ET.SubElement(conditions,'launchrodlength')
        launchrodlength.text = self.launch_rod

        #Ângulo de lançamento
        launchrodangle = l.ET.SubElement(conditions,'launchrodangle')
        launchrodangle.text = str(elevation)

        #Direção do lançamento
        launchroddirection = l.ET.SubElement(conditions,'launchroddirection')
        #launchroddirection.text = str(launchangles[3][1])
        launchroddirection.text = str(0)

        #Vento Médio
        windaverage = l.ET.SubElement(conditions,'windaverage')
        windaverage.text = str(wind_velocity)

        #Turbulência do Vento
        windturbulence = l.ET.SubElement(conditions,'windturbulence')
        windturbulence.text = str(turbulency)

        #Direção do Vento
        launchwinddirection = l.ET.SubElement(conditions,'winddirection')
        launchwinddirection.text = str(wind_direction)

        #Altitude do lugar de lançamento
        launchaltitude = l.ET.SubElement(conditions,'launchaltitude')
        launchaltitude.text = str(916.0)

        #Latitude do lugar de lançamento
        launchlatitude = l.ET.SubElement(conditions,'launchlatitude')
        launchlatitude.text = str(-15.6)

        #Longitude do lugar de lançamento
        launchlongitude = l.ET.SubElement(conditions,'launchlongitude')
        launchlongitude.text = str(-47.3)

        #Condições ambientais padrão
        geodeticmethod = l.ET.SubElement(conditions,'geodeticmethod')
        geodeticmethod.text = 'spherical'

        atmosphere = l.ET.SubElement(conditions,'atmosphere')
        atmosphere.attrib['model'] = 'isa'

        timestep = l.ET.SubElement(conditions,'timestep')
        timestep.text = '0.05'

        flightdata = l.ET.SubElement(simulation,'flightdata')
        flightdata.attrib['maxaltitude'] = '1000' #Valor arbitrário

        rocket.to_ork(rocket_run)

    def add_all_simulations(self,rocket):
        self.rocket = rocket
        rocket_run = rocket.to_xml()
        root_before = rocket_run.getroot()
        simulations = root_before.find('simulations')

        for elev in self.elevation:
            for wind in self.wind_velocity:
                for winddir in self.wind_direction:
                        
                    #Atributo da simulação
                    simulation = l.ET.SubElement(simulations, 'simulation')
                    simulation.attrib['status'] = 'cantrun'

                    #Nome da simulação
                    name = l.ET.SubElement(simulation,'name')
                    #name.text = '{}° de elevação, sob ventos de {} m/s {}°'.format(elev, wind,winddir*180/math.pi)
                    name.text = self.name

                    #Método de resolução
                    simulator = l.ET.SubElement(simulation,'simulator')
                    simulator.text = 'RK4Simulator'

                    #Método de cálculo
                    calculator = l.ET.SubElement(simulation,'calculator')
                    calculator.text = 'BarrowmanCalculator'

                    #cria o ramo de simulações
                    conditions = l.ET.SubElement(simulation, 'conditions')

                    #Motor CRT
                    configid = l.ET.SubElement(conditions,'configid')
                    configid.text = '193878ee-d8af-46eb-9af4-e67f7149b232'

                    #Tamanho do Trilho de Lançamento
                    launchrodlength = l.ET.SubElement(conditions,'launchrodlength')
                    launchrodlength.text = self.launch_rod

                    #Ângulo de lançamento
                    launchrodangle = l.ET.SubElement(conditions,'launchrodangle')
                    launchrodangle.text = str(elev)

                    #Direção do lançamento
                    launchroddirection = l.ET.SubElement(conditions,'launchroddirection')
                    #launchroddirection.text = str(launchangles[3][1])
                    launchroddirection.text = str(0)

                    #Vento Médio
                    windaverage = l.ET.SubElement(conditions,'windaverage')
                    windaverage.text = str(wind)

                    #Turbulência do Vento
                    windturbulence = l.ET.SubElement(conditions,'windturbulence')
                    windturbulence.text = str(0.10)

                    #Direção do Vento
                    launchwinddirection = l.ET.SubElement(conditions,'winddirection')
                    launchwinddirection.text = str(winddir)

                    #Altitude do lugar de lançamento
                    launchaltitude = l.ET.SubElement(conditions,'launchaltitude')
                    launchaltitude.text = str(916.0)

                    #Latitude do lugar de lançamento
                    launchlatitude = l.ET.SubElement(conditions,'launchlatitude')
                    launchlatitude.text = str(-15.6)

                    #Longitude do lugar de lançamento
                    launchlongitude = l.ET.SubElement(conditions,'launchlongitude')
                    launchlongitude.text = str(-47.3)

                    #Condições ambientais padrão
                    geodeticmethod = l.ET.SubElement(conditions,'geodeticmethod')
                    geodeticmethod.text = 'spherical'

                    atmosphere = l.ET.SubElement(conditions,'atmosphere')
                    atmosphere.attrib['model'] = 'isa'

                    timestep = l.ET.SubElement(conditions,'timestep')
                    timestep.text = '0.05'

                    flightdata = l.ET.SubElement(simulation,'flightdata')
                    flightdata.attrib['maxaltitude'] = '1000' #Valor arbitrário

        rocket.to_ork(rocket_run)

    def run(self,rocket):
        l.subprocess.call(["java", "-jar", "D:/Documentos/lib/UnB/4Semestre/Capital/OpenRocketTurbo3.jar", "--runSimulations", self.rocket.file_path])
        self.simu_path = rocket.file_path

    def results(self,path):
        #tree = ET.parse(path)
        tree = self.rocket.to_xml()
        root_after = tree.getroot()
        simulations_after = root_after.find('simulations')

        simus = []

        for simulation_after in simulations_after.findall('simulation'):
            sep = ','
            simu = []
            simu_title = simulation_after.find('name').text
            flightdata = simulation_after.find('flightdata')
            databranch = flightdata.find('databranch')

            for datapoints in databranch.findall('datapoint'):
                line = datapoints.text
                line = l.ListConversor(line,sep)
                simu.append(line)
                simu = l.pd.DataFrame(simu)
            
            simus.append(simu)

        return simus

    def plot(self,data, simulation_number = 0):
        fig = l.plt.figure(figsize=(9,9))
        ax = l.plt.axes(projection='3d')
        if simulation_number == 0:
            ax.plot(data[:][:][7],data[:][:][6],data[:][:][1])
        else:
            ax.plot(data[simulation_number][:][7],data[simulation_number][:][6],data[simulation_number][:][1])
        l.plt.show()