import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
from streamlit_style import hide_streamlit_style

def app():
    # Oculta el estilo básico de Streamlit
    hide_streamlit_style()

    # Título principal de la página
    st.title("Data Cleaning and Exploration Tool 🧼")
    
    # Barra lateral de configuración
    with st.sidebar:
        st.header("🔧 Configuration")
        file_type = st.radio("Select file type:", ["CSV", "Excel"])
        uploaded_file = st.file_uploader("Choose a file")

    # Detiene la ejecución si no se ha subido un archivo
    if uploaded_file is None:
        st.info("Please upload a file to begin", icon="ℹ️")
        st.stop()

    @st.cache_data
    def load_data(file_type, file):
        if file_type == "CSV":
            df = pd.read_csv(file)
        elif file_type == "Excel":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error("Unsupported file type", icon="❌")
            st.stop()
        return df

    # Carga el archivo de datos
    df = load_data(file_type, uploaded_file)

    # Paso 1: Información básica del DataFrame
    st.subheader("Step 1: Inspect DataFrame Information")

    col1, col_space, col2, col_space2, col3 = st.columns([3, 0.3, 1, 0.3, 2])

    with col1:
        st.write("**DataFrame Information:**")
        buffer = StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

    with col2:
        st.write("**DataFrame Shape:**")
        st.write(df.shape)

    with col3:
        st.write("**Data Types of Each Column:**")
        st.write(df.dtypes)

    # Paso 2: Vista previa de los datos
    st.subheader("Step 2: Preview Data")
    with st.expander("View Data Preview"):
        view_option = st.radio("Choose rows to display:", ["First 10 rows", "Last 10 rows"])
        if view_option == "First 10 rows":
            st.write(df.head(10))
        else:
            st.write(df.tail(10))

    # Paso 3: Renombrar y eliminar columnas
    st.subheader("Step 3: Manage Columns")
    
    # Renombrar columnas
    st.write("**Rename Columns:**")
    col_names = df.columns.tolist()
    new_names = {}
    for col in col_names:
        new_name = st.text_input(f"Rename '{col}' to:", col)
        if new_name:
            new_names[col] = new_name
    df = df.rename(columns=new_names)

    # Eliminar columnas
    st.write("**Delete Columns:**")
    columns_to_delete = st.multiselect("Select columns to delete:", options=df.columns)
    if columns_to_delete:
        df = df.drop(columns=columns_to_delete)
        st.write("Columns deleted:", columns_to_delete)

    # Paso 4: Corrección de formatos de columnas
    st.subheader("Step 4: Correct Column Formats")
    columns_to_correct = st.multiselect("Select columns to change their data type:", options=df.columns)
    type_options = ["int", "float", "boolean", "date"]
    if columns_to_correct:
        for column in columns_to_correct:
            new_type = st.selectbox(f"Convert '{column}' to:", type_options, key=column)
            if new_type == "int":
                df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
            elif new_type == "float":
                df[column] = pd.to_numeric(df[column], errors='coerce')
            elif new_type == "boolean":
                df[column] = df[column].astype('bool')
            elif new_type == "date":
                if df[column].dtype in ['int64', 'Int64']:
                    df[column] = pd.to_datetime(df[column].astype(str), format='%Y', errors='coerce')
                else:
                    df[column] = pd.to_datetime(df[column], errors='coerce')
    st.write("**Updated Data Types:**")
    st.write(df.dtypes)

    # Paso 5: Manejo de valores nulos
    col2, col_space2, col3, col_space3 = st.columns([3, 0.3, 2, 0.3])

    with col2:
        st.subheader("Step 5: Handle Missing Values")
        st.write("**Number of Missing Values Per Column:**")
        st.write(df.isnull().sum())
    with col3:
        st.write("**Select action for missing values:**")    
        missing_value_action = st.radio("", ["Drop rows with missing values", "Fill with mean", "Fill with median", "Fill with mode", "Fill using forward fill (ffill)", "Fill using backward fill (bfill)"])
        if missing_value_action == "Drop rows with missing values":
            df = df.dropna()
        elif missing_value_action == "Fill with mean":
            df = df.fillna(df.mean())
        elif missing_value_action == "Fill with median":
            df = df.fillna(df.median())
        elif missing_value_action == "Fill with mode":
            df = df.fillna(df.mode().iloc[0])
        elif missing_value_action == "Fill using forward fill (ffill)":
            df = df.fillna(method='ffill')
        elif missing_value_action == "Fill using backward fill (bfill)":
            df = df.fillna(method='bfill')

    # Paso 6: Manejo de duplicados y reseteo de índice
    st.subheader("Step 6: Handle Duplicates & Reset Index")
    st.write("**Number of Duplicated Rows:**", df.duplicated().sum())
    if st.checkbox("Remove duplicated rows"):
        df = df.drop_duplicates()
        st.write("**Duplicates removed.**")

    if st.button("Reset Index"):
        df = df.reset_index(drop=True)
        st.write("**Index reset.**")

    # Guardar los datos limpios en el estado de sesión
    st.session_state['cleaned_data'] = df

    # Visualización del DataFrame después de la limpieza
    col1, col_space, col2, col_space2, col3 = st.columns([3, 0.3, 1, 0.3, 2])
    with col1:
        st.write("**DataFrame Information After Cleaning:**")
        buffer = StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

    with col2:
        st.write("**DataFrame Shape After Cleaning:**")
        st.write(df.shape)

    with col3:
        st.write("**Data Types of Each Column After Cleaning:**")
        st.write(df.dtypes)
    
    st.success("Data cleaning completed! You can now proceed with data analysis or export the cleaned data.", icon="✅")

    # Paso 7: Descarga de datos limpios
    st.subheader("Download Cleaned Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    st.download_button(
        label="Download Excel",
        data=output,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


