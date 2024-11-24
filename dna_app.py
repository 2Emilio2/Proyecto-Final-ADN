     #!/usr/bin/env python
# coding: utf-8

# In[2]:


######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

######################
# Page Title
######################

image = Image.open('Nucleotidos_ADN.png')

st.image(image, use_column_width=True)
st.write("""
<style>
h1 {
    color: #FF7F50;
    font-size: 42px;
    text-align: center;
    margin-bottom: 17px;
}

h2 {
    color: #CD5B45;
    font-size: 27px;
    margin-bottom: 6px;
}

.subheader {
    color: #FE6F5E;
    font-size: 20px;
    margin-bottom: 5px;
}

.output {
    margin-top: 20px;
}

table.dataframe {
    border-collapse: collapse;
    margin-top: 10px;
}

table.dataframe th, table.dataframe td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}

table.dataframe th {
    background-color: #5C5343;
}

.chart {
    margin-top: 14px;
}
</style>
""", unsafe_allow_html=True)

st.write("""
# Cuenta de Nucléotidos en ADN
Con esta aplicación se pueden obtener datos detalladamente de la composición de nucleotidos de la cadena de ADN que desees conocer.
Simplemente con escribir una pequeña secuencia de la cadena que gustes podrás conseguir datos para tus investigaciones, proyectos,
experimentos o conocimiento propio.
***
""")


######################
# Input Text Box
######################

#st.sidebar.header('Enter DNA sequence')
st.header('Introduzca Secuencia de ADN')

sequence_input = "Ejemplo: GAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG
"ATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGCTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

#sequence = st.sidebar.text_area("Sequence input", sequence_input, height=250)
sequence = st.text_area("Secuencia", sequence_input, height=150)
sequence = sequence.splitlines()
sequence = sequence[1:] # Skips the sequence name (first line)
sequence = ''.join(sequence) # Concatenates list to string

st.write("""
***
""")

## Prints the input DNA sequence
st.header('Secuencia Introducida')
sequence

## DNA nucleotide count
st.header('Composición de nucleótidos')


# Conteo de bases
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader('Conteo de bases')
    def DNA_nucleotide_count(seq):
        d = dict([
            ('A', seq.count('A')),
            ('T', seq.count('T')),
            ('G', seq.count('G')),
            ('C', seq.count('C'))
        ])
        return d

    X = DNA_nucleotide_count(sequence)
    st.write(X)

with col2:
    # Texto
    st.subheader('Texto')
    st.write('Hay ' + str(X['A']) + ' adeninas (A) presentes')
    st.write('Hay ' + str(X['T']) + ' timinas (T) presentes')
    st.write('Hay ' + str(X['G']) + ' guaninas (G) presentes')
    st.write('Hay ' + str(X['C']) + ' citosinas (C) presentes')

with col3:
    # Tabla
    st.subheader('Tabla')
    df = pd.DataFrame.from_dict(X, orient='index')
    df = df.rename({0: 'conteo'}, axis='columns')
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'nucleotido'})
    st.write(df)

# Add CSS styling for subheaders
st.markdown(
    """
    <style>
    .stHeader > .deco-btn-container > div {
        display: inline-block;
        margin-right: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

### 4. Display Bar Chart using Altair
st.subheader('Gráfico de Barras')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotido',
    y='conteo'
)

p = p.properties(
    width=alt.Step(80)  # controls width of bar.
)
st.write(p)

### 5. Display Pie Chart using Altair
st.subheader('Gráfica Circular')

import altair as alt

# Reshape the data for animated pie chart
df_pivot = df.melt('nucleotido', var_name='funcion', value_name='valor')

# Create animated pie chart
animated_pie_chart = alt.Chart(df_pivot).mark_arc().encode(
    alt.X('valor:Q', stack='zero'),
    color='nucleotido:N',
    tooltip=['nucleotido', 'funcion', 'valor']
).properties(
    width=500,
    height=400
).transform_joinaggregate(
    total='sum(valor)',
    groupby=['nucleotido']
).transform_calculate(
    percentage='datum.valor / datum.total'
).encode(
    text=alt.Text('percentage:Q', format='.1%')
).configure_mark(
    opacity=0.8
)

# Adjust properties of the animated pie chart
animated_pie_chart = animated_pie_chart.properties(
    width=300,
    height=300
)

# Display the animated pie chart
st.altair_chart(animated_pie_chart, use_container_width=True)

p = alt.Chart(df).mark_bar().encode(
    x='nucleotido',
    y='conteo',
    column='nucleotido'
)

p = p.properties(
    width=alt.Step(80),  # controls width of bar
    height=alt.Step(40),  # controls height of bar
    column=alt.Column(
        spacing=10  # controls spacing between grouped bars
    )
)


p = p.properties(
    width=alt.Step(80),  # controls width of bar
    height=alt.Step(40),  # controls height of bar
    column=alt.Column(
        spacing=10  # controls spacing between grouped bars
    )
)

st.header('Alumnos')
st.markdown('**Arvayo Carrasco Omar Eduardo**')
st.markdown('- **N°Exp:** ')
st.markdown('**Mendoza Rascón Emilio**')
st.markdown('- **N°Exp:** 221209549')


# In[ ]:




