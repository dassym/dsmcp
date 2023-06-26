from pyocd.core.helpers import ConnectHelper
from pyocd.flash.file_programmer import FileProgrammer

import logging
logging.basicConfig(level=logging.INFO)

with ConnectHelper.session_with_chosen_probe() as session:

    board = session.board
    target = board.target
    flash = target.memory_map.get_boot_memory()

    # Load firmware into device.
    FileProgrammer(session).program("/home/fv/Dassym/firm/MB-30_v5_dassym-direct-electric_v1.55_full.bin")

    # Reset, run.
    target.reset_and_halt()