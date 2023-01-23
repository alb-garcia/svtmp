from __future__ import annotations # for compatibility with python 3.7-3.9

"""
**svtmp** is a collection of small SystemVerilog templates to ease the automatic
generation of SystemVerilog code.

=============
Dependencies
=============

None. The module is standalone (other than Python standard library)

Python version required: *3.7+*

=============
Installation
=============

Simple::

    pip install svtmp

=============
The module
=============

**svtmp** is a collection of small SystemVerilog templates to ease the automatic
generation of SystemVerilog code. **svtmp** templating functions compose with each
other in terms in terms of indentation, so that templating code doesn't have to
care about indents.

**svtmp** support templating functions for the following constructs:

* case statements: :meth:`case`
* case statement items: :meth:`citem`
* always_ff blocks: :meth:`always_ff`
* always_comb blcoks: :meth:`always_comb`
* continuous assignments: :meth:`assign`
* blocking/non-blocking assignemnts :meth:`eq`
* struct typedef definition: :meth:`struct`
* if-else blocks: :meth:`ifelse`
* if block: :meth:`If`
* file headers: :meth:`header`
* comments: :meth:`comment`
* comment header: :meth:`cheader`
* parameters, localparams, constants: :meth:`parameter` :meth:`localparam`, :meth:`const`
* conversion from (string) ints to SV binary/hex literals: :meth:`ui2b`, :meth:`sui2b`, :meth:`ui2h`, :meth:`sui2h`
* preprocessor directives: :meth:`ifdef` :meth:`ifndef` :meth:`define` :meth:`endif`
* import directives: :meth:`Import`
* signal declarations: :meth:`logic`, :meth:`logvec`, :meth:`decl`
* I/O definitions for module ports: :meth:`Input`, :meth:`invec`, :meth:`Output`, :meth:`outvec`, :meth:`inputs`, :meth:`outputs`
* module definitions: :meth:`module`
* package definitions: :meth:`package`

In addition to templating functions, **svtmp** provides a convenience class, :class:`SVTxt` that allows easy
wrapping of templated code into modules/packages/include segments and writing them into .sv/.svh files together with
headers.

===============
svtmp Examples
===============


* Flip Flop. The following code::

    from svtmp import *   # import the module
    t = SVTxt()           # create a SystemVerilog text instance
    # I/Os for the SV module
    ios = [Input(s) for s in 'clk_i','reset_n_i','di'] + [Output('do')]

    # add an always_ff block to the SV text instance
    t.add(always_ff(rbody = eq('do',ui2b(0,1)), body  = eq('do','di')))

    # wrap SV text contents in a module with the previously defined I/Os
    t.to_module('dff', ios = ios)

    # write into a file with header
    t.to_sv_file('dff', desc = 'Flip Flop implementation', prj = 'svtmp')

results in a file ``dff.sv`` with these contents:::

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

* Register thermometer encoder. The following code::

    from svtmp import * # import all templates from svtmp
    IW = 4       # selection input sel_i width
    OW = 2**IW   # thermometer output th_o width

    t = SVTxt() #SV text instance
    
    #I/Os of the module
    ios = inputs(['clk_i','reset_n_i']) + [invec('sel_i',IW-1,0), outvec('th_o',OW-1,0)]

    # thermometer output case items
    case_items = [citem(cond = ui2h(i, IW),
                 body = eq('th_o', ui2b((2**(i+1))-1, OW))) for i in range(OW)]

    # always_ff block containing the case for thermometer encoding
    t.add(always_ff(eq('th_o', ui2h(0, OW)), case('sel_i', case_items)))

    # wrap the SVTxt contents into a module
    t.to_module('th_enc', ios = ios)

    #write to file
    t.to_sv_file('th_enc', desc = 'thermometer encoder', prj = 'svtmp')

results in a ``th_enc.sv`` file containing the following::

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

===============
Module contents
===============


"""


##################################################################
# indentation level: change to meet your site coding style

SVTMP_INDENTATION_WIDTH = 3
""" indentation width in spaces for all templates in ``svtmp``."""
##################################################################

import logging as log
from typing import List
from datetime import date
import os

INDENT = SVTMP_INDENTATION_WIDTH * ' '
""" default indentation for all templates in svtmp. ``INDENT = SVTMP_INDENTATION_WIDTH * ' '``"""

