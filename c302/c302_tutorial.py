import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import c302
import neuroml.writers as writers
import numpy as np

'''
PYTHON 2 SCRIPT TO RUN A c302 MODEL

In this file you will find a commented layout of how to code a python script to run a neuronal simulation in c302.
Note that this script will not produce any network, it is only presented as a tutorial.
'''

range_incl = lambda start, end:range(start, end + 1) # Produces a list from start to end


def setup(parameter_set,
          generate=False,
          duration=10000, # Change here the duration of the simulation in ms
          dt=0.05, # Time step 
          target_directory='examples',
          data_reader="UpdatedSpreadsheetDataReader2",
          param_overrides={},
          verbose=True,
          config_param_overrides={}):

    # Import this from the defined parameters. 
    exec ('from parameters_%s import ParameterisedModel' % parameter_set, globals())
    params = ParameterisedModel()
    
    #*******************************************
    # 1. DEFINE THE ELEMENTS TO SIMULATE 
    #*******************************************
    
    cells = [] 
    # Neurons to include in the simulation (e.g. cells = ['AVBL', 'DB1'])
        
    muscles_to_include = [] 
    # Muscles to include in the simulation (e.g. muscles_to_include = ['MDL07'], muscles = True for all the muscles)

    cells_to_stimulate = [] 
    # Neurons to stimulate
    # This is used to stimulate the neurons and muscles, I use a different method to stimulate however.


    cells_to_plot = cells
    # Neurons to include in the plot (e.g. cells_to_plot = ['DB1'])
    # If you do not want to plot all the neurons defined, change cells by the only neurons you want plotted.
    
    reference = "c302_%s_tutorial" % parameter_set
    # Reference for the subsequent generated NeuroML files
    # (Make sure this corresponds with the script name: c302_NAME.py --> reference = "c302_%s_NAME" % parameter_set)


    
    #*******************************************
    # 2. DEFINE THE NETWORK CONNECTIONS 
    #*******************************************
    
    conns_to_include = []
    # Only connections to include
    # By default, c302 takes all the connections from the connectome. 
    # If you only want some specific connections, specify them here.
    
    conns_to_exclude = [
        
        'DB1-DB2', # Exclude the chemical synapse from DB1 to DB2
        'DB1-DB2_GJ', # Exclude the gap junction from DB1 to DB2
        'DB2-DB1_GJ',
        # Note that gap junctions need to be excluded in both ways
        
        r'^AVB.-DB\d+$', # Regular expression to exclude AVBR and AVBL synapses to DB1, DB2... DB7
        
    ]    
    # Connections to exclude or 'ablate' 
    # I included some examples of connections to be excluded. 
    # Search on how to use Regular Expressions in python. 
    
    conn_polarity_override = {
        
        r'^VB\d+-VB\d+$': 'inh', #Change any VB# to VB# synapse to inhibitory
        r'^DD\d+-DD\d+$': 'exc', #Change any DD# to DD# synapse to excitatory
        
    }
    # Change the polarity of chemical synapses
    # c302 takes as inhibitory those synapses coming from GABAergic neurons.
    
    conn_number_override = {
        '^.+-.+$': 1,
    }
    # Changed the number of synapses between neurons all to 1.
    
    
    
    #*******************************************
    # 3. ADD INPUTS TO NEURONS AND MUSCLES 
    #*******************************************
    # (This is where I define the inputs, instead of using cells_to_stimulate)
    
    input_list = [] # Step current input
    sine_input_list = [] # Sinusoidal input
    ramp_input_list = [] # Ramp inputs are still under development
    
    input_list.append((neuron, start, duration, amplitude))
    # Add a step input to a neuron, at a given time, with a duration and intensity. 
    # This can also be used to stimulate muscles!
    # (e.g. input_list.append(('AVBL', '0ms', '4000ms', '15pA')))
    
    sine_input_list.append((neuron, start, duration, peak_amplitude, period)) 
    # Add a step input to a neuron, at a given time, with a duration and intensity. 
    # This can also be used to stimulate muscles!
    # (e.g. sine_input_list.append(('DB1', '0ms', '5000ms', '1.5pA', '800ms')) )
    
    config_param_overrides['input'] = input_list
    
    
    
    
    #*******************************************
    # 4. OVERRIDE CERTAIN PARAMETERS  
    #*******************************************

    param_overrides = {
        
        # Symmetrical Gap junctions
        'mirrored_elec_conn_params': {
            
            #r'^AVB._to_AVB._GJ$_elec_syn_gbase': '0.001 nS',
            
        },
        
        # Change the initial membrane potential
        'initial_memb_pot': '-50 mV',
        
        # Here, any parameters found in the Parameters_#.py can be changed and specified for this specific simulation.
    }
    

    nml_doc = None
    
    # Create the NeuroML file of the network using c302 functions. 
    if generate:
        nml_doc = c302.generate(reference,
                                params,
                                cells=cells,
                                cells_to_plot=cells_to_plot,
                                cells_to_stimulate=cells_to_stimulate,
                                conns_to_include=conns_to_include,
                                conns_to_exclude=conns_to_exclude,
                                conn_polarity_override=conn_polarity_override,
                                conn_number_override=conn_number_override,
                                muscles_to_include=muscles_to_include,
                                duration=duration,
                                dt=dt,
                                target_directory=target_directory,
                                data_reader=data_reader,
                                param_overrides=param_overrides,
                                verbose=verbose)

        for stim_input in input_list:
            cell, start, dur, current = stim_input
            c302.add_new_input(nml_doc, cell, start, dur, current, params)
        
        for sine_stim_input in sine_input_list:
            cell, delay, dur, amp, period = sine_stim_input
            c302.add_new_sinusoidal_input(nml_doc, cell, delay, dur, amp, period, params)
        
        for ramp_stim_input in ramp_input_list:
            cell, delay, dur, start_amp, finish_amp, base_amp = ramp_stim_input
            c302.add_new_ramp_input(nml_doc, cell, delay, dur, start_amp, finish_amp, base_amp, params)
        
        nml_file = target_directory + '/' + reference + '.net.nml'
        writers.NeuroMLWriter.write(nml_doc, nml_file)  # Write over network file written above...

        c302.print_("(Re)written network file to: " + nml_file)


    return cells, cells_to_stimulate, params, muscles_to_include, nml_doc


'''
When the c302_tutorial.py is run with python, it starts this condition __name__ == '__main__'
Running this in the terminal can have two arguments:
1. The first one states the parameter set (if not stated it is C2)
2. The second one states the data reader (if not stated it is UpdatedSpreadsheetDataReader2)
    (The data reader reads the connectome, structural information ... )
'''
if __name__ == '__main__':
    parameter_set = sys.argv[1] if len(sys.argv) == 2 else 'C2'
    data_reader = sys.argv[2] if len(sys.argv) == 3 else 'UpdatedSpreadsheetDataReader2'

    setup(parameter_set, generate=True, data_reader=data_reader) 
    # Call the setup function to create the NeuroML file with all the specifications we made above.
