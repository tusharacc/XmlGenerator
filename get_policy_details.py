import queries as q
import query_db as db
from datetime import datetime

class GetPolicyDetails:
    def __init__(self,policy):
        self.policy = policy

    def get_transformed_xml(self,appid):
        query = q.queries['get_transformed_xml'],(appid)
        conn = db.ConnectToDb()
        results = conn.execute_query(query)
        conn.close_conn
        records = []
        if results['status'] == 'Ok':
            return results['rows'][0][0]
        else:
            return 'Failed'



    def get_term_number(self,appid):
        query = q.queries['get_policy_term'],('%'+self.policy+'%',appid)
        conn = db.ConnectToDb()
        results = conn.execute_query(query)
        conn.close_conn
        records = []
        if results['status'] == 'Ok':
            for row in results['rows']:
                cell = []
                for c in row:
                    cell.append(c)
                records.append(cell)
        if records[-1][1] == 'Renewal':
            if (datetime.now() - records[-1][2]).days < 100:
                return 'Renewal Processed'
            else:
                return self.policy + ' 00' + str((int(records[-1][0][-1]) + 1))
        else:
            return self.policy + ' 00' + str((int(records[-1][0][-1]) + 1))

if __name__ == '__main__':
    policy = GetPolicyDetails('D39365182')
    print (policy.get_transformed_xml(1501702))