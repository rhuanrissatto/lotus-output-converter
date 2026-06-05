# Conversor de output do Lotus Suspension Analysis para Excel
# Por Rhuan Rissatto Araújo - Equipe Fórmula UTFPR - 2026
# Contato: rrissatto08@gmail.com
#
# Objetivo:
# Automatizar a conversão dos arquivos de saída (.txt) do Lotus
# Suspension Analysis para planilhas Excel estruturadas.
#
# O sistema foi desenvolvido para tornar o pós-processamento das
# simulações mais rápido, prático e menos suscetível a erros humanos,
# substituindo o antigo processo de transcrição manual dos dados.
#
# Observação:
# Caso o formato de exportação do software seja alterado em outras
# versões, este código poderá necessitar de adaptações.

import sys
import pandas as pd
import re
import os

print("Cole aqui a tabela do Lotus na íntegra (pressione Ctrl+D+Enter no Linux/Mac ou Ctrl+Z+Enter no Windows para finalizar):")

tabela_sem_conversao = sys.stdin.read()

linhas_tabela = tabela_sem_conversao.splitlines()
front_suspension_linha = 0
rear_suspension_linha = 0
front_suspension_linha_bump = 0
rear_suspension_linha_bump = 0
front_suspension_linha_roll = 0
rear_suspension_linha_roll = 0
front_suspension_linha_steering = 0

hd_simulacao_steering_travel = ["Toe Angle RHS (deg)",
                                "Toe Angle LHS (deg)",
                                "Camber Angle RHS (deg)",
                                "Camber Angle LHS (deg)",
                                "Ackermann (%)",
                                "Turning Circle Radius (mm)"
]

hd_simulacao_incremental_bump = ["Anti Dive (%)",
                                 "Anti Squat (%)",
                                 "Roll Centre Height to Body (mm)",
                                 "Roll Centre Height to Grnd (mm)",
                                 "Half Track Change (mm)",
                                 "Wheelbase Change (mm)",
                                 "Damper Travel (mm)",
                                 "Spring Travel (mm)"
]

hd_simulacao_incremental_roll = ["Roll centre pos X (mm)",
                                 "Roll centre pos Y (mm)",
                                 "Roll centre pos Z (mm)",
                                 "Half Track Change (mm)",
                                 "Wheelbase Change (mm)",
                                 "Damper Travel (mm)",
                                 "Spring Travel (mm)"
]

hd_simulacao_r_b = ["Camber Angle (deg)",
                     "Toe Angle (deg)",
                     "Castor Angle (deg)",
                     "Kingpin Angle (deg)",
                     "Damper Ratio (-)",
                     "Spring Ratio (-)"]

pontos = ["Lower wishbone front pivot",
"Lower wishbone rear pivot",
"Lower wishbone outer ball joint",
"Upper wishbone front pivot",
"Upper wishbone rear pivot",
"Upper wishbone outer ball joint",
"Push rod wishbone end",
"Push rod rocker end",
"Outer track rod ball joint",
"Inner track rod ball joint",
"Damper to body point",
"Damper to rocker point",
"Wheel spindle point",
"Wheel centre point",
"Rocker axis 1st point",
"Rocker axis 2nd point",
"Part 1 C of G",
"Part 2 C of G",
"Part 3 C of G",
"Part 4 C of G",
"Part 5 C of G",
"Part 6 C of G"]

for i in enumerate(linhas_tabela):
    #print(i)
    if "FRONT SUSPENSION       FILENAME:" in i[1]:
        front_suspension_linha = i[0]
    if "REAR SUSPENSION       FILENAME:" in i[1]:
        rear_suspension_linha = i[0]
    if "FRONT SUSPENSION     -    BUMP TRAVEL" in i[1]:
        front_suspension_linha_bump = i[0]
    if "REAR SUSPENSION     -    BUMP TRAVEL" in i[1]:
        rear_suspension_linha_bump = i[0]
    if "FRONT SUSPENSION     -    ROLL" in i[1]:
        front_suspension_linha_roll = i[0]
    if "REAR SUSPENSION     -    ROLL" in i[1]:
        rear_suspension_linha_roll = i[0]
    if "FRONT SUSPENSION     -    STEERING TRAVEL" in i[1]:
        front_suspension_linha_steering = i[0]


#print(front_suspension_linha)
#print(rear_suspension_linha)

#Aquisição dos valores para as tabelas com regeX
coordenadas_dianteira = []
coordenadas_traseira = []
valores_bump_front = []
valores_bump_rear = []
valores_roll_front = []
valores_roll_rear = []
valores_steering_front = []
valores_incremental_front_bump = []
valores_incremental_rear_bump = []
valores_incremental_front_roll = []
valores_incremental_rear_roll = []

def pegar_valores(inicio, fim, array):
    for j in range(inicio, fim):
        array.append(re.findall(r"-?\d+\.\d+", linhas_tabela[j]))

