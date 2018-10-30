from lxml import etree
import get_policy_details as p

class XmlProcesser:
    def __init__(self,xml):
        self.root = etree.fromstring(xml)
    
    def update_xml(self,xpath,value):
        n_map = self.root.nsmap
        n_map['int'] = 'http://rebusis.com/webservices/gcs/IntegrationService'
        self.root.find(f'.//int:{xpath[3:]}',namespaces=n_map).text = value
    
    def write_to_file(self,path,policy,appid):
        etree.ElementTree(self.root).write(f'{path}/{policy}_{appid}.xml',pretty_print=True)


if __name__ == '__main__':
    policy = p.GetPolicyDetails('D39389502')
    x = policy.get_transformed_xml(1511509)
    new_policy = policy.get_term_number(1511509)
    if new_policy != 'Renewal Processed':
        xml = XmlProcesser(x)
        xml.update_xml('.//Reference',new_policy)
        policy_num, term_num = new_policy.split()
        print ((term_num))
        old_policy = policy_num + ' 00' + str(int(term_num[-1]) - 1)
        xml.update_xml('.//AssuredReference',old_policy)
        xml.write_to_file(policy_num,1501702)


    