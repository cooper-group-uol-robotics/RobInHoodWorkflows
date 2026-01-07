import sys
from datetime import datetime
import os
from robinhood import RobInHood
import time

from robinhood.utils.timer import Timer



def prepare_single_sample(sample_number:int, results_directory: str, logname = datetime.now().strftime("%d_%m_%Y")) -> None:
    """
    Prepare a single sample for synthesis.

    Args:
        station (RobInHood): The RobInHood station object.
        sample_number (int): The sample number to prepare.
        results_directory (str): The directory to save the results.
        logname (str): The name of the log file. Defaults to current date and time.

    Returns:
        None
    """


    station = RobInHood(inst_logger = logname, data_path=results_directory)

    print(station.sample_dict)


    #read solids and liquids to dispense from the sample dictionary

   

 
    sample_number = int(sample_number)

    vial_pos = station.sample_dict[sample_number]['vial']
    liquid = station.sample_dict[sample_number]['liquid']
    liquid_volume = station.sample_dict[sample_number]['volume (ml)']
    solid = station.sample_dict[sample_number]['solid']
    solid_mass = station.sample_dict[sample_number]['mass (mg)']

    station._logger.info(f"Preparing sample {sample_number} with the following liquids: {liquid} and solids: {solid}")
    
    station._logger.info("Moving vial to the quantos")
    station.robot.open_gripper_set_width(0.03)
    station.vial_rack_to_quantos(vial_pos)
    

    station._logger.info("Adding solids to the sample")

       
    station.quantos_cartridge_handling_logic(solid_name=solid)


    station._logger.info(f"Dispensing {solid} mg of {solid_mass} to the sample")

    mass = station.quantos_dosing(quantity=solid_mass)

    station.record_weight(sample_name=solid, file_name= sample_number, weight =mass, file_path = results_directory )

   
    station._logger.info("Moving vial to the liquid handling station")
    station.robot.open_gripper_set_width(0.03)
    station.vial_quantos_to_pump()

      
    vol_ul = int(liquid_volume)*1000
    station.hold_position()
    station._logger.info(f"Priming {station.pump.device_name} with {liquid}")
    station.pump_prime_dispense_tubing(chemical=liquid)

      
    station._logger.info(f"Dispensing {vol_ul} ul of {liquid} to the sample")
    station.infuse_position()
    station.dispense_volume(vol=vol_ul, chemical=liquid)
    station.hold_position()

    station._logger.info("Moving vial to the capper")
    
    station.vial_pump_to_capper()
    station.cap()

    station._logger.info("Moving vial to the vial rack")
    station.vial_capper_to_rack(vial_pos)

    station._logger.info(f"Sample preparation of sample number: {sample_number} complete")


def move_sample_to_hotplate(sample_number: int, results_directory: str, logname = datetime.now().strftime("%d_%m_%Y") ) -> None:
    """
    Move samples to the hotplate.

    Args:
        station (RobInHood): The RobInHood station object.
        sample_numbers (list): The list of sample numbers to move.
        results_directory (str): The directory to save the results.

    Returns:
        None
    """

    station = RobInHood(inst_logger = logname, data_path=results_directory)
    vial_pos = station.sample_dict[sample_number]['vial']

 
    station._logger.info(f"Moving sample {sample_number} to the hotplate")
    station.vial_rack_to_ika(vial_pos, ika_slot_number=vial_pos)


def reaction_timer(results_directory: str, time_secs:int, time_mins:int, time_hours:int, logname = datetime.now().strftime("%d_%m_%Y") ):
    
    
    station = RobInHood(inst_logger = logname, data_path=results_directory)
    station._logger.info("Starting Timer")
    clock = Timer()
    clock.set_timer(hours = time_hours, min = time_mins, sec = time_secs)
    clock.start_timer()

    station._logger.info("Heating and Stirring Done, setting hotplate temperature back to RT and turning off stirring")
    station.ika.stop_stirring()
    station.ika.stop_temperature_regulation() 

    

