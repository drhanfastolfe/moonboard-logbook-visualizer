from dataclasses import dataclass

@dataclass
class MoonboardSetup:
    setup_id: str
    configuration: str
    setup_name: str

MOONBOARD_SETUPS = [
    MoonboardSetup(setup_id="1", configuration="2", setup_name="2016-25"),
    MoonboardSetup(setup_id="1", configuration="3", setup_name="2016-40"),
    MoonboardSetup(setup_id="15", configuration="1", setup_name="2017-40"),
    MoonboardSetup(setup_id="15", configuration="2", setup_name="2017-25"),
    MoonboardSetup(setup_id="17", configuration="1", setup_name="2019-40"),
    MoonboardSetup(setup_id="17", configuration="2", setup_name="2019-25"),
    MoonboardSetup(setup_id="19", configuration="1", setup_name="2020-40"),
    MoonboardSetup(setup_id="21", configuration="2", setup_name="2024-25"),
    MoonboardSetup(setup_id="21", configuration="3", setup_name="2024-40"),
]