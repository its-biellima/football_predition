import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.stats import poisson


# Função para calcular a probabilidade com base nos jogos
def calcular_probabilidades(vitorias_a, derrotas_a, empates_a, gols_a_marcados, gols_a_sofridos,
                            vitorias_b, derrotas_b, empates_b, gols_b_marcados, gols_b_sofridos):
    
    total_jogos_a = vitorias_a + derrotas_a + empates_a
    total_jogos_b = vitorias_b + derrotas_b + empates_b

    # Probabilidade do time A vencer com base em seus jogos
    prob_vitoria_a = vitorias_a / total_jogos_a
    prob_empate_a = empates_a / total_jogos_a

    # Probabilidade do time B vencer com base em seus jogos
    prob_vitoria_b = vitorias_b / total_jogos_b
    prob_empate_b = empates_b / total_jogos_b

    # Ajuste com base nos gols marcados e sofridos
    media_gols_a = (gols_a_marcados - gols_a_sofridos) / total_jogos_a
    media_gols_b = (gols_b_marcados - gols_b_sofridos) / total_jogos_b

    # Ajustando probabilidades com base nas médias de gols
    ajuste_a = 1 + max(0, media_gols_a / total_jogos_a)  # Evita valores negativos
    ajuste_b = 1 + max(0, media_gols_b / total_jogos_b)

    prob_vitoria_a *= ajuste_a
    prob_vitoria_b *= ajuste_b

    # Ajustando para empate considerando ambas as equipes
    prob_empate = (prob_empate_a + prob_empate_b) / 2

    # Reajustar probabilidades para somar 1
    soma_prob = prob_vitoria_a + prob_vitoria_b + prob_empate
    prob_vitoria_a /= soma_prob
    prob_vitoria_b /= soma_prob
    prob_empate /= soma_prob

    return prob_vitoria_a, prob_vitoria_b, prob_empate


# Função para prever um possível placar usando o modelo de Poisson
def prever_placar_poisson(prob_vitoria_a, prob_vitoria_b, media_gols_a_marcados, media_gols_a_sofridos, media_gols_b_marcados, media_gols_b_sofridos):
    # Calculando a média de gols por jogo para cada time
    media_gols_time_a = (media_gols_a_marcados + media_gols_b_sofridos) / 2 * prob_vitoria_a
    media_gols_time_b = (media_gols_b_marcados + media_gols_a_sofridos) / 2 * prob_vitoria_b

    # Usando a distribuição de Poisson para prever o número de gols de cada time
    gols_time_a = np.random.poisson(media_gols_time_a)
    gols_time_b = np.random.poisson(media_gols_time_b)

    # Ajustando os resultados para que estejam mais alinhados com as probabilidades
    gols_time_a = int(np.clip(np.round(gols_time_a + (0.5 * prob_vitoria_a * (gols_time_a - gols_time_b))), 0, 10))
    gols_time_b = int(np.clip(np.round(gols_time_b + (0.5 * prob_vitoria_b * (gols_time_b - gols_time_a))), 0, 10))

    return gols_time_a, gols_time_b


# Função para processar os dados e calcular probabilidades
def processar_dados():
    try:
        # Obtendo os valores inseridos pelo usuário
        nome_time_a = entry_time_a.get()
        nome_time_b = entry_time_b.get()
        
        vitorias_a = int(entry_vitorias_a.get())
        empates_a = int(entry_empates_a.get())
        derrotas_a = int(entry_derrotas_a.get())
        gols_a_marcados = int(entry_gols_a_marcados.get())
        gols_a_sofridos = int(entry_gols_a_sofridos.get())
        
        vitorias_b = int(entry_vitorias_b.get())
        empates_b = int(entry_empates_b.get())
        derrotas_b = int(entry_derrotas_b.get())
        gols_b_marcados = int(entry_gols_b_marcados.get())
        gols_b_sofridos = int(entry_gols_b_sofridos.get())
        
        # Calculando probabilidades
        prob_a, prob_b, prob_empate = calcular_probabilidades(vitorias_a, derrotas_a, empates_a, gols_a_marcados, gols_a_sofridos,
                                                              vitorias_b, derrotas_b, empates_b, gols_b_marcados, gols_b_sofridos)
        
        # Prevendo o placar
        placar_a, placar_b = prever_placar_poisson(prob_a, prob_b, gols_a_marcados / 10, gols_a_sofridos / 10, gols_b_marcados / 10, gols_b_sofridos / 10)
        
        # Preparando a mensagem de resultado
        resultado_msg = (
            f"Probabilidades:\n"
            f"Vitória do {nome_time_a}: {prob_a * 100:.2f}%\n"
            f"Vitória do {nome_time_b}: {prob_b * 100:.2f}%\n"
            f"Empate: {prob_empate * 100:.2f}%\n\n"
            f"Previsão de placar: {nome_time_a} {placar_a} x {placar_b} {nome_time_b}"
        )

        # Exibindo os resultados em uma messagebox
        messagebox.showinfo("Resultados da Análise", resultado_msg)
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")


