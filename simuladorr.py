import dash
from dash import dcc, html, Input, Output
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
    html.Div([
        html.H2("Simulador de Cinemática Directa — Brazo 3-DoF", 
                style={'textAlign': 'left', 'color': '#0F172A', 'fontFamily': 'Inter, sans-serif', 'marginBottom': '5px'}),
        html.P("Modelado espacial de articulaciones y alcance máximo operacional.", 
               style={'color': '#64748B', 'fontFamily': 'Inter, sans-serif', 'marginTop': '0px', 'marginBottom': '20px'})
    ]),
    
    html.Div([
        # Contenedor del Gráfico
        html.Div([
            dcc.Graph(
                id='robot-graph-fk', 
                style={'height': '78vh'},
                config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
            )
        ], style={
            'width': '64%', 'display': 'inline-block', 'verticalAlign': 'top',
            'backgroundColor': '#FFFFFF', 'borderRadius': '12px', 
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            'padding': '10px'
        }),
        
        # Contenedor de Controles
        html.Div([
            html.H4("Estado del Efector Final", style={'color': '#1E293B', 'marginTop': '0px'}),
            html.Div(id='fk-output', style={
                'padding': '16px', 'backgroundColor': '#F8FAFC', 'borderRadius': '8px', 
                'border': '1px solid #E2E8F0', 'fontFamily': 'monospace', 'fontSize': '14px'
            }),
            html.Hr(style={'borderColor': '#F1F5F9', 'margin': '20px 0'}),
            
            html.H4("Ángulos Articulares", style={'color': '#1E293B'}),
            html.Label("θ1 (Base):", style={'fontWeight': '600', 'color': '#334155'}),
            dcc.Slider(id='slider-t1', min=-180, max=180, step=1, value=30, marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),
            
            html.Label("θ2 (Hombro):", style={'fontWeight': '600', 'color': '#334155', 'marginTop': '10px'}),
            dcc.Slider(id='slider-t2', min=-180, max=180, step=1, value=45, marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),
            
            html.Label("θ3 (Muñeca):", style={'fontWeight': '600', 'color': '#334155', 'marginTop': '10px'}),
            dcc.Slider(id='slider-t3', min=-180, max=180, step=1, value=-30, marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),
            
            html.Hr(style={'borderColor': '#F1F5F9', 'margin': '20px 0'}),
            
            html.H4("Geometría de Eslabones", style={'color': '#1E293B'}),
            html.Div([
                html.Div([html.Label("L1:"), dcc.Slider(id='slider-l1', min=0.5, max=6, step=0.1, value=3.0, marks={1: '1m', 6: '6m'})], style={'marginBottom': '5px'}),
                html.Div([html.Label("L2:"), dcc.Slider(id='slider-l2', min=0.5, max=6, step=0.1, value=2.5, marks={1: '1m', 6: '6m'})], style={'marginBottom': '5px'}),
                html.Div([html.Label("L3:"), dcc.Slider(id='slider-l3', min=0.5, max=6, step=0.1, value=1.5, marks={1: '1m', 6: '6m'})]),
            ])
            
        ], style={
            'width': '31%', 'display': 'inline-block', 'marginLeft': '2%', 'verticalAlign': 'top',
            'backgroundColor': '#FFFFFF', 'borderRadius': '12px', 'padding': '24px',
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
        })
    ], style={'display': 'flex', 'alignItems': 'stretch'})
], style={'backgroundColor': '#F1F5F9', 'padding': '24px', 'fontFamily': 'Inter, system-ui, sans-serif', 'minHeight': '100vh'})

@app.callback(
    [Output('robot-graph-fk', 'figure'), Output('fk-output', 'children')],
    [Input('slider-t1', 'value'),
     Input('slider-t2', 'value'),
     Input('slider-t3', 'value'),
     Input('slider-l1', 'value'),
     Input('slider-l2', 'value'),
     Input('slider-l3', 'value')]
)
def update_fk(t1, t2, t3, l1, l2, l3):
    xs, ys, px, py, phi = calcular_fk(t1, t2, t3, l1, l2, l3)
    r_max = l1 + l2 + l3
    
    fig = go.Figure()
    
    # 1. Área de trabajo (Alcance Máximo) con relleno suave
    theta_workspace = np.linspace(0, 2*np.pi, 120)
    fig.add_trace(go.Scatter(
        x=r_max * np.cos(theta_workspace), 
        y=r_max * np.sin(theta_workspace),
        mode='lines', 
        name='Espacio de Trabajo',
        line=dict(color='#94A3B8', width=1.5, dash='dash'),
        fill='toself',
        fillcolor='rgba(241, 245, 249, 0.4)',
        hoverinfo='skip'
    ))
    
    # 2. Eslabones del brazo mecánico
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
    
    # 3. Soporte visual para la Base (Trípode/Ancla)
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        name='Base Fija',
        marker=dict(size=20, symbol='triangle-up', color='#0F172A'),
        hoverinfo='skip'
    ))
    
    # 4. Marcador del Efector Final (Punta P)
    fig.add_trace(go.Scatter(
        x=[px], y=[py], 
        mode='markers', 
        name='Efector Final P',
        marker=dict(size=14, color='#EF4444', symbol='circle', line=dict(width=2.5, color='#FFFFFF')),
        hovertemplate="<b>Efector Final (P)</b><br>Px: %{x:.3f} m<br>Py: %{y:.3f} m<extra></extra>"
    ))
    
    # 5. Anotación dinámica de coordenadas
    fig.add_annotation(
        x=px, y=py,
        text=f"<b>P</b> ({px:.2f}, {py:.2f})",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="#EF4444",
        ax=45, ay=-35,
        bgcolor="rgba(255, 255, 255, 0.95)",
        bordercolor="#EF4444",
        borderwidth=1,
        borderpad=6,
        font=dict(size=12, color="#0F172A", family="Inter, sans-serif")
    )
    
    # Configuración global del Layout
    limite = r_max * 1.12
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
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(size=11, color="#475569")
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    info_text = [
        html.Div([html.Span("Px: ", style={'color': '#64748B'}), html.Strong(f"{px:.3f} m")]),
        html.Div([html.Span("Py: ", style={'color': '#64748B'}), html.Strong(f"{py:.3f} m")]),
        html.Div([html.Span("Orientación (Φ): ", style={'color': '#64748B'}), html.Strong(f"{phi:.1f}°")])
    ]
    
    return fig, info_text

if __name__ == '__main__':
    app.run(debug=False)
