# Face-Recognition-Based-Personal-Information-Access-System
A web-based facial recognition system built with Python, Flask, and DeepFace, allowing authorized personnel and public authorities to securely identify individuals and access their credentials.

##UPDATE NOTES

###Web Architecture & UI Overhaul (Latest)
[NEW] Web Architecture: Migrated the entire system to a scalable web application using Flask.
[NEW] User Interface: Built a formal, government-style web interface (HTML/CSS) for secure browser capability.
[NEW] Browser Querying: Authorized personnel can now securely upload images and query individuals directly from modern web browsers.
[NEW] Dynamic Results Dashboard: Added automatic, dynamic rendering of queried profiles (Student/Staff Number, Department, DOB) upon successful facial match.
[UPDATE] Error Handling Mechanism: Implemented robust session alerts and visual feedback for database mismatches, undetected faces, or processing errors.

###Relational Database Integration & ArcFace Implementation
[NEW] SQLite Database: Deprecated static folder structures in favor of a fast, relational SQLite database (person_info.db).
[NEW] Access Logging: Created automatic tracking (access_logs table) that records the date, time, queried identity, and success status of every system interaction.
[UPDATE] Biometric Engine Upgrade: Transitioned the underlying DeepFace configuration to the ArcFace model, significantly boosting facial recognition accuracy.
[FIX] Missing Profiles Retrieval: Resolved an issue where the face matcher could detect an individual but failed to fetch their credentials.

###Initial Release & Core Engine
[NEW] Core System Logic: Developed the initial proof-of-concept utilizing Python, DeepFace, and OpenCV.
[NEW] Basic Detection: Implemented local script execution capable of comparing a test image against a static dataset directory.
[NEW] Local Testing Environment: Provided a command-line testing protocol via standard output (print logs).

