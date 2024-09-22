-- source : https://vhdlguru.blogspot.com/2020/12/synthesizable-clocked-square-root.html
--Synthesisable Design for Finding Square root of a number.
--
-- modified for the RT2024 cocotb workshop
-- modification: added valid flag bit for training purposes


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity sqrt_conv is
    port (
        clk : in std_logic;     --Clock
        reset : in std_logic;     --Asynchronous active high reset.
        arg : in unsigned(7 downto 0);  --this is the number for which we want to find square root.
		
		arg_valid       : in std_logic;
        sqrt_valid : out std_logic;   --This signal goes high when output is ready
        sqrt_res : out unsigned(3 downto 0)  --square root of 'arg'
    );
end sqrt_conv;

architecture Behav of sqrt_conv is

constant N : integer := 8;
signal sqrt_valid_internal : std_logic;
signal index : integer := 0;

signal r_sqrt_res :  unsigned(3 downto 0); --for SVA

begin

    sqrt_res <= r_sqrt_res;

    SQROOT_PROC : process(Clk,reset)
        variable a : unsigned(N-1 downto 0);  --original arg.
        variable left,right,r : unsigned(N/2+1 downto 0):=(others => '0');  --arg to adder/sub.r-remainder.
        variable q : unsigned(N/2-1 downto 0) := (others => '0');  --result.
        variable i : integer := 0;  --index of the loop. 
		variable calculating : boolean := false;
    begin
		
        if(reset = '1') then  --reset the variables.
            sqrt_valid_internal <= '0';
            r_sqrt_res <= (others => '0');
            i := 0;
            a := (others => '0');
            left := (others => '0');
            right := (others => '0');
            r := (others => '0');
            q := (others => '0');
			calculating := false;
        elsif(rising_edge(Clk)) then
			index <= i;
            --Before we start the first clock cycle get the 'arg' to the variable 'a'.
            if(arg_valid = '1' and calculating = false) then  
                a := arg;
				calculating := true;
                sqrt_valid_internal <= '0';    --reset 'sqrt_valid_internal' signal.
                i := i+1;   --increment the loop index.
            elsif(i < N/2 and calculating = true) then --keep incrementing the loop index.
                i := i+1;  
            end if;
			
			if(sqrt_valid_internal = '1') then
				sqrt_valid_internal <= '0';
			end if;
			
			if(calculating = true) then
				--These statements below are derived from the block diagram.
				right := q & r(N/2+1) & '1';
				left := r(N/2-1 downto 0) & a(N-1 downto N-2);
				a := a(N-3 downto 0) & "00";  --shifting left by 2 bit.
				if ( r(N/2+1) = '1') then   --add or subtract as per this bit.
					r := left + right;
				else
					r := left - right;
				end if;
				q := q(N/2-2 downto 0) & (not r(N/2+1));
				if(i = N/2) then    --This means the max value of loop index has reached. 
					sqrt_valid_internal <= '1';    --make 'sqrt_valid_internal' high because output is ready.
					i := 0; --reset loop index for beginning the next cycle.
					calculating := false;
					r_sqrt_res <= q;   --assign 'q' to the output port.
					--reset other signals for using in the next cycle.
					left := (others => '0');
					right := (others => '0');
					r := (others => '0');
					q := (others => '0');
				end if;
			end if;
        end if;    
    end process;
	
	sqrt_valid <= sqrt_valid_internal;

end architecture;