import re

FILE_PATH = "refs/app_2.log"

def parse_log_file():
    with open(FILE_PATH, "r") as file:
        lines = file.readlines()

    big_handler_ok_count = {}
    failed_devices = {}
    device_messages = {}

    for line in lines:
        match = re.search(r">\s*\'BIG;(\d+);([0-9A-F]+);.*?;(\d{4});.*?;(\d{3});.*?;([0-9A-F]{2});\'", line)
        if match:
            handler, device_id, sp1, sp2, state = match.groups()
            device_id = device_id.upper()

            if device_id not in device_messages:
                device_messages[device_id] = {"ok": 0, "failed": False}

            if state == "02":  # ok
                if not device_messages[device_id]["failed"]:
                    device_messages[device_id]["ok"] += 1

            elif state == "DD":  # failed
                device_messages[device_id]["failed"] = True

                # errors processing
                sp1 = sp1[:-1]
                combined = sp1 + sp2
                pairs = [combined[i:i+2] for i in range(0, len(combined), 2)]
                bin_pairs = [bin(int(pair, 10))[2:].zfill(8) for pair in pairs]
                flags = [binary_pair[4] for binary_pair in bin_pairs]

                errors = []
                if flags[0] == "1":
                    errors.append("Battery device error")
                if flags[1] == "1":
                    errors.append("Temperature device error")
                if flags[2] == "1":
                    errors.append("Threshold central error")

                if not errors:
                    errors = ["Unknown device error"]

                failed_devices[device_id] = errors

    for device_id, stats in device_messages.items():
        if not stats["failed"] and stats["ok"] > 0:
            big_handler_ok_count[device_id] = stats["ok"]

    return device_messages, big_handler_ok_count, failed_devices

def main():
    device_messages, big_handler_ok_count, failed_devices = parse_log_file()

    print(f"All big messages: {len(device_messages)}")
    print(f"Successful big messages: {len(big_handler_ok_count)}")
    print(f"Failed big messages: {len(failed_devices)}\n")

    print("Failed devices:")
    for device_id, errors in failed_devices.items():
        print(f"{device_id}: {errors[0]}")

    print("\nSuccess messages count:")
    for device_id, count in big_handler_ok_count.items():
        print(f"{device_id}: {count}")

if __name__ == "__main__":
    main()
