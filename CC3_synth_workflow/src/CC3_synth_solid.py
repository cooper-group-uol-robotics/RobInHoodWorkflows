import sys
from robinhood import RobInHood
from robinhood.utils.timer import Timer 
from typing import Union

from datetime import datetime



def add_solid_aldehyde(vial_pos: int, results_directory: str,solid_name:str, solid_amount:float, logname: str = datetime.now().strftime("%d_%m_%Y")) -> None:

    """ Adds solid aldehyde sample by dispensing the solid into a vial, returns uncapped vial to the rack."""

    station = RobInHood(inst_logger=logname, data_path=results_directory)

    
    
    station._logger.info(f"Preparing sample {vial_pos} with the following solid: {solid_name}")

    station._logger.info("Moving vial to the quantos")
    station.robot.open_gripper_set_width(0.03)
    station.vial_rack_to_quantos(vial_pos)

    station._logger.info("Adding solid to the sample")

    station.quantos_cartridge_handling_logic(solid_name=solid_name)
    station._logger.info(f"Dispensing {solid_amount} mg of {solid_name}")
    mass = station.quantos_dosing(solid_amount)
    station._logger.info(f"Dispensed {mass} mg of {solid_name}")
    station.record_weight(sample_name=solid_name, file_name=vial_pos, weight=mass, file_path=results_directory)

    station._logger.info("Moving vial to the vial rack")
    station.robot.open_gripper_set_width(0.03)
    station.vial_quantos_to_rack(vial_pos)
    
    station._logger.info(f"Solid aldehyde added to sample number: {vial_pos}")

def dispense_solvent(vial_pos: int, results_directory: str, liquid_name: str, liquid_vol:float, logname: str = datetime.now().strftime("%d_%m_%Y")) -> None:
    """ Dispenses solvent into a vial."""

    station = RobInHood(inst_logger=logname, data_path=results_directory)

    
    station._logger.info(f"Preparing sample {vial_pos} with the following liquid: {liquid_name}")

    station._logger.info(f"Priming the tubing with {liquid_name}")
    station.hold_position()
    station.pump_prime_dispense_tubing(liquid_name)
    
    liquid_vol_ul = liquid_vol * 1000  # Convert from mL to uL
    station._logger.info(f"Dispensing {liquid_vol_ul} uL of {liquid_name}")
    
    station.vial_rack_to_pump(vial_pos)
    station.infuse_position()
    station.dispense_volume(vol=liquid_vol_ul, chemical=liquid_name)

    station.hold_position()
    station._logger.info("Moving vial back to the rack")

    station.vial_pump_to_rack(vial_pos)
    station._logger.info(f"{liquid_name} added to sample number: {vial_pos}")

def add_amine_and_cap(vial_pos: int, results_directory: str, liquid_name, liquid_vol, logname: str = datetime.now().strftime("%d_%m_%Y")) -> None:
    """ Adds amine to a sample and caps it."""

    station = RobInHood(inst_logger=logname, data_path=results_directory)

    station._logger.info(f"Preparing sample {vial_pos} with the following liquid: {liquid_name}")
    
    station._logger.info(f"Priming the tubing with {liquid_name}")
    station.hold_position()
    station.pump_prime_dispense_tubing(liquid_name)
    
    liquid_vol_ul = liquid_vol * 1000  # Convert from mL to uL
    station._logger.info(f"Dispensing {liquid_vol_ul} uL of {liquid_name}")
    
    station.vial_rack_to_pump(vial_pos)
    station.infuse_position()
    station.dispense_volume(vol=liquid_vol_ul, chemical=liquid_name)

    station.hold_position()
    station._logger.info("Moving vial back to the capper")

    station.vial_pump_to_capper()  # Check this
    station.cap()

    station._logger.info("Moving vial back to the rack")
    station.vial_capper_to_rack(vial_pos)
    station._logger.info(f"Amine added and sample number: {vial_pos} capped")

def filter_sample(vial_pos: int, liquid_volume: float, cleaning_vial_number:int, cleaning_vial_solvent:str, anti_solvent:str, anti_solvent_vol:float,
                   results_directory:str, logname: str = datetime.now().strftime("%d_%m_%Y")) -> None:
    """ Filters samples using the filter station."""

    station = RobInHood(inst_logger=logname, data_path=results_directory)

    station._logger.info(f"Filtering sample {vial_pos}")

    vial_pos = int(vial_pos)
    liquid_volume_ul = float(liquid_volume)*1000
   

    station.filtration_prep(cleaning_vial_number=cleaning_vial_number, cleaning_solvent=cleaning_vial_solvent, cleaning_solvent_volume=liquid_volume * 1000)

    station.vial_decap(vial_pos)
    
    #adding an antisolvent
    station._logger.info(f"Adding {anti_solvent_vol} ml of {anti_solvent} ")

    station.pump_prime_dispense_tubing(chemical= anti_solvent)

    station.infuse_position()
    
    anti_solvent_vol_ul= float(anti_solvent_vol)*1000
    station.dispense_volume(vol = anti_solvent_vol_ul, chemical= anti_solvent)

    station.hold_position()
    
    station.vial_pump_to_rack(vial_number=vial_pos)

    total_volume = liquid_volume_ul + anti_solvent_vol_ul

    station._logger.info(f"Filtering sample total volume of {total_volume}")

    station.just_filter_sample_disgard_filtrate(sample_vial_number=vial_pos, sample_vial_volume=total_volume)
   

    station._logger.info(f"Sample {vial_pos} filtered")



