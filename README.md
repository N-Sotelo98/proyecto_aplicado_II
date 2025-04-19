# Building an End-to-End Retrieval-Augmented Generation System

Welcome to the **Building an End-to-End Retrieval-Augmented Generation System** repository. This repository is designed to guide you through the process of creating a complete Retrieval-Augmented Generation (RAG) system from scratch, following a structured curriculum.

## Setup Instructions

To get started with the course:

1. Clone this repository:
   ```bash
   git clone https://github.com/CarlosCaris/practicos-rag.git
2. Create a virtual environment
    ```bash
    python -m venv .venv
3. Activate the environment
   ```bash
    # On Mac
    .venv/bin/activate
    # On Windows
    .venv\Scripts\activate
4. Install requirements
    ```bash
    pip install -r requirements.txt
## Table of Contents

- [Building an End-to-End Retrieval-Augmented Generation System](#building-an-end-to-end-retrieval-augmented-generation-system)
  - [Setup Instructions](#setup-instructions)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Course Outline](#course-outline)
    - [Lesson 1: Introduction to Retrieval-Augmented Generation (RAG)](#lesson-1-introduction-to-retrieval-augmented-generation-rag)
    - [Lesson 2: Document Chunking Strategies](#lesson-2-document-chunking-strategies)

## Introduction

This repository contains the materials and code needed to build a complete Retrieval-Augmented Generation (RAG) system. A RAG system combines the strengths of large language models with an external knowledge base to improve the accuracy and relevance of generated responses. Throughout this course, you'll gain hands-on experience with the various components of a RAG system, from document chunking to deployment in the cloud.

## Course Outline

### Lesson 1: Introduction to Retrieval-Augmented Generation (RAG)
- **Objective:** Understand the fundamentals of RAG and its applications.
- **Topics:**
  - Overview of RAG systems
  - Challenges in large language models (e.g., hallucinations, outdated information)
  - Basic components of a RAG system
- **Practical Task:** Set up your development environment and familiarize yourself with the basic concepts.
- **Resources:** 
  - Basics
  - More concepts

### Lesson 2: Document Chunking Strategies
- **Objective:** Learn how to effectively segment documents for better retrieval performance.
- **Topics:**
  - Chunking techniques: token-level, sentence-level, semantic-level
  - Balancing context preservation with retrieval precision
  - Small2Big and sliding window techniques
- **Practical Task:** Implement chunking strategies on a sample dataset.
- **Resources:**
  - The five levels of chunking
  - A guide to chunking
 
---
### Entrega 1: Implementacion de sistema de ingestion
- **Objetivos**
- **Diseñar y desarrollar un sistema modular**: Crear una solución que permita refinar, estructurar y enriquecer un conjunto de datos, asegurando su calidad y consistencia antes de su almacenamiento.

- **Implementar procesos de obtención y preprocesamiento de datos**: Diseñar flujos que incluyan la limpieza, normalización y transformación de las fuentes de información, optimizando los datos para su uso en etapas posteriores.

- **Aplicar estrategias avanzadas de chunking**: Dividir documentos en segmentos manejables y coherentes, facilitando su análisis, procesamiento y almacenamiento de manera eficiente.

- **Almacenar los datos en una base vectorizada**: Estructurar los datos refinados en un formato optimizado para consultas rápidas y eficientes, garantizando su integración con sistemas de análisis y consumo.
---
### Diseño de la solcuion
![RAG drawio-3](https://github.com/user-attachments/assets/be0a436d-ac39-4f8d-a44f-25e868994c86)

**Componentes**
- **Control**: Orquesta toda la ejecución del sistema y actúa como punto de comunicación entre la lógica del programa y la interfaz gráfica, asegurando la integración y el correcto flujo de operaciones.

- **Procesador**: Aplica reglas de segmentación al conjunto de datos utilizando expresiones regulares, garantizando que los datos estén estructurados y listos para su procesamiento posterior.

- **Chunker**: Responsable de aplicar diversas estrategias para la fragmentación de datos. En esta iteración, se implementaron estrategias de *chunking* jerárquico y *chunking* recursivo para los textos. Para las tablas, estas se reconocen como tales y se procesa cada tabla dentro de un chunk.

- **Embedder**: Para la generación de *embeddings*, utilizamos el modelo de OpenAI `text-embedding-ada-002`, que produce representaciones vectoriales de 384 dimensiones, optimizadas para tareas semánticas.

- **VectorClient**: Gestiona la comunicación con el servicio de almacenamiento (*Qdrant*), facilitando la creación de colecciones y la inserción de puntos, lo que permite un acceso rápido y eficiente a los datos vectorizados.

- **UI**: Componente visual desarrollado en *Streamlit*, que permite realizar consultas interactivas sobre la base vectorizada, proporcionando una experiencia de usuario intuitiva y funcional.
----
## Ejecución del Programa

La aplicación fue compartida en un contenedor Docker para garantizar el encapsulamiento de las dependencias. Sin embargo, es necesario obtener credenciales de **OPENAI** antes de iniciar. Cambiar la varaible `OPENAI_API_KEY` dentro del archivo docker compose.

### Pasos para la ejecución:
1. **Montar los archivos a procesar dentro de la ruta**: 
  ```bash
   data/reglamentacion
   ```

2. **Montar la imagen**:  
   ```bash
   docker compose build
   ```

3. **Ejecutar la aplicación**:  
   ```bash
   docker compose up
   ```

> **Nota:**  
> - La construcción de la imagen puede demorar aproximadamente **10 minutos**.  
> - Si es la primera vez que ejecutas el programa, el tiempo promedio de ejecución es de **30 minutos**.
> - Para ver la ejecucion completa del pipeline modificar el archivo `compose.yaml` la entrada:
  ``` bash
    - PIPE_COLLECTION_NAME=<poner_nombre_coleccion>
   ```

## Sobre el metodo avanzado escogido  

El metodo de retrieval avanzado escogido en estre proyecto es el de Summarization, el cual consiste en resumir los chunks obtenidos del primer retrieval. Cada chunk es analizado en función de la query original, para generar una extracción y/o resumen de la información relevante de este, o en su defecto descartarlo en caso de no detectar elementos atingentes a la consulta.
![Summarization drawio-3](/imgs/summ.png)

Esto permite por un lado aplicar un segundo filtro al "naive retrieval", donde se aprovecha las capacidades de un LLM para analizar el contenido y confirmar o descartar la seleccion de chunks realizada mediante la similaridad coseno antes aplicada. De esta manera se le entrega un contexto más concentrado y rico en información al LLM encargado de la respuesta final.

- **Ventajas:**
  - Análisis más robusto de los chunks via LLM
  - Eliminación de ruido (Elimina partes irrelevantes de los chunks)
  - Horizontalmente escalable
- **Desventajas:**
  - Dependiente de la capacidad del LLM
  - Exposición a halucionaciones
  - Posibilidad de perder detalle fino de la información

## Resultado Benchmark

Para este modelo se realizó un benchmark utilizando 10 querys predefinidas con sus respectivas ground truth. Este dataset se encuentra disponible en el archivo `benchmark/evaluacion.xlsx`.

![Summarization drawio-3](/imgs/benchmark.png)

|métrica                                                                                        |answer_relevancy                                                                                 |answer_relevancy            |context_precision         |context_precision            |context_recall             |context_recall             |faithfulness             |faithfulness             |
|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|----------------------------|--------------------------|-----------------------------|---------------------------|---------------------------|-------------------------|-------------------------|
|retrieval_type                                                                                 |Advanced                                                                                         |Naive                       |Advanced                  |Naive                        |Advanced                   |Naive                      |Advanced                 |Naive                    |
|user_input                                                                                     |                                                                                                 |                            |                          |                             |                           |                           |                         |                         |
|¿Cuáles son los límites de metales aceptados en los alimentos?                                 |0.9                                                                                              |0.0                         |0.98                      |1.0                          |1.0                        |1.0                        |1.0                      |1.0                      |
|¿Cómo se clasifican las cervezas?                                                              |0.91                                                                                             |0.91                        |0.95                      |1.0                          |0.6                        |0.75                       |0.83                     |1.0                      |
|¿Los condimentos vegetales tienen algunas restricciones?                                       |0.97                                                                                             |0.94                        |1.0                       |1.0                          |0.2                        |1.0                        |1.0                      |1.0                      |
|¿Quiénes deben cumplir con la regulación alimentaria?                                          |0.95                                                                                             |0.91                        |0.94                      |1.0                          |1.0                        |1.0                        |1.0                      |1.0                      |
|¿Qué antioxidantes o sinergistas pueden agregarse a los aceites y grasas vegetales comestibles?|0.88                                                                                             |0.87                        |1.0                       |1.0                          |0.33                       |0.3                        |1.0                      |1.0                      |
|¿Qué caracteristicas debe tener la harina de chia?                                             |0.91                                                                                             |0.91                        |1.0                       |1.0                          |0.23                       |1.0                        |1.0                      |0.17                     |
|¿Qué se define como aditivo alimentario?                                                       |0.92                                                                                             |0.92                        |1.0                       |0.92                         |0.5                        |1.0                        |1.0                      |1.0                      |
|¿Qué se define como sidra?                                                                     |0.86                                                                                             |0.98                        |1.0                       |1.0                          |0.0                        |1.0                        |1.0                      |1.0                      |
|¿Qué se entiende por cerveza?                                                                  |0.89                                                                                             |0.86                        |1.0                       |1.0                          |1.0                        |1.0                        |1.0                      |1.0                      |
|¿Se pueden añadir aromas a los vinos?                                                          |0.96                                                                                             |0.94                        |0.0                       |0.0                          |0.0                        |0.0                        |0.0                      |0.0                      |

Podemos ver en detalle las diferencias de las respuestas en un ejemplo particular.

> **Query: "¿Qué caracteristicas debe tener la harina de chia?"**  

> **Respuesta Naive:**  
> La harina de chía debe tener las siguientes características:
>- Humedad máxima entre 9% y 5%.
>- Proteína mínima de 20% y 29%.
>- Contenido máximo de grasa entre 18% y 7%.
>- Fibra total máxima entre 35% y 52%.
>- Cenizas máximas entre 5% y 6%.
>Además, la denominación de venta será Harina de Chía Desgrasada o Harina de Chía Parcialmente Desgrasada, según corresponda.


  
> **Respuesta Avanzada:**  
> La harina de chía debe tener las siguientes características:
>
>- Humedad máxima de 9% para la harina parcialmente desgrasada y 5% para la desgrasada.
>- Proteína mínima de 20% para la harina parcialmente desgrasada y 29% para la desgrasada.
>- Grasa máxima de 18% para la harina parcialmente desgrasada y 7% para la desgrasada.
>- Fibra total máxima de 35% para la harina parcialmente desgrasada y 52% para la desgrasada.
>- Cenizas máximas de 5% para la harina parcialmente desgrasada y 6% para la desgrasada.
>
>Además, se menciona que el 95% de la harina debe pasar por un tamiz de 149 micrones y que las harinas pueden someterse o no a un tostado durante el procesamiento.

> **Ground Truth:**  
> Con la denominación de Harina de Chía, se entiende el producto proveniente de la
molienda de la semilla de chía (Salvia hispana L.) debiendo presentar esta última,
características de semillas sanas, limpias y bien conservadas, que han sido sometidas a
prensado para la remoción parcial o prácticamente total del aceite que contienen.
Los diversos tipos de Harina de Chía que se consideran responderán a las siguientes
características:
Harina de Chía
Parcialmente Desgrasada Desgrasada
Por ciento
Humedad (100 -105º C) máx. 9 5
Proteína (N x 6.25) mín. 20 29
Grasa (extracto etéreo) máx. 18 7
Fibra Total máx. 35 52
Cenizas (500 - 550º C) máx. 5 6
Granulometría: 0.5 - 1 mm.
Color: marrón grisáceo.
Sabor y aroma: suave, agradable, propio de la semilla.
Los límites máximos de tolerancia de contaminantes inorgánicos serán los establecidos en el
presente Código.
Criterios microbiológicos:
Coliformes Totales, máx. 100 UFC/g
Coliformes Fecales (E. coli) Ausencia en 1g
Salmonella sp. Ausencia en 25g
Clostridium, sp. (Sulfito reductores) Ausencia en 1g
Staphilococcus sp. Ausencia en 1g
Recuento total de hongos y levaduras, máx. 100 UFC/g
Aflatoxinas máx. 0,03 μg/kg
La denominación de venta será Harina de Chía Desgrasada o Harina de Chía Parcialmente
Desgrasada, según corresponda.”
