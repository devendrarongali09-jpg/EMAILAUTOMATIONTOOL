#Email Automation Tool
import csv
from email.message import EmailMessage
import os
import smtplib
import time

# --- Configuration ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "devendrarongali09@gmail.com"
SENDER_PASSWORD = "wcxx wxea kuzu prvq"

# Update with your confirmed CSV path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "students.csv")
# Or use your raw path if it's elsewhere:
# CSV_FILE = r"C:\path\to\your\students1.csv"


def send_personalized_emails():
  if not os.path.exists(CSV_FILE):
    print(f"Error: Could not find '{CSV_FILE}'.")
    return

  try:
    print("Connecting to SMTP server...")
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
      server.ehlo()
      server.starttls()
      server.login(SENDER_EMAIL, SENDER_PASSWORD)
      print("Login successful! Starting to process student list...\n")

      # Use 'utf-8-sig' to automatically remove any hidden Excel BOM marks
      with open(CSV_FILE, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Print detected headers so you can see them clearly
        print(f"Columns found in CSV: {reader.fieldnames}\n")

        for index, raw_row in enumerate(reader, start=1):
          # Normalize all keys: strip whitespace and convert to lowercase
          row = {
              k.strip().lower(): v.strip()
              for k, v in raw_row.items()
              if k is not None
          }

          # Match common variations of column headers
          name = row.get("name") or row.get("student name") or "Student"
          email = row.get("email") or row.get("email address") or ""
          course = row.get("course") or row.get("subject") or "your course"

          if not email:
            print(
                f"[{index}] Skipped: Missing email. Row contents were: {raw_row}"
            )
            continue

          # Prepare message
          subject = f"Enrollment Confirmation: {course}"
          body = (
              f"Hi {name},\n\n"
              f"Welcome aboard! You have been successfully enrolled in"
              f" {course}.\n\n"
              f"Classes start shortly. Please check your student portal for the"
              " syllabus.\n\n"
              f"Best regards,\n"
              f"Student Admissions Team"
          )

          msg = EmailMessage()
          msg["Subject"] = subject
          msg["From"] = SENDER_EMAIL
          msg["To"] = email
          msg.set_content(body)

          try:
            server.send_message(msg)
            print(f"[{index}] Successfully sent to {name} ({email})")
          except Exception as err:
            print(f"[{index}] Failed to send to {name} ({email}): {err}")

          time.sleep(1)

      print("\nAll emails processed. Connection closed successfully.")

  except Exception as e:
    print(f"SMTP Error: {e}")


if __name__ == "__main__":
  send_personalized_emails()