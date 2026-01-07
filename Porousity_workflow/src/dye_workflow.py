import sys
from robinhood import RobInHood
from robinhood.utils.timer import Timer 
from typing import Union

from datetime import datetime

# datetime object containing current date and time

def prepare_single_sample(sample_number:int, results_directory: str, logname = datetime.now().strftime("%d_%m_%Y")) -> None:
    """
    """

    station = RobInHood(inst_logger = logname, data_path=results_directory)

    #unpacking sample information from sample_dictionary
    sample_number = int(sample_number)

    vial_pos = station.sample_dict[sample_number]['vial']
    liquid_name = station.sample_dict[sample_number]['liquid']
    liquid_volume = station.sample_dict[sample_number]['volume (ml)']*1000 #all dispense steps in uL
    solid_name = station.sample_dict[sample_number]['solid']
    solid_mass = station.sample_dict[sample_number]['mass (mg)']

    
    print(type(solid_name))
    print(type(liquid_name))

    station._logger.info(f"Preparing sample {sample_number} with the following liquid: {liquid_name} and solid: {solid_name}")

    station._logger.info("Moving vial to the quantos")
    station.robot.open_gripper_set_width(0.03)
    station.vial_rack_to_quantos(vial_pos)

    station._logger.info("Adding solid to the sample")

    station.quantos_cartridge_handling_logic(solid_name=solid_name)
    station._logger.info(f"Dispensing {solid_mass} mg of {solid_name}")
    #mass = station.quantos_dosing(solid_mass)
    mass = 100
    station._logger.info(f"Dispensed {mass} mg of {solid_name}")
    station.record_weight(sample_name=solid_name, file_name= sample_number, weight =mass, file_path = results_directory )

    station._logger.info("Moving vial to the liquid handling station")
    station.robot.open_gripper_set_width(0.03)
    station.vial_quantos_to_pump()

    station._logger.info(f"Priming the tubing with {liquid_name}")
    station.hold_position()
    station.pump_prime_dispense_tubing(liquid_name)

    station._logger.info(f"Dispensing {liquid_volume} uL of {liquid_name}")
    station.infuse_position()
    #station.dispense_volume(vol = liquid_volume, chemical=liquid_name)
    station.hold_position()

    station._logger.info("Moving vial to the capper")
    station.vial_pump_to_capper()
    station.cap()

    station._logger.info("Moving vial to the vial rack")
    station.vial_capper_to_rack(vial_pos)
    station._logger.info(f"Sample preparation of sample number: {sample_number} complete")
    return


def move_sample_to_hotplate(sample_number:int, results_directory: str, logname = datetime.now().strftime("%d_%m_%Y") ) -> None:

    
    sample_number = int(sample_number)

    station = RobInHood(inst_logger = logname, data_path=results_directory)
    vial_pos = station.sample_dict[sample_number]['vial']

    

 
    station._logger.info(f"Moving sample {sample_number} to the hotplate")
    station.vial_rack_to_ika(vial_pos, ika_slot_number=vial_pos)

    return

def reaction_timer(results_directory: str, speed:int, time_secs:int, time_mins:int, time_hours:int, logname = datetime.now().strftime("%d_%m_%Y") ):
    
    
    station = RobInHood(inst_logger = logname, data_path=results_directory)
    
    station._logger.info("Setting stirring speed")
    station.ika.set_speed(speed)
    station.ika.start_stirring()
    station._logger.info("Starting Timer")
    clock = Timer()
    clock.set_timer(hours = time_hours, min = time_mins, sec = time_secs)
    clock.start_timer()

    station._logger.info("Stirring Done, turning off stirring")
    station.ika.stop_stirring()

def store_sample(sample_number, results_directory: str, logname = datetime.now().strftime("%d_%m_%Y")) -> None:

    
    station = RobInHood(inst_logger = logname, data_path= results_directory)

    station._logger.info(f"Moving sample {sample_number} to the vial rack")
    
    vial_pos = station.sample_dict[sample_number]['vial']
    station.vial_ika_to_rack(vial_pos)

def filter_sample(results_directory:str, sample_number: int, filtrate_vial: int, cleaning_vial:int, cleaning_solvent:str, 
             filter_time: Union[int, None] = None, logname=datetime.now().strftime("%d_%m_%Y")):
    
    station = RobInHood(inst_logger=logname, data_path=results_directory)
    
    station._logger.info(f"Filtering sample {sample_number}")

    vial_pos = station.sample_dict[sample_number]['vial']
    liquid_volume = station.sample_dict[sample_number]['volume (ml)']*1000 #all dispense steps in uL

    station.filter_sample_collect_filtrate(sample_vial_number= vial_pos, sample_vial_volume=liquid_volume, filtrate_vial_number=filtrate_vial, cleaning_vial_number=cleaning_vial, 
                                           cleaning_solvent=cleaning_solvent, cleaning_solvent_volume=liquid_volume, filter_time=filter_time)
    

def photograph_sample(sample_number:int,filtrate_number:int, results_directory:str, logname=datetime.now().strftime("%d_%m_%Y")):
        """
    Photographs samples and saves them in the specified path
    """
        station=RobInHood(inst_logger = logname, data_path=results_directory)
        
        #Getting the sample information from the sample dictionary from the filtered vial
        sample_number = int(sample_number)
        liquid_name = station.sample_dict[sample_number]["liquid"]
        solid_name = station.sample_dict[sample_number]["solid"]
        
        
        station._logger.info(f"Photographing sample {sample_number} with the following liquid: {liquid_name} and solid: {solid_name}")
        station.vial_rack_to_pump(vial_number=filtrate_number)
        station.open_lightbox()
        station.vial_pump_to_lightbox()
        station.close_lightbox()
        station.light_on()
        station.save_picture_from_lightbox(solid_name=solid_name,dye_name=liquid_name,path=results_directory)
        station.light_off()
        station.open_lightbox()
        station.vial_lightbox_to_pump()
        station.vial_pump_to_rack(vial_number=filtrate_number)
        
        station.close_lightbox()




if __name__ == '__main__':
  
    if sys.argv[1]=='prepare_sample':
        prepare_single_sample(sample_number=int(sys.argv[2]),results_directory=sys.argv[3])
    elif sys.argv[1] == 'stirr_samples':
        reaction_timer(results_directory=sys.argv[2], speed=int(sys.argv[3]), time_secs=int(sys.argv[4]), time_mins=int(sys.argv[5]), time_hours=int(sys.argv[6]))
    elif sys.argv[1] == 'store_sample':
        #has to be in reverse order
        store_sample(sample_number=int(sys.argv[2]), results_directory=sys.argv[3])
    elif sys.argv[1] == 'filter_sample':
        filter_sample(results_directory=sys.argv[2], sample_number=int(sys.argv[3]), filtrate_vial=int(sys.argv[4]), cleaning_vial=int(sys.argv[5]), cleaning_solvent=sys.argv[6])
    elif sys.argv[1] == 'photograph_sample':
        print(sys.argv[3])
        photograph_sample(sample_number=int(sys.argv[2]), filtrate_number=int(sys.argv[3]), results_directory=sys.argv[4])
    elif sys.argv[1] == "sample_rack_to_ika":
        move_sample_to_hotplate(sample_number= sys.argv[2], results_directory=sys.argv[3])
    else:
        print("Not a valid argument.")


    
    




