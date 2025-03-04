import re

FILE_PATH = "refs/app_2.log"

def parse_log_file():
    with open(FILE_PATH, "r") as file:
        lines = file.readlines()

    big_handler_ok_count = {}
    failed_devices = {}
    total_big_messages = 0

    for line in lines:
        match = re.search(r">\s*\'BIG;(\d+);([0-9A-F]+);.*;([0-9A-F]{2});\'", line)
        if match:
            total_big_messages += 1
            handler, device_id, state = match.groups()
            if state == "02":  # ok
                if device_id not in big_handler_ok_count:
                    big_handler_ok_count[device_id] = 0
                big_handler_ok_count[device_id] += 1
            elif state == "DD":  # fail
                sp1_match = re.search(r";(\d{4});", line)
                sp2_match = re.search(r";(\d{3});", line)
                if sp1_match and sp2_match:
                    sp1 = sp1_match.group(1)[:-1]
                    sp2 = sp2_match.group(1)
                    combined = sp1 + sp2
                    pairs = [combined[i:i+2] for i in range(0, len(combined), 2)]
                    bin_pairs = [bin(int(pair))[2:].zfill(8) for pair in pairs]
                    flags = [binary_pair[4] for binary_pair in bin_pairs]
                    errors = []
                    if flags[0] == "1":
                        errors.append("Battery device error")
                    if flags[1] == "1":
                        errors.append("Temperature device error")
                    if flags[2] == "1":
                        errors.append("Threshold central error")
                    failed_devices[device_id] = errors if errors else ["Unknown device error"]

    return total_big_messages, big_handler_ok_count, failed_devices


def main():
    total_big_messages, big_handler_ok_count, failed_devices = parse_log_file()

    print(f"All big messages: {len(big_handler_ok_count)}")
    print(f"Successful big messages: {len(big_handler_ok_count) - len(failed_devices)}")
    print(f"Failed big messages: {len(failed_devices)}\n")

    for device_id, errors in failed_devices.items():
        print(f"{device_id}: {errors[0]}")

    print("\nSuccess messages count:")
    for device_id, count in big_handler_ok_count.items():
        print(f"{device_id}: {count}")

if __name__ == "__main__":
    main()
