"""Pick-Up-Tip OT3."""
import argparse
import asyncio

from hardware_testing.opentrons_api import types
from hardware_testing.opentrons_api import helpers_ot3


async def _main(is_simulating: bool, mount: types.OT3Mount, tip_length: int = 40) -> None:
    api = await helpers_ot3.build_async_ot3_hardware_api(
        is_simulating=is_simulating, pipette_left="p1000_single_v3.3"
    )
    # home
    await api.home()
    home_pos = await api.gantry_position(mount)
    tip_pos = home_pos._replace(z=120)
    while True:
        inp = input("\"p\"=pick-up-tip, \"r\"=return-tip, \"j\"=j, \"n\"=new-tip-pos, \"s\"=stop")
        if inp == "p":
            await helpers_ot3.move_to_arched_ot3(api, mount, tip_pos, safe_height=150)
            await api.pick_up_tip(mount, tip_length=tip_length)
        elif inp == "r":
            await helpers_ot3.move_to_arched_ot3(api, mount, tip_pos, safe_height=150)
            await api.drop_tip(mount, home_after=False)
        elif inp == "j":
            await helpers_ot3.jog_mount_ot3(api, mount)
        elif inp == "n":
            tip_pos = await api.gantry_position(mount)
            print(f"found tip position: {tip_pos}")
        elif inp == "s":
            break
        else:
            continue
    # move close to home position
    await helpers_ot3.move_to_arched_ot3(api, mount, home_pos - types.Point(x=-2, y=-2, z=-2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--mount", choices=["left", "right"])
    parser.add_argument("--tip-length", type=int, default=40)
    args = parser.parse_args()
    _mount = types.OT3Mount.LEFT if args.mount == "left" else types.OT3Mount.RIGHT
    asyncio.run(_main(args.simulate, _mount, args.tip_length))
