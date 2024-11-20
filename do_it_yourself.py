def read_file_lines(file_path):
    """
    Reads all lines from a file and returns a list of lines.
    """
    try:
        with open(file_path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except IOError:
        print(f"Error: Unable to read file {file_path}.")
        return []


def parse_log_line(line):
    """
    Parses a log file string and returns the separated parts in a dictionary.
    """
    parts = line.strip().split(";")
    return {
        "handler": parts[1] if len(parts) > 1 else None,
        "sensor_id": parts[2] if len(parts) > 2 else None,
        "state": parts[-2] if len(parts) > 2 else None,
        "sp1": parts[6][:-1] if len(parts) > 6 else None,
        "sp2": parts[13] if len(parts) > 13 else None,
    }


def analyze_logs(file_logs_path):
    """
    Analyzes the log file, determines the number of successful and failed sensors.
    """
    successful_devices = {}
    failed_devices = set()

    lines = read_file_lines(file_logs_path)
    for line in lines:
        if "BIG" not in line:
            continue

        log_data = parse_log_line(line)
        sensor_id = log_data["sensor_id"]
        state = log_data["state"]

        if state == "02":
            successful_devices[sensor_id] = (
                    successful_devices.get(sensor_id, 0) + 1
            )
        elif state == "DD":
            failed_devices.add(sensor_id)

    successful_devices = {
        sensor_id: count
        for sensor_id, count in successful_devices.items()
        if sensor_id not in failed_devices
    }

    successful_sensor_count = len(successful_devices)
    failed_sensor_count = len(failed_devices)

    print(f"All big messages: {successful_sensor_count + failed_sensor_count}")
    print(f"Successful big messages: {successful_sensor_count}")
    print(f"Failed big messages: {failed_sensor_count}")
    print("Success messages count:")
    for sensor_id, count in successful_devices.items():
        print(f"{sensor_id}: {count}")

    return successful_devices, failed_devices


def analyze_failed_sensors(file_logs_path, failed_devices):
    """
    Analyzes sensors with 'DD' status and displays error details.
    """
    error_messages = {
        1: "Battery device error",
        2: "Temperature device error",
        3: "Threshold central error",
    }

    lines = read_file_lines(file_logs_path)
    for line in lines:
        if "BIG" not in line or "DD" not in line:
            continue

        log_data = parse_log_line(line)
        sensor_id = log_data["sensor_id"]

        if sensor_id not in failed_devices:
            continue

        sp1 = log_data["sp1"]
        sp2 = log_data["sp2"]

        if not sp1 or not sp2:
            print(f"{sensor_id}: Incomplete data")
            continue

        combined_value = sp1 + sp2
        grouped_values = [
            combined_value[i:i + 2] for i in range(0, len(combined_value), 2)
        ]
        binary_values = [
            bin(int(value))[2:].zfill(8) for value in grouped_values
        ]
        flags = [binary_value[4] for binary_value in binary_values]

        error_codes = [
            index + 1 for index, flag in enumerate(flags) if flag == "1"
        ]
        if error_codes:
            error_output = ", ".join(
                [error_messages[code] for code in error_codes]
            )
            print(f"{sensor_id}: {error_output}")
        else:
            print(f"{sensor_id}: Unknown device error")


file_path = "app_2.log"


successful_test_devices, failed_test_devices = analyze_logs(file_path)
analyze_failed_sensors(file_path, failed_test_devices)
