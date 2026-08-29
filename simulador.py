import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
server = app.server  # <-- REQUERIDO PARA DESPLIEGUE EN LA NUBE

def calcular_ik(Px, Py, phi_deg, L1, L2, L3, codo_arriba=False):
    phi = np.radians(phi_deg)
    Wx = Px - L3 * np.cos(phi)
    Wy = Py - L3 * np.sin(phi)
    denom = 2 * L1 * L2
    if denom == 0:
        return None, None, None
    D = (Wx**2 + Wy**2 - L1**2 - L2**2) / denom
    if np.abs(D) > 1.0:
        return None, None, None
    s2 = -1.0 if codo_arriba else 1.0
    theta2 = np.arctan2(s2 * np.sqrt(1 - D**2), D)
    theta1 = np.arctan2(Wy, Wx) - np.arctan2(L2 * np.sin(theta2), L1 + L2 * np.cos(theta2))
    theta3 = phi - theta1 - theta2
    return theta1, theta2, theta3

def obtener_articulaciones(t1, t2, t3, L1, L2, L3):
    x0, y0 = 0.0, 0.0
    x1 = L1 * np.cos(t1)
    y1 = L1 * np.sin(t1)
    x2 = x1 + L2 * np.cos(t1 + t2)
    y2 = y1 + L2 * np.sin(t1 + t2)
    x3 = x2 + L3 * np.cos(t1 + t2 + t3)
    y3 = y2 + L3 * np.sin(t1 + t2 + t3)
    return [x0, x1, x2, x3], [y0, y1, y2, y3]

app.layout = html.Div([
    html.H2("Simulador de Cinemática Inversa", style={'textAlign': 'center'}),
    html.Div([
        html.Div([dcc.Graph(id='robot-graph', style={'height': '75vh'})], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        html.Div([
            html.H4("Configuración del Brazo"),
            html.Div(id='angles-output', style={'padding': '10px', 'backgroundColor': '#f0f2f5', 'borderRadius': '5px', 'fontWeight': 'bold'}),
            html.Hr(),
            html.Label("Configuración de Codo:"),
            dcc.RadioItems(id='codo-config', options=[{'label': ' Codo Abajo', 'value': False}, {'label': ' Codo Arriba', 'value': True}], value=False, inline=True, style={'marginBottom': '15px'}),
            html.H5("Objetivo Efector Final P"),
            html.Label("Posición Px:"),
            dcc.Slider(id='slider-px', min=-10, max=10, step=0.1, value=4.0, marks={i: str(i) for i in range(-10, 11, 5)}),
            html.Label("Posición Py:"),
            dcc.Slider(id='slider-py', min=-10, max=10, step=0.1, value=2.0, marks={i: str(i) for i in range(-10, 11, 5)}),
            html.Label("Orientación Phi (°):"),
            dcc.Slider(id='slider-phi', min=-180, max=180, step=1, value=45, marks={i: str(i) for i in range(-180, 181, 90)}),
            html.Hr(),
            html.H5("Longitud de los Eslabones"),
            html.Label("Longitud L1:"),
            dcc.Slider(id='slider-l1', min=0.5, max=6, step=0.1, value=3.0, marks={i: str(i) for i in range(1, 7)}),
            html.Label("Longitud L2:"),
            dcc.Slider(id='slider-l2', min=0.5, max=6, step=0.1, value=2.5, marks={i: str(i) for i in range(1, 7)}),
            html.Label("Longitud L3:"),
            dcc.Slider(id='slider-l3', min=0.5, max=6, step=0.1, value=1.5, marks={i: str(i) for i in range(1, 7)}),
        ], style={'width': '35%', 'display': 'inline-block', 'paddingLeft': '3%', 'verticalAlign': 'top'})
    ])
])

@app.callback(
    [Output('robot-graph', 'figure'), Output('angles-output', 'children')],
    [Input('slider-px', 'value'), Input('slider-py', 'value'), Input('slider-phi', 'value'),
     Input('slider-l1', 'value'), Input('slider-l2', 'value'), Input('slider-l3', 'value'),
     Input('codo-config', 'value')]
)
def update_graph(px, py, phi, l1, l2, l3, codo_arriba):
    t1, t2, t3 = calcular_ik(px, py, phi, l1, l2, l3, codo_arriba)
    r_max = l1 + l2 + l3
    fig = go.Figure()
    
    theta_workspace = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(go.Scatter(x=r_max * np.cos(theta_workspace), y=r_max * np.sin(theta_workspace), mode='lines', name='Espacio de Trabajo', line=dict(color='lightgrey', dash='dash')))
    
    if t1 is None:
        fig.add_trace(go.Scatter(x=[px], y=[py], mode='markers', name='Inalcanzable', marker=dict(size=14, color='red', symbol='x')))
        info_text = html.Span("❌ Objetivo fuera del espacio de trabajo", style={'color': 'red'})
    else:
        xs, ys = obtener_articulaciones(t1, t2, t3, l1, l2, l3)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines+markers', name='Eslabones', line=dict(color='#1f77b4', width=6), marker=dict(size=12, color=['black', '#ff7f0e', '#2ca02c', 'red'])))
        fig.add_trace(go.Scatter(x=[px], y=[py], mode='markers', name='Objetivo P', marker=dict(size=12, color='red', symbol='cross')))
        deg1, deg2, deg3 = np.degrees([t1, t2, t3])
        info_text = [html.Div(f"θ1: {deg1:.2f}°"), html.Div(f"θ2: {deg2:.2f}°"), html.Div(f"θ3: {deg3:.2f}°")]
    
    limite = r_max * 1.15
    fig.update_layout(xaxis=dict(range=[-limite, limite], zeroline=True), yaxis=dict(range=[-limite, limite], zeroline=True, scaleanchor="x", scaleratio=1), margin=dict(l=20, r=20, t=30, b=20))
    return fig, info_text

if __name__ == '__main__':
    app.run(debug=False)