-- mod21.vhd
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mod21 is
    Port ( 
        clk, dir, ebl, clr: in bit;
        q: buffer integer range 0 to 31
    );
end mod21;

architecture Behavioral of mod21 is

begin
process (clk)
    begin
        if (clr = '0') then
            q <= 0;
        elsif (ebl = '0') then
            q <= q;
        elsif (clk'event and dir = '0' and clk = '1') then
            if (q = 20) then
                q <= 0;
            else
                q <= q + 1;
            end if;
        elsif (clk'event and dir = '1' and clk = '1') then
            if (q = 0) then
                q <= 20;
            else
                q <= q - 1;
            end if;
        end if;
    end process;
end Behavioral;
