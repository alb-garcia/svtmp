import pytest
from svtmp import *

def test_header():
    hout = '/*------------------------------------------------------------------------------\n |  Title   : name\n |  Project : project\n +------------------------------------------------------------------------------\n |  Automatically generated with svtmp python library\n |\n +------------------------------------------------------------------------------\n |  Description:\n |  description\n +------------------------------------------------------------------------------\n | File     : name.sv\n | Language : SystemVerilog\n | Created  : 2022-11-02\n +------------------------------------------------------------------------------\n |  Copyright (c) Infineon Technologies AG 2022 -  Confidential\n +------------------------------------------------------------------------------\n */\n'
    assert hout == header('name', 'name.sv', 'description', 'project')

def test_numbers():

    with pytest.raises(ValueError):
        ui2b(16,2)
        
    with pytest.raises(ValueError):
        ui2b(0,0)

    assert ui2b(16,5) == "5'b10000"
    assert ui2b(1,8)  == "8'b00000001"
    assert ui2b(0,8)  == "8'b00000000"
    assert ui2b(255, 8) == "8'b11111111"

    with pytest.raises(ValueError):
        sui2b('16',2)
        
    with pytest.raises(ValueError):
        sui2b('0',0)

    assert sui2b('16',5) == "5'b10000"
    assert sui2b('1',8)  == "8'b00000001"
    assert sui2b('0',8)  == "8'b00000000"
    assert sui2b('255', 8) == "8'b11111111"

    with pytest.raises(ValueError):
        ui2h(16,2)
        
    with pytest.raises(ValueError):
        ui2h(0,0)

    assert ui2h(16,5) == "5'h10"
    assert ui2h(1,8)  == "8'h01"
    assert ui2h(0,8)  == "8'h00"
    assert ui2h(255, 8) == "8'hFF"

    with pytest.raises(ValueError):
        sui2h('16',2)
        
    with pytest.raises(ValueError):
        sui2h('0',0)

    assert sui2h('16',5) == "5'h10"
    assert sui2h('1',8)  == "8'h01"
    assert sui2h('0',8)  == "8'h00"
    assert sui2h('255', 8) == "8'hFF"

def test_cheader():
    ch =  "//------------------------------------------------------------------------------\n"
    ch += "// THIS IS A COMMENT HEADER\n"
    ch += "//------------------------------------------------------------------------------"
        
    assert cheader("THIS IS A COMMENT HEADER") == ch
        
    ch =  "//------------------------------------------------------------------------------\n"
    ch += "// \n"
    ch += "//------------------------------------------------------------------------------"
    
    assert cheader("") == ch

def test_ports():
    assert invec('data_i', 7, 0) == 'input logic [7:0] data_i'
    assert invec('data_i', 'DATA_WIDTH-1', 0) == 'input logic [DATA_WIDTH-1:0] data_i'
    assert invec('data_i', 0, 0) == 'input logic [0:0] data_i'
    assert invec('register', 3,0, typ = 'memory_t') == 'input memory_t [3:0] register'
    
    with pytest.raises(ValueError):
        assert invec('', 0, 0)
        
    assert outvec('data_i', 7, 0) == 'output logic [7:0] data_i'
    assert outvec('data_i', 'DATA_WIDTH-1', 0) == 'output logic [DATA_WIDTH-1:0] data_i'
    assert outvec('data_i', 0, 0) == 'output logic [0:0] data_i'
    assert outvec('register', 3,0, typ = 'memory_t') == 'output memory_t [3:0] register'
    
    with pytest.raises(ValueError):
        assert outvec('', 0, 0)

    assert Input('data_i') == 'input logic data_i'
    assert Input('data_i', typ = 'memory_t') == 'input memory_t data_i'
    
    with pytest.raises(ValueError):
        assert Input('')

    assert Output('data_i') == 'output logic data_i'
    assert Output('data_i', typ = 'memory_t') == 'output memory_t data_i'
    
    with pytest.raises(ValueError):
        assert Output('')

    assert inputs(['d1', 'd2', 'd3']) == ['input logic d1',
                                          'input logic d2',
                                          'input logic d3']

    assert outputs(['d1', 'd2', 'd3']) == ['output logic d1',
                                           'output logic d2',
                                           'output logic d3']

    assert inputs([]) == []
    assert outputs([]) == []

def test_declaration():
    assert logic('data') == 'logic data;'
    assert logic('data', 'this is a comment') == 'logic data; // this is a comment'    
    assert logvec('data', 'WIDTH - 1', 0) == 'logic [WIDTH - 1:0] data;'
    assert logvec('data', 'WIDTH - 1', 0, 'comment') == 'logic [WIDTH - 1:0] data; // comment'
    assert decl('memory_t', 'register', 'comment') == 'memory_t register; // comment'

def test_struct():
    sp  = "typedef struct packed {\n"
    sp += "   logic en;\n"
    sp += "   logic dis;\n"
    sp += "   logic [7:0] cnt;\n"
    sp += "} sfr_cnt_t;"

    s  = "typedef struct {\n"
    s += "   logic en;\n"
    s += "   logic dis;\n"
    s += "   logic [7:0] cnt;\n"
    s += "} sfr_cnt_t;"
    
    decls = [logic('en'), logic('dis'), logvec('cnt', 7,0)]
    str_decls = "logic en;\nlogic dis;\nlogic [7:0] cnt;"
    assert struct(typ = 'sfr_cnt_t', decls = decls) == sp
    assert struct(typ = 'sfr_cnt_t', decls = str_decls) == sp    
    assert struct(typ = 'sfr_cnt_t', decls = decls, packed  = False) == s
    assert struct(typ = 'sfr_cnt_t', decls = str_decls, packed = False) == s

    with pytest.raises(ValueError):
        struct(typ = 'dum', decls = [])

    with pytest.raises(ValueError):
        struct(typ = 'dum', decls = '')
    
