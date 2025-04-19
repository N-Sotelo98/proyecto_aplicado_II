import logging.config
import streamlit as st
from src.controler import Controler
import logging
import os
import pandas as pd

console_handler = logging.StreamHandler()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[console_handler],
)


@st.cache_resource
def get_controler():
    """
    Initialize and cache the Controler instance.
    
    Returns:
        Controler: An instance of the Controler class.
    """
    controler = Controler(type="qdrant")
    return controler


@st.cache_resource
def get_metrics():
    """
    Load and cache metrics from a CSV file.
    
    Returns:
        DataFrame: A pandas DataFrame containing the metrics.
    """
    metrics = pd.read_csv(
        "./data/metrics.csv",
        usecols=[
            "user_input",
            "context_precision",
            "faithfulness",
            "answer_relevancy",
            "context_recall",
            "retrieval",
        ],
    )
    return metrics


# Load data and controler
metrics = get_metrics()
controler = get_controler()
db_status_collection = controler.db_check_collection()
db_status_vectors = controler.db_check_vector()

if st.button("Ejecutar pipeline",type="primary"):
    with st.spinner("Ejecutando pipeline..."):
        controler.init_pipeline()
    db_status_vectors = controler.db_check_vector()


st.sidebar.title("Menú")
page = st.sidebar.radio("Seleccione una opción", ["Chat", "Métricas"])

if page == "Chat":
    if db_status_collection and db_status_vectors:
        st.title("Reglamentación alimentaria Argentina")

        with st.chat_message("assistant"):
            st.write(
                "Bienvenido a la aplicación de búsqueda de reglamentación alimentaria Argentina"
            )

        if prompt := st.chat_input("Ingrese su consulta"):
            with st.chat_message("user"):
                st.write(prompt)
            with st.spinner("Buscando respuesta..."):
                respuesta_naive, respuesta_enhanced = controler.process_query(prompt)

            with st.chat_message("assistant"):
                st.markdown(":blue-background[Respuesta Advanced:]")
                st.text(respuesta_enhanced)
                st.divider()

            with st.chat_message("assistant"):
                st.markdown(":red-background[Respuesta basic:]")
                st.text(respuesta_naive)
                st.divider()

elif page == "Métricas":
    st.title("Métricas")
    st.title("Métricas Basic")
    st.dataframe(
        metrics.loc[
            lambda x: x.retrieval == "Basic",
            [
                "user_input",
                "context_precision",
                "faithfulness",
                "answer_relevancy",
                "context_recall",
                "retrieval",
            ],
        ],
        height=500,
    )
    st.title("Métricas Advanced")
    st.dataframe(
        metrics.loc[
            lambda x: x.retrieval == "Advanced",
            [
                "user_input",
                "context_precision",
                "faithfulness",
                "answer_relevancy",
                "context_recall",
                "retrieval",
            ],
        ],
        height=500,
    )
