from jinja2 import Template
import codecs
import re
import string
import random

class RDL():
    
    def __init__(self,server_url,datasource,query,template='template.rdl'):
        self.query = query
        self.server_url = server_url
        self.datasource = datasource
        self.template = template
        
        self.fields = []
        self.paramters = []

        self.init_parameters()
        self.init_fields()
        
    def get_text(self,):
        with open(self.template, 'r') as template_file:
            template = Template(template_file.read().decode('utf8'))
            return template.render(
                query=self.query,
                data_source_reference=self.datasource,
                data_source_id=self.gen_id(),
                fields=self.fields,
                parameters=self.parameters,
                server_url = self.server_url,
                report_id = self.gen_id(),
            )
    
    def write_file(self,filename):
            with open(filename, 'w') as out_file:
                out_file.write(codecs.BOM_UTF8)

                out_file.write(self.get_text())
    
    def init_fields(self):
        m = re.match(r'select(.*?)\nfrom', self.query, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)
        
        for field in m.group(1).strip().split(',\n'):
            names = field.split(' as ')
            
            name = names[0]
            
            if len(names) > 1:
                name = names[1]
            
            name = name.replace('\'','')
            name = name.strip()
            
            self.fields.append({
                "name":name
            })
  
    def init_parameters(self):
        matches = re.findall(r'@[a-zA-Z0-9_]*?[ \n\r]', self.query, flags=re.MULTILINE)

        self.parameters = set([m.strip().replace('@','') for m in matches])
            
    def gen_id(self,size=16,chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    import sys
    
    try:
        server_url = str(sys.argv[1])
        datasource = '/' + str(sys.argv[2])
        outfile = str(sys.argv[3])
        query = str(sys.stdin.read())
    except:
        print 'Usage: %s [server_url] [datasource] [outfile]\nSQL query is supplied on stdin' % (sys.argv[0],)
        exit(1)
    
    rdl = RDL(server_url,datasource,query)

    rdl.write_file(outfile)
    print "Output written to %s" % outfile