from configparser import ConfigParser


class Config:
    parser :ConfigParser
    def __init__(self):
        self.file = "database.ini"

    def save(self,section:ConfigParser):
        self.parser = section
        for sect in self.parser.sections():
            if self.section_exists(sect):        
                cfgfile = open(self.file,'a',encoding='cp1251')
                section.write(cfgfile)
                cfgfile.close()
            else:
                cfgfile = open(self.file,'a',encoding='cp1251')
                self.parser.write(cfgfile)
                cfgfile.close()

                
    def load(self,section:ConfigParser):       
        section.read(self.file)
        db = {}
        for sect in section.sections():
            params = section.items(sect)
            for param in params:
                    db[param[0]] = param[1]
        return db

    def section_exists(self, section) -> bool:
            parser = ConfigParser()
            parser.read(self.file)
            if parser.has_section(section):
                return True
            else:
                return False