def wash_filtered_sample(vial_pos:int, wash_volume: float, wash_cycles:int, wash_solvent:str, results_directory:str, logname: str = datetime.now().strftime("%d_%m_%Y")) -> None:
    """ Washes the filtered sample with a specified solvent."""

    station = RobInHood(inst_logger=logname, data_path=results_directory)

    cycle_number = range(wash_cycles)

    for cycle in cycle_number:
        station._logger.info(f"Starting wash cycle {cycle + 1} for sample {vial_pos}")
        station._logger.info(f"Washing the filter with {wash_solvent}")
        station._logger.info(f"Filling the sample vial {vial_pos} with {wash_volume} ml of {wash_solvent}")
        station.hold_position()
        station.pump_prime_dispense_tubing(wash_solvent)
        wash_volume_ul =wash_volume * 1000  # Convert from mL to uL
        station.vial_rack_to_pump(vial_pos)
        station.infuse_position()
        station.dispense_volume(vol=wash_volume_ul, chemical=wash_solvent)
        station.hold_position()
        station.vial_pump_to_rack(vial_number=vial_pos)
        station._logger.info("Moving vial back to the rack")
        station.just_filter_sample_disgard_filtrate(sample_vial_number=vial_pos, sample_vial_volume=wash_volume_ul)

    station._logger.info(f"Sample {vial_pos} washed {wash_cycles} times with {wash_solvent} and returned to the rack")

def clean_filter_station(cleaning_solvent:str, cleaning_solvent_volume:float, results_directory:str, logname: str = datetime.now().strftime("%d_%m_%Y")) -> None:
    """ Cleans the filter station with a specified solvent."""

    station = RobInHood(inst_logger=logname, data_path=results_directory)
    
    cleaning_solvent_volume_ul = cleaning_solvent_volume * 1000  # Convert from mL to uL

    station._logger.info(f"Cleaning the filter station with {cleaning_solvent}")

    station.filter_cleaning_packdown(cleaning_solvent=cleaning_solvent, cleaning_solvent_volume=cleaning_solvent_volume_ul)
    


if __name__ == "__main__":
        # Example usage
        if sys.argv[1] == "add_solid_aldehyde":
            add_solid_aldehyde(vial_pos=int(sys.argv[2]),results_directory= sys.argv[3],solid_name= sys.argv[4], solid_amount= float(sys.argv[5]))
        elif sys.argv[1] == "dispense_solvent":
            dispense_solvent(vial_pos=int(sys.argv[2]), results_directory=sys.argv[3], liquid_name= sys.argv[4], liquid_vol=float(sys.argv[5]))
        elif sys.argv[1] == "add_amine_and_cap":
            add_amine_and_cap(vial_pos=int(sys.argv[2]), results_directory=sys.argv[3],liquid_name= sys.argv[4], liquid_vol= float(sys.argv[5]))
        elif sys.argv[1] == "filter_sample":
            filter_sample(vial_pos=int(sys.argv[2]), liquid_volume=float(sys.argv[3]), cleaning_vial_number=int(sys.argv[4]),
                           cleaning_vial_solvent=str(sys.argv[5]), anti_solvent=sys.argv[6], anti_solvent_vol= sys.argv[7], results_directory=sys.argv[8])
        elif sys.argv[1] == "wash_filtered_sample":
            wash_filtered_sample(vial_pos=int(sys.argv[2]), wash_volume=float(sys.argv[3]), wash_cycles=int(sys.argv[4]),
                                 wash_solvent=str(sys.argv[5]), results_directory=sys.argv[6])
        elif sys.argv[1] == "clean_filter_station":
            clean_filter_station(cleaning_solvent=sys.argv[2], 
                                 cleaning_solvent_volume=float(sys.argv[3]), results_directory=sys.argv[4])
    
        else:
            print("Invalid command. Use 'add_solid_aldehyde', 'dispense_solvent','add_amine_and_cap', 'filter_sample', 'wash_filtered_sample', 'clean_filter_station'.")