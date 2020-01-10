-- mux41.vhd
-- Lab:     2
-- Name:    Jordan Nguyen
-- TA:      Sadaf Sarafan

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
-- Define the input and output signals
entity mux41 is
port (
        A0, A1, A2, A3: in bit;
        S: in bit_vector;
        Cout: buffer bit);
end mux41;

-- Describe behavior of the Multiplexer (Selector)
architecture Behavioral of mux41 is
begin
    with S select
    Cout <= A0 when "00",
            A1 when "01",
            A2 when "10",
            A3 when "11";
end Behavioral;