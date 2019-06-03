import os
import time
import subprocess

import discoveryservice
import settings
import irc
import log
import tools


def main():
    if os.path.isfile('UPDATE'):
        os.remove('UPDATE')
    if os.system('service rsync status') != 0:
        print('rsync not running; attempting to start')
        try:
            os.system('service rsync start')
        except OSError:
            print('failed to start rsync service')
            os.system('service rsync status')
    settings.init()
    settings.logger = log.Log(settings.log_file_name)
    settings.logger.daemon = True
    settings.logger.start()
    settings.logger.log('Starting NewsGrabber')

    tools.create_dir(settings.dir_assigned_services)

    if not os.path.isfile(settings.target):
        settings.logger.log("Please add one or more discovery rsync targets to file '{target}'".format(target=settings.target), 'ERROR')

    settings.irc_bot = irc.IRC()
    settings.irc_bot.daemon = True
    settings.irc_bot.start()
    time.sleep(30)
    settings.upload = discoveryservice.Upload()
    settings.upload.daemon = True
    settings.upload.start()
    settings.run_services = discoveryservice.RunServices()
    settings.run_services.daemon = True
    settings.run_services.start()
    
    while settings.running:
        if os.path.isfile('STOP'):
            os.remove('STOP')
            open('UPDATE', 'w').close()
            break
        time.sleep(1)

if __name__ == '__main__':
    main()