def heat_stirr(temperature:float, speed:int,  results_directory:str, temperature_delta = 3, logname = datetime.now().strftime("%d_%m_%Y") ) -> None:
    """
    Heat and stir samples on the hotplate.

    Args:
        station (RobInHood): The RobInHood station object.
        sample_numbers (list): The list of sample numbers to heat and stir.
        results_directory (str): The directory to save the results.

    Returns:
        None
    """
    station = RobInHood(inst_logger = logname, data_path=results_directory)

    station._logger.info("Heating and stirring samples on the hotplate")
    
    station.ika.set_temperature(temperature=temperature)
    station.ika.set_speed(speed = 500)
    station.ika.start_temperature_regulation()
    station.ika.start_stirring()


    while True:
        measured_temp = station.ika.get_temperature(sensor=0)
        if abs(measured_temp - temperature) <= temperature_delta:
            station._logger.info(f"Temperature of {temperature} reached")
            break
        else: 
            station._logger.info(f"Temperature of {temperature} not reached, current temperature is {measured_temp}")
            time.sleep(5)

  
    #station.ika.stop_all_tasks()

def store_samples_from_hotplate(sample_number: int, results_directory:str, logname = datetime.now().strftime("%d_%m_%Y") ) -> None:
    """
    Store samples from the hotplate.

    Args:
        station (RobInHood): The RobInHood station object.
        sample_numbers (list): The list of sample numbers to store.
        results_directory (str): The directory to save the results.

    Returns:
        None
    """
    
    station = RobInHood(inst_logger = logname, data_path= results_directory)

    station._logger.info(f"Moving sample {sample_number} to the vial rack")
    
    vial_pos = station.sample_dict[sample_number]['vial']
    station.vial_ika_to_rack(vial_pos,vial_pos)

def add_solvent(sample_number: int, wash_solvent:str, wash_amount:float, results_directory:str, logname = datetime.now().strftime("%d_%m_%Y") ) -> None:
    """
    Wash samples.

    Args:
        station (RobInHood): The RobInHood station object.
        sample_numbers (list): The list of sample numbers to wash.
        wash_solvent (str): The solvent to use for washing.
        wash_amount (float): The amount of solvent to use for washing.
        results_directory (str): The directory to save the results.

    Returns:
        None
    """
    
    station = RobInHood(inst_logger= logname, data_path=results_directory)

    station._logger.info(f"Washing sample {sample_number} with {wash_solvent} and {wash_amount} ml")

    vial_pos = station.sample_dict[sample_number]['vial']
  

    station.vial_decap(vial_pos)

    station.pump_prime_dispense_tubing(wash_solvent)

    station.infuse_position()

    station.dispense_volume(vol = float(wash_amount)*1000, chemical= wash_solvent)

    station.hold_position()

    station.vial_pump_to_capper()
    
    station.cap()

    station.vial_capper_to_pump()

    station.vial_pump_to_rack(vial_number=vial_pos)


def wash_filtered_sample(sample_number:int, wash_volume: float, wash_cycles:int, wash_solvent:str, results_directory:str, logname: str = datetime.now().strftime("%d_%m_%Y")) -> None:
    """ Washes the filtered sample with a specified solvent."""

    station = RobInHood(inst_logger=logname, data_path=results_directory)

    station.quantos.close_front_door()
    vial_pos = station.sample_dict[sample_number]['vial']


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