pegar_valores(front_suspension_linha+6, front_suspension_linha+28, coordenadas_dianteira)
pegar_valores(rear_suspension_linha+6, rear_suspension_linha+28, coordenadas_traseira)
pegar_valores(front_suspension_linha_bump+12, front_suspension_linha_bump+24, valores_bump_front)
pegar_valores(front_suspension_linha_bump+35, front_suspension_linha_bump+47, valores_incremental_front_bump)
pegar_valores(rear_suspension_linha_bump+12, rear_suspension_linha_bump+24, valores_bump_rear)
pegar_valores(rear_suspension_linha_bump+35, rear_suspension_linha_bump+47, valores_incremental_rear_bump)
pegar_valores(front_suspension_linha_roll+12, front_suspension_linha_roll+31, valores_roll_front)
pegar_valores(front_suspension_linha_roll+40, front_suspension_linha_roll+59, valores_incremental_front_roll)
pegar_valores(rear_suspension_linha_roll+12, rear_suspension_linha_roll+31, valores_roll_rear)
pegar_valores(rear_suspension_linha_roll+40, rear_suspension_linha_roll+59, valores_incremental_rear_roll)
pegar_valores(front_suspension_linha_steering+11, front_suspension_linha_steering+32, valores_steering_front)

#Transformação dos vetores em dataframes, com suas headlines específicas
def formatar_array_sim(array, simulacao, restante_hd):
    sim = [simulacao]
    sim.extend(restante_hd)
    df = pd.DataFrame(array, columns=sim)
    df[sim] = df[sim].apply(pd.to_numeric)
    return df


dfSimulacaoRearBumpInc = formatar_array_sim(valores_incremental_rear_bump, "Bump Travel (mm)", hd_simulacao_incremental_bump)
dfSimulacaoFrontBumpInc = formatar_array_sim(valores_incremental_front_bump, "Bump Travel (mm)", hd_simulacao_incremental_bump)
dfSimulacaoFrontBump = formatar_array_sim(valores_bump_front, "Bump Travel (mm)", hd_simulacao_r_b)
dfSimulacaoRearBump = formatar_array_sim(valores_bump_rear, "Bump Travel (mm)", hd_simulacao_r_b)
dfSimulacaoFrontRoll = formatar_array_sim(valores_roll_front, "Roll Angle (deg)", hd_simulacao_r_b)
dfSimulacaoFrontRollInc = formatar_array_sim(valores_incremental_front_roll, "Roll Angle (deg)", hd_simulacao_incremental_roll)
dfSimulacaoRearRoll = formatar_array_sim(valores_roll_rear, "Roll Angle (deg)", hd_simulacao_r_b)
dfSimulacaoRearRollInc = formatar_array_sim(valores_incremental_rear_roll, "Roll Angle (deg)", hd_simulacao_incremental_roll)
dfSimulacaoFrontSteering = formatar_array_sim(valores_steering_front, "Rack Travel (mm)", hd_simulacao_steering_travel)

#print(dfSimulacaoFrontRollInc)
#print(dfSimulacaoFrontBumpInc)
#print(dfSimulacaoFrontSteering)
#print(dfSimulacaoRearRoll)

def formatar_array_coords(array):
    df = pd.DataFrame(array, columns=["X", "Y", "Z"])
    df[["X","Y","Z"]] = df[["X","Y","Z"]].apply(pd.to_numeric)
    df.insert(0, "Points", pontos)
    return df

dfCoordenadas_dianteira = formatar_array_coords(coordenadas_dianteira) 
dfCoordenadas_traseira = formatar_array_coords(coordenadas_traseira)

#print(dfCoordenadas_dianteira)
#print(dfCoordenadas_traseira)

#Confirmação do caminho de salvamento
pasta_script = os.path.dirname(os.path.abspath(sys.argv[0]))
caminho_excel = os.path.join(pasta_script, "lotus_output.xlsx")

#Escrita no Excel dos dataframes
with pd.ExcelWriter(caminho_excel, engine="openpyxl") as writer:
    
    dfCoordenadas_dianteira.to_excel(writer, sheet_name="Points Coordinates", startrow=0, startcol=0, index=False)

    dfCoordenadas_traseira.to_excel(writer, sheet_name="Points Coordinates",
                                     startrow=0, startcol=len(dfCoordenadas_dianteira.columns) + 2,
                                     index=False)
    
    dfSimulacaoFrontRoll.to_excel(writer, sheet_name="Front Roll", startrow=0, startcol = 0, index=False)

    dfSimulacaoFrontRollInc.to_excel(writer, sheet_name="Front Roll",
                                     startrow=len(dfSimulacaoFrontRoll)+2, startcol=0,
                                     index=False)
    
    dfSimulacaoRearRoll.to_excel(writer, sheet_name="Rear Roll",startrow=0,startcol=0, index=False)
    
    dfSimulacaoRearRollInc.to_excel(writer, sheet_name="Rear Roll",
                                    startrow=len(dfSimulacaoRearRoll)+2, startcol=0,
                                    index=False)

    dfSimulacaoFrontBump.to_excel(writer, sheet_name="Front Bump",startrow=0, startcol=0, index=False)

    dfSimulacaoFrontBumpInc.to_excel(writer, sheet_name="Front Bump",
                                     startrow=len(dfSimulacaoFrontBump) + 2, startcol=0,
                                     index=False)

    dfSimulacaoRearBump.to_excel(writer, sheet_name="Rear Bump", startrow=0, startcol=0, index=False)

    dfSimulacaoRearBumpInc.to_excel(writer, sheet_name="Rear Bump",
                                    startrow=len(dfSimulacaoRearBump) + 2, startcol=0,
                                    index = False)
    
    dfSimulacaoFrontSteering.to_excel(writer, sheet_name="Front Steering", index=False)

print(f"Arquivo salvo em:\n{caminho_excel}")
input("Pressione Enter para fechar...")
sys.exit()
