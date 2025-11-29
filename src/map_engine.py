import folium


def generate_map_html(stations, city_name):
    """
    Gera o código HTML de um mapa com os pinos das estações.
    """
    if not stations:
        return None

    # 1. Calcular o centro do mapa (média das coordenadas)
    latitudes = [s['AddressInfo']['Latitude']
                 for s in stations if s.get('AddressInfo')]
    longitudes = [s['AddressInfo']['Longitude']
                  for s in stations if s.get('AddressInfo')]

    if not latitudes or not longitudes:
        return None

    center_lat = sum(latitudes) / len(latitudes)
    center_lon = sum(longitudes) / len(longitudes)

    # 2. Criar o objeto mapa
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # 3. Adicionar um marcador para cada estação
    for station in stations:
        addr = station.get('AddressInfo', {})
        lat = addr.get('Latitude')
        lon = addr.get('Longitude')
        title = addr.get('Title', 'Estação Desconhecida')

        # Pega info de potência para mostrar no popup
        connections = station.get('Connections', [])
        power = "Desconhecido"
        if connections:
            power = f"{connections[0].get('PowerKW', '?')} kW"

        if lat and lon:
            # Cria o texto que aparece ao clicar
            popup_text = f"<b>{title}</b><br>Potência: {power}"

            # Adiciona o pino no mapa
            folium.Marker(
                [lat, lon],
                popup=popup_text,
                tooltip=title,
                icon=folium.Icon(color="green", icon="bolt", prefix='fa')
            ).add_to(m)

    # 4. Retorna o HTML do mapa como string
    return m.get_root().render()
