import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix
import json
from matplotlib.backends.backend_pdf import PdfPages


# Ruta al archivo JSON
file_path = "chatbot/results/intent_errors.json"

# Cargar datos del archivo JSON
with open(file_path, "r", encoding='utf-8') as file:
    data = json.load(file)

# Verificar si los datos se han cargado correctamente
print(data)

# Preparar los datos
actual_intents = [entry["intent"] for entry in data]
predicted_intents = [entry["intent_prediction"]["name"] for entry in data]
confidences = [entry["intent_prediction"]["confidence"] for entry in data]

# Crear un DataFrame a partir de los datos
df = pd.DataFrame({
    'text': [entry['text'] for entry in data],
    'intent': actual_intents,
    'predicted_intent': predicted_intents,
    'confidence': confidences,
    'index': range(len(data))
})

# Crear un archivo PDF para almacenar los gráficos
with PdfPages('graficos_intents.pdf') as pdf:
    
    # Gráfico de Barras para Precisión por Intento
    plt.figure(figsize=(12, 6))
    intent_confidences = df.groupby('intent')['confidence'].mean()
    plt.bar(intent_confidences.index, intent_confidences.values, color='skyblue')
    plt.xticks(rotation=45)
    plt.xlabel('Intents')
    plt.ylabel('Confianza Media')
    plt.title('Confianza Media de Predicciones por Intento')
    plt.tight_layout()
    pdf.savefig()  # Guarda la figura actual en el PDF
    plt.close()
    
    # Gráfico de Dispersión para Relación entre Intents y Confianza
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='intent', y='confidence', hue='predicted_intent', data=df)
    plt.xticks(rotation=45)
    plt.xlabel('Intents')
    plt.ylabel('Confianza')
    plt.title('Distribución de Confianza por Intento')
    plt.legend(title='Intentos Predichos', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    pdf.savefig()
    plt.close()
    
    # Gráfico de Pastel para Distribución de Intents
    plt.figure(figsize=(8, 8))
    intent_counts = df['intent'].value_counts()
    plt.pie(intent_counts, labels=intent_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title('Distribución de Intents en los Datos')
    pdf.savefig()
    plt.close()
    
    # Gráfico de Línea para Evolución de Confianza por Intento
    df_sorted = df.sort_values(by=['intent', 'confidence']).reset_index(drop=True)
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=df_sorted.index, y='confidence', hue='intent', data=df_sorted)
    plt.xlabel('Índice')
    plt.ylabel('Confianza')
    plt.title('Evolución de la Confianza por Intento')
    plt.legend(title='Intents', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    pdf.savefig()
    plt.close()
    
    # Gráfico de Área Apilada para Evolución de la Confianza
    plt.figure(figsize=(12, 6))
    for intent in df['intent'].unique():
        plt.fill_between(df[df['intent'] == intent]['index'], df[df['intent'] == intent]['confidence'], label=intent, alpha=0.5)
    plt.xlabel('Índice')
    plt.ylabel('Confianza')
    plt.title('Evolución de la Confianza por Intento (Área Apilada)')
    plt.legend(title='Intents')
    plt.tight_layout()
    pdf.savefig()
    plt.close()
    
    # Gráfico de Líneas con Subgráficos
    unique_intents = df['intent'].unique()
    num_intents = len(unique_intents)
    fig, axes = plt.subplots(nrows=num_intents, ncols=1, figsize=(12, 4 * num_intents))
    for i, intent in enumerate(unique_intents):
        sns.lineplot(x=df[df['intent'] == intent]['index'], y=df[df['intent'] == intent]['confidence'], ax=axes[i])
        axes[i].set_title(f'Evolución de la Confianza para {intent}')
        axes[i].set_xlabel('Índice')
        axes[i].set_ylabel('Confianza')
    plt.tight_layout()
    pdf.savefig()
    plt.close()
    
    # Gráfico de Violín para la Distribución de Confianza
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='intent', y='confidence', data=df, inner="quartile", hue='intent', palette="pastel", legend=False)
    plt.xticks(rotation=45)
    plt.xlabel('Intents')
    plt.ylabel('Confianza')
    plt.title('Distribución de la Confianza por Intento (Gráfico de Violín)')
    plt.tight_layout()
    pdf.savefig()
    plt.close()
    
    # Gráfico de Caja y Bigotes (Boxplot)
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='intent', y='confidence', data=df, hue='intent', palette="pastel", legend=False)
    plt.xticks(rotation=45)
    plt.xlabel('Intents')
    plt.ylabel('Confianza')
    plt.title('Distribución de la Confianza por Intento (Boxplot)')
    plt.tight_layout()
    pdf.savefig()
    plt.close()
    
    # Crear la matriz de confusión
    labels = list(set(actual_intents))
    conf_matrix = confusion_matrix(actual_intents, predicted_intents, labels=labels)
    
    # Convertir la matriz de confusión en un DataFrame para mejor visualización
    conf_matrix_df = pd.DataFrame(conf_matrix, index=labels, columns=labels)
    
    # Dibuja la matriz de confusión
    plt.figure(figsize=(10, 7))
    sns.heatmap(conf_matrix_df, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicción')
    plt.ylabel('Real')
    plt.title('Matriz de Confusión')
    pdf.savefig()
    plt.close()