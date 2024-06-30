import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

# Cargar datos desde el archivo JSON
with open('chatbot/results/intent_report.json', 'r', encoding='utf-8') as f:
    report_data = json.load(f)

# Convertir datos a un DataFrame adecuado
intent_names = list(report_data.keys())[:-3]  # Excluir avg y micro avg
metrics = ['precision', 'recall', 'f1-score', 'support']

data = []
for intent in intent_names:
    if isinstance(report_data[intent], dict):  # Verificar si report_data[intent] es un diccionario
        row = {
            'Intent': intent,
            'Precision': report_data[intent]['precision'],
            'Recall': report_data[intent]['recall'],
            'F1-score': report_data[intent]['f1-score'],
            'Support': report_data[intent]['support']
        }
        data.append(row)
    else:
        print(f"Warning: Unexpected data format for intent '{intent}'. Skipping.")

df = pd.DataFrame(data)

# Heatmap con límites de color ajustados (0 como el más claro y 1 como el más oscuro)
plt.figure(figsize=(8, 6))
sns.heatmap(df[['Precision', 'Recall', 'F1-score']], annot=True, cmap='Blues', fmt=".2f", vmin=0, vmax=1)
plt.title('Métricas de Clasificación por Intent')
plt.xlabel('Métricas')
plt.ylabel('Intent')
plt.savefig('metrics_heatmap_inverted.pdf')
plt.show()

# Gráfico de Barras del Support por Intent
plt.figure(figsize=(10, 6))
sns.barplot(x='Intent', y='Support', data=df)
plt.title('Support por Intent')
plt.xlabel('Intent')
plt.ylabel('Support')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('support_barplot.pdf')
plt.show()

# Gráfico de Barras de Precision, Recall y F1-score
plt.figure(figsize=(10, 6))
df.set_index('Intent')[['Precision', 'Recall', 'F1-score']].plot(kind='bar', stacked=False)
plt.title('Métricas de Clasificación por Intent')
plt.xlabel('Intent')
plt.ylabel('Score')
plt.xticks(rotation=45)
plt.legend(title='Métricas')
plt.tight_layout()
plt.savefig('metrics_barplot.pdf')
plt.show()