def filter_samples(sample_number: int, cleaning_vial_number:int, cleaning_vial_solvent:str,
                    results_directory:str,logname = datetime.now().strftime("%d_%m_%Y") ) -> None:
    """
    Filter samples.

    Args:
        station (RobInHood): The RobInHood station object.
        sample_numbers (list): The list of sample numbers to filter.
        results_directory (str): The directory to save the results.

    Returns:
        None
    """
    
    station = RobInHood(inst_logger= logname,data_path=results_directory)

    station._logger.info(f"Filtering sample {sample_number}")

    sample_number = int(sample_number)

    vial_pos = station.sample_dict[sample_number]['vial']
    liquid_volume = int(station.sample_dict[sample_number]['volume (ml)'])

    station.filtration_prep(cleaning_vial_number=cleaning_vial_number, cleaning_solvent=cleaning_vial_solvent, cleaning_solvent_volume=liquid_volume*1000), 

    station.vial_decap(vial_pos)

    station.vial_pump_to_rack(vial_number=vial_pos)

    station.just_filter_sample_disgard_filtrate(sample_vial_number=vial_pos, sample_vial_volume= int(liquid_volume)*1000)


def clean_filter(filt_cleaning_solvent:str, filt_cleaning_volume:float, results_directory:str, logname = datetime.now().strftime("%d_%m_%Y") ) -> None:
    """
    Clean the filter.

    Args:
        station (RobInHood): The RobInHood station object.
        filt_cleaning_solvent (str): The solvent to use for cleaning the filter.
        filt_cleaning_volume (float): The volume of solvent to use for cleaning the filter.
        results_directory (str): The directory to save the results.

    Returns:
        None
    """
    
    station = RobInHood(inst_logger=logname, data_path=results_directory)

    filt_cleaning_volume_ul = float(filt_cleaning_volume) * 1000  # Convert from mL to uL
    station._logger.info(f"Cleaning the filter with {filt_cleaning_solvent} and {filt_cleaning_volume_ul} uL")
    station.filter_cleaning_packdown(cleaning_solvent= filt_cleaning_solvent, cleaning_solvent_volume=filt_cleaning_volume_ul)


if __name__ == "__main__":
    if sys.argv[1] == "prepare_samples":
        prepare_single_sample(sample_number = int(sys.argv[2]), results_directory = sys.argv[3])

    elif sys.argv[1] == "samples_to_hotplate":
        move_sample_to_hotplate(sample_number = int(sys.argv[2]), results_directory = sys.argv[3])

    elif sys.argv[1] == "heat_stirr":
        heat_stirr(temperature = float(sys.argv[2]) , speed = int(sys.argv[3]),  results_directory=sys.argv[4])

    elif sys.argv[1] == "store_samples":
        store_samples_from_hotplate(sample_number = int(sys.argv[2]), results_directory = sys.argv[3])
    
    elif sys.argv[1] == "filter_samples":
        filter_samples(sample_number = int(sys.argv[2]), cleaning_vial_number = int(sys.argv[3]), cleaning_vial_solvent = sys.argv[4], 
                         results_directory = sys.argv[5])

    elif sys.argv[1] == "reaction_timer":
        reaction_timer(results_directory=sys.argv[2], time_hours= int(sys.argv[3]), time_mins= int(sys.argv[4]), time_secs= int(sys.argv[5]))

    elif sys.argv[1] == "add_solvent":
        add_solvent(sample_number = int(sys.argv[2]), wash_solvent = sys.argv[3], wash_amount = float(sys.argv[4]), results_directory= sys.argv[5])
    
    elif sys.argv[1] == "wash_filtered_sample":
        wash_filtered_sample(sample_number = int(sys.argv[2]), wash_volume = float(sys.argv[3]), wash_cycles = int(sys.argv[4]), wash_solvent = sys.argv[5], results_directory= sys.argv[6])

    elif sys.argv[1] == "clean_filter":
        clean_filter(filt_cleaning_solvent = sys.argv[2], filt_cleaning_volume = float(sys.argv[3]), results_directory = sys.argv[4])
    else:
        print("Invalid command. Please use one of the following commands:")
        print("1. prepare_samples")
        print("2. samples_to_hotplate")
        print("3. heat_stirr")
        print("4. store_samples")
        print("5. filter_samples")
        print("6. reaction_timer")
        print("7. add_solvent")
        print("8. wash_filtered_sample")