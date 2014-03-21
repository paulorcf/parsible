import logging


def process_api(result):
    """
    Only a test output the entire list.
    This method is automatic call after a successful parser.
    """
    if 'status' in result.keys():
        for k in result.iterkeys():
            logging.debug(k, result[k])
            print("%s = %s" % (k, result[k]))
