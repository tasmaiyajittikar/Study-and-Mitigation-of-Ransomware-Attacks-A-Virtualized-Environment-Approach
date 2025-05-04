from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import psutil
import json
import os
import subprocess
from datetime import datetime
# Import mitigation functions
from mitigation import mitigation, ask_to_unlock, backup


# Setup variables, watchdog will be watching the "critical" folder and write to monitoring_log.json
LOG_FILE = "monitoring_log.json"
WATCH_PATH = os.path.abspath("./critical")
AUDIT_KEY = "critical_watch"


# Create honeypot file to catch ransomware
def create_honeypot_file(path="critical/zzzzz_HONEYPOT.txt"):
        if not os.path.exists(path):
                with open(path, "w") as f:
                        f.write("Gotcha")
                os.chmod(path, 0o444)


# Run auditd to catch the curl process
def run_auditd():
        try:
                subprocess.run(["systemctl", "is-active", "--quiet", "auditd"], check=True)
        except subprocess.CalledProcessError:
                print("starting auditd")
                try:
                        subprocess.run(["sudo", "systemctl", "start", "auditd"], check=True)
                        print(f"auditd started successfully")
                except subprocess.CalledProcessError:
                        print(f"failed to start auditd")


# Write to a json log file
def log_event(event_type, file_path, pid, note):
        log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "file": file_path,
                "pid": pid,
                "note": note,
                "action_taken": "logged"
        }
        with open(LOG_FILE, "a") as f:
                f.write(json.dumps(log_entry) + "\n")


# Add the auditd rule to linux to find fast processes
def add_audit(path_to_watch):
        try:
                subprocess.run(["auditctl", "-w", path_to_watch, "-p", "rwxa", "-k", AUDIT_KEY], check=True)
                print(f"[AUDIT] Rule added for {path_to_watch}")
        except subprocess.CalledProcessError:
                print(f"Audit rule already exists")


# Find the correct pid of the ransomware from the audit
def pid_from_audit(file_path):
        try:
                output = subprocess.check_output(["ausearch", "-k", AUDIT_KEY, "-ts", "recent"]).decode()
                basename = os.path.basename(file_path)
                grouped = {}
                current_msg = None


                for line in output.splitlines():
                        if "msg=audit(" in line:
                                parts = line.split("msg=audit(")
                                if len(parts) > 1:
                                        msg_id = parts[1].split(")")[0]
                                        current_msg = msg_id
                                        grouped.setdefault(current_msg, []).append(line)
                                elif current_msg:
                                        grouped[current_msg].append(line)


                for msg_id, lines in reversed(grouped.items()):
                        for line in lines:
                                if basename in line:
                                        for l in lines:
                                                if "pid=" in l:
                                                        for part in l.strip().split():
                                                               if part.startswith("pid="):
                                                                        pid = int(part.split("=")[1])
                                                                        return pid
        except subprocess.CalledProcessError:
                pass
        return None


# Separate the actions
class MonitorHandler(FileSystemEventHandler):
        def handle_event(self, event_type, event):
                pid = pid_from_audit(event.src_path)
                time.sleep(0.2)


                # Discover suspicious extensions and to see if the honeypot was accessed
                sus_extensions = [".encrypted", ".enc", ".lock"]
                _, ext = os.path.splitext(event.src_path)


                if "HONEYPOT" in os.path.basename(event.src_path):
                        note = "Honeypot was accessed. Ransomware maybe detected"
                        mitigation(WATCH_PATH)
                elif ext in sus_extensions:
                        note = f"suspicious file: {ext}"
                        mitigation(WATCH_PATH)
                else:
                        note = f"Safe"


                log_event(event_type, event.src_path, pid, note)


        def on_created(self, event):
                self.handle_event("created", event)


        def on_modified(self, event):
                self.handle_event("modified", event)


        def on_deleted(self, event):
                self.handle_event("deleted", event)


        def on_moved(self, event):
                self.handle_event("moved", event)


# Continuously monitor the folder
if __name__ == "__main__":


        if not os.path.exists(WATCH_PATH):
                os.makedirs(WATCH_PATH)


        subprocess.run(["chattr", "-R", "-i", WATCH_PATH], check=True)


        create_honeypot_file()
        run_auditd()
        add_audit(WATCH_PATH)


        handler = MonitorHandler()
        observer = Observer()


        path_to_watch = "./critical"
        observer.schedule(handler, path=WATCH_PATH, recursive=True)
        observer.start()


        print(f"Monitoring started on: {WATCH_PATH}")
        print(f"Logging to : {os.path.abspath(LOG_FILE)}")


        try:
                while True:
                        time.sleep(1)
        except KeyboardInterrupt:
                print(f"Monitoring stopped")
                observer.stop()


        observer.join()
        subprocess.run(["auditctl", "-W", WATCH_PATH, "-k", AUDIT_KEY])