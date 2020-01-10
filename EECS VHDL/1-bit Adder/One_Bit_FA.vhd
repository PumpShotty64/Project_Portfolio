library IEEE;
use IEEE.std_logic_1164.all;

-- Define the input and output signals

entity One_Bit_FA is
port (
        A, B, Cin: in std_logic;
        Sum, Cout: out std_logic);
end One_Bit_FA;

-- Describe the one-bit full adder's behavior

architecture FA1 of One_Bit_FA is
begin
        Sum <= A xor B xor Cin;
        Cout <= (A and B) or (A and Cin) or (B and Cin); 
end FA1;
