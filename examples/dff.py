from svtmp import *   # import the svtmp
t = SVTxt()           # create a SystemVerilog text instance

# I/Os for the SV module
ios = [Input(s) for s in ('clk_i','reset_n_i','di')] + [Output('do')]
#add always_ff block
t.add(always_ff(eq('do',ui2b(0,1)), eq('do','di'))) 
#wrap SV into a module
t.to_module('dff', ios = ios) 
# write to file
t.to_sv_file('dff', desc = 'Flip Flop implementation') 
