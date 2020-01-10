-- tb_mux161.vhd
-- Lab:     2
-- Name:    Jordan Nguyen
-- TA:      Sadaf Sarafan

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_mux161 is
end tb_mux161;

architecture Behavioral of tb_mux161 is
    Component mux161 is
        port (
            a : in bit_vector(15 downto 0);
            sa, sb : in bit_vector(1 downto 0);
            cout : buffer bit
            );
    end component;
    
    signal A : bit_vector(15 downto 0);
    signal SA, SB : bit_vector(1 downto 0);
    signal Cout : bit;
    
begin
    uut: mux161 port map(A, SA, SB, Cout);
    A <= x"7dab"; 
    SA <= "11", "10" after 20ns;
    SB <= "00", "10" after 20ns, "11" after 40ns;
end Behavioral;
