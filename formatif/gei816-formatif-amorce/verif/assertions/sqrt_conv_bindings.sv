//////////////////////////////////////////////////////////////////////
// Author  :    Marc-Andre Tetrault
// Project :    GEI815
//
// Universite de Sherbrooke
//////////////////////////////////////////////////////////////////////


// Bind statement usage in mixed-langage environments
//			https://www.youtube.com/watch?v=VuBqJoTRYyU

bind sqrt_conv sqrt_conv_bindings inst_sqrt_conv_bindings(
	.cov_reset(reset),
	.cov_clk(clk),

	.cov_arg(arg),
	.cov_arg_valid(arg_valid),
	.cov_sqrt_valid(sqrt_valid_internal),
	.cov_sqrt_res(r_sqrt_res)
	);

module sqrt_conv_bindings
	(
	input logic cov_reset,
	input logic cov_clk,

	// Entrees/Sorties
    input logic cov_arg_valid,
    input logic [7:0] cov_arg,
    input logic cov_sqrt_valid,
    input logic [3:0] cov_sqrt_res
	);

covergroup sqrt_covg @(posedge cov_clk);
    in_full  : coverpoint cov_arg;
    out_full : coverpoint cov_sqrt_res;
endgroup
sqrt_covg sqrt_cov = new();

default clocking DEFCLK @(posedge cov_clk);
endclocking

property q2_3;
    $rose(cov_arg_valid) |-> ##4 cov_sqrt_valid;
endproperty
cov_q2_3 : cover property(q2_3);
ass_q2_3 : assert property(q2_3);

// Voir aide mémoire pour covergroup et coverpoint



endmodule
