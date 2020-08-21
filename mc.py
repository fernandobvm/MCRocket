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
        xml.write(self.name+'.ork','utf-8')
        self.file_path = l.os.getcwd() +  '\\' + self.name + '.ork'



class Simulation:
    def __init__(self, name, elevation, wind_velocity, wind_direction, launchrod_direction, launch_rod, turbulency):
        self.name = name
        self.location = ""
        self.simu_path = ""
        self.elevation = elevation
        self.wind_velocity = wind_velocity
        self.launch_rod = launch_rod
        self.turbulency = turbulency
        self.wind_direction = wind_direction
        self.launchrod_direction = launchrod_direction

    def add_simulation(self,rocket):
        self.rocket = rocket
        try:
            rocket_run = rocket.to_xml()
        except:
            rocket_run = l.ET.parse(l.os.path.dirname(rocket.file_path) +'\\' + rocket.name + '.ork')
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
        launchrodlength.text = str(self.launch_rod)

        #Ângulo de lançamento
        launchrodangle = l.ET.SubElement(conditions,'launchrodangle')
        launchrodangle.text = str(self.elevation)

        #Direção do lançamento
        launchroddirection = l.ET.SubElement(conditions,'launchroddirection')
        #launchroddirection.text = str(launchangles[3][1])
        launchroddirection.text = str(self.launchrod_direction)

        #Vento Médio
        windaverage = l.ET.SubElement(conditions,'windaverage')
        windaverage.text = str(self.wind_velocity)

        #Turbulência do Vento
        windturbulence = l.ET.SubElement(conditions,'windturbulence')
        windturbulence.text = str(self.turbulency)

        #Direção do Vento
        launchwinddirection = l.ET.SubElement(conditions,'winddirection')
        launchwinddirection.text = str(self.wind_direction)

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
        timestep.text = '0.01'

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
                    name.text = str(self.name)

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
                    launchrodlength.text = str(self.launch_rod)

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
                    windturbulence.text = str(self.turbulency)

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
                    timestep.text = '0.01'

                    flightdata = l.ET.SubElement(simulation,'flightdata')
                    flightdata.attrib['maxaltitude'] = '1000' #Valor arbitrário

        rocket.to_ork(rocket_run)

    def run(self,rocket,or_path):
        l.subprocess.call(["java", "-jar", or_path, "--runSimulations", self.rocket.file_path])
        self.simu_path = rocket.file_path

    def results(self,rocket):
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
                line = [float(item) for item in line.split(',')]
                simu.append(line)    
            simu = l.pd.DataFrame(simu)
            simus.append(simu)

        self.data = simus

    def plot(self,simulation_number = 0, projection = 3):
        if projection == 3:    
            fig = l.plt.figure()
            ax = l.plt.axes(projection='3d')
            if simulation_number == 0:
                ax.plot(self.data[0].iloc[:,7],self.data[0].iloc[:,6],self.data[0].iloc[:,1])
                ax.set_xlabel('Posição a Norte')
                ax.set_ylabel('Posição a Leste')
                ax.set_zlabel('Altitude')
                #l.plt.plot(self.data[0].iloc[:,0],self.data[0].iloc[:,1])
            else:
                ax.plot(self.data[simulation_number].iloc[:,7],self.data[simulation_number].iloc[:,6],self.data[simulation_number].iloc[:,1])
                ax.set_xlabel('Posição a Norte')
                ax.set_ylabel('Posição a Leste')
                ax.set_zlabel('Altitude')
            l.plt.show()
        elif projection == 2:
            l.plt.plot(self.data[0].iloc[:,0],self.data[0].iloc[:,1])
            l.plt.xlabel('Tempo (s)')
            l.plt.ylabel('Altitude (m)')
            l.plt.show()
        else:
            print("projection só assume os valores 2 e 3!")

    def impact_point(self):
        self.points = l.pd.DataFrame([[self.data[simu].iloc[-1,7],self.data[simu].iloc[-1,6]] for simu in range(len(self.data))])
        self.points.columns = ['x','y']

    def mean_point(self):
        return self.points.mean()

    def std_point(self):
        return self.points.std()

    def plot_impact_points(self,sigma=3):
        avg = self.mean_point()
        std = self.std_point()
        temp = self.points[((self.points.x >= avg[0] - sigma*std[0]) & (self.points.x <= avg[0] + sigma*std[0])) & (self.points.y >= avg[1] - sigma*std[1]) & (self.points.y <= avg[1] + sigma*std[1])]
        l.plt.scatter(temp.iloc[:,0],temp.iloc[:,1])
        l.plt.title("Dispersão dos Pontos de Impacto {}-sigma".format(sigma))
        l.plt.xlabel("x")
        l.plt.ylabel("y")
        l.plt.show()

class MonteCarlo:
    def __init__(self,avg_variables,std_variables):
        self.avg_values = avg_variables
        self.std_values  = std_variables

    def random_values(self,distribution="normal", num = 1):
        if distribution == "normal":
            vetor = []
            for i in range(0,len(self.avg_values)):
                vetor.append(l.np.random.normal(self.avg_values[i],self.std_values[i],num))
            #vetor = l.np.append(vetor,axis=0)
            self.values = vetor
    
    def montecarlo_simulation(self):
        return Simulation('Teste1', self.values[0], [0], [0], self.values[1], self.values[2], 0)
        # simu.add_all_simulations(foguete)
        # simu.run(foguete, openrocket)
        # simu.results(foguete)
        # self.mc_data = simu.data
