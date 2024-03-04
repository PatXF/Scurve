import pandas as pd
import streamlit as st


st.header("Convert Unit Hydrographs using S-Curve Method")
st.sidebar.title("WATER RESOURCES AND GEOTECHNICAL ENGINEERING SESSIONAL (CE39204) ")
st.sidebar.header("Divyajyoti Pattnaik, 21CE10020")
D = int(st.number_input("Enter D for the D-hr unit hydrograph"))
T = int(st.number_input("Enter T for the T-hr unit hydrograph you want as result"))
dataset = st.file_uploader("Upload a 'CSV' file, It should only contain two columns 'Time' and 'Discharge'(case-sensitive)",
                           type=['csv'], key="uploaded_file")
if dataset is not None:
    dataset = pd.read_csv(st.session_state["uploaded_file"], sep=",", header=0)


def gcd(a, b):
    while b:
        temp = b
        b = a % b
        a = temp
    return a


def create_S(data, D, unit):
    times = list(data.keys())
    S = [0 for i in range(len(times))]
    for i in range(0, D, unit):
        S[i] = data[times[i]]
    for i in range(D, len(times)):
        S[i] = data[times[i]] + S[i - D]
    return S


def create_unit(S, T, D):
    ans = [S[i] * (D / T) for i in range(len(S))]
    for i in range(T, len(S)):
        ans[i] = (S[i] - S[i - T]) * (D / T)
    return ans


if st.button("Convert"):
    if D == 0:
        st.error("D cannot be zero")
    elif T == 0:
        st.error('T cannot be zero')
    elif dataset is None:
        st.error("No file uploaded!")
    else:
        unit = gcd(max(D, T), min(D, T))
        num = len(dataset["Time"])
        maxi = dataset["Time"][num - 1]

        data_dict = {}
        for i in range(num):
            data_dict[int(dataset.iloc(0)[i][0])] = dataset.iloc(0)[i][1]

        for i in range(unit, maxi, unit):
            if i not in list(data_dict.keys()):
                data_dict[i] = (((data_dict[i + 1] - data_dict[i - 1]) / D) + data_dict[i - 1])

        times = list(data_dict.keys())
        times.sort()
        data_f = {}
        for time in times:
            data_f[time] = data_dict[time]

        S = create_S(data_f, D, unit)
        Tunit = create_unit(S, T, D)
        df_dict = {}
        df_dict['Discharge'] = Tunit
        df = pd.DataFrame(df_dict)
        st.success("Converted!")
        maxi = max(Tunit)
        st.info(f"Peak discharge for this unit hydrograph is {maxi}")
        st.balloons()
        st.area_chart(df)
