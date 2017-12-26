import xml.dom.minidom
import yaml
import pprint

class tools:
    def loadconfig(self):
        # pass
        # 打开xml文档
        DOMTree = xml.dom.minidom.parse('RunTool.xml')
        # 得到文档元素对象
        Data = DOMTree.documentElement
        select = Data.getElementsByTagName('useconfig')
        if select:
            self.select = select[0].childNodes[0].data
        configs = Data.getElementsByTagName('config')
        #self.configs = configs
        #self.configNameTab = []
        #self.buttons = []
        self.config = {'RunTool':{}}

        if configs:
            if not(self.select):
                self.select = configs[0].getAttribute('name')
            #self.config['RunTool'] = {}
            for config in configs:
                # print '***config***'
                if config.hasAttribute("name"):
                    # self.configNameTab.append(config.getAttribute("name"))
                    configname = config.getAttribute("name")
                    configtab = {} #{'name': configname, }
                    buttons = []
                    for subconfig in config.childNodes:
                        if subconfig.nodeName == 'button':
                            buttonname = subconfig.getAttribute('name')
                            print("is button %s path %s" , buttonname, subconfig.childNodes[0].data)
                            buttons.append(
                                {"name": buttonname, "cmd": subconfig.childNodes[0].data})
                            #self.buttons.append({'name': buttonname, 'path': subconfig.childNodes[0].data})
                        elif subconfig.nodeName == 'workdir':
                            configtab['workdir'] = subconfig.childNodes[0].nodeValue
                    configtab['button'] = buttons
                    self.config['RunTool'][configname] = configtab
                    #self.config['RunTool'].append(configtab)
    def save2yaml(self,filename):
        f=open(filename,"w", encoding='utf-8')
        print(yaml.dump(self.config,f,default_flow_style=False,encoding='utf-8',allow_unicode=True))
        f.close()


if __name__ == '__main__':
    ts = tools()
    ts.loadconfig()
    pprint.pprint(ts.config)
    ts.save2yaml("RunTool2.yaml")