def header(name: str, fname: str, desc: str, prj: str) -> str:
    """ generates a SystemVerilog file header.

    The generated header automatically picks up the date of creation and if possible, the
    Camino project where the file is created.
    
    Example::
    
        >>> print(header(name='dtop', fname='dtop.sv', desc='Digital Top Level', prj='myproject'))

        /*------------------------------------------------------------------------------
         |  Title   : dtop
         |  Project : myproject
         +------------------------------------------------------------------------------
         |  Automatically generated with svtmp python library
         |
         +------------------------------------------------------------------------------
         |  Description:
         |  Digital Top Level
         +------------------------------------------------------------------------------
         | File     : dtop.sv
         | Language : SystemVerilog
         | Created  : 2022-10-15
         +------------------------------------------------------------------------------
         |  Copyright (c) Infineon Technologies AG 2022 -  Confidential
         +------------------------------------------------------------------------------
         */

    Arguments:
        name : the name of the package/module implemented in the file.
        fname : filename where the header will be included.
        desc : short description of the file contents.
        prj: project for file. If ``None``, project name will be picked up from Camino env variable SUBPROJECTNAME.

    Returns: 
        a string containing the header.
    """
    sdate = date.today().isoformat()
    syear = sdate.split('-')[0]
    return f"""/*------------------------------------------------------------------------------
 |  Title   : {name}
 |  Project : {prj}
 +------------------------------------------------------------------------------
 |  Automatically generated with svtmp python library
 |
 +------------------------------------------------------------------------------
 |  Description:
 |  {desc}
 +------------------------------------------------------------------------------
 | File     : {fname}
 | Language : SystemVerilog
 | Created  : {sdate}
 +------------------------------------------------------------------------------
 |  Copyright (c) Infineon Technologies AG {syear} -  Confidential
 +------------------------------------------------------------------------------
 */
"""

def ui2b(x: int, nbits: int) -> str:
    """converts unsigned integers to SystemVerilog binary literals.

    Example::

        >>> ui2b(63, 8)
        "8'b00111111"
    
    Arguments:
        x : integer input (assumed unsigned).
        nbits : number of bits of the SystemVerilog literal.

    Returns:
        a string with the SystemVerilog binary literal.
    """

    if x > (2**nbits - 1) or nbits == 0:
        raise ValueError(f'{x} cannot be represented in {nbits} bits')
    
    return f"{nbits}'b{x:0{nbits}b}"

def sui2b(x: str, nbits: int) -> str:
    """converts unsigned integer strings to SystemVerilog binary literals.

    Example::

        >>> sui2b('63', 8)
        "8'b00111111"
    
    Arguments:
        x : integer input (assumed unsigned).
        nbits : number of bits of the SystemVerilog literal.

    Returns:
        a string with the SystemVerilog binary literal.
    """
    return ui2b(int(x), nbits)

