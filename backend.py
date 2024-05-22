import pygame
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging




class Backend:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            # Initialize pygame mixer
            pygame.mixer.init()
            # Initialize schedule storage
            self.schedules = []

    def add_schedule(self, announcement, date, time, repeat, file_path):
        # Combine date and time strings into a single datetime object
        dt_string = f"{date} {time}"
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")

        # Get the current timestamp
        timestamp = datetime.now()

        # Schedule the job using the background scheduler
        scheduler.add_job(self.schedule_job, 'date', run_date=dt,
                          args=(announcement, repeat, file_path))

        # Store the values in a data structure
        schedule_data = {
            'announcement': announcement,
            'date': date,
            'schedule_time': time,
            'repeat': repeat,
            'file_path': file_path,
            'timestamp': timestamp
        }
        self.schedules.append(schedule_data)

        # Log the schedule details
        logger.info("Scheduled Announcement: %s | Scheduled Date: %s | Scheduled Time: %s | Repeat: %s | Sound File Path: %s",
                    announcement, date, time, repeat, file_path)


    def schedule_job(self, announcement, repeat, file_path):
        try:
            # Log the scheduled time and sound file path
            logger.debug("Scheduled Time: %s | Sound File Path: %s", datetime.now(), file_path)

            # Check if the announcement still exists in the schedules list
            if any(schedule['announcement'] == announcement for schedule in self.schedules):
                # Play the sound
                self.play_sound(file_path)
            else:
                # Announcement was deleted, so skip playing the sound
                logger.info("Skipped deleted announcement: %s", announcement)
        except Exception as e:
            # Log any errors that occur
            logger.exception("An error occurred during the scheduled job.")

    def play_sound(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def __del__(self):
        # Disconnect from MongoDB when the object is destroyed
        pygame.mixer.quit()



# Create a backend instance
backend = Backend()

# Create a background scheduler
scheduler = BackgroundScheduler()

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the logger's level to INFO

# Create a file handler and set the log file path
log_file = "backend.log"
file_handler = logging.FileHandler(log_file, mode='a')  # Set mode to 'a' for append

# Disable the stream output for the file handler
file_handler.stream = None

# Create a formatter and set the format for log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Add your scheduled announcements here using backend.add_schedule()

# Start the scheduler
scheduler.start()
