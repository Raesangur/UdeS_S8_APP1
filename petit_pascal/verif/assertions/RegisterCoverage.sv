//////////////////////////////////////////////////////////////////////
// Author  :    Marc-Andre Tetrault
// Project :    GEI815
//
// Universite de Sherbrooke
//////////////////////////////////////////////////////////////////////


// Bind statement usage in mixed-langage environments
//			https://www.youtube.com/watch?v=VuBqJoTRYyU


bind Registers RegisterBankCoverage u_RegisterBankCoverage(
	.cov_reset(reset),
	.cov_clk(clk),
	.cov_writeEnable(writeEnable),
	.cov_writeAck(writeAck),
	.cov_readEnable(readEnable),
	.cov_address(address)
	);

module RegisterBankCoverage
	//#(parameter g_ChannelId = 15)
	(
	input logic cov_reset,
	input logic cov_clk,
    input logic cov_writeEnable,
    input logic cov_readEnable,
    input logic cov_writeAck,
    input logic [7:0] cov_address
	);

default clocking DEFCLK @(posedge cov_clk);
endclocking

// Check that read strobes only 1 clock
property p_read_strobe_once;
	$rose(cov_readEnable) |=> $fell(cov_readEnable);
endproperty
ast_read_strobe_once : assert property(p_read_strobe_once);
cov_read_strobe_once : cover property(p_read_strobe_once);

// Check that write strobes only 1 clock
property p_write_ack_twice;
	$rose(cov_writeAck) |=> cov_writeAck ##1 $fell(cov_writeAck);
endproperty
ast_write_ack_twice : assert property(p_write_ack_twice);
cov_write_ack_twice : cover property(p_write_ack_twice);

// cover group: log if read and write access occured for all
// documented register address
// Lab: this covergroup will not work properly. Explore why and update.
covergroup covg_reg
    @(negedge cov_clk iff (!cov_reset && cov_readEnable || cov_writeEnable));
	option.name		= "cov_RegisterAccess";
    readMode      : coverpoint cov_readEnable{bins rm[] = {[1:1]}; }
    writeMode     : coverpoint cov_writeEnable{bins wm[] = {[1:1]}; }
    addressSpace  : coverpoint cov_address{bins as[] = {[0:9]}; }
    addressTime   : coverpoint cov_address{bins at[1] = {[10:$]}; }

    read_addressSpace  : cross readMode,  addressSpace;
    write_addressSpace : cross writeMode, addressSpace;

endgroup

covg_reg cov_userifCover = new();



// ----------------------------
// REG 5 - writeAck
property p_reg5a;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 0) |=> ##1 cov_writeAck;
endproperty
cov_reg5a : cover property(p_reg5a);
ast_reg5a : assert property(p_reg5a)
    else $display($stime,,,"\t\tREG5a::writeAck::writeAck didn't respond at address 0\n");

property p_reg5b;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 1) |=> ##1 cov_writeAck;
endproperty
cov_reg5b : cover property(p_reg5b);
ast_reg5b : assert property(p_reg5b)
    else $display($stime,,,"\t\tREG5b::writeAck::writeAck didn't respond at address 1\n");

property p_reg5c;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 2) |=> ##1 cov_writeAck;
endproperty
cov_reg5c : cover property(p_reg5c);
ast_reg5c : assert property(p_reg5c)
    else $display($stime,,,"\t\tREG5c::writeAck::writeAck didn't respond at address 2\n");
    
property p_reg5d;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 3) |=> ##1 cov_writeAck;
endproperty
cov_reg5d : cover property(p_reg5d);
ast_reg5d : assert property(p_reg5d)
    else $display($stime,,,"\t\tREG5d::writeAck::writeAck didn't respond at address 3\n");

property p_reg5e;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 4) |=> ##1 cov_writeAck;
endproperty
cov_reg5e : cover property(p_reg5e);
ast_reg5e : assert property(p_reg5e)
    else $display($stime,,,"\t\tREG5e::writeAck::writeAck didn't respond at address 4\n");

property p_reg5f;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 5) |=> ##1 cov_writeAck;
endproperty
cov_reg5f : cover property(p_reg5f);
ast_reg5f : assert property(p_reg5f)
    else $display($stime,,,"\t\tREG5f::writeAck::writeAck didn't respond at address 5\n");

property p_reg5g;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 6) |=> ##1 !cov_writeAck;
endproperty
cov_reg5g : cover property(p_reg5g);
ast_reg5g : assert property(p_reg5g)
    else $display($stime,,,"\t\tREG5g::writeAck::writeAck shouldn't respond at address 6\n");

property p_reg5h;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 7) |=> ##1 cov_writeAck;
endproperty
cov_reg5h : cover property(p_reg5h);
ast_reg5h : assert property(p_reg5h)
    else $display($stime,,,"\t\tREG5g::writeAck::writeAck didn't respond at address 7\n");

property p_reg5i;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 8) |=> ##1 cov_writeAck;
endproperty
cov_reg5i : cover property(p_reg5i);
ast_reg5i : assert property(p_reg5i)
    else $display($stime,,,"\t\tREG5i::writeAck::writeAck didn't respond at address 8\n");

property p_reg5j;
    @(posedge cov_clk) disable iff (cov_reset)
        $rose(cov_writeEnable) && (cov_address == 9) |=> ##1 !cov_writeAck;
endproperty
cov_reg5j : cover property(p_reg5j);
ast_reg5j : assert property(p_reg5j)
    else $display($stime,,,"\t\tREG5j::writeAck::writeAck shouldn't respond at address 9\n");


endmodule
