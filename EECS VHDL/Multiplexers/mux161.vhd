-- mux161.vhd
-- Lab:     2
-- Name:    Jordan Nguyen
-- TA:      Sadaf Sarafan

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mux161 is
    port(
        a : in bit_vector(15 downto 0);
        sa, sb : in bit_vector;
        cout : buffer bit
    );
end mux161;

architecture Behavioral of mux161 is
    component mux41 is -- component declarations
        port (
                A0, A1, A2, A3: in bit;
                S: in bit_vector;
                Cout: buffer bit);
    end component;
    signal c: bit_vector(3 downto 0);
begin
    u1: mux41 port map (a(0), a(1), a(2), a(3), sa, c(0));
    u2: mux41 port map (a(4), a(5), a(6), a(7), sa, c(1));
    u3: mux41 port map (a(8), a(9), a(10), a(11), sa, c(2));
    u4: mux41 port map (a(12), a(13), a(14), a(15), sa, c(3));
    u5: mux41 port map (c(0), c(1), c(2), c(3), sb, cout);

end Behavioral;
