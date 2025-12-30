import requests
import json
import copy

WEBHOOK_URL = "https://qaoneorigin.app.n8n.cloud/webhook/testairr" 

# THE BASE TRUTH (Based on Arnold Okoye's Transcript)
base_data = {
    "filename": "okoye_arnold.pdf",
    "extracted_gpa": "89.17",
    "courses": [
        {"course": "History of Salvation I", "grade": "91"},
        {"course": "Honors Biology", "grade": "92"},
        {"course": "AP Biology", "grade": "92"},
        {"course": "AP Language and Composition", "grade": "92"}
    ]
}

def send_test(name, data):
    print(f"Running Test: {name}...")
    try:
        # Send data to n8n
        response = requests.post(WEBHOOK_URL, json=data)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"❌ ERROR: Webhook returned status {response.status_code}")
            return

        result = response.json()
        
        # Check if n8n returned what we expected
        if result.get('status') == 'PASS' and name == "Perfect Data":
            print("✅ SUCCESS: Passed valid data.")
        elif result.get('status') == 'FAIL' and name != "Perfect Data":
            print(f"✅ SUCCESS: Correctly caught error in {name}.")
            # Handle both string and list formats for errors
            error_count = len(result.get('errors', []))
            print(f"   Errors found: {error_count}")
        else:
            print(f"❌ FAILURE: QA System output unexpected result for {name}")
            print(f"   System Response: {result}")
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("   (Make sure n8n is running and the Webhook URL is correct)")

# --- TEST SUITE ---

# 1. The Happy Path (Should PASS)
send_test("Perfect Data", base_data)

# 2. Mutation: Typo in GPA (Should FAIL)
bad_gpa = copy.deepcopy(base_data)
bad_gpa['extracted_gpa'] = "89.71" # Swapped digits
send_test("Bad GPA", bad_gpa)

# 3. Mutation: Missing Course (Should FAIL)
missing_course = copy.deepcopy(base_data)
missing_course['courses'].pop(0) # Remove first course
send_test("Missing Course", missing_course)

# 4. Mutation: Wrong Grade (Should FAIL)
bad_grade = copy.deepcopy(base_data)
bad_grade['courses'][2]['grade'] = "65" # AP Biology grade mismatch
send_test("Bad Grade", bad_grade)