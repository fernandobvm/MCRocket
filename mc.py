import lib as l

class Rocket:
    """ 
    A class used to represent a Rocket

    ...

    Attributes
    ----------
    name : str
        rocket name as a string
    file_path : str
        path to .ork file
    engine_path : str
        path to .eng file
    xml : 
        xml object that represents .ork file unzipped

    Method
    ------
    to_xml()
        unzip .ork file and uses ElementTree to read the xml file
    to_ork(xml)
        save the rocket xml file as a .ork file
    """

    def __init__(self,name,file_path,engine_path):
        """
        Parameters
        ----------
        name : str
            The name of the rocket
        file_path : str
            The path to .ork file
        engine_path : str
            The path to .eng file
        """

        self.name = name
        self.file_path = file_path
        self.engine_path = engine_path

    def to_xml(self):
        """ Unzip the rocket .ork file and load it as a xml file using ElementTree Python module

        Returns
        -------
        ET object
            rocket ElementTree object
        """

        l.unzip_rocket(self.file_path)
        return l.ET.parse(l.os.path.dirname(self.file_path) + '/rocket.ork')

    def to_ork(self,xml):
        """ Save xml file as .ork file

        Parameters
        ----------
        xml :
            Xml object that represents .ork file unzipped
        """
        xml.write(self.name+'.ork','utf-8')
        self.file_path = l.os.getcwd() +  '\\' + self.name + '.ork'


class Simulation:
    """
    A class used to setup an OpenRocket simulation

    ....

    Attributes
    ----------
    name : str
        simulation name or description
    elevation : float
        launch rod angle from vertical in degrees
    wind_velocity : float
        wind velocity in meters per second
    wind_direction : float
        wind direction in degrees
    launcrod_direction : float
        direction of launch in degrees
    launch_rod : float
        launch rod length
    turbulency : float
        turbulency intensity
    rocket : 
        class Rocket object
    or_path : str
        path to OpenRocket file
    

    Method
    ------
    add_simulation(rocket)
        add a simulation to the rocket file
    add_all_simulations(rocket)
        by inpunting vectors as initial conditions it combine them all in many simulations
    run(rocket,or_path)
        run all simulations
    """
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
                    launchroddirection.text = str(self.launchrod_direction)

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

    def plot(self,simulation_number = -1, projection = 3):
        if projection == 3:    
            fig = l.plt.figure()
            ax = l.plt.axes(projection='3d')
            if simulation_number != -1:
                ax.plot(self.data[simulation_number].iloc[:,7],self.data[simulation_number].iloc[:,6],self.data[simulation_number].iloc[:,1])
                ax.set_xlabel('Posição a Norte')
                ax.set_ylabel('Posição a Leste')
                ax.set_zlabel('Altitude')
                #l.plt.plot(self.data[0].iloc[:,0],self.data[0].iloc[:,1])
            else:
                for simus in self.data:
                    ax.plot(simus.iloc[:,7],simus.iloc[:,6],simus.iloc[:,1])
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
        avg = self.__mean_point()
        std = self.__std_point()
        self.points['sigma'] = 0
        self.points.loc[((self.points.x >= avg[0] - 3*std[0]) & (self.points.x <= avg[0] + 3*std[0])) & (self.points.y >= avg[1] - 3*std[1]) & (self.points.y <= avg[1] + 3*std[1]),'sigma'] = 3
        self.points.loc[((self.points.x >= avg[0] - 2*std[0]) & (self.points.x <= avg[0] + 2*std[0])) & (self.points.y >= avg[1] - 2*std[1]) & (self.points.y <= avg[1] + 2*std[1]),'sigma'] = 2
        self.points.loc[((self.points.x >= avg[0] - 1*std[0]) & (self.points.x <= avg[0] + 1*std[0])) & (self.points.y >= avg[1] - 1*std[1]) & (self.points.y <= avg[1] + 1*std[1]),'sigma'] = 1

    def __mean_point(self):
        return self.points.mean()

    def __std_point(self):
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
    def __init__(self,avg_variables,std_variables,foguete):
        self.avg_values = avg_variables
        self.std_values  = std_variables
        self.foguete = foguete
        self.openrocket = "D:/Documentos/library/UnB/4Semestre/Capital/OpenRocketTurbo2.jar"

    def random_values(self,distribution="normal", num = 1):
        if distribution == "normal":
            vetor = []
            for i in range(0,len(self.avg_values)):
                a = l.np.random.normal(self.avg_values[i],self.std_values[i],num)
                vetor.append(l.np.append(self.avg_values[i],a))
            #vetor = l.np.append(vetor,axis=0)
            self.values = vetor
            #print(vetor)
    
    def montecarlo_simulation(self):
        #return Simulation('Teste1', self.values[0], [0], [0], self.values[1], 6.0, 0)
        for itens in range(0,len(self.values[0])):
            simu = Simulation('Teste1', self.values[0][itens], 0, 0, self.values[1][itens], 6.0, 0)
            simu.add_simulation(self.foguete)
        simu.run(self.foguete, self.openrocket)
        simu.results(self.foguete)
        simu.impact_point()
        self.simulation = simu
        self.data = simu.data
        self.points = simu.points
    
    def plot(self):

        fig = l.plt.figure()
        ax = l.plt.axes(projection='3d')

        ax.plot(self.data[0].iloc[:,7],self.data[0].iloc[:,6],self.data[0].iloc[:,1])
        ax.set_xlabel('Posição a Norte')
        ax.set_ylabel('Posição a Leste')
        ax.set_zlabel('Altitude')
        #l.plt.xlim(-10,10)

        col = l.np.where(self.points.sigma == 1,'g', l.np.where(self.points.sigma == 2, 'b','m'))

        ax.scatter(self.points.x,self.points.y,0,color=col)
        l.plt.show()


