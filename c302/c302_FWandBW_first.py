import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import c302
import neuroml.writers as writers

range_incl = lambda start, end:range(start, end + 1)

def setup(parameter_set,
          generate=False,
          duration=12000,
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
    
    inters = ['AVBL', 'AVBR', 'AVAL', 'AVAR']

    cells = list(motors + inters)

    
    
    muscles_to_include = []

    cells_to_stimulate = []

    cells_to_plot = cells
    reference = "c302_%s_FWandBW_first" % parameter_set


    conns_to_include = [
        
    ]
    conns_to_exclude = [
        #'''
        'VB2-VB4_GJ',
        'VB4-VB2_GJ',
        r'^AVB.-AVA.$', # GOOD
        r'^AVA.-AVB.$', # GOOD
        r'^AVB.-AVA._GJ$', # GOOD
        r'^AVA.-AVB._GJ$',
        #r'^AVA.-DA\d+$', # GOOD
        #r'^AVA.-VA\d+$',
        'DA1-DB1',
        'DB1-DA1',
        'VB1-VA1',
        #'''
    ]    
    conn_polarity_override = {
        r'^AS\d+-VD\d+$': 'inh',
        #r'^DB\d+-DD\d+$': 'inh',
        r'^DB\d+-AS\d+$': 'inh',
        r'^DB\d+-VD\d+$': 'inh',
        'DA1-VD2': 'inh',
        'DA2-VD1': 'inh',
        #r'^VB\d+-VD\d+$': 'inh',
        r'^VD\d+-VA\d+$': 'inh',
        r'^VA\d+-VD\d+$': 'inh',
        
        #r'^VD\d+-DB\d+$': 'inh',
        
    }
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
    #'''
    input_list.append(('AVBL', '0ms', '3000ms', '15pA'))
    input_list.append(('AVBR', '0ms', '3000ms', '15pA'))
    input_list.append(('AVAL', '3000ms', '6000ms', '15pA'))
    input_list.append(('AVAR', '3000ms', '6000ms', '15pA'))
    input_list.append(('AVBL', '9000ms', '3000ms', '15pA'))
    input_list.append(('AVBR', '9000ms', '3000ms', '15pA'))
    #'''
    #ramp_input_list.append(('AVBL', '0ms', '1000ms', "0pA", "15pA", "0pA"))
    #ramp_input_list.append(('AVBL', '1000ms', '0ms', '15pA', '0pA', '0pA'))
    
    '''
    input_list.append(('AVBL', '0ms', '1000ms', '15pA'))
    input_list.append(('AVBL', '3000ms', '1000ms', '15pA'))
    input_list.append(('AVBL', '4000ms', '1000ms', '10pA'))
    input_list.append(('AVBL', '7000ms', '1000ms', '10pA'))
    input_list.append(('AVBL', '8000ms', '1000ms', '15pA'))
    input_list.append(('AVBL', '9000ms', '1000ms', '10pA'))
    
    input_list.append(('AVBR', '0ms', '1000ms', '15pA'))
    input_list.append(('AVBR', '3000ms', '1000ms', '15pA'))
    input_list.append(('AVBR', '4000ms', '1000ms', '10pA'))
    input_list.append(('AVBR', '7000ms', '1000ms', '10pA'))
    input_list.append(('AVBR', '8000ms', '1000ms', '15pA'))
    input_list.append(('AVBR', '9000ms', '1000ms', '10pA'))
    
    input_list.append(('AVAL', '1000ms', '2000ms', '10pA'))
    input_list.append(('AVAL', '5000ms', '1000ms', '5pA'))
    input_list.append(('AVAL', '6000ms', '1000ms', '15pA'))
    input_list.append(('AVAL', '10000ms', '1000ms', '5pA'))
    input_list.append(('AVAL', '11000ms', '1000ms', '10pA'))
    input_list.append(('AVAL', '12000ms', '2000ms', '15pA'))
    
    input_list.append(('AVAR', '1000ms', '2000ms', '10pA'))
    input_list.append(('AVAR', '5000ms', '1000ms', '5pA'))
    input_list.append(('AVAR', '6000ms', '1000ms', '15pA'))
    input_list.append(('AVAR', '10000ms', '1000ms', '5pA'))
    input_list.append(('AVAR', '11000ms', '1000ms', '10pA'))
    input_list.append(('AVAR', '12000ms', '2000ms', '15pA'))
    '''
    
    #*************************
    # HEAD MUSCLE STIMULATION
    #*************************
    '''
    amp = '4pA'
    dur = '250ms'

    for stim_num in range(15):
        for muscle_num in range(7):
            mdlx = 'MDL0%s' % (muscle_num + 1)
            mdrx = 'MDR0%s' % (muscle_num + 1)
            mvlx = 'MVL0%s' % (muscle_num + 1)
            mvrx = 'MVR0%s' % (muscle_num + 1)
            
            if muscle_num >= 9:
                mdlx = 'MDL%s' % (muscle_num + 1)
                mdrx = 'MDR%s' % (muscle_num + 1)
                mvlx = 'MVL%s' % (muscle_num + 1)
                mvrx = 'MVR%s' % (muscle_num + 1)
            
            startd = '%sms' % (stim_num * 800 + muscle_num * 30)
            startv = '%sms' % ((stim_num * 800 + 400) + muscle_num * 30)
            
            input_list.append((mdlx, startd, dur, amp))
            input_list.append((mdrx, startd, dur, amp))
            if muscle_num != 6:
                input_list.append((mvlx, startv, dur, amp))
                input_list.append((mvrx, startv, dur, amp))
    '''
    
    #*************************
    # DB1 and VB1 STIMULATION
    #*************************
    '''
    d_v_delay = 400

    #start = 190
    start = 0
    motor_dur = '250ms'

    input_list.append(('DB1', '%sms'%(start), motor_dur, '3pA'))
    input_list.append(('VB1', '%sms'%(start+d_v_delay), motor_dur, '3pA'))

    i = start + 2 * d_v_delay
    j = start + 3 * d_v_delay
    for pulse_num in range(1,15):
        input_list.append(('DB1', '%sms'%i, motor_dur, '3pA'))
        input_list.append(('VB1', '%sms'%j, motor_dur, '3pA'))
        i += d_v_delay * 2
        j += d_v_delay * 2
    '''
    # Sinusoidal Input
    #'''
    sine_input_list.append(('DB1', '0ms', '15000ms', '2pA', '800ms'))
    sine_input_list.append(('VB1', '0ms', '15000ms', '2pA', '800ms'))
    sine_input_list.append(('DA1', '0ms', '15000ms', '-2pA', '800ms'))
    sine_input_list.append(('VA1', '0ms', '15000ms', '2pA', '800ms'))
    #'''
    # Offset input
    '''
    input_list.append(('DB1', '0ms', '15000ms', '1.5pA'))
    input_list.append(('VB1', '0ms', '15000ms', '1.5pA'))
    input_list.append(('DA1', '0ms', '15000ms', '1.5pA'))
    input_list.append(('VA1', '0ms', '15000ms', '1.5pA'))
    #'''
    # Self-activated neuron
    '''
    input_list.append(('AS1', '0ms', '15000ms', '3pA'))
    input_list.append(('AS2', '0ms', '15000ms', '3pA'))
    #'''

    config_param_overrides['input'] = input_list

    param_overrides = {
        
        'mirrored_elec_conn_params': {
            r'^AVB._to_DB\d+\_GJ$_elec_syn_gbase': '0.01 nS',
            r'^AVB._to_VB\d+\_GJ$_elec_syn_gbase': '0.01 nS',
            r'^AVA._to_DA\d+\_GJ$_elec_syn_gbase': '0.01 nS',
            r'^AVA._to_VA\d+\_GJ$_elec_syn_gbase': '0.01 nS',
        },
        
        'initial_memb_pot': '-50 mV',

        #*********************************
        # Motoneuron to muscle parameters
        #*********************************
        '''
        'neuron_to_muscle_exc_syn_conductance': '0.5 nS',
        r'^DB\d+_to_MDL\d+$_exc_syn_conductance': '0.4 nS',
        r'^DB\d+_to_MDR\d+$_exc_syn_conductance': '0.4 nS',
        r'^VB\d+_to_MVL\d+$_exc_syn_conductance': '0.6 nS',
        r'^VB\d+_to_MVR\d+$_exc_syn_conductance': '0.6 nS',
        'neuron_to_muscle_exc_syn_vth': '37 mV',
        'neuron_to_muscle_inh_syn_conductance': '0.6 nS',
        'neuron_to_neuron_inh_syn_conductance': '0.2 nS',
        '''
        
        
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
        '''
        c302.add_new_sinusoidal_input(nml_doc, cell='DB1', delay="0ms", duration="10000ms", amplitude="1.5pA", period="800ms", params=params)
        c302.add_new_sinusoidal_input(nml_doc, cell='VB1', delay="0ms", duration="10000ms", amplitude="1.5pA", period="800ms", params=params)
        c302.add_new_sinusoidal_input(nml_doc, cell='DA1', delay="0ms", duration="10000ms", amplitude="-1.5pA", period="800ms", params=params)
        c302.add_new_sinusoidal_input(nml_doc, cell='VA1', delay="0ms", duration="10000ms", amplitude="1.5pA", period="800ms", params=params)
        '''
        #c302.add_new_input(nml_doc, cell='VB1', delay="1200ms", duration="1000ms", amplitude="1pA", params=params)
        #c302.add_new_input(nml_doc, cell='VB1', delay="0ms", duration="2000ms", amplitude="1.5pA", params=params)
        
        

        nml_file = target_directory + '/' + reference + '.net.nml'
        writers.NeuroMLWriter.write(nml_doc, nml_file)  # Write over network file written above...

        c302.print_("(Re)written network file to: " + nml_file)


    return cells, cells_to_stimulate, params, muscles_to_include, nml_doc


if __name__ == '__main__':
    parameter_set = sys.argv[1] if len(sys.argv) == 2 else 'C2'
    #data_reader = sys.argv[2] if len(sys.argv) == 3 else 'My_Reader'
    data_reader = sys.argv[2] if len(sys.argv) == 3 else 'UpdatedSpreadsheetDataReader2'

    setup(parameter_set, generate=True, data_reader=data_reader)
