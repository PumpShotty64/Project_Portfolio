-- mod32.vhd
-- notes: t-flip flop connecting q1 to clk leads to decrement
--        t-flip flop connecting ~q1 to clk leads to increment
-- t-flip flop is a toggle flip flop
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mod32 is
    Port ( 
        clk, dir, ebl, clr: in bit;
        q: buffer integer range 0 to 31
    );
end mod32;

architecture Behavioral of mod32 is

begin
process (clk)
    begin
        if (clr = '0') then
            q <= 0;
        elsif (ebl = '0') then
            q <= q;
        elsif (clk'event and dir = '0' and clk = '1') then
            if (q = 31) then
                q <= 0;
            else
                q <= q + 1;
            end if;
        elsif (clk'event and dir = '1' and clk = '1') then
            if (q = 0) then
                q <= 31;
            else
                q <= q - 1;
            end if;
        end if;
    end process;
end Behavioral;
