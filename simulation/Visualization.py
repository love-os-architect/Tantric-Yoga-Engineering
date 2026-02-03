# --- 4. Visualization (The Evidence) ---
df = pd.DataFrame(history)

# Setup the plot
fig, ax1 = plt.subplots(figsize=(14, 7))
plt.title('Love-OS: The Physics of "Sudden" Success\n(Integration of Invisible Value -> Phase Transition)', fontsize=16)

# Plot 1: The Hidden Accumulation (Blue)
color_love = 'tab:blue'
ax1.set_xlabel('Time (Days)', fontsize=12)
ax1.set_ylabel('Integrated Love / Karma (Hidden Variable)', color=color_love, fontsize=14)
ax1.plot(df['t'], df['A_acc'], color=color_love, linewidth=2, label='Integrated Area (A)')
ax1.fill_between(df['t'], 0, df['A_acc'], color=color_love, alpha=0.1)
ax1.tick_params(axis='y', labelcolor=color_love)
ax1.grid(True, alpha=0.3)

# Plot 2: The Visible Wealth (Gold)
ax2 = ax1.twinx()  
color_money = 'tab:gold'
ax2.set_ylabel('Real World Manifestation (Flow)', color=color_money, fontsize=14)
ax2.plot(df['t'], df['M_flow'], color=color_money, linewidth=3, linestyle='-', label='Manifestation (M)')
ax2.tick_params(axis='y', labelcolor=color_money)

# Mark the Transition Point
transition_idx = df[df['m'] > 0.01].index[0] if any(df['m'] > 0.01) else 0
ax1.axvline(x=transition_idx, color='red', linestyle='--', linewidth=2, label='Phase Slip (Awakening)')
ax1.text(transition_idx + 2, df['A_acc'].max()*0.5, ' Phase Transition\n (Reality Shift)', color='red', fontsize=12)

# Annotations
plt.annotate('Period of Doubt\n(High Effort, Low Result)', xy=(50, 100), xytext=(50, 40000),
             arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='center')

plt.annotate('Superconductivity\n(Flow State)', xy=(180, df['M_flow'].iloc[-1]), xytext=(140, df['M_flow'].iloc[-1]),
             arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='center')

fig.tight_layout()
plt.show()

# Final Stats
print(f"--- Results ---")
print(f"Threshold for Awakening: {cfg.critical_area:.2f}")
print(f"Time of Awakening:       Day {transition_idx}")
print(f"Final Exchange Rate:     {df['kappa'].iloc[-1]:.0f}x (Leverage)")
