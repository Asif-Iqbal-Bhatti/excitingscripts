from lxml import etree

def attrib2float(tree,attrib_xpath):
    return str2float(tree.xpath(attrib_xpath)[0].split())
    
    
def str2float(str_vec):
    vf = []
    for str in str_vec:
        vf.append(float(str))
        
    return vf 