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

default clocking DEFCLK @(posedge cov_clk);
endclocking

//property p_NomPropriete;
//	description de sequence;
//endproperty
//cov_NomCouverture : cover property(p_NomPropriete);

// Voir aide mémoire pour covergroup et coverpoint



endmodule
