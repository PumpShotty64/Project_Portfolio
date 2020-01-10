-- elv_state.vhd
-- Name:    Jordan Nguyen
-- Lab:     Lab 4
-- TA:      Sadaf Sarafan


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity elv_state is
    port(
        clk: in bit;      
        a1, a2: in bit;
        q: buffer bit_vector(2 downto 0)
    );
end elv_state;

architecture Behavioral of elv_state is
type state_type is (S0, S1, S2, S3, S4, S5);
signal state: state_type;
begin
    process(clk)
        begin
            if (clk'event and clk = '1') then
                case state is
                    when S0 => state <= S1;
                    when S1 => state <= S2;
                    when S2 => 
                        if a1 = '1' then 
                            state <= S3; 
                        end if;
                    when S3 => state <= S4;
                    when S4 => state <= S5;
                    when S5 => 
                        if a2 = '1' then
                            state <= S0;
                        end if;
                end case;
            end if;
    end process;
    with state select
        q <="000" when S0,
            "100" when S1,       
            "101" when S2,       
            "010" when S3,       
            "110" when S4,       
            "111" when S5;       
end Behavioral;
