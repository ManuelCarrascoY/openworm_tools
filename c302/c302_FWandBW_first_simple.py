import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import c302
import neuroml.writers as writers

range_incl = lambda start, end:range(start, end + 1)

def setup(parameter_set,
          generate=False,
          duration=16000,
          dt=0.05,
          target_directory='examples',
          data_reader="UpdatedSpreadsheetDataReader2",
          param_overrides={},
          verbose=True,
          config_param_overrides={}):

    exec ('from parameters_%s import ParameterisedModel' % parameter_set, globals())
    params = ParameterisedModel()
    
    #'''
    units_start = 1
    units_end = 1
    VA_motors = ["VA%s" % c for c in range_incl(units_start, units_end)]
    VB_motors = ["VB%s" % c for c in range_incl(units_start, units_end)]
    DA_motors = ["DA%s" % c for c in range_incl(units_start, units_end)]
    DB_motors = ["DB%s" % c for c in range_incl(units_start, units_end)]
    DD_motors = ["DD%s" % c for c in range_incl(units_start, units_end)]
    VD_motors = ["VD%s" % c for c in range_incl(units_start, units_end)]
    AS_motors = ["AS%s" % c for c in range_incl(units_start, units_end)] 
    #'''
    '''
    VA_motors = ["VA%s" % c for c in range_incl(1, 2)]
    VB_motors = ["VB%s" % c for c in range_incl(1, 2)]
    DA_motors = ["DA%s" % c for c in range_incl(1, 2)]
    DB_motors = ["DB%s" % c for c in range_incl(1, 1)]
    # DD_motors = ["DD%s" % c for c in range_incl(units_start, units_end)]
    VD_motors = ["VD%s" % c for c in range_incl(1, 2)]
    AS_motors = ["AS%s" % c for c in range_incl(1, 2)] 
    #'''
    motors = list(VA_motors + VB_motors + AS_motors + DA_motors + DB_motors + VD_motors + DD_motors)
    motors = ['DB1','DA1','VB1','VA1']
    
    inters = ['AVBL', 'AVBR', 'AVAL', 'AVAR']

    cells = list(motors + inters)

    
    
    muscles_to_include = []

    cells_to_stimulate = []

    cells_to_plot = cells
    reference = "c302_%s_FWandBW_first_simple" % parameter_set


    conns_to_include = [
        
    ]
    conns_to_exclude = [
        
        r'^.A\d+-.B\d+_GJ$',
        r'^.B\d+-.A\d+_GJ$',
        r'^.A\d+-.B\d+$',
        r'^.B\d+-.A\d+$',
        
        'VB2-VB4_GJ',
        'VB4-VB2_GJ',
        
        
        #########################################
        # Remove unwanted interneuron connections
        #########################################
        
        # Disconnect the AVA and AVB interneurons
        r'^AVB.-AVA.$',
        r'^AVA.-AVB.$',
        r'^AVB.-AVA._GJ$',
        r'^AVA.-AVB._GJ$',
        
        # Disconnect chemical stimulation from AVA and AVB
        r'^AVB.-.A\d+$', 
        r'^AVB.-.B\d+$',
        r'^AVB.-.D\d+$',
        r'^AVB.-AS\d+$',
        r'^AVA.-.A\d+$',
        r'^AVA.-.B\d+$',
        r'^AVA.-.D\d+$',
        r'^AVA.-AS\d+$',
        
        # Disconnect AVA and AVB gap junctions not pressent. 
        r'^AVB.-.A\d+_GJ$',
        r'^AVB.-AS\d+_GJ$',
        r'^AVB.-.D\d+_GJ$',
        
        r'^AVA.-.B\d+_GJ$',
        r'^AVA.-AS\d+_GJ$',
        r'^AVA.-.D\d+_GJ$',
        
        # Disconnect feedback GJ into AVA and AVB. 
        
        r'^..\d+-AV.._GJ$',
        
        
        #########################################################
        # Remove connections not present in Haspel and O'Donovan
        #########################################################
        
        #'''
        r'^AS\d+-.B\d+$',
        r'^AS\d+-VA\d+$',
        r'^AS\d+-DD\d+$',
        r'^AS\d+-..\d+_GJ$',
        r'^..\d+-AS\d+_GJ$',
        
        r'^DA\d+-AS\d+$',
        r'^DA\d+-DD\d+$',
        r'^DA\d+-VB\d+$',
        r'^DA\d+-VA\d+$',
        r'^DA\d+-AS\d+$',
        r'^DA\d+-.B\d+_GJ$',
        r'^DA\d+-.D\d+_GJ$',
        r'^.B\d+-DA\d+_GJ$',
        r'^.D\d+-DA\d+_GJ$',
        
        r'^DB\d+-.A\d+$',
        r'^DB\d+-VB\d+$',
        r'^DB\d+-.A\d+_GJ$',
        r'^DB\d+-.D\d+_GJ$',
        r'^DB\d+-VB\d+_GJ$',
        r'^.A\d+-DB\d+_GJ$',
        r'^.D\d+-DB\d+_GJ$',
        r'^VB\d+-DB\d+_GJ$',
        
        r'^DD\d+-..\d+$',
        r'^DD\d+-VD\d+_GJ$',
        r'^DD\d+-.B\d+_GJ$',
        r'^DD\d+-.A\d+_GJ$',
        r'^VD\d+-DD\d+_GJ$',
        r'^.B\d+-DD\d+_GJ$',
        r'^.A\d+-DD\d+_GJ$',
        
        r'^VD\d+-D.\d+$',
        r'^VD\d+-AS\d+$',
        r'^VD\d+-VB\d+_GJ$',
        r'^VB\d+-VD\d+_GJ$',
        
        r'^VB\d+-DB\d+$',
        r'^VB\d+-.A\d+$',
        r'^VB\d+-AS\d+$',
        r'^VB\d+-VD\d+$',
        r'^VB\d+-VA\d+_GJ$',
        r'^VA\d+-VB\d+_GJ$',
        
        r'^VA\d+-.B\d+$',
        r'^VA\d+-DA\d+$',
        r'^VA\d+-AS\d+$',
        
        ###############################################
        # Remove connections going forward in DA and VA
        ###############################################
        
        #Forward connections in DA-VA
        'DA3-DA4',
        'DA2-DA3',
        'VA2-VA3',
        'VA3-VA4',
        'VA5-VA6',
        'DA9-VA12',
        'VA12-DA8',
        'VA12-DA9',
        'VA1-DA2',
        
        
        #'''
    ]    
    conn_polarity_override = {
        
        #Inhibitory in Olivares
        
        r'^AS\d+-VD\d+$': 'inh',
        r'^DB\d+-AS\d+$': 'inh',
        r'^DB\d+-VD\d+$': 'inh',
        r'^VD\d+-VA\d+$': 'inh',
        r'^VA\d+-VD\d+$': 'inh',
        
        #Excitatory in Olivares
        
        r'^VD\d+-VB\d+$': 'exc',
        
        #Inhibitory in LUNG
        
        #r'^DB\d+-DD\d+$': 'inh',
        #r'^VB\d+-VD\d+$': 'inh',
                
    }
    
    conn_polarity_override = {
        #### NEW CIRCUIT ####
        r'^VA\d+-VD\d+$': 'inh',
        
        r'^DA\d+-DD\d+$': 'inh',
        r'^AS\d+-DD\d+$': 'inh',
        r'^DB\d+-DD\d+$': 'inh',
        
        r'^AS\d+-VD\d+$': 'inh',
        #VD-DD, VD-VA and VD-VB are already inhibitory
        
    }
    
    #conn_polarity_override = {}
    
    conn_number_override = {
        '^.+-.+$': 1,
    }
    
    #*********
    # INPUTS
    #*********
    
    input_list = []
    sine_input_list = []
    ramp_input_list = []
    
    #*************************
    # Interneuron STIMULATION
    #*************************
    
    #Stimulations for the long nice plots
    #'''
    input_list.append(('AVBL', '0ms', '4000ms', '15pA'))
    input_list.append(('AVBR', '0ms', '4000ms', '15pA'))
    input_list.append(('AVAL', '4000ms', '8000ms', '15pA'))
    input_list.append(('AVAR', '4000ms', '8000ms', '15pA'))
    input_list.append(('AVBL', '12000ms', '4000ms', '15pA'))
    input_list.append(('AVBR', '12000ms', '4000ms', '15pA'))
    #'''
    
    
    #*************************
    # DB1 and VB1 STIMULATION
    #*************************

    # OPTION A: Square steps Input
    #'''
    d_v_delay = 400

    start = 190
    motor_dur = '250ms'
    amplitude = 1.5
    
    input_list.append(('DB1', '%sms'%(start), motor_dur, '%spA' %amplitude))
    input_list.append(('VB1', '%sms'%(start+d_v_delay), motor_dur, '%spA' %amplitude))
    
    input_list.append(('DA1', '%sms'%(start), motor_dur, '%spA' %amplitude))
    input_list.append(('VA1', '%sms'%(start+d_v_delay), motor_dur, '%spA' %amplitude))
    
    i = start + 2 * d_v_delay
    j = start + 3 * d_v_delay
    for pulse_num in range(1,20):
        input_list.append(('DB1', '%sms'%i, motor_dur, '%spA' %amplitude))
        input_list.append(('VB1', '%sms'%j, motor_dur, '%spA' %amplitude))
        input_list.append(('DA1', '%sms'%i, motor_dur, '%spA' %amplitude))
        input_list.append(('VA1', '%sms'%j, motor_dur, '%spA' %amplitude))
        i += d_v_delay * 2
        j += d_v_delay * 2
    #'''
    
    
    # OPTION C: Square + & - step inputs
    
    
    
    
    # OPTION B: Sinusoidal Input
    '''
    sine_input_list.append(('DB1', '0ms', '20000ms', '1.5pA', '800ms'))
    sine_input_list.append(('VB1', '0ms', '20000ms', '1.5pA', '800ms'))
    sine_input_list.append(('DA1', '0ms', '20000ms', '1.5pA', '800ms'))
    sine_input_list.append(('VA1', '0ms', '20000ms', '-1.5pA', '800ms'))
    #'''
    

    config_param_overrides['input'] = input_list

    param_overrides = {
        
        'mirrored_elec_conn_params': {
            r'^AVB._to_DB\d+\_GJ$_elec_syn_gbase': '0.005 nS',
            r'^AVB._to_VB\d+\_GJ$_elec_syn_gbase': '0.005 nS',
            r'^AVA._to_DA\d+\_GJ$_elec_syn_gbase': '0.005 nS',
            r'^AVA._to_VA\d+\_GJ$_elec_syn_gbase': '0.005 nS',
        },
        
        'initial_memb_pot': '-50 mV',
        
        
        'AVBR_to_MVL16_exc_syn_conductance': '0 nS',
        'ca_conc_decay_time_muscle': '60.8 ms',
        'ca_conc_rho_muscle': '0.002338919 mol_per_m_per_A_per_s',
        
    }
    

    nml_doc = None
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

        #if config_param_overrides.has_key('input'):
        #    input_list = config_param_overrides['input']
        
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


if __name__ == '__main__':
    parameter_set = sys.argv[1] if len(sys.argv) == 2 else 'C2'
    #data_reader = sys.argv[2] if len(sys.argv) == 3 else 'My_Reader'
    data_reader = sys.argv[2] if len(sys.argv) == 3 else 'UpdatedSpreadsheetDataReader2'

    setup(parameter_set, generate=True, data_reader=data_reader)
