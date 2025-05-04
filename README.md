# Ransomware Attack Simulation Project

![Project Banner](assets/img/infectionDFD.png)

A virtualized environment approach to studying and mitigating ransomware attacks.

## Project Overview
This research simulates ransomware attacks in controlled environments to:
- Analyze attack vectors and patterns
- Test detection methodologies
- Develop effective mitigation strategies
## Table of Contents
- [Project Overview](#project-overview)
- [Key Components](#key-components)
- [Setup Instructions](#setup-instructions)
- [Execution Workflow](#execution-workflow)
- [Detection & Mitigation Strategies](#detection--mitigation-strategies)
- [Future Enhancements](#future-enhancements)
- [Team](#team)

## Project Overview
This project simulates a ransomware attack in a controlled virtualized environment to:
- Demonstrate ransomware mechanics (AES-256 encryption, phishing vectors)
- Test detection methods (honeypots, file monitoring)
- Implement mitigation strategies (directory lockdowns, automated backups)

**Scenario**:  
An employee receives a phishing email from "Amazon Careers" with a link to a fake job portal. Upon downloading the "offer letter", a ransomware payload encrypts files in the `critical` directory.

## Key Components

### 1. Attack Simulation
| Component          | Technology Used          |
|--------------------|-------------------------|
| Phishing Email     | Python SMTP             |
| Fake Job Portal    | Flask (AWS EC2)         |
| Ransomware Payload | OpenSSL AES-256-CBC     |
| C2 Communication   | HTTP POST to 192.168.56.15 |

### 2. Defense System
| Component          | Technology Used          |
|--------------------|-------------------------|
| Real-Time Monitoring | Python `watchdog`      |
| Honeypot           | Read-only bait file     |
| Directory Lockdown | `chattr +i` command    |
| Automated Backups  | `shutil.copytree`      |

## Setup Instructions

### Prerequisites
- VMware/VirtualBox with:
  - Attacker VM (Ubuntu 22.04, IP: 192.168.56.10)
  - Victim VM (Windows/Ubuntu, IP: 192.168.56.20)
- AWS EC2 instance (for job portal)
- Python 3.x, OpenSSL, Flask


## FILES

- **monitor.py** - main script to start monitoring and detecting alterations on a directory
- **monitor.sh** - executable to start monitoring
- **mitigation.py** - extra file holding functions to mitigate intrusion

## SETUP

*monitor.py*, *monitor.sh*, and *mitigation.py* should all be in the parent directory of the **"critical"** directory. The **"critical"** directory should contain another folder with the files that are deemed **"sensitive"**. 

## DEPENDENCIES

The following dependencies need to be installed on the system:  
- Python's watchdog
- auditd
- Python's tkinter

## COMPILING

```
python3 monitor.sh
./monitor.sh
```

## Key Components
- **Virtual Lab Setup**: AttackerVM and VictimVM configuration
- **Encryption Module**: AES-256-CBC implementation
- **Monitoring System**: File integrity watching with honeypots
- **Mitigation Protocols**: Directory lockdowns and backups

## Live Demo
View the project website: 

## Research Team
- Tasmaiya Tamboli
- Ujjwal Rana Magar
- Kaylyn King
- Jean-Charles Hekamanu

## License
This project is for academic research purposes only.
