svtmp - template functions for SystemVerilog
==========================================================

**svtmp** is a package with small templating functions for SystemVerilog. It takes care of
indentation, header insertion in files, conversion from integer to SV hex/bin, and most
tiresome stuff when automatically generating SystemVerilog code.

**svtmp** is not meant to be a complete SV-generation solution: it just implements most
common snippets necessary for common RTL automated blocks: address decoders, register maps,
module ports, and all the necessary small snippets to do so (always_ff/comb, case, if/else,
etc).

Dependencies
-------------

* Python version required: `3.7+`
* If documentation is to be generated ``sphinx`` and ``sphinx_rtd_theme`` packages are required:

.. code-block:: console

    pip install sphinx sphinx_rtd_theme

Installation
-------------

Simply type:

.. code-block:: console
		
    pip install svtmp

  
Documentation
----------------

Documentation can be found @ `readthedocs <https://svtmp.readthedocs.io>`_


Examples
---------------

Flip Flop 
''''''''''''''

This code snippet

.. code-block:: python
		
    from svtmp import *   # import the svtmp
    t = SVTxt()           # create a SystemVerilog text instance
    # I/Os for the SV module
    ios = [Input(s) for s in 'clk_i','reset_n_i','di'] + [Output('do')]

    t.add(always_ff(eq('do',ui2b(0,1)), eq('do','di'))) #add always_ff block

    t.to_module('dff', ios = ios) #wrap SV into a module

    t.to_sv_file('dff', desc = 'Flip Flop implementation') # write to file


produces a SystemVerilog file ``dff.sv`` with the following contents:

.. code-block:: verilog

    /*------------------------------------------------------------------------------
     |  Title   : dff
     |  Project : svtmp
     +------------------------------------------------------------------------------
     |  Automatically generated with svtmp python library
     |
     +------------------------------------------------------------------------------
     |  Description:
     |  Flip Flop implementation
     +------------------------------------------------------------------------------
     | File     : dff.sv
     | Language : SystemVerilog
     | Created  : 2022-10-23
     +------------------------------------------------------------------------------
     |  Copyright (c) Infineon Technologies AG 2022 -  Confidential
     +------------------------------------------------------------------------------
     */

    module dff
      ( input logic clk_i,
        input logic reset_n_i,
        input logic di,
        output logic do
       );

       always_ff @(posedge clk_i,negedge reset_n_i)
       begin
          if (!reset_n_i)
             do <= 1'b0;
          else
             do <= di;
       end

    endmodule

Registered thermometer encoder
''''''''''''''''''''''''''''''''

The following code

.. code-block:: python

    from svtmp import * # import all templates from svtmp
    IW = 4       # selection input sel_i width
    OW = 2**IW   # thermometer output th_o width

    t = SVTxt() #SV text instance
    
    #I/Os of the module
    ios = inputs(['clk_i','reset_n_i']) + [invec('sel_i',IW-1,0), outvec('th_o',OW-1,0)]

    # thermometer output case items
    items = [citem(ui2h(i, IW), eq('th_o', ui2b((2**(i+1))-1, OW))) for i in range(OW)]

    # always_ff block containing the case for thermometer encoding
    t.add(always_ff(eq('th_o', ui2h(0, OW)), case('sel_i', items)))

    t.to_module('th_enc', ios = ios) # wrap the SVTxt contents into a module

    t.to_sv_file('th_enc', desc = 'thermometer encoder', prj = 'svtmp') #write to file


results in a SystemVerilog ``th_enc.sv`` file with these contents:

.. code-block:: verilog   

    /*------------------------------------------------------------------------------
     |  Title   : th_enc
     |  Project : svtmp
     +------------------------------------------------------------------------------
     |  Automatically generated with svtmp python library
     |
     +------------------------------------------------------------------------------
     |  Description:
     |  thermometer encoder
     +------------------------------------------------------------------------------
     | File     : th_enc.sv
     | Language : SystemVerilog
     | Created  : 2022-10-23
     +------------------------------------------------------------------------------
     |  Copyright (c) Infineon Technologies AG 2022 -  Confidential
     +------------------------------------------------------------------------------
     */

    module th_enc
      ( input logic clk_i,
        input logic reset_n_i,
        input logic [3:0] sel_i,
        output logic [15:0] th_o
       );

       always_ff @(posedge clk_i,negedge reset_n_i)
       begin
          if (!reset_n_i)
             th_o <= 16'h0000;
          else
          begin
             case(sel_i)
                4'h0:    th_o <= 16'b0000000000000001;
                4'h1:    th_o <= 16'b0000000000000011;
                4'h2:    th_o <= 16'b0000000000000111;
                4'h3:    th_o <= 16'b0000000000001111;
                4'h4:    th_o <= 16'b0000000000011111;
                4'h5:    th_o <= 16'b0000000000111111;
                4'h6:    th_o <= 16'b0000000001111111;
                4'h7:    th_o <= 16'b0000000011111111;
                4'h8:    th_o <= 16'b0000000111111111;
                4'h9:    th_o <= 16'b0000001111111111;
                4'ha:    th_o <= 16'b0000011111111111;
                4'hb:    th_o <= 16'b0000111111111111;
                4'hc:    th_o <= 16'b0001111111111111;
                4'hd:    th_o <= 16'b0011111111111111;
                4'he:    th_o <= 16'b0111111111111111;
                4'hf:    th_o <= 16'b1111111111111111;
             endcase

          end
       end

    endmodule
		

Development
---------------

1. clone this repository (or download a zip and unzip it somewhere)

.. code-block:: console

    git clone https://github.com/alb-garcia/svtmp.git

2. inside the cloned folder, make a editable installation
   
.. code-block:: console

    pip install -e .

3. To run tests (pytest needs to be installed):

.. code-block:: console

    cd test; pytest -vvv
    
Documentation Generation
---------------------------
    
To generate the documentation (assuming the clone repository lives @ ``$SVTMP_DIR``:

.. code-block:: console

    cd $SVTMP_DIR/docs
    make html

the documentation can be then accessed @ ``$SVTMP_DIR/docs/_build/html/index.htm``
    
    
Package Documentation
===========================================
   
.. toctree::
   :maxdepth: 1

   svtmp

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
