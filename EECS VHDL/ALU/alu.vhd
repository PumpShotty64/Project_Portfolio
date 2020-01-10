-- alu.vhd
-- Name: Jordan Nguyen 
-- Lab: Final Project
-- TA: Sadaf Sarafan

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;


entity alu is
    -- A (in): REVERSE, NOT, RROTATION, LROTATION
    -- C (out): ADDITION 
    -- A, B (in): MULTIPLICATION, XNOR
    -- C, D (out): MULTIPLICATION -- something about adding 6
    Port ( 
        CLK: in bit; -- Clk, and carry input
        S: in bit_vector (2 downto 0); -- Selector
        A, B: in bit_vector (3 downto 0); -- Input values
        Cout: buffer bit; -- carry out for adder
        D, C: buffer bit_vector (3 downto 0) -- C is the main output
    );
end alu;

architecture Behavioral of alu is

-- adder function
function f_CLA_4_bit(
    A, B: in bit_vector(3 downto 0)) 
    return bit_vector is
    variable Cn, Gn, Pn: bit_vector(3 downto 0);
    variable Sum: bit_vector(4 downto 0);
begin
    Sum(0) := A(0) xor B(0);
    for n in 0 to 3 loop
        Gn(n) := A(n) and B(n); -- Carry Generator
        Pn(n) := A(n) xor B(n); -- Carry Propogator
        if (n = 0) then
            Cn(n) := Gn(n); -- C0 expression
        else
            Cn(n) := Gn(n) or (Pn(n) and Cn(n-1)); -- Cn expression
            Sum(n) := A(n) xor B(n) xor Cn(n-1); -- Sum output
        end if;
    end loop;
    Sum(4) := Cn(3);
    return Sum; -- 5 bits
end function;

function f_CLA_8_bit(
    A, B: in bit_vector(7 downto 0)) 
    return bit_vector is
    variable Cn, Gn, Pn: bit_vector(7 downto 0);
    variable Sum: bit_vector(7 downto 0);
begin
    Sum(0) := A(0) xor B(0);
    for n in 0 to 7 loop
        Gn(n) := A(n) and B(n); -- Carry Generator
        Pn(n) := A(n) xor B(n); -- Carry Propogator
        if (n = 0) then
            Cn(n) := Gn(n); -- C0 expression
        else
            Cn(n) := Gn(n) or (Pn(n) and Cn(n-1)); -- Cn expression
            Sum(n) := A(n) xor B(n) xor Cn(n-1); -- Sum output
        end if;
    end loop;
    return Sum; -- 8 bits
end function;

-- Bit to Integer Converter
function f_bit_to_integer(
    B: in bit_vector(3 downto 0))
    return integer is
    variable Y: integer := 0;
begin
    for i in 0 to 3 loop
        if (B(i) = '1') then
            Y := Y + 2**i;
        else
            Y:= Y;
        end if;
    end loop;
    return Y;
end function;

begin
    
    process(CLK) 
    variable Sum: bit_vector(4 downto 0) := "00000";
    variable Sum8b: bit_vector(7 downto 0) := "00000000";
    variable Sum8b2: bit_vector(7 downto 0) := "00000000";
        begin
            -- 000 Add; 001 Reverse; 010 Mul; 011 Inc; 100 Xnor; 101 Not; 110 RRotation; 111 LRotation
            if (CLK'event and clk = '1') then
                if (S = "000") then -- ADD
                    Sum := f_CLA_4_bit(A, B);
                    C <= Sum(3 downto 0);
                    Cout <= Sum(4);
                elsif (S = "001") then -- REVERSE
                    C(3 downto 0) <= A(0) & A(1) & A(2) & A(3);
                elsif (S = "010") then -- MULTIPLY
                    Sum8b := "0000" & A;
                    for i in 2 to f_bit_to_integer(B) loop
                        Sum8b2 := f_CLA_8_bit(Sum8b, "0000" & A);
                        Sum8b := Sum8b2;
                    end loop;
                    C <= Sum8b(3 downto 0);
                    D <= Sum8b(7 downto 4);
                elsif (S = "011") then -- INCREMENT
                    Sum := f_CLA_4_bit(A, "0001");
                    C <= Sum(3 downto 0);
                    Cout <= Sum(4);
                elsif (S = "100") then -- XNOR
                    C <= A xnor B;
                elsif (S = "101") then -- NOT
                    C <= not A;
                elsif (S = "110") then -- RROTATION
                    C <= A(0) & A(3 downto 1);
                elsif (S = "111") then -- LROTATION
                    C <= A(2 downto 0) & A(3);
                end if;    
            end if;
    end process;
end Behavioral;
