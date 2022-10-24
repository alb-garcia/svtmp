from svtmp import *   # import the svtmp
t = SVTxt()           # create a SystemVerilog text instance

ios = inputs(['clk_i', 'rst_n_i', 'di']) + [Output('do')] # I/Os for SV module
t.add(always_ff(eq('do',ui2b(0,1)), eq('do','di')))       # add always_ff block

t.to_module('dff', ios = ios)                             # wrap SV into a module
t.to_sv_file('dff', desc = 'Flip Flop implementation')    # write to file
