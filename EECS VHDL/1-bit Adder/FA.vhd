-- Lab:     1
-- Name:    Jordan Nguyen
-- TA:      Sadaf Sarafan

library IEEE;
use IEEE.std_logic_1164.all;

-- Define the input and output signals

entity FA is
port (
        A2A1, B2B1: in std_logic_vector(1 downto 0);
        Cin: in std_logic;
        Sum2Sum1: out std_logic_vector(1 downto 0);
        Cout: out std_logic);
end FA;

-- Describe the two-bit full adder's behavior

architecture FA1 of FA is
signal tempCout: std_logic;
begin
        Sum2Sum1(0) <= A2A1(0) xor B2B1(0) xor Cin;
        tempCout <= (A2A1(0) and B2B1(0)) or (A2A1(0) and Cin) or (B2B1(0) and Cin); 
        Sum2Sum1(1) <= A2A1(1) xor B2B1(1) xor tempCout;
        Cout <= (A2A1(1) and B2B1(1)) or (A2A1(1) and tempCout) or (B2B1(1) and tempCout); 
end FA1;
