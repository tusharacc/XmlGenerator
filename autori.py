import get_policy_details as p
import queries as q
import query_db as db
import scixml as x
from datetime import datetime
import os
from pubsub import pub

def process_auto_ri():

    path = 'results/autori/' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 
    os.mkdir(path)
    pub.sendMessage('message',message1={'type':'info','msg':f'Auto RI - Folder created {path}'})

    query = q.queries['auto-ri']
    conn = db.ConnectToDb()
    results = conn.execute_query(query)
    conn.close_conn
    pub.sendMessage('message',message1={'type':'info','msg':f'Auto RI - Querying table'})

    if results['status'] == 'Ok':
        for row in results['rows']:
            appid = row[0]
            policy_number = row[2] if row[1] == '' else row[1]
            pub.sendMessage('message',message1={'type':'info','msg':f"Auto RI - processing policy {policy_number}"})
            policy = p.GetPolicyDetails(policy_number.split()[0])
            tran_xml = policy.get_transformed_xml(appid)
            if tran_xml is not None:
                cl_xml = x.XmlProcesser(tran_xml)
                cl_xml.update_xml('.//RunAutoRI','false')
                cl_xml.write_to_file(path,policy_number.split()[0],appid)
        pub.sendMessage('message',message1={'type':'succ','msg':f"Auto RI - processing completed"})
    else:
        pub.sendMessage('message',message1={'type':'err','msg':f"Auto RI - Failed {results['status']}"})