from sseclient import SSEClient

# Replace with your SSE endpoint URL
sse_url = "http://localhost:8000/streams/events" 

client = SSEClient(sse_url)
print(client)
for event in client:
    # print(f"Event ID: {event.id}")
    # print(f"Event Type: {event.event}")
    # print(f"Event Data: {event.data}")
    # print("-" * 20)
    print(event.event)