-- tb_elv_state.vhd

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;


entity tb_elv_state is
end tb_elv_state;

architecture Behavioral of tb_elv_state is
    component elv_state is
        port (
          clk: in bit;
          a1, a2: in bit;
          q: buffer bit_vector(2 downto 0)  
        );
    end component;
    
    signal CLK: bit;
    signal A1, A2: bit;
    signal Q: bit_vector(2 downto 0);
    
    begin
        uut: elv_state
        port map(
            clk => CLK, a1 => A1, a2 => A2, q => Q
        );
        process
            begin
                wait for 40ns;
                if CLK = '0' then
                    CLK <= '1';
                else
                    CLK <= '0';
                end if;
        end process;
        process
            begin
                wait for 50ns;
                    if A1 = '0' then
                        A1 <= '1';
                    else
                        A1 <= '0';
                    end if;
                    if A2 = '0' then
                        A2 <= '1';
                    else
                        A2 <= '0';
                    end if;
        end process;
end Behavioral;
