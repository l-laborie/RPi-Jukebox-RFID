import subprocess
import os 
from Reader import Reader


reader = Reader()

# get absolute path of this script
dir_path = os.path.dirname(os.path.realpath(__file__))


print dir_path


while True:
    # reading the card id
    card_id = reader.read_card()
    try:
        # start the player script and pass on the cardid
        subprocess.call([
            dir_path + '/rfid_trigger_play.sh --cardid=' + card_id],
            shell=True)
    except OSError as e:
        print "Execution failed:"
