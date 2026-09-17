import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
server = app.server

# ---------------------------------------------------------------------------
# Paleta de la interfaz — consola tipo HMI industrial
# ---------------------------------------------------------------------------
BG_APP      = "#0A0E17"
BG_PANEL    = "#111827"
BG_SCREEN   = "#0D1420"
BORDER      = "#1F2A3D"
BORDER_HI   = "#2E3B52"
TEXT_MAIN   = "#DCE3ED"
TEXT_MUTED  = "#64748B"
TEXT_DIM    = "#48566E"
AMBER       = "#F5A524"
CYAN        = "#2DD4E5"
RED         = "#F0616B"
GREEN       = "#3ECF8E"

FONT_UI   = "'Inter', -apple-system, sans-serif"
FONT_MONO = "'JetBrains Mono', 'SFMono-Regular', monospace"

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; }
  body {
    background-color: ''' + BG_APP + ''';
    background-image:
      linear-gradient(''' + BORDER + ''' 1px, transparent 1px),
      linear-gradient(90deg, ''' + BORDER + ''' 1px, transparent 1px);
    background-size: 34px 34px;
    background-attachment: fixed;
  }
  ::-webkit-scrollbar { width: 10px; height: 10px; }
  ::-webkit-scrollbar-track { background: ''' + BG_APP + '''; }
  ::-webkit-scrollbar-thumb { background: ''' + BORDER_HI + '''; border-radius: 5px; }

  /* --- Reestilizado de los sliders rc-slider para la consola --- */
  .rc-slider { margin: 10px 0 22px 0 !important; }
  .rc-slider-rail {
    background-color: ''' + BG_SCREEN + ''' !important;
    border: 1px solid ''' + BORDER_HI + ''' !important;
    height: 4px !important;
  }
  .rc-slider-track {
    background-color: ''' + AMBER + ''' !important;
    height: 4px !important;
  }
  .rc-slider-handle {
    width: 15px !important;
    height: 15px !important;
    margin-top: -6px !important;
    background-color: ''' + AMBER + ''' !important;
    border: 2px solid #0A0E17 !important;
    box-shadow: 0 0 0 1px ''' + AMBER + ''' !important;
    opacity: 1 !important;
  }
  .rc-slider-handle:hover, .rc-slider-handle:focus, .rc-slider-handle-dragging {
    border-color: #0A0E17 !important;
    box-shadow: 0 0 0 4px rgba(245, 165, 36, 0.25) !important;
  }
  .rc-slider-mark-text {
    color: ''' + TEXT_DIM + ''' !important;
    font-family: ''' + FONT_MONO + ''' !important;
    font-size: 10px !important;
  }
  .rc-slider-mark-text-active { color: ''' + TEXT_MUTED + ''' !important; }
  .rc-slider-tooltip-inner {
    background-color: ''' + AMBER + ''' !important;
    color: #0A0E17 !important;
    font-family: ''' + FONT_MONO + ''' !important;
    font-weight: 700 !important;
    box-shadow: none !important;
  }
  .rc-slider-tooltip-arrow { border-top-color: ''' + AMBER + ''' !important; }

  .console-label { font-family: ''' + FONT_UI + '''; font-weight: 600; font-size: 12.5px; color: ''' + TEXT_MAIN + '''; }
  .console-sub   { font-family: ''' + FONT_MONO + '''; font-size: 10.5px; color: ''' + TEXT_DIM + '''; letter-spacing: 0.02em; }

  @keyframes pulse-dot {
    0%   { box-shadow: 0 0 0 0 rgba(62, 207, 142, 0.55); }
    70%  { box-shadow: 0 0 0 6px rgba(62, 207, 142, 0); }
    100% { box-shadow: 0 0 0 0 rgba(62, 207, 142, 0); }
  }
  .status-dot { animation: pulse-dot 2s infinite; }

  .estop-btn {
    width: 72px; height: 72px; border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #ff8a80, ''' + RED + ''' 55%, #b23a42 100%);
    border: 3px solid #7a2228;
    box-shadow: 0 4px 0 #7a2228, 0 6px 10px rgba(0,0,0,0.45), inset 0 2px 3px rgba(255,255,255,0.35);
    color: #ffffff; font-family: ''' + FONT_UI + '''; font-weight: 700; font-size: 10.5px;
    letter-spacing: 0.03em; cursor: pointer; transition: transform 0.06s ease, box-shadow 0.06s ease;
  }
  .estop-btn:active {
    transform: translateY(3px);
    box-shadow: 0 1px 0 #7a2228, 0 2px 4px rgba(0,0,0,0.4), inset 0 2px 3px rgba(255,255,255,0.35);
  }
