from dotenv import load_dotenv
load_dotenv(override=True)

from scripts import ai_cam


if __name__ == "__main__" :
    ai_cam.display_processed_frames(speed_engine=True)
    print("All done")