import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

interface Props {
  lat: number;
  lng: number;
}

export default function MapView({ lat, lng }: Props) {
  return (
    <div style={{ borderRadius: 12, overflow: "hidden", border: "1px solid var(--border)" }}>
      <MapContainer center={[lat, lng]} zoom={15} style={{ height: 260, width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={[lat, lng]}>
          <Popup>
            {lat.toFixed(4)}, {lng.toFixed(4)}
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}
