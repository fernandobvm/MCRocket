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
