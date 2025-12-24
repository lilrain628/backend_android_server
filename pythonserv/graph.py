import psycopg2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors  
def fetch_points_from_db():
    conn = psycopg2.connect(
        dbname="telephony_bd",
        host="localhost",
        user="postgres",
        password="vova100305",
        port="5432",
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT latitude, longitude, rssi
        FROM user_equipment
        WHERE latitude IS NOT NULL
          AND longitude IS NOT NULL
          AND rssi IS NOT NULL
        ORDER BY id
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    latitudes = [r[0] for r in rows]
    longitudes = [r[1] for r in rows]
    rssis = [r[2] for r in rows]

    return latitudes, longitudes, rssis

def update(frame):
    lat, lon, rssi = fetch_points_from_db()

    if not lat:
        return scatter,

    scatter.set_offsets(list(zip(lon, lat)))
    scatter.set_array(rssi)

    return scatter,

lat_init, lon_init, rssi_init = fetch_points_from_db()

if not lat_init:
    print("В таблице нет данных")
    exit(0)

norm=mcolors.Normalize(vmin=-125, vmax=-70)

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(
    lon_init,
    lat_init,
    c=rssi_init,
    norm=norm,
    cmap="jet",
    s=60,
    alpha=1.0,
    linewidths=0,
    edgecolors="k",

)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Уровень сигнала RSSI ")
ax.grid(True)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('RSRP (дБм)')
cbar.set_ticks([-125, -97.5, -70])
cbar.set_ticklabels(['-125 (плохо)', '-97.5', '-70 (отлично)'])
ani = FuncAnimation(
    fig,
    update,
    interval=2000, 
    blit=False
)

plt.tight_layout()
plt.show()
