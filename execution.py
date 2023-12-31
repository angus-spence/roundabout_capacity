from modules_python import *

CALIBRATION = False
PROFILING = False

geometry = [3, 6, 30, 20, 60, 40]

def main(geometry):
    io = Data_Input()    
    # Define worksheets and location references for inputs
    app, wb, ctrl, odin, loc_dict = io.main()

    # Iterate through each parameter to parse values and return checks
    geometry = []
    for param in ["v", "e", "l", "r", "icd", "phi"]:
        geometry.append(io.import_params(ctrl, param, loc_dict)) 

    od, arms = io.import_od(ctrl, odin)

    od_builder = OD_Eval(od_type=Flow_Type.RANDOM)
    od = od_builder.rand_od_builder(arms=5)
    if PROFILING == True:
        profiler = Profiler(profile_type=Profiles.ONEHOUR)
        od = profiler.one_hour(od, sigma=1, period=1, periods= 4, graph=False)
    if CALIBRATION == True:
        model_calibration = Calibration(
            calibration_type = Calibrations.INTERCEPT,
            calibration_method = Calibration_Target.PCU,
            rfc=[],
            calibration_variables=[],
            calibration_targets=[]
            )
        capacity = model_calibration()
    model = Capacity_Eval(*geometry, circulatory_flow=od_builder.Qc(arm_index=1, od=od))
    arm_capacity = od_builder.Qe_stack(od)[0] / model.compute()
    print(f'RFC: {round(arm_capacity,3)}')
    io.print_out(app, wb, ctrl, arm_capacity)

if __name__ == "__main__":
    main(geometry=geometry)