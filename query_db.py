import pyodbc
import logging


logger = logging.getLogger(__name__)

class ConnectToDb():

	def __init__(self, reg='DB'):
		region = {'DB': {'server': r'Server=NAUSP-WSQL0068\SQL12A;',
						   'database_name': 'Database=SciDuckCreInt;'}
		}
		self.status = 'Ok'
		try:
			self.conn = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};" +
							region[reg]['server'] +
							region[reg]['database_name'] +
							"Trusted_Connection=yes;")
		except Exception as ex:
			self.status = ex

	def execute_query(self,query,type="SEL"):
		cursor = self.conn.cursor()
		rows = []
		status = 'Ok'
		try:
			if isinstance(query,tuple):
				cursor.execute(*query)
			else:
				cursor.execute(query)
			if type == "SEL":
				rows = cursor.fetchall()
			else:
				self.conn.commit()
				logger.info(f'The number of records affected {cursor.rowcount}')
				status == "Ok"

		except Exception as ex:
			print (ex)
			status = ex
		finally:
			logger.info(f'The status of query {status}')
			return {'rows':rows,'status':status}

	def close_conn(self):
		status = 'Ok'
		try:
			self.conn.close()
		except Exception as ex:
			status = ex
		finally:
			return {'status':status}


if __name__ == '__main__':
	conn_to_db = ConnectToDb()
