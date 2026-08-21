import json
import urllib.request

def scan_person(name):
    data = json.dumps({"name": name}).encode('utf-8')
    request = urllib.request.Request(
        'http://localhost:8000',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        return json.loads(error.read().decode())

def webhook_callback(name, success=True):
    data = json.dumps({"name": name, "success": success}).encode('utf-8')
    request = urllib.request.Request(
        'http://localhost:8001',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    response = urllib.request.urlopen(request)
    return json.loads(response.read().decode())

print("Test 1: Petronila checks in")
result = scan_person("Petronila")
print("Scan result:", result)
webhook_callback("Petronila", True)
print("Petronila is now checked in")

print("\nTest 2: Jayden scans twice")
result1 = scan_person("Jayden")
print("First scan:", result1)
webhook_callback("Jayden", True)
result2 = scan_person("Jayden")
print("Second scan:", result2)

print("\nTest 3: Abunwasi checks in then scans again")
result1 = scan_person("Abunwasi")
print("First scan:", result1)
webhook_callback("Abunwasi", True)
result2 = scan_person("Abunwasi")
print("Second scan:", result2)

print("\nAll tests complete")