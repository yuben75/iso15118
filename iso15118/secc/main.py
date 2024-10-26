import asyncio
import logging

import sys
import os

# 動態添加專案根目錄的模組路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../', 'iso15118'))
sys.path.append(project_root)

from iso15118.secc import SECCHandler
from iso15118.secc.controller.interface import ServiceStatus
from iso15118.secc.controller.simulator import SimEVSEController
from iso15118.secc.secc_settings import Config
from iso15118.shared.exificient_exi_codec import ExificientEXICodec

logger = logging.getLogger(__name__)


async def main():
    """
    Entrypoint function that starts the ISO 15118 code running on
    the SECC (Supply Equipment Communication Controller)
    """
    config = Config()
    config.load_envs()
    config.print_settings()

    sim_evse_controller = SimEVSEController()
    await sim_evse_controller.set_status(ServiceStatus.STARTING)
    await SECCHandler(
        exi_codec=ExificientEXICodec(),
        evse_controller=sim_evse_controller,
        config=config,
    ).start(config.iface)


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug("SECC program terminated manually")


if __name__ == "__main__":
    run()
