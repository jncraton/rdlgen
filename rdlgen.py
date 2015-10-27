from jinja2 import Template
import codecs
import re
import string
import random

class RDL():
    query = ''
    fields = []
    
    def __init__(self,datasource,query,template='template.rdl'):
        self.query = query
        self.datasource = datasource
        self.template = template
        
        self.init_fields()
        
    def get_text(self,):
        with open(self.template, 'r') as template_file:
            template = Template(template_file.read().decode('utf8'))
            return template.render(
                query=self.query,
                data_source_reference=self.datasource,
                data_source_id=self.gen_id(),
                fields=self.fields
            )
    
    def write_file(self,filename):
            with open(filename, 'w') as out_file:
                out_file.write(codecs.BOM_UTF8)

                out_file.write(self.get_text())
    
    def init_fields(self):
        m = re.match(r'select (.*?) from', self.query, flags=re.IGNORECASE)
        
        for field in m.group(1).split(','):
            self.fields.append({
                "name":field.strip()
            })
            
    def gen_id(self,size=16,chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    import sys
    
    try:
        datasource = '/' + str(sys.argv[1])
        query = str(sys.stdin.read())
    except:
        print 'Usage: %s [datasource]\nSQL query is supplied on stdin' % (sys.argv[0],)
        exit(1)
    
    rdl = RDL(datasource,query)

    rdl.write_file("output.rdl")
    print "Output written to output.rdl"