import re
import logging


def parse_libxl(line):
    """
    This parser try parser only details information about libxl events.
        Example: libxl: debug: libxl.c:1043:domain_death_xswatch_callback:  exists shutdown_reported=0 dominf.flags=10004

        They extract this information:
            status      exists
            libname     libxl: (extract :) -> libxl
            loglevel    debug: (extract :) -> debug
            dominf      dominf.flags=10004 (extract :) -> 10004
            d_callback  libxl.c:1043:domain_death_xswatch_callback: (extract :) -> libxl.c:1043:domain_death_xswatch_callback
            report      shutdown_reported=0 (extract into 2 new fields):
                report_name shutdown
                report_id   0
            More information see:
    """
    line = line.strip()
    regex = re.compile("(?P<libname>[\w\S]+)\s(?P<loglevel>[\w\S]+)\s(?P<d_callback>[\w\S]+)\s\s(?P<status>[\w\S]+)\s(?P<report>[\w\S]+)\s(?P<dominf>[\w\S]+)")
    r = regex.search(line)
    result_set = {}
    if r:
        try:
            result_set["status"] = r.group("status")
            logging.debug("Get status, OK!")

            result_set["libname"] = r.group("libname")[:-1]  # extract : from str
            logging.debug("Get libname, OK!")

            result_set["loglevel"] = r.group("loglevel")[:-1]
            logging.debug("Get loglevel, OK!")

            result_set["dominf"] = (r.group("dominf").split("=")[1])  # TODO: check consistency
            logging.debug("Get dominf, OK!")

            result_set["d_callback"] = r.group("d_callback")[:-1]
            logging.debug("Get d_callback, OK!")

            # Split to get report information ID and Name
            lreport = r.group("report").split("=")
            logging.debug("Get report, OK!")

            result_set["report_id"] = lreport[1]
            logging.debug("Get report_id, OK!")

            result_set["report_name"] = lreport[0].split("_")[0]
            logging.debug("Get report_name, OK!")

        except IndexError:
            logging.error("Unable parser information in libxl, some regex group missing")

    else:
        logging.debug("Not value found on regex")

    return result_set




