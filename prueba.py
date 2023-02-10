import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

# from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

def save_multi_image(filename):
    pp = PdfPages(filename)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        pp.savefig(fig)
    pp.close()


filename = "t3.pdf"

fig, ax = plt.subplots()

fruits = ["apple", "blueberry", "cherry", "orange"]
counts = [40, 100, 30, 55]
bar_labels = ["red", "blue", "_red", "orange"]
bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

ax.set_ylabel("fruit supply")
ax.set_title("Fruit supply by kind and color")
ax.legend(title="Fruit color")

save_multi_image(filename)
st.pyplot(fig)

if st.button("Download PDF"):
    with open(filename, 'rb') as f:
        b = f.read()
    b = b.decode("utf-8")
    st.write("Here is your file: ", st.file_downloader("Download PDF", b, "t3.pdf"))




    # FUNCION PARA HACER EL PDF

    # if st.button("Say hello"):
    #     st.write("Why hello there")

    #     def save_multi_image(filename):
    #         pp = PdfPages(filename)
    #         fig_nums = plt.get_fignums()
    #         figs = [plt.figure(n) for n in fig_nums]
    #         for fig in figs:
    #             fig.savefig(pp, format="pdf")
    #         pp.close()

    #     filename = "t3.pdf"
    #     save_multi_image(filename)
    # else:
    #     st.write("Goodbye")
    # ---------------------------------------------------------------------------------------------------------------------------------
