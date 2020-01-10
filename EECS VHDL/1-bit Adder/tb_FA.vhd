
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_FA is
end tb_FA;

architecture Behavioral of tb_FA is
    component FA is -- component declarations
    port (
        A2A1, B2B1: in STD_LOGIC_VECTOR;
        Cin: in STD_LOGIC;
        Sum2Sum1: out STD_LOGIC_VECTOR;
        Cout: out STD_LOGIC
    );
    end component;
    
    signal A, B: STD_LOGIC_VECTOR(1 downto 0) := "00"; -- signal declarations
    signal Cin: STD_LOGIC := '0';
    signal Sum: STD_LOGIC_VECTOR(1 downto 0);
    signal Cout: STD_LOGIC;
    
    
begin
    uut: FA -- component instantiation
    port map (
        A2A1 => A, -- signal mappings
        B2B1 => B,
        Cin => Cin,
        Sum2Sum1 => Sum,
        Cout => Cout
    );

    A <= "10", "01" after 5ns, "11" after 10ns;
    B <= "01", "00" after 5ns, "10" after 10ns;
    Cin <= '1', '0' after 10ns;

end Behavioral;
