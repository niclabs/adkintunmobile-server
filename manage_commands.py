from flask_script import Command, Option

from app import db, application


class Geolocalization(Command):
    option_list = (
        Option('--antennas', '-a', dest='antennas'),
    )

    def run(self, antennas=1000):
        # parameters validation
        try:
            antennas = int(antennas)
        except:
            print("Antennas must be a number")
            return

        if antennas < 0:
            print("Antennas must be a positive number")
            return

        from app.data.antennas_geolocalization import update_antennas_localization

        geolocated_antennas = update_antennas_localization(max_number_of_queries=antennas)
        application.logger.info("New geolocated antennas: " + str(geolocated_antennas))
        print("New geolocated antennas:" + str(geolocated_antennas))


class ReportsGeneration(Command):
    option_list = (
        Option('--month', '-m', dest='month'),
        Option('--year', '-y', dest='year'),
    )

    def run(self, month=None, year=None):
        # parameters validation
        if month:
            try:
                month = int(month)
            except:
                print("Month must be a number")
                return

        if year:
            try:
                year = int(year)
            except:
                print("Year must be a number")
                return

        from app.report.reports_generation import monthly_reports_generation
        from app.report import reportLogger
        monthly_reports_generation(month, year)
        reportLogger.info("Reports have been generated")



class Test(Command):
    def run(self):
        import unittest
        testmodules = [
            "tests",
        ]

        suite = unittest.TestSuite()

        for t in testmodules:
            try:
                # If the module defines a suite() function, call it to get the suite.
                mod = __import__(t, globals(), locals(), ["suite"])
                suitefn = getattr(mod, "suite")
                suite.addTest(suitefn())
            except (ImportError, AttributeError):
                # else, just load all the test cases from the module.
                suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

        unittest.TextTestRunner(verbosity=2).run(suite)


from app.data.populate_methods import initial_populate


class Populate(Command):
    def run(self):
        initial_populate()


def delete_db():
    db.drop_all(bind=None)
