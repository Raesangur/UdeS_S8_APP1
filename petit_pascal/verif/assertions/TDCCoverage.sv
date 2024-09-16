//////////////////////////////////////////////////////////////////////
// Author  :    Marc-Andre Tetrault
// Project :    GEI815
//
// Universite de Sherbrooke
//////////////////////////////////////////////////////////////////////


bind TDC_dumb TDCCoverage inst_TDCCoverage(
	.cov_reset(reset),
	.cov_clk(clk),
	.cov_hasEvent(o_hasEvent),
	.cov_busy(o_busy),
	.cov_clear(i_clear),
	.cov_trigger(i_trigger),
	.cov_enable(i_enable_channel),
	.cov_TOT(o_pulseWidth),
	.cov_TS(o_timestamp)
	);

module TDCCoverage
	
	(
	input logic cov_reset,
	input logic cov_clk,
    	input logic cov_hasEvent,
	input logic cov_busy,
	input logic cov_clear,
    	input logic cov_trigger,
	input logic cov_enable,
	input logic [31:0] cov_TOT,
	input logic [31:0] cov_TS
	);

default clocking DEFCLK @(posedge cov_clk);
endclocking


// ----------------------------
// Coverage tests for all IOs
covergroup covg_tdc
    @(posedge cov_clk);
	option.name		= "cov_tdc";
    reset   : coverpoint cov_reset;
    trigger : coverpoint cov_trigger; 
    enable  : coverpoint cov_enable;
    clear   : coverpoint cov_clear;

    rst_trigger : cross reset, trigger;
    rst_enable  : cross reset, enable;
    rst_clear   : cross reset, clear;
    en_trigger  : cross enable, trigger;
    en_clear    : cross enable, clear;

    busy       : coverpoint cov_busy;
    hasEvent   : coverpoint cov_hasEvent;
    timestamp  : coverpoint cov_TS;
    pulseWidth : coverpoint cov_TOT;
endgroup


/*
// ----------------------------
// TDC 1 - i_reset
// TDC 1.a - o_busy becomes 0
property p_tdc1a;
    @(posedge cov_clk) cov_reset |=> ##1 (cov_busy == 0);
endproperty
cov_tdc1a : cover property(p_tdc1a);
ast_tdc1a : assert property(p_tdc1a)
    else $display($stime,,,"\t\tTDC1a::i_reset::o_busy didn't go to 0\n");

// TDC 1.b - o_hasEvent becomes 0
property p_tdc1b;
    @(posedge cov_clk) cov_reset |=> ##1 (cov_hasEvent == 0);
endproperty
cov_tdc1b : cover property(p_tdc1b);
ast_tdc1b : assert property(p_tdc1b)
    else $display($stime,,,"\t\tTDC1b::i_reset::o_hasEvent didn't go to 0\n");

// TDC 1.c - o_timestamp becomes 0
property p_tdc1c;
    @(posedge cov_clk) cov_reset |=> ##1 (cov_TS == 0);
endproperty
cov_tdc1c : cover property(p_tdc1c);
ast_tdc1c : assert property(p_tdc1c)
    else $display($stime,,,"\t\tTDC1c::i_reset::o_timestamp didn't go to 0\n");

// TDC 1.d - o_busy becomes 0
property p_tdc1d;
    @(posedge cov_clk) cov_reset |=> ##1 (cov_TOT == 0);
endproperty
cov_tdc1d : cover property(p_tdc1d);
ast_tdc1d : assert property(p_tdc1d)
    else $display($stime,,,"\t\tTDC1d::i_reset::o_pulseWidth didn't go to 0\n");


// ----------------------------
// CRC 2 - i_enableChannel
// TDC 2.b - All outputs remains the same
property p_tdc2b;
    @(posedge cov_clk) disable iff (!cov_reset)
        cov_enable == 0 |=> ##1 $stable(cov_busy) && $stable(cov_hasEvent)
                                   && $stable(cov_TS) && $stable(cov_TOT);
endproperty
cov_tdc2b : cover property(p_tdc2b);
ast_tdc2b : assert property(p_tdc2b)
    else $display($stime,,,"\t\tTDC2b::i_enableChannel::Some outputs changed while tdc was disabled\n");


// ----------------------------
// CRC 3 - o_busy
// TDC 3.a - o_busy rises when interpolation begins
property p_tdc3a;
    @(posedge cov_clk) disable iff (cov_reset || !cov_enable)
        cov_trigger |=> ##1 cov_busy;
endproperty
cov_tdc3a : cover property(p_tdc3a);
ast_tdc3a : assert property(p_tdc3a)
    else $display($stime,,,"\t\tTDC3a::o_busy::o_busy didn't rise after a trigger\n");

// TDC 5.a - o_busy falls 
property p_tdc5a;
    @(posedge cov_clk) disable iff (cov_reset || !cov_enable)
        $fell(cov_trigger) |=> ##20 !cov_busy;
endproperty
cov_tdc5a : cover property(p_tdc5a);
ast_tdc5a : assert property(p_tdc5a)
    else $display($stime,,,"\t\tTDC5a::o_busy::o_busy fall within 20 clock cycles of the end of the trigger\n");

// TDC 5.a - o_hasEvent rises
property p_tdc5b;
    @(posedge cov_clk) disable iff (cov_reset || !cov_enable)
        $fell(cov_trigger) |=> ##1 cov_hasEvent;
endproperty
cov_tdc5b : cover property(p_tdc5b);
ast_tdc5b : assert property(p_tdc5b)
    else $display($stime,,,"\t\tTDC5b::o_hasEvent::o_hasEvent rises after trigger falls\n");


// ----------------------------
// CRC 6 - i_clear
// TDC 6.a - o_hasEvent can be cleared
property p_tdc6a;
    @(posedge cov_clk) disable iff (cov_reset || !cov_enable)
        cov_clear |=> ##1 !cov_hasEvent;
endproperty
cov_tdc6a : cover property(p_tdc6a);
ast_tdc6a : assert property(p_tdc6a)
    else $display($stime,,,"\t\tTDC6a::i_clear::o_hasEvent didn't clear\n");

// TDC 6.b - o_timestamp can be cleared
property p_tdc6b;
    @(posedge cov_clk) disable iff (cov_reset || !cov_enable)
        cov_clear |=> ##1 cov_TS == 32'h0;
endproperty
cov_tdc6b : cover property(p_tdc6b);
ast_tdc6b : assert property(p_tdc6b)
    else $display($stime,,,"\t\tTDC6a::i_clear::o_timestamp didn't clear\n");

// TDC 6.c - o_busy can be cleared
property p_tdc6c;
    @(posedge cov_clk) disable iff (cov_reset || !cov_enable)
        cov_clear |=> ##1 !cov_busy;
endproperty
cov_tdc6c : cover property(p_tdc6c);
ast_tdc6c : assert property(p_tdc6c)
    else $display($stime,,,"\t\tTDC6c::o_busy::o_hasEvent didn't clear\n");

// TDC 6.d - o_pulseWidth can be cleared
property p_tdc6d;
    @(posedge cov_clk) disable iff (cov_reset || !cov_enable)
        cov_clear|=> ##1 cov_TOT == 32'h0;
endproperty
cov_tdc6d : cover property(p_tdc6d);
ast_tdc6d : assert property(p_tdc6d)
    else $display($stime,,,"\t\tTDC6d::i_clear::o_pulseWidth didn't clear\n");

*/

endmodule

