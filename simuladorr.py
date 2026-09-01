import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
server = app.server

def calcular_fk(t1_deg, t2_deg, t3_deg, L1, L2, L3):
    t1, t2, t3 = np.radians([t1_deg, t2_deg, t3_deg])
    
    x0, y0 = 0.0, 0.0
    x1, y1 = L1 * np.cos(t1), L1 * np.sin(t1)
    x2, y2 = x1 + L2 * np.cos(t1 + t2), y1 + L2 * np.sin(t1 + t2)
    Px, Py = x2 + L3 * np.cos(t1 + t2 + t3), y2 + L3 * np.sin(t1 + t2 + t3)
    
    phi_deg = t1_deg + t2_deg + t3_deg
    return [x0, x1, x2, Px], [y0, y1, y2, Py], Px, Py, phi_deg

app.layout = html.Div([
    # Almacenamiento en memoria para el historial de puntos de la trayectoria
    dcc.Store(id='trail-store', data=[]),
    
    # Encabezado
    html.Div([
        html.H2("Simulador de Cinemática Directa con Trazado de Trayectoria", 
                style={'textAlign': 'left', 'color': '#0F172A', 'fontFamily': 'Inter, sans-serif', 'marginBottom': '5px'}),
        html.P("Modelado espacial de articulaciones y registro en tiempo real de la trayectoria del efector final.", 
               style={'color': '#64748B', 'fontFamily': 'Inter, sans-serif', 'marginTop': '0px', 'marginBottom': '20px'})
    ]),
    
    # 1. Gráfico a ancho completo
    html.Div([
        dcc.Graph(
            id='robot-graph-fk', 
            style={'height': '58vh', 'width': '100%'},
            config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
        )
    ], style={
        'width': '100%', 'backgroundColor': '#FFFFFF', 'borderRadius': '12px', 
        'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'padding': '15px', 'marginBottom': '20px', 'boxSizing': 'border-box'
    }),
    
    # 2. Panel inferior de controles organizado en 3 columnas
    html.Div([
        # Tarjeta 1: Resultados del Efector y Botón de Limpieza
        html.Div([
            html.H4("Efector Final P", style={'color': '#1E293B', 'marginTop': '0px', 'marginBottom': '12px'}),
            html.Div(id='fk-output', style={
                'padding': '14px', 'backgroundColor': '#F8FAFC', 'borderRadius': '8px', 
                'border': '1px solid #E2E8F0', 'fontFamily': 'monospace', 'fontSize': '13px',
                'lineHeight': '1.8', 'marginBottom': '12px'
            }),
            html.Button("Borrar Trayectoria", id='btn-clear-trail', n_clicks=0, style={
                'width': '100%', 'padding': '10px 14px', 'backgroundColor': '#EF4444',
                'color': '#FFFFFF', 'border': 'none', 'borderRadius': '8px',
                'fontWeight': '600', 'cursor': 'pointer', 'fontSize': '13px',
                'boxShadow': '0 2px 4px rgba(239, 68, 68, 0.2)'
            })
        ], style={
            'flex': '1', 'backgroundColor': '#FFFFFF', 'borderRadius': '12px', 'padding': '20px',
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)', 'boxSizing': 'border-box'
        }),
        
        # Tarjeta 2: Ángulos Articulares
        html.Div([
            html.H4("Ángulos Articulares (Grados)", style={'color': '#1E293B', 'marginTop': '0px', 'marginBottom': '15px'}),
            html.Label("θ1 (Base):", style={'fontWeight': '600', 'color': '#334155', 'fontSize': '13px'}),
            dcc.Slider(id='slider-t1', min=-180, max=180, step=1, value=30, marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),
            
            html.Label("θ2 (Hombro):", style={'fontWeight': '600', 'color': '#334155', 'fontSize': '13px', 'marginTop': '10px'}),
            dcc.Slider(id='slider-t2', min=-180, max=180, step=1, value=45, marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),
            
            html.Label("θ3 (Muñeca):", style={'fontWeight': '600', 'color': '#334155', 'fontSize': '13px', 'marginTop': '10px'}),
            dcc.Slider(id='slider-t3', min=-180, max=180, step=1, value=-30, marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),
        ], style={
            'flex': '2', 'backgroundColor': '#FFFFFF', 'borderRadius': '12px', 'padding': '20px',
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)', 'boxSizing': 'border-box'
        }),
        
        # Tarjeta 3: Geometría de los Eslabones
        html.Div([
            html.H4("Geometría de Eslabones", style={'color': '#1E293B', 'marginTop': '0px', 'marginBottom': '15px'}),
            html.Label("Longitud L1:", style={'fontWeight': '600', 'color': '#334155', 'fontSize': '13px'}),
            dcc.Slider(id='slider-l1', min=0.5, max=6, step=0.1, value=3.0, marks={1: '1m', 6: '6m'}),
            
            html.Label("Longitud L2:", style={'fontWeight': '600', 'color': '#334155', 'fontSize': '13px', 'marginTop': '10px'}),
            dcc.Slider(id='slider-l2', min=0.5, max=6, step=0.1, value=2.5, marks={1: '1m', 6: '6m'}),
            
            html.Label("Longitud L3:", style={'fontWeight': '600', 'color': '#334155', 'fontSize': '13px', 'marginTop': '10px'}),
            dcc.Slider(id='slider-l3', min=0.5, max=6, step=0.1, value=1.5, marks={1: '1m', 6: '6m'}),
        ], style={
            'flex': '1.5', 'backgroundColor': '#FFFFFF', 'borderRadius': '12px', 'padding': '20px',
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)', 'boxSizing': 'border-box'
        })
    ], style={'display': 'flex', 'gap': '20px', 'width': '100%'})

], style={'backgroundColor': '#F1F5F9', 'padding': '24px', 'fontFamily': 'Inter, system-ui, sans-serif', 'minHeight': '100vh'})


