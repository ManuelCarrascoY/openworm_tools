import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import c302
import neuroml.writers as writers

range_incl = lambda start, end:range(start, end + 1)


def setup(parameter_set,
          generate=False,
          duration=8000,
          dt=0.05,
          target_directory='examples',
          data_reader="UpdatedSpreadsheetDataReader2",
          param_overrides={},
          verbose=True,
          config_param_overrides={}):

    exec ('from parameters_%s import ParameterisedModel' % parameter_set, globals())
    params = ParameterisedModel()

    #'''
    VA_motors = ["VA%s" % c for c in range_incl(1, 12)]
    VB_motors = ["VB%s" % c for c in range_incl(1, 11)]
    DA_motors = ["DA%s" % c for c in range_incl(1, 9)]
    DB_motors = ["DB%s" % c for c in range_incl(1, 7)]
    DD_motors = ["DD%s" % c for c in range_incl(1, 6)]
    VD_motors = ["VD%s" % c for c in range_incl(1, 13)]
    AS_motors = ["AS%s" % c for c in range_incl(1, 11)]
    #'''
    motors = list(VA_motors + VB_motors + AS_motors + DA_motors + DB_motors + VD_motors + DD_motors)
    
    
    inters = ['AVBL', 'AVBR', 'AVAL', 'AVAR']
    #inters = ['AVBL', 'AVBR']

    cells = list(motors + inters)
    
    muscles_to_include = True

    cells_to_stimulate = []


    cells_to_plot = cells
    reference = "c302_%s_FW_VNC_muscles" % parameter_set


    conns_to_include = [
    ]
    conns_to_exclude = [
        #'''
        'VB2-VB4_GJ',
        'VB4-VB2_GJ',
        
        # Disconnect AVA and AVB connections
        r'^AVB.-AVA.$', # GOOD
        r'^AVA.-AVB.$', # GOOD
        r'^AVB.-AVA._GJ$', # GOOD
        r'^AVA.-AVB._GJ$',
        
        #Disconnect DB and VB gap juntions
        r'^VB\d+-DB\d+_GJ$', 
        r'^DB\d+-VB\d+_GJ$', 
        
        #Disconnect DA and VA gap junctions
        r'^VA\d+-DA\d+_GJ$', 
        r'^DA\d+-VA\d+_GJ$',
        
        #Disconect AVB electrical (all except VB and DB) and chemical (.A and .B)
        r'^AVB.-.A\d+_GJ$',
        r'^.A\d+-AVB._GJ$',
        r'^AVB.-.S\d+_GJ$',
        r'^.S\d+-AVB._GJ$',
        r'^AVB.-.D\d+_GJ$',
        r'^.D\d+-AVB._GJ$',
        
        r'^AVB.-.A\d+$',
        r'^AVB.-.B\d+$',
        
        #Disconect AVA electrical (all except VA and DA) and chemical (.A and .B)
        r'^AVA.-.B\d+_GJ$',
        r'^.B\d+-AVA._GJ$',
        r'^AVA.-.S\d+_GJ$',
        r'^.S\d+-AVA._GJ$',
        r'^AVA.-.D\d+_GJ$',
        r'^.D\d+-AVA._GJ$',
                
        r'^AVA.-.A\d+$',
        r'^AVA.-.B\d+$',
        
        #Other Disconections
        r'^DA\d+-DB\d+$',
        r'^DB\d+-DA\d+$',
        r'^VB\d+-VA\d+$',
        #'''
        
        
    ]    
    conn_polarity_override = {
        r'^AS\d+-VD\d+$': 'inh',
        r'^DB\d+-DD\d+$': 'inh',
        r'^DB\d+-AS\d+$': 'inh',
        r'^DB\d+-VD\d+$': 'inh',
        #'DA1-VD2': 'inh',
        #'DA2-VD1': 'inh',
        r'^VB\d+-VD\d+$': 'inh',
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
    # Head Muscles STIMULATION
    #*************************
    #'''
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
    #'''            
    
    '''
    dur = '6000ms'
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
        
        start = '%sms' % (muscle_num * 30)
        
        sine_input_list.append((mdlx, '%sms'%, dur, '2pA', '800ms'))
        sine_input_list.append((mdrx, '0ms', dur, '2pA', '800ms'))
        input_list.append((mdlx, '0ms' , dur, '2pA'))
        input_list.append((mdrx, '0ms' , dur, '2pA'))
        if muscle_num != 6: 
            sine_input_list.append((mvlx, '0ms', dur, '-2pA', '800ms'))
            sine_input_list.append((mvrx, '0ms', dur, '-2pA', '800ms'))
            input_list.append((mvlx, '0ms' , dur, '2pA'))
            input_list.append((mvrx, '0ms' , dur, '2pA'))
    #'''
    
    #*************************
    # Interneuron STIMULATION
    #*************************
    #'''
    input_list.append(('AVBL', '0ms', '6000ms', '15pA'))
    input_list.append(('AVBR', '0ms', '6000ms', '15pA'))
    #'''
    
    
    #*************************
    # DB1 and VB1 STIMULATION
    #*************************

    # Sinusoidal Input
    #'''
    sine_input_list.append(('DB1', '190ms', '15000ms', '1.5pA', '800ms')) #AMP: 2pA seems to overstimulate
    sine_input_list.append(('VB1', '190ms', '15000ms', '1.5pA', '800ms'))

    
    config_param_overrides['input'] = input_list

    param_overrides = {
        
        'mirrored_elec_conn_params': {
            
            
            r'^AVB._to_DB\d+\_GJ$_elec_syn_gbase': '0.001 nS', 
            r'^AVB._to_VB\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            
            r'^AVA._to_DA\d+\_GJ$_elec_syn_gbase': '0.001 nS', 
            r'^AVA._to_VA\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            
            r'^DB\d+_to_DB\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            r'^VB\d+_to_VB\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            
            r'^DA\d+_to_DA\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            r'^VA\d+_to_VA\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            
        },
        
        'initial_memb_pot': '-50 mV',
        
        # Base elec_syn_gbase = 0.49nS
        #r'^AVB._to_AS\d+$_exc_syn_conductance': '0.1 nS',
        #r'^AVA._to_AS\d+$_exc_syn_conductance': '0.2 nS',


        
        #*********************************
        # Connections between units (chemical)
        #*********************************
        
        #Connect synaptically VB1 to VB2 and so on
        r'^VB\d+_to_VB\d+$_exc_syn_conductance': '30 nS',
        r'^VB\d+_to_VB\d+$_exc_syn_ar': '0.19 per_s',
        r'^VB\d+_to_VB\d+$_exc_syn_ad': '73 per_s',
        r'^VB\d+_to_VB\d+$_exc_syn_beta': '2.81 per_mV',
        r'^VB\d+_to_VB\d+$_exc_syn_vth': '-22 mV',
        r'^VB\d+_to_VB\d+$_exc_syn_erev': '10 mV',
        
        #Connect synaptically DB1 to DB2 and so on
        r'^DB\d+_to_DB\d+$_exc_syn_conductance': '30 nS',
        r'^DB\d+_to_DB\d+$_exc_syn_ar': '0.08 per_s',
        r'^DB\d+_to_DB\d+$_exc_syn_ad': '18 per_s',
        r'^DB\d+_to_DB\d+$_exc_syn_beta': '0.21 per_mV',
        r'^DB\d+_to_DB\d+$_exc_syn_vth': '-10 mV',
        r'^DB\d+_to_DB\d+$_exc_syn_erev': '10 mV',
        
        #'''
        #Connect synaptically VA1 to VA2 and so on
        r'^VA\d+_to_VA\d+$_exc_syn_conductance': '18 nS',
        r'^VA\d+_to_VA\d+$_exc_syn_ar': '0.19 per_s',
        r'^VA\d+_to_VA\d+$_exc_syn_ad': '73 per_s',
        r'^VA\d+_to_VA\d+$_exc_syn_beta': '2.81 per_mV',
        r'^VA\d+_to_VA\d+$_exc_syn_vth': '-22 mV',
        r'^VA\d+_to_VA\d+$_exc_syn_erev': '10 mV',
        
        #Connect synaptically DB1 to DB2 and so on
        r'^DA\d+_to_DA\d+$_exc_syn_conductance': '20 nS',
        r'^DA\d+_to_DA\d+$_exc_syn_ar': '0.08 per_s',
        r'^DA\d+_to_DA\d+$_exc_syn_ad': '18 per_s',
        r'^DA\d+_to_DA\d+$_exc_syn_beta': '0.21 per_mV',
        r'^DA\d+_to_DA\d+$_exc_syn_vth': '-10 mV',
        r'^DA\d+_to_DA\d+$_exc_syn_erev': '10 mV',
        #'''
        
        #Neuro - Muscular Junction Parameters
        'neuron_to_muscle_exc_syn_conductance': '0.5 nS',
        r'^DB\d+_to_MDL\d+$_exc_syn_conductance': '0.4 nS',
        r'^DB\d+_to_MDR\d+$_exc_syn_conductance': '0.4 nS',
        r'^VB\d+_to_MVL\d+$_exc_syn_conductance': '0.6 nS',
        r'^VB\d+_to_MVR\d+$_exc_syn_conductance': '0.6 nS',
        
        r'^DA\d+_to_MDL\d+$_exc_syn_conductance': '0.4 nS',
        r'^DA\d+_to_MDR\d+$_exc_syn_conductance': '0.4 nS',
        r'^VA\d+_to_MVL\d+$_exc_syn_conductance': '0.6 nS',
        r'^VA\d+_to_MVR\d+$_exc_syn_conductance': '0.6 nS',
        
        'neuron_to_muscle_exc_syn_vth': '37 mV',
        'neuron_to_muscle_inh_syn_conductance': '0.6 nS',
        'neuron_to_neuron_inh_syn_conductance': '0.2 nS',
        
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
