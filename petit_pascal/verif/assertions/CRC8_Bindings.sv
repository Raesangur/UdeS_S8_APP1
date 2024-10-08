//////////////////////////////////////////////////////////////////////
// Author  :    Marc-Andre Tetrault
// Project :    GEI815
//
// Universite de Sherbrooke
//////////////////////////////////////////////////////////////////////


bind CRC8816 CRC8_Bindings inst_CRC8_Bindings(
        .cov_reset(reset),
        .cov_clk(clk),

        .cov_valid(i_valid),
        .cov_last(i_last),
        .cov_data(i_data),

        .cov_match(o_match),
        .cov_done(o_done),
        .cov_crc8(o_crc8)
	);

module CRC8_Bindings
	(
	input logic cov_reset,
	input logic cov_clk,

    input logic cov_valid,
    input logic cov_last,
    input logic [7:0] cov_data,

    input logic cov_match,
    input logic cov_done,
    input logic [7:0] cov_crc8
	);

default clocking DEFCLK @(posedge cov_clk);
endclocking


// ----------------------------
// cover tests for all IOs
covergroup covg_crc8
    @(posedge cov_clk);
	option.name		= "cov_crc8";
    reset : coverpoint cov_reset;
    valid : coverpoint cov_valid; // CRC 2.a
    last  : coverpoint cov_last;  // CRC 3.a
    data  : coverpoint cov_data;  // CRC 4.a

    rst_valid  : cross reset, valid;
    rst_last   : cross reset, last;
    rst_data   : cross reset, data;
    last_valid : cross last, valid;

    match : coverpoint cov_match;
    done  : coverpoint cov_done;
    crc   : coverpoint cov_crc8; // CRC 7.a

    match_done : cross match, done;
endgroup


// ----------------------------
// CRC 1 - i_reset
// CRC 1.a - o_match becomes 0
property p_crc1a;
    @(posedge cov_clk) $rose(cov_reset) |=> (cov_match == 0);
endproperty
cov_crc1a : cover property(p_crc1a);
ast_crc1a : assert property(p_crc1a)
    else $display($stime,,,"\t\tCRC1a::i_reset::o_match didn't go to 0\n");

// CRC 1.b - o_done becomes 0
property p_crc1b;
    @(posedge cov_clk) $rose(cov_reset) |=> (cov_done == 0);
endproperty
cov_crc1b : cover property(p_crc1b);
ast_crc1b : assert property(p_crc1b)
    else $display($stime,,,"\t\tCRC1b::i_reset::o_done didn't go to 0\n");

// CRC 1.c - o_crc8 becomes 0x0D
property p_crc1c;
    @(posedge cov_clk) $rose(cov_reset) |=> (cov_crc8 == 8'h0D);
endproperty
cov_crc1c : cover property(p_crc1c);
ast_crc1c : assert property(p_crc1c)
    else $display($stime,,,"\t\tCRC1c::i_reset::o_crc8 didn't go to 0x0D\n");


// ----------------------------
// CRC 3 - i_last
// CRC 3.b - i_last always at the same time as i_valid
property p_crc3b;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_last) |-> cov_valid;
endproperty
cov_crc3b : cover property(p_crc3b);
ast_crc3b : assert property(p_crc3b)
    else $display($stime,,,"\t\tCRC3b::i_last::i_last didn't rise at the same time as i_valid\n");


// ----------------------------
// CRC 5 - o_done
// CRC 5.a - Rises 1-2 clock cycles after i_last
property p_crc5a;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_last) |-> ##[1:2] $rose(cov_done);
endproperty
cov_crc5a : cover property(p_crc5a);
ast_crc5a : assert property(p_crc5a)
    else $display($stime,,,"\t\tCRC5a::o_done::o_done didn't rise 2 clock cycles after i_last\n");



// ----------------------------
// CRC 6 - o_match
// CRC 6.a - o_match asserts at the same time as o_done
property p_crc6a;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_match) |-> $rose(cov_done);
endproperty
cov_crc6a : cover property(p_crc6a);
ast_crc6a : assert property(p_crc6a)
    else $display($stime,,,"\t\tCRC6a::o_match::o_match didn't rise at the same time as o_done\n");

// CRC 5.b - o_match asserts only one clock cycle after o_crc is 0x00
property p_crc6b;
    @(posedge cov_clk) disable iff (cov_reset)
        cov_crc8 == 8'h0 |=> $rose(cov_match);
endproperty
cov_crc6b : cover property(p_crc6b);
ast_crc6b : assert property(p_crc6b)
    else $display($stime,,,"\t\tCRC6b::o_match::o_match didn't trigger when o_crc is 0x00\n");



// ----------------------------
// CRC 7 - o_crc8
// CRC 7.b - o_crc8 doesn't change when i_valid is 0
property p_crc7b;
    @(posedge cov_clk) disable iff (cov_reset)
        !cov_valid |=> $stable(cov_crc8);
endproperty
cov_crc7b : cover property(p_crc7b);
ast_crc7b : assert property(p_crc7b)
    else $display($stime,,,"\t\tCRC7b::o_crc8::o_crc8 changed when i_valid was 0\n");


endmodule