@app.callback(
    [Output('robot-graph-fk', 'figure'), 
     Output('fk-output', 'children'),
     Output('trail-store', 'data')],
    [Input('slider-t1', 'value'),
     Input('slider-t2', 'value'),
     Input('slider-t3', 'value'),
     Input('slider-l1', 'value'),
     Input('slider-l2', 'value'),
     Input('slider-l3', 'value'),
     Input('btn-clear-trail', 'n_clicks')],
    [State('trail-store', 'data')]
)
def update_fk(t1, t2, t3, l1, l2, l3, n_clicks_clear, trail_data):
    xs, ys, px, py, phi = calcular_fk(t1, t2, t3, l1, l2, l3)
    r_max = l1 + l2 + l3
    
    # Gestión del historial de la trayectoria
    if trail_data is None or ctx.triggered_id == 'btn-clear-trail':
        trail_data = []
        
    nuevo_punto = {'x': float(px), 'y': float(py)}
    
    # Agregar el punto si cambio la posicion respecto al ultimo registrado
    if not trail_data or (trail_data[-1]['x'] != nuevo_punto['x'] or trail_data[-1]['y'] != nuevo_punto['y']):
        trail_data.append(nuevo_punto)
        
    # Limitar el historial a los últimos 600 puntos para optimizar rendimiento
    if len(trail_data) > 600:
        trail_data = trail_data[-600:]
        
    trail_xs = [p['x'] for p in trail_data]
    trail_ys = [p['y'] for p in trail_data]
    
    fig = go.Figure()
    
    # 1. Área de trabajo (Alcance Máximo)
    theta_workspace = np.linspace(0, 2*np.pi, 120)
    fig.add_trace(go.Scatter(
        x=r_max * np.cos(theta_workspace), 
        y=r_max * np.sin(theta_workspace),
        mode='lines', 
        name='Espacio de Trabajo',
        line=dict(color='#94A3B8', width=1.5, dash='dash'),
        fill='toself',
        fillcolor='rgba(241, 245, 249, 0.3)',
        hoverinfo='skip'
    ))
    
    # 2. Rastro de la Trayectoria (Se dibuja debajo del brazo)
    if len(trail_xs) > 1:
        fig.add_trace(go.Scatter(
            x=trail_xs, y=trail_ys,
            mode='lines',
            name='Rastro Trayectoria',
            line=dict(color='#8B5CF6', width=3),  # Color violeta vibrante
            hovertemplate="<b>Trayectoria</b><br>X: %{x:.3f} m<br>Y: %{y:.3f} m<extra></extra>"
        ))
    
    # 3. Eslabones del brazo mecánico
    fig.add_trace(go.Scatter(
        x=xs, y=ys, 
        mode='lines+markers', 
        name='Estructura Rígida',
        line=dict(color='#0F172A', width=7),
        marker=dict(
            size=[16, 14, 12, 0],
            color=['#0F172A', '#2563EB', '#2563EB', 'transparent'],
            line=dict(width=2, color='#FFFFFF')
        ),
        hovertemplate="<b>%{text}</b><br>X: %{x:.2f} m<br>Y: %{y:.2f} m<extra></extra>",
        text=["Base (J0)", "Articulación 1 (J1)", "Articulación 2 (J2)", "Efector Final (P)"]
    ))
    
    # 4. Soporte de la Base
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        name='Base Fija',
        marker=dict(size=20, symbol='triangle-up', color='#0F172A'),
        hoverinfo='skip'
    ))
    
    # 5. Marcador del Efector Final (Punta P)
    fig.add_trace(go.Scatter(
        x=[px], y=[py], 
        mode='markers', 
        name='Efector Final P',
        marker=dict(size=14, color='#EF4444', symbol='circle', line=dict(width=2.5, color='#FFFFFF')),
        hovertemplate="<b>Efector Final (P)</b><br>Px: %{x:.3f} m<br>Py: %{y:.3f} m<extra></extra>"
    ))
    
    # 6. Anotación dinámica de coordenadas
    fig.add_annotation(
        x=px, y=py,
        text=f"<b>P</b> ({px:.2f}, {py:.2f})",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="#EF4444",
        ax=40, ay=-30,
        bgcolor="rgba(255, 255, 255, 0.95)",
        bordercolor="#EF4444",
        borderwidth=1,
        borderpad=5,
        font=dict(size=12, color="#0F172A", family="Inter, sans-serif")
    )
    
    # Configuración del Layout del Gráfico
    limite = r_max * 1.10
    fig.update_layout(
        template='plotly_white',
        xaxis=dict(
            range=[-limite, limite], 
            zeroline=True, 
            zerolinecolor='#CBD5E1', 
            zerolinewidth=1.5,
            gridcolor='#F1F5F9',
            title=dict(text="Posición X (m)", font=dict(size=12, color="#64748B"))
        ),
        yaxis=dict(
            range=[-limite, limite], 
            zeroline=True, 
            zerolinecolor='#CBD5E1', 
            zerolinewidth=1.5,
            gridcolor='#F1F5F9',
            scaleanchor="x", 
            scaleratio=1,
            title=dict(text="Posición Y (m)", font=dict(size=12, color="#64748B"))
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.01,
            xanchor="right", x=1,
            font=dict(size=11, color="#475569")
        ),
        margin=dict(l=40, r=40, t=30, b=40)
    )
    
    info_text = [
        html.Div([html.Span("Px: ", style={'color': '#64748B'}), html.Strong(f"{px:.3f} m")]),
        html.Div([html.Span("Py: ", style={'color': '#64748B'}), html.Strong(f"{py:.3f} m")]),
        html.Div([html.Span("Orientación (Φ): ", style={'color': '#64748B'}), html.Strong(f"{phi:.1f}°")])
    ]
    
    return fig, info_text, trail_data

if __name__ == '__main__':
    app.run(debug=False)