def ui2h(x: int, nbits: int) -> str:
    """converts unsigned integers to SystemVerilog hex literals.

    Example::

        >>> ui2h(63,23)
        "23'h00003f"
    
    Arguments:
        x : integer input (assumed unsigned).
        nbits : number of bits of the SystemVerilog literal.

    Returns:
        a string with the SystemVerilog binary literal.
    """
    if x > (2**nbits - 1) or nbits == 0:
        raise ValueError(f'{x} cannot be represented in {nbits} bits')
    
    nhex_digits = (nbits // 4) if nbits % 4 == 0 else (nbits // 4) + 1
    number = f"{x:0{nhex_digits}x}".upper()
    return f"{nbits}'h{number}"

def sui2h(x: str, nbits: int) -> str:
    """converts unsigned integer stings to SystemVerilog hex literals.

    Example::

        >>> ui2h('63',23)
        "23'h00003f"
    
    Arguments:
        x : integer input (assumed unsigned).
        nbits : number of bits of the SystemVerilog literal.

    Returns:
        a string with the SystemVerilog binary literal.
    """
    
    return ui2h(int(x), nbits)

def comment(comment: str) -> str:
    """ returns a single line comment.

    Example::

        >>> comment('this is a comment')
        '// this is a comment'

    Arguments:
        comment : comment content.

    Returns:
        string comment.
    """
    if comment != '':
        return f'// {comment}'
    else:
        return ''


def cheader(comment: str) -> str:
    """returns a commend header.

    Example::

        >>> print(cheader('THIS IS A COMMENT HEADER'))    
        //------------------------------------------------------------------------------
        // THIS IS A COMMENT HEADER
        //------------------------------------------------------------------------------

    Arguments:
        comment : the content of the comment header

    Returns:
        a string with the comment header

    """
    return f"//{78*'-'}\n// {comment}\n//{78*'-'}"


def invec(name:str, lhs: int | str, rhs: int | str, typ = 'logic') -> str:
    """ generates a packed vector input port. Used to be included in a list of ports
    and passed as argument to :meth:`module` or :meth:`SVTxt.to_module`

    Example::
    
        >> invec('data_i', 7, 0)
           'input logic [7:0] data_i'

        >> invec('sfr_i', 3, 0, typ = 'sfr_in')
           'input sfr_in [3:0] sfr_i'

    Arguments:
        name : input name
        lhs  : left-hand-side of the vector width definition (typ. MSB)
        rhs  : right-hand-side of the vector width definition  (typ. LSB)
        typ  : port type

    Returns: a string with the port definition
    """
    if name == '':
        raise ValueError('a port requires a non-empty string name')
    
    return f'input {typ} [{lhs}:{rhs}] {name}'

def Input(name:str,typ:str = 'logic') -> str:
    """ generates a single input port. Used to be included in a list of ports
    and passed as argument to :meth:`module` or :meth:`SVTxt.to_module`.

    Examples::

      >> Input('clk_i')
         'input logic clk_i'

      >> Input('reset_i', 'reset_t')
         'input reset_t reset_i'

    Arguments:
        name : input port name
        typ  : input port type

    Returns: a string with the port definition
    """
    
    if name == '':
        raise ValueError('a port requires a non-empty string name')
    
    return f'input {typ} {name}'

def inputs(ins: List[str]) -> List[str]:
    """ short-hand function to generate a list of logic single inputs from 
    a list of string names.

    Examples::

      >> inputs(['clk_i', 'reset_n_i', 'enable_i'])
         ['input logic clk_i', 'input logic reset_n_i', 'input logic enable_i']    

    Arguments:
        ins : list of names for the input signals

    Returns: a list of strings with the inputs definition
    """
    return list([Input(i) for i in ins])

def Output(name:str,typ:str = 'logic') -> str:
    """ generates a single output port. Used to be included in a list of ports
    and passed as argument to :meth:`module` or :meth:`SVTxt.to_module`.

    Examples::

      >> Output('clk_i')
         'output logic clk_i'

      >> Output('reset_i', 'reset_t')
         'output reset_t reset_i'

    Arguments:
        name : output port name
        typ  : output port type

    Returns: a string with the port definition
    """
    if name == '':
        raise ValueError('a port requires a non-empty string name')
    
    return f'output {typ} {name}'

def outvec(name:str, lhs:int | str, rhs:int | str, typ = 'logic') -> str:
    """ generates a packed vector output port. Used to be included in a list of ports
    and passed as argument to :meth:`module` or :meth:`SVTxt.to_module`

    Example::
    
        >> outvec('data_o', 7, 0)
           'output logic [7:0] data_o'

        >> outvec('sfr_o', 3, 0, typ = 'sfr_out')
           'output sfr_out [3:0] sfr_o'

    Arguments:
        name : output name
        lhs  : left-hand-side of the vector width definition (typ. MSB)
        rhs  : right-hand-side of the vector width definition  (typ. LSB)
        typ  : port type

    Returns: a string with the port definition
    """
    if name == '':
        raise ValueError('a port requires a non-empty string name')
    
    return f'output {typ} [{lhs}:{rhs}] {name}'

def outputs(outs: List[str]) -> List[str]:
    """ short-hand function to generate a list of logic single outputs from 
    a list of string names.

    Example::

      >> outputs(['clk_i', 'reset_n_i', 'enable_i'])
         ['output logic clk_i', 'output logic reset_n_i', 'output logic enable_i']    

    Arguments:
        outs : list of names for the output signals

    Returns: a list of strings with the outputs definition
    """
    
    return list([Output(o) for o in outs])

        
def struct(typ : str, decls : str | List[str], packed : bool = True, debug : bool = False):
    """ generates SystemVerilog struc type definition.

    Example::
    
      >> decls = [logic('en'), logic('dis'), logvec('cnt', 7,0)]
      >> print(struct(typ = 'sfr_cnt_t', decls = decls))
         typedef struct packed {
         logic en; 
         logic dis; 
         logic [7:0] cnt; 
      } sfr_cnt_t;

    Arguments:
        typ: name of the struc type
        decls: newline-separated string with signal declarations, or list of strings with them

    Returns: a string with the typedef struct definition
    """
    if decls == [] or decls == '':
        raise ValueError('struct definition cannot be empty')
    
    pk = 'packed ' if packed else ''
    ind_body = indent(_ljoin(decls))
    s_struct = f'typedef struct {pk}{{\n{ind_body}\n}} {typ};'
    
    if debug:
        log.debug(f'SVTMP - struct: {s_struct}')

    return s_struct

def package(name: str, body: str | List[str], debug : bool = False):
    """ generates a SystemVerilog package.

    Example::

      >> lps = [localparam(c[0],c[1]) for c in (('DATAWIDTH', 16), ('ADDRWIDTH', 10) ,('OFFSET', 100))]
      >> print(package(name = 'data_pkg', body = lps))
         package data_pkg;
            localparam DATAWIDTH = 16 ;
            localparam ADDRWIDTH = 10 ;
            localparam OFFSET = 100 ;
         endpackage: data_pkg

    Arguments:
        name  : name of the package.
        body  : string or list of strings containing the body of the package. 

    Returns: a string with the complete SV package.
    """
    
    ibody = indent(_ljoin(body))
    s_pack = f'package {name};\n{ibody}\nendpackage: {name}'
    if debug:
        log.debug('SVTMP - package: \n{s_pack}')
    return s_pack

def assign(lhs: str,rhs: str, debug: bool = False):
    """ generates an continuous assignment statement.
    
    Example::
    
      >> assign('a', ui2h(64,16))
         "assign a = 16'h0040;"

    Arguments:
        lhs : left-hand side of the assigment.
        rhs : right hand side of the assignment.

    Returns: a string with the assign statement.
    """
    s_assign = f'assign {lhs} = {rhs};'
    if debug:
        log.debug('SVTMP - assign: {s_assign}')
    return s_assign

def const(typ: str, lhs: str,rhs: str, cmt: str = '', debug: bool = False):
    """ generates a constant declaration.

    Example::

      >> const(typ = 'real', lhs = 'T', rhs = 25.0 , cmt = 'this is a comment')
         'const real T = 25.0; // this is a comment;'

    Arguments:
        typ : type of the constant
        lhs : constant name
        rhs : constant value
        cmt : comment after constant

    Returns: a constant declaration.
    """
    s_const = f'const {typ} {lhs} = {rhs}; {comment(cmt)};'
    if debug:
        log.debug(f'SVTMP - constant declaration: {s_const}')
    return s_const

def parameter(lhs: str,rhs: str , mod_decl: bool = True, debug: bool = False):
    s_parameter = f'parameter {lhs} = {rhs};'
    if debug:
        log.debug(f'SVTMP - parameter declaration: {s_parameter}')
    return s_parameter

def localparam(lhs: str,rhs: str, cmt: str = '', debug: bool = False):
    s_localparam = f'localparam {lhs} = {rhs} {comment(cmt)};'
    if debug:
        log.debug(f'SVTMP - localparam declaration: {s_localparam}')
    return s_localparam


def ifdef(s: str) -> str:
    return f'`ifdef {s}'

def ifndef(s: str) -> str:
    return f'`ifndef {s}'


def define(s: str) -> str:
    return f'`define {s}'

def endif() -> str:
    return f'`endif'

def Import(pkg: str) -> str:
    return f'import {pkg}::*;'

def logvec(name, lsb, rsb,cmt = '', debug: bool = False):
    if name == '':
        raise ValueError('a declaration requires a non-empty string name')

    if cmt == '':
        s_logvec = f'logic [{lsb}:{rsb}] {name};'
    else:
        s_logvec = f'logic [{lsb}:{rsb}] {name}; {comment(cmt)}'

    if debug:
        log.debug(f'SVTMP - logic vector declaration: {s_logvec}')
    return s_logvec
        

def logic(name: str, cmt: str = '', debug: bool = False):
    if name == '':
        raise ValueError('a declaration requires a non-empty string name')
    
    if cmt == '':
        s_logic = f'logic {name};'
    else:
        s_logic = f'logic {name}; {comment(cmt)}'
        
    if debug:
        log.debug(f'SVTMP - logic declaration: {s_logic}')
    return s_logic

def decl(typ: str, name: str, cmt: str  = '', debug: bool = False):
    if name == '':
        raise ValueError('a declaration requires a non-empty string name')

    if cmt == '':
        s_decl = f'{typ} {name};'
    else:    
        s_decl = f'{typ} {name}; {comment(cmt)}'
        
    if debug:
        log.debug(f'SVTMP - signal declaration: {s_decl}')
    return s_decl

def eq(lhs,rhs, block = False, debug: bool = False):
    op = '=' if block else '<='
    s_assignment = f'{lhs} {op} {rhs};'
    if debug:
        log.debug(f'SVTMP - assignment: {s_assignment}')
    return s_assignment

def concat(items: List[str], debug: bool = False):
    s_concat = f'{{{", ".join(items)}}}'
    if debug:
        log.debug(f'SVTMP - concatenation: {s_concat}')
    return s_concat

def If(cond: str, body: str | List[str], debug: bool = False):
    s_if = f'if ({cond})\n{block(body)}'
    if debug:
        log.debug(f'SVTMP - if-block:\n {s_if}')
    return s_if

def ifelse(cond: str, tbody: str | List[str], fbody: str | List[str], debug: bool = False):
    s = f'if ({cond})\n'
    s += block(tbody)
    s += f'\nelse\n'
    s += block(fbody)
    if debug:
        log.debug(f'SVTMP - if-else-block:\n {s}')
    return s

def always_comb(body: str | List[str], debug: bool = False):
    s_always_comb = f'always_comb\n{block(body)}'
    if debug:
        log.debug(f'SVTMP - always_comb block:\n {s_always_comb}')
    return s_always_comb


def make_always_ff(clk = 'clk_i', reset = 'reset_n_i',elevel = True, rlevel = False):
    def aff(rbody, body):
        return always_ff(body, rbody, clk, reset, elevel, rlevel)
    return aff
    
def always_ff(rbody: str | List[str],
              body:  str | List[str],
              clk:   str = 'clk_i',
              reset: str = 'reset_n_i',
              elevel: bool = True,
              rlevel: bool = False,
              debug:  bool = False):
    
    cedge = 'posedge' if elevel else 'negedge'
    redge = 'posedge' if rlevel else 'negedge'
    first = f'always_ff @({cedge} {clk},{redge} {reset})\nbegin\n'
    rcond = f'{reset}' if rlevel else f'!{reset}'
    aff_body = ifelse(rcond, rbody, body)
    s_always_ff = first + indent(aff_body) + '\nend'
    if debug:
        log.debug(f'SVTMP - always_ff block:\n {s_always_ff}')
    return s_always_ff

def case_item(cond, body):
    return f'{cond}: {block(body)}'

def citem(cond, body):
    return f'{cond}: {block(body)}'

def case(key: str, body: str | List[str]):
    return f'case({key})\n{indent(body)}\nendcase\n'

def module(name:str, body: List[str] | str,
           ios:        List[str] | str | None = None,
           parameters: List[str] | str | None = None,
           imports:    List[str] | str | None = None) -> str:
    
    s = f'module {name}\n' if ios else f'module {name}; \n'
    if imports:
        s += indent(_ljoin(imports))
        s += '\n'
    if parameters:
        s += indent(',\n'.join(parameters),spaces = 5 * ' ', first = '  #( ')
        s += "\n     )\n"

    if ios:
        s += indent(',\n'.join(ios),spaces = 4 * ' ',  first = '  ( ')
        
    s += '\n   );\n\n'
    s += indent(_ljoin(body))
    s += '\nendmodule\n'
    return s

def indent(fragment: List[str] | str, spaces:str = INDENT, first:str = INDENT) -> str:
    """ takes a (potentially) multiline string or a list of strings and indents it
    (joining the result by newlines if the input was a list of strings)

    Example 1::

        >>> s = ['logic a;', 'logic b;', 'logic c;']
        >>> print(indent(s, spaces = 4*' ', first = 6*' '))
              logic a;
           logic b;
           logic c;

    Example 2::

        >> print(indent('a\\nb\\nc\\n'))  # with SVTMP_INDENTATION_WIDTH = 3
           a
           b
           c

    Arguments:
        fragment : string or list of strings to be indented.
        spaces   : indentation string (normally a number of consecutive spaces) for all lines except for first.
        first    : indentation string for first line/string in list.

    Returns:
        a string with indented input (either indented string or newling-concatenated string with list strings indented.
    """
    if isinstance(fragment, list):
        items = []
        for s in fragment:
            lines = s.split('\n')
            items.extend(lines)

    elif isinstance(fragment, str):
        items = fragment.split('\n')
        
        
    indented_items = []
    for i,item in enumerate(items):
        if i == 0:
            indented_items.append(first  + item)
        else:
            indented_items.append(spaces  + item)

    return '\n'.join(indented_items)

def block(s: str | List[str]) -> str:
    """ takes a newline separated string of commands or a list of string commands, and returns a newline separated string of indented commands, wrapped by begin-end if necessary.

    Examples::
      
          >> print(block("a = 1")) 
                a = 1

          >> print(block('a = 1\\nb = 2'))
             begin
                a = 1
                b = 2
             end

          >> stmts = ['a = 1', 'b = 2']
          >> print(block(stmts))
             begin
                a = 1
                b = 2
             end

    Arguments:
        s : a string of newline separated statements or a list of statement strings

    Returns: 
        an indented, possibly wrapped in begin-end string with the input statements
    """
    if isinstance(s, str):
        if '\n' in s[:-1]: #more than 2 lines
            lines = s.split('\n')
            return f'begin\n{indent(_ljoin(s))}\nend'
        else:
            return indent(s)
        
    elif isinstance(s, list):
        if len(s) > 1:
            return f'begin\n{indent(_ljoin(s))}\nend'
        else:
            return indent(s[0])


def _ljoin(strs: List[str] | str) -> str:
    """ returns the newline-concatenation of a list of strings into a single string.

    Example::

        >>> _ljoin(['string0', 'string1', 'string2'])
        'string0\nstring1\nstring2'

    Arguments:

    """
    if isinstance(strs, str):
        return strs
    else:
        return '\n'.join(strs)

class SVTxt(object):
    def __init__(self):
        self.txt = ""

    def sep(self, n : int = 1):
        self.txt += '\n'*n

    def add(self, f : str | List[str]):
        if isinstance(f, str):
            self.txt += f + '\n'
        else:
            self.txt += '\n'.join(f) + '\n'

    def addsp(self, f : str | List[str]):
        if isinstance(f, str):
            self.txt += f + ('\n'*2)
        else:
            self.txt += '\n'.join(f) + ('\n'*2)

    def to_module(self, name : str,
                  ios:        List[str] | str | None = None,
                  parameters: List[str] | str | None = None,
                  imports:    List[str] | str | None = None):
        
        self.txt = module(name, self.txt, ios, parameters, imports)


    def to_package(self, name : str):
        self.txt = package(name, self.txt)


    def to_sv_file(self, name : str,
                   path : str = '.',
                   desc : str = '',
                   prj : str | None = None):

        fname = name + '.svh'
        
        h = header(name, fname = fname, desc = desc, prj = prj)
        
        try:
            with open(os.path.join(path, fname), 'w') as fout:
                print(h + '\n' + self.txt, file = fout)
        except FileNotFoundError:
            log.error(f'SVTMP - cannot find {fname}. Exiting.')
            exit(1)
        except PermissionError:
            log.error(f'SVTMP - permission denied to open {fname}. Exiting.')
            exit(1)

    def to_svh_file(self, name : str,
                    path : str = '.',
                    desc : str = '',
                    prj : str | None = None,
                    noheader: bool = False):

        fname = os.path.join(path, name + '.svh')
        
        sguard = '_' + name.upper()+'_SVH_'
        
        if noheader:
            h = ''
        else:
            h = header(name = name, fname = name + '.svh', desc = desc, prj = prj)
        
        self.txt = ifndef(sguard) + '\n' + define(sguard) +'\n\n' + h + '\n' + self.txt + '\n`endif'

        try:
            with open(fname, 'w') as fout:
                print(self.txt, file = fout)
        except FileNotFoundError:
            log.error(f'SVTMP - cannot find {fname}. Exiting.')
            exit(1)
        except PermissionError:
            log.error(f'SVTMP - permission denied to open {fname}. Exiting.')
            exit(1)

