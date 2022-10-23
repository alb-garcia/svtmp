from svtmp import * # import all templates from svtmp
IW = 4              # selection input sel_i width
OW = 2**IW          # thermometer output th_o width

t = SVTxt() #SV text instance

#I/Os of the module
ios = inputs(['clk_i','reset_n_i']) + [invec('sel_i',IW-1,0), outvec('th_o',OW-1,0)]

# thermometer output case items
items = [citem(ui2h(i, IW), eq('th_o', ui2b((2**(i+1))-1, OW))) for i in range(OW)]

# always_ff block containing the case for thermometer encoding
t.add(always_ff(eq('th_o', ui2h(0, OW)), case('sel_i', items)))

t.to_module('th_enc', ios = ios) # wrap the SVTxt contents into a module

t.to_sv_file('th_enc', desc = 'thermometer encoder', prj = 'svtmp') #write to file