</style>
</head>
<body>
{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
'''

def calcular_fk(t1_deg, t2_deg, t3_deg, L1, L2, L3):
    t1, t2, t3 = np.radians([t1_deg, t2_deg, t3_deg])

    x0, y0 = 0.0, 0.0
    x1, y1 = L1 * np.cos(t1), L1 * np.sin(t1)
    x2, y2 = x1 + L2 * np.cos(t1 + t2), y1 + L2 * np.sin(t1 + t2)
    Px, Py = x2 + L3 * np.cos(t1 + t2 + t3), y2 + L3 * np.sin(t1 + t2 + t3)

    phi_deg = t1_deg + t2_deg + t3_deg
    return [x0, x1, x2, Px], [y0, y1, y2, Py], Px, Py, phi_deg


def panel_style(flex):
    return {
        'flex': flex,
        'backgroundColor': BG_PANEL,
        'borderRadius': '10px',
        'border': f'1px solid {BORDER}',
        'padding': '20px 22px',
        'boxSizing': 'border-box',
    }


def slider_label(text):
    return html.Div(text, className='console-label', style={'marginBottom': '2px'})


app.layout = html.Div([
    dcc.Store(id='trail-store', data=[]),

    # --- Encabezado de la consola ---
    html.Div([
        html.Div([
            html.Div(style={
                'width': '9px', 'height': '9px', 'borderRadius': '50%',
                'backgroundColor': GREEN, 'display': 'inline-block', 'marginRight': '9px'
            }, className='status-dot'),
            html.Span("Sistema en línea", style={
                'fontFamily': FONT_MONO, 'fontSize': '11px', 'color': TEXT_MUTED, 'letterSpacing': '0.03em'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),

        html.H2("Cinemática directa — brazo de 3 eslabones",
                style={'color': TEXT_MAIN, 'fontFamily': FONT_UI, 'fontWeight': '700',
                       'fontSize': '22px', 'margin': '0 0 4px 0'}),
        html.P("Modelado espacial de articulaciones y registro en tiempo real de la trayectoria del efector final.",
               style={'color': TEXT_MUTED, 'fontFamily': FONT_UI, 'fontSize': '13.5px', 'margin': '0 0 20px 0'})
    ]),

    # --- Pantalla principal (gráfico) ---
    html.Div([
        dcc.Graph(
            id='robot-graph-fk',
            style={'height': '56vh', 'width': '100%'},
            config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
        )
    ], style={
        'width': '100%', 'backgroundColor': BG_PANEL, 'borderRadius': '10px',
        'border': f'1px solid {BORDER}',
        'padding': '14px', 'marginBottom': '18px', 'boxSizing': 'border-box'
    }),

    # --- Panel inferior de controles ---
    html.Div([

        # Tarjeta 1 — Lectura del efector + reset
        html.Div([
            html.Div("Efector final P", className='console-label', style={'marginBottom': '12px', 'fontSize': '13px'}),
            html.Div(id='fk-output', style={
                'padding': '14px 16px', 'backgroundColor': BG_SCREEN, 'borderRadius': '6px',
                'border': f'1px solid {BORDER_HI}', 'fontFamily': FONT_MONO, 'fontSize': '13px',
                'color': TEXT_MAIN, 'lineHeight': '2', 'marginBottom': '18px'
            }),
            html.Div([
                html.Button("RESET", id='btn-clear-trail', n_clicks=0, className='estop-btn'),
                html.Div("Borrar trayectoria", className='console-sub', style={'marginTop': '8px'})
            ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
        ], style=panel_style('1')),

        # Tarjeta 2 — Ángulos articulares
        html.Div([
            html.Div("Ángulos articulares", className='console-label', style={'marginBottom': '16px', 'fontSize': '13px'}),

            slider_label("θ1 — base"),
            dcc.Slider(id='slider-t1', min=-180, max=180, step=1, value=30,
                       marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),

            slider_label("θ2 — hombro"),
            dcc.Slider(id='slider-t2', min=-180, max=180, step=1, value=45,
                       marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),

            slider_label("θ3 — muñeca"),
            dcc.Slider(id='slider-t3', min=-180, max=180, step=1, value=-30,
                       marks={i: f"{i}°" for i in range(-180, 181, 90)}, tooltip={"placement": "bottom"}),
        ], style=panel_style('2')),

        # Tarjeta 3 — Geometría de eslabones
        html.Div([
            html.Div("Geometría de eslabones", className='console-label', style={'marginBottom': '16px', 'fontSize': '13px'}),

            slider_label("Longitud L1"),
            dcc.Slider(id='slider-l1', min=0.5, max=6, step=0.1, value=3.0, marks={1: '1 m', 6: '6 m'}),

            slider_label("Longitud L2"),
            dcc.Slider(id='slider-l2', min=0.5, max=6, step=0.1, value=2.5, marks={1: '1 m', 6: '6 m'}),

            slider_label("Longitud L3"),
            dcc.Slider(id='slider-l3', min=0.5, max=6, step=0.1, value=1.5, marks={1: '1 m', 6: '6 m'}),
        ], style=panel_style('1.5')),

    ], style={'display': 'flex', 'gap': '18px', 'width': '100%'})

], style={'padding': '26px', 'fontFamily': FONT_UI, 'minHeight': '100vh'})


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

    if trail_data is None or ctx.triggered_id == 'btn-clear-trail':
        trail_data = []

    nuevo_punto = {'x': float(px), 'y': float(py)}

    if not trail_data or (trail_data[-1]['x'] != nuevo_punto['x'] or trail_data[-1]['y'] != nuevo_punto['y']):
        trail_data.append(nuevo_punto)

    if len(trail_data) > 600:
        trail_data = trail_data[-600:]

    trail_xs = [p['x'] for p in trail_data]
    trail_ys = [p['y'] for p in trail_data]

    fig = go.Figure()

    # 1. Espacio de trabajo (alcance máximo)
    theta_workspace = np.linspace(0, 2 * np.pi, 120)
    fig.add_trace(go.Scatter(
        x=r_max * np.cos(theta_workspace),
        y=r_max * np.sin(theta_workspace),
        mode='lines',
        name='Espacio de trabajo',
        line=dict(color=BORDER_HI, width=1.5, dash='dash'),
        fill='toself',
        fillcolor='rgba(46, 59, 82, 0.15)',
        hoverinfo='skip'
    ))

    # 2. Rastro de la trayectoria
    if len(trail_xs) > 1:
        fig.add_trace(go.Scatter(
            x=trail_xs, y=trail_ys,
            mode='lines',
            name='Rastro trayectoria',
            line=dict(color=CYAN, width=2.5),
            hovertemplate="<b>Trayectoria</b><br>X: %{x:.3f} m<br>Y: %{y:.3f} m<extra></extra>"
        ))

    # 3. Eslabones del brazo
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode='lines+markers',
        name='Estructura rígida',
        line=dict(color=TEXT_MAIN, width=6),
        marker=dict(
            size=[15, 13, 11, 0],
            color=[AMBER, CYAN, CYAN, 'rgba(0,0,0,0)'],
            line=dict(width=2, color=BG_SCREEN)
        ),
        hovertemplate="<b>%{text}</b><br>X: %{x:.2f} m<br>Y: %{y:.2f} m<extra></extra>",
        text=["Base (J0)", "Articulación 1 (J1)", "Articulación 2 (J2)", "Efector final (P)"]
    ))

    # 4. Base fija
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        name='Base fija',
        marker=dict(size=20, symbol='triangle-up', color=AMBER, line=dict(width=1.5, color=BG_SCREEN)),
        hoverinfo='skip'
    ))

    # 5. Efector final
    fig.add_trace(go.Scatter(
        x=[px], y=[py],
        mode='markers',
        name='Efector final P',
        marker=dict(size=14, color=RED, symbol='circle', line=dict(width=2.5, color=BG_SCREEN)),
        hovertemplate="<b>Efector final (P)</b><br>Px: %{x:.3f} m<br>Py: %{y:.3f} m<extra></extra>"
    ))

    # 6. Anotación de coordenadas
    fig.add_annotation(
        x=px, y=py,
        text=f"<b>P</b> ({px:.2f}, {py:.2f})",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor=RED,
        ax=40, ay=-30,
        bgcolor=BG_SCREEN,
        bordercolor=RED,
        borderwidth=1,
        borderpad=5,
        font=dict(size=12, color=TEXT_MAIN, family=FONT_UI)
    )

    limite = r_max * 1.10
    fig.update_layout(
        paper_bgcolor=BG_PANEL,
        plot_bgcolor=BG_SCREEN,
        xaxis=dict(
            range=[-limite, limite],
            zeroline=True, zerolinecolor=BORDER_HI, zerolinewidth=1.5,
            gridcolor=BORDER,
            title=dict(text="Posición X (m)", font=dict(size=12, color=TEXT_MUTED)),
            tickfont=dict(color=TEXT_DIM, size=10.5, family=FONT_MONO)
        ),
        yaxis=dict(
            range=[-limite, limite],
            zeroline=True, zerolinecolor=BORDER_HI, zerolinewidth=1.5,
            gridcolor=BORDER,
            scaleanchor="x", scaleratio=1,
            title=dict(text="Posición Y (m)", font=dict(size=12, color=TEXT_MUTED)),
            tickfont=dict(color=TEXT_DIM, size=10.5, family=FONT_MONO)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.01,
            xanchor="right", x=1,
            font=dict(size=11, color=TEXT_MUTED, family=FONT_UI),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=40, r=40, t=30, b=40)
    )

    info_text = [
        html.Div([html.Span("Px  ", style={'color': TEXT_MUTED}), html.Strong(f"{px:.3f} m", style={'color': AMBER})]),
        html.Div([html.Span("Py  ", style={'color': TEXT_MUTED}), html.Strong(f"{py:.3f} m", style={'color': AMBER})]),
        html.Div([html.Span("Φ   ", style={'color': TEXT_MUTED}), html.Strong(f"{phi:.1f}°", style={'color': CYAN})])
    ]

    return fig, info_text, trail_data


if __name__ == '__main__':
    app.run(debug=False)
