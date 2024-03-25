import time


def process_image_model(image_guid: str):
    time.sleep(3)
    print("Hello world " + image_guid)
    return "Result after 3 seconds"