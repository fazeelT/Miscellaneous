import boto3

domain = '${domain}'
swf = boto3.client('swf', 'ap-northeast-1')
filename = "${fileName}"

def fetch_input(wfId, runId):
    response = swf.get_workflow_execution_history(
        domain=domain,
        execution={
            'workflowId': wfId,
            'runId': runId
        },
        maximumPageSize=123,
        reverseOrder=False
    )

    firstEvent = find(lambda event: event['eventId'] == 1, response['events'])

    return firstEvent['workflowExecutionStartedEventAttributes']['input']

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item

def run_workflow(id, input, wfName, wfVersion):
    response = swf.start_workflow_execution(
        domain=domain,
        workflowId=id,
        workflowType={
            'name': wfName,
            'version': wfVersion
        },
        input=input
    )

    print(response)

with open(filename) as f:
    for line in f:
        processed_line = line.replace('WORKFLOWEXECUTION', '').strip()
        wf = processed_line.split('|')
        input = fetch_input(wf[0], wf[1])
        run_workflow(wf[0], input, '${workflowName}', '${workflowVersion}')