-- tb_mux41.vhd
-- Lab:     2
-- Name:    Jordan Nguyen
-- TA:      Sadaf Sarafan

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_mux41 is
end tb_mux41;

architecture Behavioral of tb_mux41 is
    component mux41 is -- component declarations
        port (
                A0, A1, A2, A3: in bit;
                S: in bit_vector(1 downto 0);
                Cout: buffer bit);
    end component;
    
    -- signal declarations
    signal A0, A1, A2, A3: bit;
    signal S: bit_vector(1 downto 0);
    signal Cout: bit;
    
begin
    uut: mux41 -- component installation (uut = "unit under test" ?)
    port map (
        A0 => A0, -- signal mappings~original components connecting to signals
        A1 => A1,
        A2 => A2,
        A3 => A3,
        S(0) => S(0),
        S(1) => S(1),
        Cout => Cout);
    
    A0 <= '1';
    A1 <= '1';
    A2 <= '0';
    A3 <= '1';
    S(0) <= '1','0' after 20ns;
    S(1) <= '0','1' after 10ns;

end Behavioral;
