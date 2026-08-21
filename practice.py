import time
memory = {}
# Helps to remember who was cheking-in
printer_mailbox= []

def drop_in_mailbox(attendee_name): 
    """Put message in the que for printer."""

    message = {"name": attendee_name, "time": time.time()}
    printer_mailbox.append(message)
    print(f"Dropped in mailbox: Proceed to print badge for {attendee_name}")

# Working assumption: Attendees use QR code to check-in
def scan_qr_code(attendee_name):
    print(f"\nScanning QR code for {attendee_name}...")

    if attendee_name in memory:
        status = memory[attendee_name]
        if status == "Pending":
            print(f"STOP! {attendee_name} is alreading waiting for the badge.")
            return "ERROR: Already waiting."
        elif status == "Checked-in": 
            print(f"STOP! {attendee_name} is already Checked-in!")
            return "ERROR: Already Checked-in."

    else: 




# For scenarios where attendees attempt a duplicate scan
        memory[attendee_name] = "Pending"
        print(f"Marked {attendee_name} as Pending (waiting for printer).")
        drop_in_mailbox(attendee_name)
        print(f"Screen shows: Printing on-going for {attendee_name}...")
        return "Success: Pending."

# To ensure the printer gets it right
def printer_finished_callback(attendee_name, success=True): 
    print(f"\nPrinter calls back for {attendee_name}")
    if success: 
        memory[attendee_name] = "Checked-in"
        print(f"Updated {attendee_name} to Checked-in.")
    else: 
        memory [attendee_name] = "Failed"
        print(f"Updated {attendee_name} to Failed.")


# Testing the 3 scenarios
if __name__ == "__main__": 
    print("---STARTING CHECK-IN---")

# Scenario 1: Petronila checks-in
    scan_qr_code("Petronila")
    printer_finished_callback("Petronila", success=True)

# Scenario 2: Jayden attempts a duplicate scan
    scan_qr_code("Jayden")
    scan_qr_code("Jayden")

# Scenario 3: Abunwasi (Normal check-in then duplicate later)
    scan_qr_code("Abunwasi")
    printer_finished_callback("Abunwasi", success=True)
    scan_qr_code("Abunwasi")

    print("\n---FINAL MEMORY STATUS---")
    for name, status in memory.items():
        print(f"{name}: {status}")