# Função para limpar os campos de entrada
def limpar_campos():
    entry_time_a.delete(0, tk.END)
    entry_time_b.delete(0, tk.END)
    entry_vitorias_a.delete(0, tk.END)
    entry_empates_a.delete(0, tk.END)
    entry_derrotas_a.delete(0, tk.END)
    entry_gols_a_marcados.delete(0, tk.END)
    entry_gols_a_sofridos.delete(0, tk.END)
    entry_vitorias_b.delete(0, tk.END)
    entry_empates_b.delete(0, tk.END)
    entry_derrotas_b.delete(0, tk.END)
    entry_gols_b_marcados.delete(0, tk.END)
    entry_gols_b_sofridos.delete(0, tk.END)


# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Previsão de Partida")
root.geometry("600x600")
root.configure(bg='#f0f0f0')

# Título
titulo = tk.Label(root, text="Previsão de Partida de Futebol", font=("Helvetica", 16, "bold"), bg='#f0f0f0')
titulo.pack(pady=10)

# Frame para dados do time A
frame_time_a = tk.Frame(root, bg='#f0f0f0')
frame_time_a.pack(pady=5)
tk.Label(frame_time_a, text="Dados do Time A", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=0, column=0, columnspan=2)

entry_time_a = tk.Entry(frame_time_a)
tk.Label(frame_time_a, text="Nome do Time A:", bg='#f0f0f0').grid(row=1, column=0, sticky='e')
entry_time_a.grid(row=1, column=1)

entry_vitorias_a = tk.Entry(frame_time_a)
tk.Label(frame_time_a, text="Vitórias:", bg='#f0f0f0').grid(row=2, column=0, sticky='e')
entry_vitorias_a.grid(row=2, column=1)

entry_empates_a = tk.Entry(frame_time_a)
tk.Label(frame_time_a, text="Empates:", bg='#f0f0f0').grid(row=3, column=0, sticky='e')
entry_empates_a.grid(row=3, column=1)

entry_derrotas_a = tk.Entry(frame_time_a)
tk.Label(frame_time_a, text="Derrotas:", bg='#f0f0f0').grid(row=4, column=0, sticky='e')
entry_derrotas_a.grid(row=4, column=1)

entry_gols_a_marcados = tk.Entry(frame_time_a)
tk.Label(frame_time_a, text="Gols Marcados:", bg='#f0f0f0').grid(row=5, column=0, sticky='e')
entry_gols_a_marcados.grid(row=5, column=1)

entry_gols_a_sofridos = tk.Entry(frame_time_a)
tk.Label(frame_time_a, text="Gols Sofridos:", bg='#f0f0f0').grid(row=6, column=0, sticky='e')
entry_gols_a_sofridos.grid(row=6, column=1)

# Frame para dados do time B
frame_time_b = tk.Frame(root, bg='#f0f0f0')
frame_time_b.pack(pady=5)
tk.Label(frame_time_b, text="Dados do Time B", font=("Helvetica", 12, "bold"), bg='#f0f0f0').grid(row=0, column=0, columnspan=2)

entry_time_b = tk.Entry(frame_time_b)
tk.Label(frame_time_b, text="Nome do Time B:", bg='#f0f0f0').grid(row=1, column=0, sticky='e')
entry_time_b.grid(row=1, column=1)

entry_vitorias_b = tk.Entry(frame_time_b)
tk.Label(frame_time_b, text="Vitórias:", bg='#f0f0f0').grid(row=2, column=0, sticky='e')
entry_vitorias_b.grid(row=2, column=1)

entry_empates_b = tk.Entry(frame_time_b)
tk.Label(frame_time_b, text="Empates:", bg='#f0f0f0').grid(row=3, column=0, sticky='e')
entry_empates_b.grid(row=3, column=1)

entry_derrotas_b = tk.Entry(frame_time_b)
tk.Label(frame_time_b, text="Derrotas:", bg='#f0f0f0').grid(row=4, column=0, sticky='e')
entry_derrotas_b.grid(row=4, column=1)

entry_gols_b_marcados = tk.Entry(frame_time_b)
tk.Label(frame_time_b, text="Gols Marcados:", bg='#f0f0f0').grid(row=5, column=0, sticky='e')
entry_gols_b_marcados.grid(row=5, column=1)

entry_gols_b_sofridos = tk.Entry(frame_time_b)
tk.Label(frame_time_b, text="Gols Sofridos:", bg='#f0f0f0').grid(row=6, column=0, sticky='e')
entry_gols_b_sofridos.grid(row=6, column=1)

# Botões para calcular e limpar
btn_calcular = tk.Button(root, text="Calcular Previsão", command=processar_dados, bg='#4caf50', fg='white', font=("Helvetica", 12))
btn_calcular.pack(pady=15)

btn_limpar = tk.Button(root, text="Limpar Campos", command=limpar_campos, bg='#f44336', fg='white', font=("Helvetica", 12))
btn_limpar.pack(pady=5)

# Iniciar o loop da interface
root.mainloop()
