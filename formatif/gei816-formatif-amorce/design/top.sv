
/*
    Author(s) : Thomas Labbé, Gabriel Lessard
    Project : Sigma Delta DAQ
    
    Universite de Sherbrooke, 2021
*/
`timescale 1ns/1ps


/* verilator lint_off REDEFMACRO */
module top (
    input logic reset, clk, rx_uart_serial_in,
    output logic tx_uart_serial_out
);  



    //  mapping
    topvhdl inst_topvhdl(.reset(reset),
                               .clk(clk),
                               .rx_uart_serial_in(rx_uart_serial_in),
                               .tx_uart_serial_out(tx_uart_serial_out)
                               );

endmodule
