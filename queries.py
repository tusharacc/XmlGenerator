queries = {
    'failure_list': "SELECT MicroMessagesDownStreamApplicationId, ProcessStatusCode, TransStatus, Reference FROM MicroMessageDownStreamTransactionDetail WHERE LastErrorDescription like '%is not unique%' and LastErrorDescription like '%Another record exists on the master file with a%' and PolicyAction = 'Renewal' and TransStatus = 'FAILURE'",
    'get_policy_term': "select Reference, PolicyAction,CreatedDateTime from MicroMessageDownStreamTransactionDetail where Reference like ? AND MicroMessagesDownStreamApplicationId <> ? Order by PolicyAction",
    'get_transformed_xml': 'select TransformedXml from MicroMessageDownstreamApplication where MicroMessageDownstreamApplicationId = ?',
    'auto-ri':"select MicroMessagesDownStreamApplicationId, MasterRef, Reference from MicroMessageDownStreamTransactionDetail where LastErrorDescription like '%Auto RI errors have occurred%' and TransStatus = 'Failure'"
}