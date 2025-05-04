# Ransomware Attack Simulation Project

![Project Banner](assets/img/infectionDFD.png)

A virtualized environment approach to studying and mitigating ransomware attacks.

## Project Overview
This research simulates ransomware attacks in controlled environments to:
- Analyze attack vectors and patterns
- Test detection methodologies
- Develop effective mitigation strategies


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
