import get_policy_details as p
import queries as q
import query_db as db
import scixml as x
from datetime import datetime
import os
from pubsub import pub

def process_renewal():
    query = q.queries['failure_list']
    path = 'results/renewal/' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 
    os.mkdir(path)
    pub.sendMessage('message',message1={'type':'info','msg':f'Renewal - Folder created {path}'})

    conn = db.ConnectToDb()
    results = conn.execute_query(query)
    conn.close_conn
    pub.sendMessage('message',message1={'type':'info','msg':f'Renewal - Querying table'})
    
    if results['status'] == 'Ok':
        records = []
        for row in results['rows']:
            policy_number = row[3].split()[0]
            pub.sendMessage('message',message1={'type':'info','msg':f'Renewal - Processing Policy Number {policy_number}'})
            appid = row[0]
            policy = p.GetPolicyDetails(policy_number)
            tran_xml = policy.get_transformed_xml(appid)
            new_policy = policy.get_term_number(appid)
            if new_policy != 'Renewal Processed':
                cl_xml = x.XmlProcesser(tran_xml)
                cl_xml.update_xml('.//Reference',new_policy)
                policy_num, term_num = new_policy.split()
                old_policy = policy_number + ' 00' + str(int(term_num[-1]) - 1)
                cl_xml.update_xml('.//AssuredReference',old_policy)
                cl_xml.write_to_file(path,new_policy,appid)
                records.append([new_policy,' ',str(appid)])
        #print ('\n'.join(map(lambda x: ''.join(x),records)))
        with open('summary.txt','w') as f:
            f.write('\n'.join(map(lambda x: ''.join(x),records)))
        pub.sendMessage('message',message1={'type':'succ','msg':f'Renewal - Processing Completed'})
    else:
        pub.sendMessage('message',message1={'type':'err','msg':f"Renewal - Failed {results['status']}"})

if __name__ == '__main__':
    process_renewal()