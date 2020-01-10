-- tb_mod32.vhd

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_mod32 is
--    Port ( );
end tb_mod32;

architecture Behavioral of tb_mod32 is

    component mod32 is
        port(
            clk, dir, ebl, clr: in bit;
            q: buffer integer range 0 to 31
        );
    end component;
    
    signal CLK, DIR, EBL, CLR: bit;
    signal Q: integer range 0 to 31;
    
    begin
    uut: mod32 port map(clk => CLK, dir => DIR, ebl => EBL, clr => CLR, q => Q);
    process
    begin
        wait for 40ns;
        if CLK = '0' then
            CLK <= '1';
        else
            CLK <= '0';
        end if;
    end process;
    DIR <= '1', '0' after 100ns;
    CLR <= '1', '0' after 100ns, '1' after 200ns;
    EBL <= '1', '0' after 300ns, '1' after 600ns;
end Behavioral;
