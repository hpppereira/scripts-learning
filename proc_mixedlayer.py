def plot_mixed_layer(df, datei, datef):

    # cria matriz com profundidade e temperaturas

    dft = df[['t01','t02','t03','t04','t05','t06','t07','t08','t09','t10']]
    prof = np.arange(10,110,10) * -1

    # temp = dft.T
    # temp.index = prof
    # temp.index.name = 'prof'

    # temp = pd.DataFrame(dft.T, index=prof)
    temp = pd.DataFrame(dft[datei:datef].T.values, index=prof)
    # temp.index.name = 'prof'
    dft.plot(grid='on')
    plt.figure()
    plt.plot(temp, temp.index, 'k-o')
    plt.grid()
    plt.show()
    return

def plot_3d_mixed_layer(df):


    dft = df[['t01','t02','t03','t04','t05','t06','t07','t08','t09','t10']]

    prof = np.arange(10,110,10) * -1
    temps = dft.iloc[100:150].values

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    for i in range(len(temps)):
        ax.plot(temps[i], np.linspace(i,i,len(temps[i])), prof)

    plt.show()

    return


def plot_contour_sbe(df, depth_sbe, sbe, depth_adcp, adcp):
    """
    Plot SBE contour
    """

    fig=plt.figure(figsize=(10,12),facecolor='w')
    gs = gridspec.GridSpec(5, 1)

    ax1 = fig.add_subplot(gs[0])
    ax1.plot(df.ws, color='tab:blue')
    ax1.grid('on')
    ax1.set_xlim(df.index[0], df.index[-1])
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_ylabel('WS (m/s)', color='tab:blue')
    ax1.set_ylim(0,15)

    ax11 = ax1.twinx()
    ax11.plot(df.hs, color='tab:red')
    ax11.set_xlim(df.index[0], df.index[-1])
    ax11.tick_params(axis='y', labelcolor='tab:red')
    ax11.set_ylabel('Hs (m)', color='tab:red')
    ax11.set_ylim(0,5)

    ax12 = ax1.twinx()
    ax12.plot(df.tp, color='g')
    ax12.spines["right"].set_position(("axes", 1.06))
    make_patch_spines_invisible(ax12)
    ax12.spines["right"].set_visible(True)
    ax12.set_ylabel("Tp (s)")
    ax12.tick_params(axis='y', labelcolor='tab:green')
    ax12.yaxis.label.set_color('g')
    ax12.set_ylim(4,16)

    ax2 = fig.add_subplot(gs[1:3], sharex=ax1)
    lvls = np.arange(np.nanmin(sbe), np.nanmax(sbe)+1,1)
    # lvls = np.arange(16, 30,1)
    CF = ax2.contourf(df.index, depth_sbe, sbe, levels = lvls)
    CS = ax2.contour(df.index, depth_sbe, sbe, colors = 'k', levels = lvls, linewidths=.5)
    cbar = plt.colorbar(CF, ticks=lvls, format='%.i', label=r'Temperatura (ºC)',
                        orientation='horizontal', fraction=0.1, pad=0.11)
    ax2.set_ylabel('Profundidade (m)')
    ax2.grid('on')
    plt.xticks(rotation=0)

    ax3 = fig.add_subplot(gs[3:5], sharex=ax1)
    lvls = np.arange(np.nanmin(adcp), np.nanmax(adcp)+.1,.1)
    # lvls = np.arange(0, 1.1,.1)
    CF = ax3.contourf(df.index, depth_adcp, adcp, levels = lvls)
    CS = ax3.contour(df.index, depth_adcp, adcp, colors = 'k', levels = lvls, linewidths=.5)
    cbar = plt.colorbar(CF, ticks=lvls, format='%.1f', label=r'Intensidade da Corrente (m/s)',
                        orientation='horizontal', fraction=0.1, pad=0.11)
    ax3.set_ylabel('Profundidade (m)')
    ax3.grid('on')
    plt.xticks(rotation=0)
    ax3.set_ylim(-100, -10)

    return fig

# aplica filtragem nas series vv (melhorar)
vv = ['t01', 't02', 't03', 't04', 't05', 't06', 't07', 't08', 't09', 't10']
for v in vv:
    df[v] = make_filter(df[v].values, cutoff=1.0/24, fs=1/(1.0/24), btype='high', order=5)
vv = ['t01', 't02', 't03', 't04', 't05', 't06', 't07', 't08', 't09', 't10']    
plot_spec(df, vv=vv)
plot_mixed_layer(df, datei, datef)
plot_3d_mixed_layer(df)
