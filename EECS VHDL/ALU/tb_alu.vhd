-- tb_alu.vhd

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;


entity tb_alu is
end tb_alu;

architecture Behavioral of tb_alu is
component alu is
    port (
        CLK: in bit;
        S: in bit_vector (2 downto 0);
        A, B: in bit_vector (3 downto 0);
        Cout: buffer bit;
        D, C: buffer bit_vector (3 downto 0)
    );
end component;
signal clk: bit;
signal s: bit_vector (2 downto 0);
signal a, b, d, c: bit_vector (3 downto 0);
signal cout: bit;
begin
    uut: alu 
    port map (
        clk => CLK,
        s => S,
        a => A,
        b => B,
        d => D,
        c => C,
        cout => Cout
    );
    
    process begin
        wait for 50ns;
        if CLK = '0' then
            CLK <= '1';
        else
            CLK <= '0';
        end if;
    end process;
    -- A (in): REVERSE, NOT, RROTATION, LROTATION
    -- C (out): ADDITION 
    -- A, B (in): MULTIPLICATION, XNOR
    -- C, D (out): MULTIPLICATION -- something about adding 6
    a <= "1000";
    b <= "0110";
    -- 000 Add; 001 Reverse; 010 Mul; 011 Inc; 100 Xnor; 101 Not; 110 RRotation; 111 LRotation
    s <= "000",
         "001" after 100ns,
         "010" after 200ns,
         "011" after 300ns,
         "100" after 400ns,
         "101" after 500ns,
         "110" after 600ns,
         "111" after 700ns;
    
end Behavioral;
