pip install streamlit pandas numpy matplotlib seaborn -q -q

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(context="paper",
				style="whitegrid")
## Judul
st.write(
	"""
		# Dashboard Kualitas Udara
	"""
	)

## Sidebar
with st.sidebar:
	year = st.number_input("Tahun : ",
						min_value = 2013, max_value=2017,
						step = 1, value = 2013)

	stasiun = st.selectbox(
		label = "Stasiun : ",
		options=('Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou',
	           'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'),
		)

	hour = st.number_input("Hour : ",
						min_value = 0, max_value = 23,
						step = 1, value = 7)

st.write(

		f"## Stasiun {stasiun}"
	)

list_file = {'Aotizhongxin': 'PRSA_Data_Aotizhongxin_20130301-20170228',
             'Changping': 'PRSA_Data_Changping_20130301-20170228',
             'Dingling': 'PRSA_Data_Dingling_20130301-20170228',
             'Dongsi': 'PRSA_Data_Dongsi_20130301-20170228',
             'Guanyuan': 'PRSA_Data_Guanyuan_20130301-20170228',
             'Gucheng': 'PRSA_Data_Gucheng_20130301-20170228',
             'Huairou': 'PRSA_Data_Huairou_20130301-20170228',
             'Nongzhanguan': 'PRSA_Data_Nongzhanguan_20130301-20170228',
             'Shunyi': 'PRSA_Data_Shunyi_20130301-20170228',
             'Tiantan': 'PRSA_Data_Tiantan_20130301-20170228',
             'Wanliu': 'PRSA_Data_Wanliu_20130301-20170228',
             'Wanshouxigong': 'PRSA_Data_Wanshouxigong_20130301-20170228'}

path = f"../data/{list_file[stasiun]}.csv"

df = pd.read_csv(path)
var = ['PM2.5', 'PM10', 'NO2', "O3","PRES", 'WSPM', 'TEMP']
for i in var:
	df[i] = df[i].fillna(df[i].mean())

select = df.loc[(df["year"] == year)]
gb = select.groupby("hour")[var].mean()
gb['hour'] = gb.index
gb = gb.reset_index(drop=True)


## Grafik isi 4
fig, ax = plt.subplots(2, 2)

sns.lineplot(x="hour", y=var[0], data=gb, ax=ax[0][0])
ax[0][0].set_ylim(0, 150)

sns.lineplot(x="hour", y=var[1], data=gb, ax=ax[0][1])
ax[0][1].set_ylim(0, 150)

sns.lineplot(x="hour", y=var[2], data=gb, ax=ax[1][0])
ax[1][0].set_ylim(0, 150)

sns.lineplot(x="hour", y=var[3], data=gb, ax=ax[1][1])
ax[1][1].set_ylim(0, 150)

fig.tight_layout()
fig.set_size_inches(7, 5)
fig.suptitle("Perkembangan rata-rata konsentrasi tiap polutan berdasarkan jam", y=1.05, x=0.5, size=15)
st.pyplot(fig)

st.write(f"#### Kondisi cuaca pada pukul 0{hour}.00")

col1, col2, col3 = st.columns(3)

def metrics(gb, hour, category):
    if hour == 0:
        val1 = gb[category].loc[gb['hour'] == hour].values[0]
        val2 = gb[category].loc[gb['hour'] == 23].values[0]
        diff = val1 - val2
        return round(val1, 2), round(diff, 2)
    else:
        val1 = gb[category].loc[gb['hour'] == hour].values[0]
        val2 = gb[category].loc[gb['hour'] == hour+1].values[0]
        diff = val1 - val2
        return round(val1, 2), round(diff, 2)

pressure, delta_pressure = metrics(gb, hour, "PRES")
wind_speed, delta_wind_speed = metrics(gb, hour, "WSPM")
temperature, delta_temperature = metrics(gb, hour, "TEMP")


# Temperature dll
with col1:
    st.metric(label="Pressure",
        value=str(pressure) + " pa",
        delta=delta_pressure)

with col2:
    st.metric(label="Wind Speed",
        value=str(wind_speed) + " m/s",
        delta=delta_wind_speed)

with col3:
    st.metric(label="Temperature",
        value=str(temperature) + "  °C",
        delta=delta_temperature)

st.write(f"#### Detail tiap polutan pada tahun {year}")

fig, ax = plt.subplots(1, 2, figsize=(8,4),
	gridspec_kw={'width_ratios': [3, 2]})

polutan = ["PM2.5", "PM10",  "NO2", "O3"]
polutan_sum = select.groupby("year")[polutan].sum().T
polutan_sum.sort_values(by=year, ascending=True).plot(
	kind="barh", legend=False, ax=ax[0],)
ax[0].set_title(f"Polutan penyumbang emisi paling besar tahun {year}",
	size=11, pad=17, x=0.4)
ax[0].set_xlabel("Jumlah volume dalam µg/m³")

matrix = select[polutan].corr()
mask = np.triu(np.ones_like(matrix, dtype=bool))
sns.heatmap(matrix, annot=True, 
	mask=mask, cmap="crest", ax=ax[1])
ax[1].set_title(f"Korelasi tiap polutan pada tahun {year}",
	size=11, pad=17, x=0.4)

fig.tight_layout()
st.pyplot(fig)
