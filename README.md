# Log Analyzer and QR Code Tester


### Foreword

This repository provides solutions to two tasks related to the automation of specialized programs. All data, logs, and code are fictional and intended exclusively for educational purposes.

### Prepare the project

1. Fork the repo (GitHub repository)
2. Clone the forked repo
    ```
    git clone the-link-from-your-forked-repo
    ```
    - You can get the link by clicking the `Clone or download` button in your repo
3. Open the project folder in your IDE
4. Open a terminal in the project folder
5. Create a branch for the solution and switch on it
    ```
    git checkout -b develop
    ```
    - You can use any other name instead of `develop`
6. If you are using PyCharm - it may propose you to automatically create venv for your project
   and install requirements in it, but if not:
    ```
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    pip install -r requirements.txt
## Log File Analysis

### Description
Based on log files, the program determines the number of successful and failed messages from sensors, analyzes error causes, and generates a report.
### Features
1. **Primary Functionality**:
   - Counts the number of BIG handler messages that successfully passed the test.
   - Determines the total number of successful and failed sensors.
   - Ignores sensors that have ever reported STATE:DD.

2. **Additional Functionality**:
   - Analyzes the errors of sensors that failed the test using flags S_P_1 and S_P_2.
   - Generates a detailed report of errors (Battery, Temperature, Threshold central).

### How to Run
   1. Place the log file (app_2.log) in the same directory as the script.
   2. Run the script from the terminal:
      ```bash
      python do_it_yourself.py

##  Testing the CheckQr Class

### Key Test Cases

#### Positive Scenarios:
1. **Scanning a QR Code Present in the Database**:
   - Validates the correct color assignment based on the QR code length.

#### Negative Scenarios:
1. **Scanning a QR Code Not in the Database**:
   - Ensures proper error handling by the program.
2. **Scanning a QR Code with Undefined Length**:
   - Confirms the send_error method is called with the correct arguments.

#### Additional Tests:
1. **Testing the `send_error` Method**:
   - Verifies that error messages are transmitted correctly.
2. **Testing Successful Device Addition via `can_add_device`**:
   - Ensures the method sends the appropriate message for successful QR scans.


---

### Running Tests

To execute the tests:
   ```bash
   pytest test_name.py

