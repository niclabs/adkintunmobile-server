from config import Files
from logging.handlers import RotatingFileHandler
import os
import logging

reportLogger = logging.getLogger(__name__)

log_folder = Files.LOGS_FOLDER
log_filename = Files.REPORT_GENERATOR_LOG_FILE
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

file_handler = RotatingFileHandler(log_folder + "/" + log_filename, maxBytes=50 * 1024 * 1024)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
reportLogger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
reportLogger.addHandler(file_handler)
reportLogger.info("Report Generator log start")

from app.report import antenna_signal_report_generation
from app.report import general_report_generation
from app.report import antenna_network_report_generation
from app.report import application_report_generation
from app.report import reports_generation
from app.report import views

